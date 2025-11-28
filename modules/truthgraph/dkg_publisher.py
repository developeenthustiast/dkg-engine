"""
DKG Knowledge Asset Publisher
Enterprise-grade publishing to OriginTrail DKG with validation and error handling
"""

import logging
import hashlib
import uuid
from typing import Dict, Any, Optional
from datetime import datetime

from truthgraph.knowledge_assets import (
    ComparisonKnowledgeAsset,
    HallucinationKnowledgeAsset,
    BiasKnowledgeAsset,
    ProvenanceKnowledgeAsset,
    validate_jsonld,
    create_ual
)
from truthgraph.exceptions import DKGPublishException, ValidationException
from truthgraph.logging_config import get_correlation_id
from truthgraph.utils.retry import retry_with_backoff
from truthgraph.utils.circuit_breaker import CircuitBreaker, CircuitBreakerConfig

logger = logging.getLogger(__name__)


class DKGPublisher:
    """
    Enterprise-grade DKG Knowledge Asset publisher
    Handles validation, publishing, and error recovery
    """
    
    def __init__(self, dkg_config: Optional[Dict[str, Any]] = None):
        """
        Initialize DKG publisher
        
        Args:
            dkg_config: DKG configuration (endpoint, credentials, etc.)
        """
        self.config = dkg_config or {}
        self.endpoint = self.config.get('endpoint', 'http://localhost:8900')
        
        # Circuit breaker for fault tolerance
        self.circuit_breaker = CircuitBreaker(
            CircuitBreakerConfig(
                failure_threshold=5,
                success_threshold=2,
                timeout=60.0
            )
        )
        
        # Track published assets
        self.published_assets: Dict[str, str] = {}
        
        logger.info(f"DKG Publisher initialized - endpoint: {self.endpoint}")
    
    @retry_with_backoff(max_retries=3)
    async def publish_comparison(
        self,
        comparison_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Publish comparison result as Knowledge Asset
        
        Args:
            comparison_result: Comparison engine output
        
        Returns:
            Published asset info with UAL
        
        Raises:
            DKGPublishException: If publishing fails
            ValidationException: If data is invalid
        """
        correlation_id = get_correlation_id()
        logger.info(f"Publishing comparison Knowledge Asset - correlation_id: {correlation_id}")
        
        try:
            # Create Knowledge Asset
            asset = ComparisonKnowledgeAsset(
                claim1=comparison_result['claim1'],
                claim2=comparison_result['claim2'],
                similarity_score=comparison_result['similarity_score'],
                conflict=comparison_result['conflict'],
                explanation=comparison_result['explanation'],
                confidence=comparison_result['confidence'],
                sources=comparison_result.get('sources', [])
            )
            
            # Generate unique ID
            asset_id = str(uuid.uuid4())
            ual = create_ual('comparison', asset_id)
            asset.id = ual
            
            # Convert to JSON-LD
            jsonld = asset.to_jsonld()
            
            # Validate
            validate_jsonld(jsonld)
            
            # Publish to DKG
            result = await self._publish_to_dkg(jsonld, asset_id)
            
            # Track published asset
            self.published_assets[asset_id] = ual
            
            logger.info(f"Successfully published comparison asset - UAL: {ual}")
            
            return {
                'ual': ual,
                'asset_id': asset_id,
                'published_at': datetime.utcnow().isoformat() + 'Z',
                'dkg_result': result
            }
            
        except ValidationException:
            raise
        except Exception as e:
            logger.error(f"Failed to publish comparison asset: {str(e)}")
            raise DKGPublishException(
                f"Failed to publish comparison: {str(e)}",
                cause=e
            )
    
    @retry_with_backoff(max_retries=3)
    async def publish_hallucination(
        self,
        detection_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Publish hallucination detection as Knowledge Asset
        
        Args:
            detection_result: Hallucination detector output
        
        Returns:
            Published asset info with UAL
        """
        correlation_id = get_correlation_id()
        logger.info(f"Publishing hallucination Knowledge Asset - correlation_id: {correlation_id}")
        
        try:
            asset = HallucinationKnowledgeAsset(
                text=detection_result['text'],
                is_hallucination=detection_result['is_hallucination'],
                score=detection_result['score'],
                segments=detection_result.get('segments', []),
                evidence=detection_result.get('evidence', [])
            )
            
            asset_id = str(uuid.uuid4())
            ual = create_ual('hallucination', asset_id)
            asset.id = ual
            
            jsonld = asset.to_jsonld()
            validate_jsonld(jsonld)
            
            result = await self._publish_to_dkg(jsonld, asset_id)
            
            self.published_assets[asset_id] = ual
            
            logger.info(f"Successfully published hallucination asset - UAL: {ual}")
            
            return {
                'ual': ual,
                'asset_id': asset_id,
                'published_at': datetime.utcnow().isoformat() + 'Z',
                'dkg_result': result
            }
            
        except Exception as e:
            logger.error(f"Failed to publish hallucination asset: {str(e)}")
            raise DKGPublishException(
                f"Failed to publish hallucination: {str(e)}",
                cause=e
            )
    
    @retry_with_backoff(max_retries=3)
    async def publish_bias_analysis(
        self,
        bias_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Publish bias analysis as Knowledge Asset
        
        Args:
            bias_result: Bias analyzer output
        
        Returns:
            Published asset info with UAL
        """
        correlation_id = get_correlation_id()
        logger.info(f"Publishing bias Knowledge Asset - correlation_id: {correlation_id}")
        
        try:
            asset = BiasKnowledgeAsset(
                text=bias_result['text'],
                bias_score=bias_result['bias_score'],
                leaning=bias_result['leaning'],
                explanation=bias_result['explanation'],
                confidence=bias_result['confidence']
            )
            
            asset_id = str(uuid.uuid4())
            ual = create_ual('bias', asset_id)
            asset.id = ual
            
            jsonld = asset.to_jsonld()
            validate_jsonld(jsonld)
            
            result = await self._publish_to_dkg(jsonld, asset_id)
            
            self.published_assets[asset_id] = ual
            
            logger.info(f"Successfully published bias asset - UAL: {ual}")
            
            return {
                'ual': ual,
                'asset_id': asset_id,
                'published_at': datetime.utcnow().isoformat() + 'Z',
                'dkg_result': result
            }
            
        except Exception as e:
            logger.error(f"Failed to publish bias asset: {str(e)}")
            raise DKGPublishException(
                f"Failed to publish bias analysis: {str(e)}",
                cause=e
            )
    
    async def _publish_to_dkg(
        self,
        jsonld: Dict[str, Any],
        asset_id: str
    ) -> Dict[str, Any]:
        """
        Internal method to publish to DKG
        Uses circuit breaker for fault tolerance
        
        Args:
            jsonld: JSON-LD data
            asset_id: Asset identifier
        
        Returns:
            DKG response
        """
        def _do_publish():
            # TODO: Replace with actual DKG SDK call
            # For now, simulate publishing
            logger.debug(f"Publishing asset {asset_id} to DKG")
            
            # Placeholder for DKG SDK integration
            # from dkg import DKG
            # dkg = DKG(self.config)
            # result = dkg.asset.create(jsonld, {'epochsNum': 2})
            
            # Simulated response
            return {
                'status': 'success',
                'ual': jsonld.get('@id'),
                'published': True,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        
        # Use circuit breaker
        return self.circuit_breaker.call(_do_publish)
    
    async def create_provenance(
        self,
        original_source: str,
        data_hash: str,
        related_assets: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create provenance Knowledge Asset
        Links sources and verification chain
        
        Args:
            original_source: Source URL or identifier
            data_hash: SHA256 hash of original data
            related_assets: List of related UALs
        
        Returns:
            Published provenance asset
        """
        try:
            asset = ProvenanceKnowledgeAsset(
                original_source=original_source,
                data_hash=data_hash,
                related_assets=related_assets or []
            )
            
            asset_id = str(uuid.uuid4())
            ual = create_ual('provenance', asset_id)
            asset.id = ual
            
            jsonld = asset.to_jsonld()
            validate_jsonld(jsonld)
            
            result = await self._publish_to_dkg(jsonld, asset_id)
            
            logger.info(f"Successfully published provenance asset - UAL: {ual}")
            
            return {
                'ual': ual,
                'asset_id': asset_id,
                'published_at': datetime.utcnow().isoformat() + 'Z',
                'dkg_result': result
            }
            
        except Exception as e:
            logger.error(f"Failed to publish provenance: {str(e)}")
            raise DKGPublishException(
                f"Failed to publish provenance: {str(e)}",
                cause=e
            )
    
    def get_published_assets(self) -> Dict[str, str]:
        """Get map of published asset IDs to UALs"""
        return self.published_assets.copy()
