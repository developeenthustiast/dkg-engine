"""
Comparison Engine with Enterprise Features and DKG Integration
Compares claims and publishes results to OriginTrail DKG
"""

import logging
        publish: bool = True
    ) -> Dict:
        """
        Compare two claims and detect conflicts
        
        Args:
            claim1: First claim to compare
            claim2: Second claim to compare
            context: Optional context for comparison
            publish: Whether to publish to DKG (default: True)
        
        Returns:
            ComparisonResult dictionary with similarity score, analysis, and UAL if published
        
        Raises:
            ComparisonFailedException: If comparison fails
            ValidationException: If inputs are invalid
        """
        # Validate input
        try:
            request = ComparisonRequest(
                claim1=claim1,
                claim2=claim2,
                context=context
            )
            claim1 = request.claim1
            claim2 = request.claim2
            context = request.context
        except Exception as e:
            logger.error(f"Comparison input validation failed: {e}")
            raise ValidationException(f"Invalid comparison request: {str(e)}", cause=e)
        
        logger.info(f"Comparing claims")
        
        try:
            # Check cache
            cache_key = f"comparison:{hash((claim1, claim2, context or ''))}"
            cached_result = self.cache.get(cache_key)
            if cached_result:
                logger.debug("Cache hit for comparison")
                return cached_result
            
            # Extract key topics from claims
            topics1 = self._extract_topics(claim1)
            topics2 = self._extract_topics(claim2)
            
            # Fetch supporting evidence
            sources:List[ArticleSource] = []
            for topic in set(topics1 + topics2[:3]):  # Limit to avoid too many API calls
                try:
                    article = await self.wikipedia_client.fetch_article(topic)
                    sources.append(ArticleSource(**article))
                except Exception as e:
                    logger.warning(f"Failed to fetch evidence for topic '{topic}': {e}")
            
            # Compute similarity using simple word overlap for now
            # In production, use sentence embeddings (OpenAI, etc.)
            similarity = self._compute_similarity(claim1, claim2)
            
            # Detect conflicts
            conflict = similarity < 0.3  # Threshold for conflict detection
            
            # Generate explanation
            if conflict:
                explanation = f"Claims appear to conflict (similarity: {similarity:.2f}). Significant differences detected."
            elif similarity > 0.7:
                explanation = f"Claims appear similar (similarity: {similarity:.2f}). Substantial agreement detected."
            else:
                explanation = f"Claims are somewhat related (similarity: {similarity:.2f}). Partial similarity detected."
            
            # Build result
            result_dict = {
                'claim1': claim1,
                'claim2': claim2,
                'similarity_score': similarity,
                'conflict': conflict,
                'explanation': explanation,
                'confidence': min(0.9, similarity + 0.1),  # Simplified confidence
                'sources': [s.dict() for s in sources]
            }
            
            # Validate result
            try:
            raise
        except Exception as e:
            logger.error(f"Comparison failed: {str(e)}")
            raise ComparisonFailedException(f"Failed to compare claims: {str(e)}", cause=e)
    
    def _extract_topics(self, text: str) -> List[str]:
        """
        Extract key topics from text
        
        In production: use NLP/NER models
        For now: simple word extraction
        """
        # Simple extraction: Get capitalized words (likely proper nouns)
        words = text.split()
        topics = []
        
        for word in words:
            word = word.strip('.,!?;:"()[]{}')
            if len(word) > 3 and word[0].isupper():
                topics.append(word)
        
        return topics[:5]  # Limit to top 5
    
    def _compute_similarity(self, text1: str, text2: str) -> float:
        """
        Compute similarity between two texts
        
        In production: use embeddings (OpenAI text-embedding-ada-002, etc.)
        For now: simple Jaccard similarity
        """
        # Convert to lowercase and tokenize
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        if union == 0:
            return 0.0
        
        return intersection / union