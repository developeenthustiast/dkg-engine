"""
JSON-LD Schema Definitions for DKG Knowledge Assets
Follows W3C standards and OriginTrail DKG specifications
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, validator
import json


class JSONLDContext(BaseModel):
    """Base JSON-LD context following W3C standards"""
    
    @staticmethod
    def get_base_context() -> Dict[str, Any]:
        """Get base @context for all Knowledge Assets"""
        return {
            "@vocab": "https://schema.org/",
            "dkg": "https://dkg.origintrail.io/",
            "truthgraph": "https://truthgraph.ai/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
        }


class ComparisonKnowledgeAsset(BaseModel):
    """
    JSON-LD Knowledge Asset for claim comparison results
    Enterprise-grade with full validation
    """
    
    context: Dict[str, Any] = Field(
        default_factory=JSONLDContext.get_base_context,
        alias="@context",
        description="JSON-LD context"
    )
    type: str = Field(
        default="truthgraph:ComparisonAsset",
        alias="@type",
        description="Asset type"
    )
    id: Optional[str] = Field(
        None,
        alias="@id",
        description="UAL (Uniform Asset Locator)"
    )
    
    # Core comparison data
    claim1: str = Field(..., min_length=1, max_length=10000)
    claim2: str = Field(..., min_length=1, max_length=10000)
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    conflict: bool
    explanation: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    
    # Provenance
    creator: str = Field(default="TruthGraph Enterprise v1.0")
    created: datetime = Field(default_factory=datetime.utcnow)
    modified: Optional[datetime] = None
    
    # Sources
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Verification
    verified_by: Optional[str] = None
    verification_method: str = Field(default="Wikipedia + DKG cross-reference")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "@context": JSONLDContext.get_base_context(),
                "@type": "truthgraph:ComparisonAsset",
                "@id": "dkg://comparison/uuid-here",
                "claim1": "Climate change is caused by human activity",
                "claim2": "Global warming is primarily anthropogenic",
                "similarity_score": 0.92,
                "conflict": False,
                "explanation": "Claims are highly similar and aligned",
                "confidence": 0.88,
                "creator": "TruthGraph Enterprise v1.0",
                "created": "2024-11-28T15:45:00Z",
                "sources": [],
                "verification_method": "Wikipedia + DKG cross-reference"
            }
        }
    
    def to_jsonld(self) -> Dict[str, Any]:
        """Convert to JSON-LD format for DKG publishing"""
        data = self.model_dump(by_alias=True, exclude_none=True)
        
        # Format datetime as ISO string
        if isinstance(data.get('created'), datetime):
            data['created'] = data['created'].isoformat() + 'Z'
        if data.get('modified') and isinstance(data['modified'], datetime):
            data['modified'] = data['modified'].isoformat() + 'Z'
        
        return data


class HallucinationKnowledgeAsset(BaseModel):
    """
    JSON-LD Knowledge Asset for hallucination detection results
    """
    
    context: Dict[str, Any] = Field(
        default_factory=JSONLDContext.get_base_context,
        alias="@context"
    )
    type: str = Field(
        default="truthgraph:HallucinationAsset",
        alias="@type"
    )
    id: Optional[str] = Field(None, alias="@id")
    
    # Core data
    text: str = Field(..., min_length=1, max_length=50000)
    is_hallucination: bool
    score: float = Field(..., ge=0.0, le=1.0)
    segments: List[Dict[str, Any]] = Field(default_factory=list)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Provenance
    creator: str = Field(default="TruthGraph Enterprise v1.0")
    created: datetime = Field(default_factory=datetime.utcnow)
    detection_method: str = Field(default="NLP + Wikipedia verification")
    
    class Config:
        populate_by_name = True
    
    def to_jsonld(self) -> Dict[str, Any]:
        """Convert to JSON-LD format"""
        data = self.model_dump(by_alias=True, exclude_none=True)
        if isinstance(data.get('created'), datetime):
            data['created'] = data['created'].isoformat() + 'Z'
        return data


class BiasKnowledgeAsset(BaseModel):
    """
    JSON-LD Knowledge Asset for bias analysis results
    """
    
    context: Dict[str, Any] = Field(
        default_factory=JSONLDContext.get_base_context,
        alias="@context"
    )
    type: str = Field(
        default="truthgraph:BiasAsset",
        alias="@type"
    )
    id: Optional[str] = Field(None, alias="@id")
    
    # Core data
    text: str = Field(..., min_length=1, max_length=50000)
    bias_score: float = Field(..., ge=0.0, le=1.0)
    leaning: str = Field(..., pattern="^(left|right|center-left|center-right|neutral)$")
    explanation: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    
    # Provenance
    creator: str = Field(default="TruthGraph Enterprise v1.0")
    created: datetime = Field(default_factory=datetime.utcnow)
    analysis_method: str = Field(default="Keyword analysis + semantic evaluation")
    
    class Config:
        populate_by_name = True
    
    def to_jsonld(self) -> Dict[str, Any]:
        """Convert to JSON-LD format"""
        data = self.model_dump(by_alias=True, exclude_none=True)
        if isinstance(data.get('created'), datetime):
            data['created'] = data['created'].isoformat() + 'Z'
        return data


class ProvenanceKnowledgeAsset(BaseModel):
    """
    JSON-LD Knowledge Asset for provenance tracking
    Links to source data and verification chain
    """
    
    context: Dict[str, Any] = Field(
        default_factory=JSONLDContext.get_base_context,
        alias="@context"
    )
    type: str = Field(
        default="truthgraph:ProvenanceAsset",
        alias="@type"
    )
    id: Optional[str] = Field(None, alias="@id")
    
    # Provenance chain
    original_source: str
    verification_steps: List[Dict[str, Any]] = Field(default_factory=list)
    data_hash: str = Field(..., pattern="^sha256:[a-f0-9]{64}$")
    signature: Optional[str] = None
    
    # Timestamps
    created: datetime = Field(default_factory=datetime.utcnow)
    last_verified: datetime = Field(default_factory=datetime.utcnow)
    
    # Links to other assets
    related_assets: List[str] = Field(default_factory=list)
    
    class Config:
        populate_by_name = True
    
    def to_jsonld(self) -> Dict[str, Any]:
        """Convert to JSON-LD format"""
        data = self.model_dump(by_alias=True, exclude_none=True)
        if isinstance(data.get('created'), datetime):
            data['created'] = data['created'].isoformat() + 'Z'
        if isinstance(data.get('last_verified'), datetime):
            data['last_verified'] = data['last_verified'].isoformat() + 'Z'
        return data


# Schema validation utilities

def validate_jsonld(data: Dict[str, Any]) -> bool:
    """
    Validate JSON-LD structure
    
    Args:
        data: JSON-LD data to validate
    
    Returns:
        True if valid
    
    Raises:
        ValueError: If validation fails
    """
    required_fields = ['@context', '@type']
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    if not isinstance(data['@context'], dict):
        raise ValueError("@context must be a dictionary")
    
    if not isinstance(data['@type'], str):
        raise ValueError("@type must be a string")
    
    return True


def create_ual(asset_type: str, identifier: str) -> str:
    """
    Create Uniform Asset Locator (UAL) for Knowledge Asset
    
    Args:
        asset_type: Type of asset (comparison, hallucination, bias)
        identifier: Unique identifier (usually UUID or hash)
    
    Returns:
        UAL string
    """
    return f"dkg://{asset_type}/{identifier}"
