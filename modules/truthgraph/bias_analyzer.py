"""
Bias Analyzer with Enterprise Features
Analyzes text for political and ideological bias
"""

import logging
from typing import Dict, List, Optional

from truthgraph.exceptions import ProcessingException, ValidationException
from truthgraph.validators import BiasRequest, BiasResult, BiasLeaning
from truthgraph.utils.cache import SimpleCache

logger = logging.getLogger(__name__)


class BiasAnalyzer:
    """
    Enterprise-grade bias analyzer
    """
    
    def __init__(self):
        self.cache = SimpleCache()
        
        self.left_keywords = {
            'progressive', 'social justice', 'equality', 'regulation',
            'climate change', 'universal healthcare', 'labor unions'
        }
        
        self.right_keywords = {
            'conservative', 'traditional', 'free market', 'deregulation',
            'individual liberty', 'law and order', 'fiscal responsibility'
        }
    
    async def analyze(self, text: str) -> Dict:
        """
        Analyze text for bias
        
        Args:
            text: Text to analyze
        
        Returns:
            BiasResult dictionary with bias score and leaning
        
        Raises:
            ProcessingException: If analysis fails
            ValidationException: If input is invalid
        """
        # Validate input
        try:
            request = BiasRequest(text=text)
            text = request.text
        except Exception as e:
            logger.error(f"Bias analysis input validation failed: {e}")
            raise ValidationException(f"Invalid bias analysis request: {str(e)}", cause=e)
        
        logger.info("Analyzing text for bias")
        
        try:
            # Check cache
            cache_key = f"bias:{hash(text)}"
            cached_result = self.cache.get(cache_key)
            if cached_result:
                logger.debug("Cache hit for bias analysis")
                return cached_result
            
            # Convert to lowercase for matching
            text_lower = text.lower()
            words = set(text_lower.split())
            
            # Count bias indicators
            left_count = sum(1 for word in self.left_keywords if word in text_lower)
            right_count = sum(1 for word in self.right_keywords if word in text_lower)
            
            total_bias = left_count + right_count
            
            # Determine leaning
            if total_bias == 0:
                leaning = BiasLeaning.NEUTRAL
                bias_score = 0.0
            elif left_count > right_count * 1.5:
                leaning = BiasLeaning.LEFT
                bias_score = min(1.0, left_count / 10)
            elif right_count > left_count * 1.5:
                leaning = BiasLeaning.RIGHT
                bias_score = min(1.0, right_count / 10)
            elif left_count > right_count:
                leaning = BiasLeaning.CENTER_LEFT
            
            return result_dict    bias_score = min(0.6, left_count / 15)
            elif right_count > left_count:
                leaning = BiasLeaning.CENTER_RIGHT
                bias_score = min(0.6, right_count / 15)
            else:
                leaning = BiasLeaning.NEUTRAL
                bias_score = 0.0
            
            # Generate explanation
            explanation = self._generate_explanation(leaning, bias_score, left_count, right_count)
            
            # Confidence (simplified)
            confidence = min(0.9, bias_score + 0.2)
            
            # Build result
            result_dict = {
                'bias_score': bias_score,
                'leaning': leaning,
                'explanation': explanation,
                'confidence': confidence
            }
            
            
        except ValidationException:
            raise
        except Exception as e:
            logger.error(f"Bias analysis failed: {str(e)}")
            raise ProcessingException(f"Failed to analyze bias: {str(e)}", cause=e)
    
    def _generate_explanation(
        self,
        leaning: BiasLeaning,
        score: float,
        left_count: int,
        right_count: int
    ) -> str:
        """Generate explanation for bias analysis"""
        if leaning == BiasLeaning.NEUTRAL:
            return f"Text appears neutral with minimal political bias indicators."
        
        direction = "left" if "left" in leaning.value.lower() else "right"
        strength = "strong" if score > 0.6 else "moderate" if score > 0.3 else "slight"
        
        return (
            f"Text shows {strength} {direction}-leaning bias (score: {score:.2f}). "
            f"Detected {left_count} left-leaning and {right_count} right-leaning indicators."
        )
