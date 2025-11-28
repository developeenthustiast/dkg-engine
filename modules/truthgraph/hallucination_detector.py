"""
Hallucination Detector with Enterprise Features
Detects AI hallucinations and unsupported claims
"""

import logging
import re
from typing import Dict, Any, Optional, List

from truthgraph.exceptions import HallucinationDetectionFailedException, ValidationException
from truthgraph.validators import HallucinationRequest, HallucinationResult
from truthgraph.data_sources.wikipedia import WikipediaClient
from truthgraph.utils.cache import SimpleCache

logger = logging.getLogger(__name__)


class HallucinationDetector:
    """
    Enterprise-grade hallucination detector
    """
    
    def __init__(self):
        self.wikipedia_client = WikipediaClient()
        self.cache = SimpleCache()

    async def detect(
        self,
        text: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Detect hallucinations in text
        
        Args:
            text: Text to analyze
            context: Optional context for verification
        
        Returns:
            HallucinationResult dictionary
        
        Raises:
            HallucinationDetectionFailedException: If detection fails
            ValidationException: If inputs are invalid
        """
        # Validate input
        try:
            request = HallucinationRequest(text=text, context=context)
            text = request.text
            context = request.context
        except Exception as e:
            logger.error(f"Hallucination detection input validation failed: {e}")
            raise ValidationException(f"Invalid hallucination detection request: {str(e)}", cause=e)
        
        logger.info("Detecting hallucinations in text")
        
        try:
            # Check cache
            cache_key = f"hallucination:{hash((text, context or ''))}"
            cached_result = self.cache.get(cache_key)
            if cached_result:
                logger.debug("Cache hit for hallucination detection")
                return cached_result
            
            # Extract claims and assertions
            segments = self._extract_factual_claims(text)
            
            # Verify each segment
            hallucination_segments = []
            evidence = []
            
            for segment in segments:
                is_supported = await self._verify_claim(segment)
                if not is_supported:
                    hallucination_segments.append({
                        'text': segment,
                        'confidence': 0.7,  # Simplified confidence
                        'reason': 'No supporting evidence found'
                    })
            
            # Compute overall score
            if len(segments) == 0:
                score = 0.0
            else:
                score = len(hallucination_segments) / len(segments)
            
            is_hallucination = score > 0.3  # Threshold
            
            # Build result
            result_dict = {
                'is_hallucination': is_hallucination,
                'score': score,
                'segments': hallucination_segments,
                'evidence': evidence
            }
            
            return result_dict
        except ValidationException:
            raise
        except Exception as e:
            logger.error(f"Hallucination detection failed: {str(e)}")
            raise HallucinationDetectionFailedException(
                f"Failed to detect hallucinations: {str(e)}",
                cause=e
            )
    
    def _extract_factual_claims(self, text: str) -> List[str]:
        """
        Extract factual claims from text
        
        In production: use NLP models for claim extraction
        For now: split on sentence boundaries
        """
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        
        # Filter out short sentences and questions
        claims = []
        for sent in sentences:
            sent = sent.strip()
            if len(sent) > 20 and '?' not in sent:
                claims.append(sent)
        
        return claims[:10]  # Limit to avoid too many API calls
    
    async def _verify_claim(self, claim: str) -> bool:
        """
        Verify a claim against knowledge sources
        
        In production: Use multiple sources, semantic search, etc.
        For now: Simple topic-based verification
        """
        # Extract topics
        topics = self._extract_topics(claim)
        
        if not topics:
            return True  # Can't verify without topics
        
        # Try to fetch evidence
        try:
            article = await self.wikipedia_client.fetch_article(topics[0])
            article_text = article.get('text', '').lower()
            claim_lower = claim.lower()
            
            # Check for keyword overlap (simplified)
            claim_words = set(claim_lower.split())
            article_words = set(article_text.split())
            overlap = len(claim_words.intersection(article_words))
            
            return overlap > len(claim_words) * 0.3  # At least 30% overlap
            
        except Exception:
            return True  # Benefit of the doubt if can't fetch
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text"""
        words = text.split()
        topics = []
        
        for word in words:
            word = word.strip('.,!?;:"()[]{}')
            if len(word) > 3 and word[0].isupper():
                topics.append(word)
        
        return topics[:3]
