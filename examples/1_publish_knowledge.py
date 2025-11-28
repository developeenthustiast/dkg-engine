"""
Example 1: Publishing Knowledge Assets to the DKG
--------------------------------------------------
This script demonstrates how to:
1. Create a structured Knowledge Asset (Comparison Result).
2. Publish it to the OriginTrail Decentralized Knowledge Graph (DKG).
3. Receive a Unique Asset Locator (UAL).
"""

import asyncio
import logging
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from truthgraph.dkg_publisher import DKGPublisher

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Example1")

async def main():
    logger.info("Initializing DKG Publisher...")
    publisher = DKGPublisher()
    
    # Define a sample comparison result
    # In a real scenario, this would come from the ComparisonEngine
    comparison_data = {
        "claim1": "The earth is flat.",
        "claim2": "The earth is an oblate spheroid.",
        "similarity_score": 0.1,
        "conflict": True,
        "explanation": "Direct contradiction regarding the shape of the earth.",
        "sources": ["Wikipedia", "Science Journal"]
    }
    
    logger.info(f"Publishing comparison data: {comparison_data}")
    
    try:
        # Publish to DKG
        result = await publisher.publish_comparison(comparison_data)
        
        logger.info("✅ Publish Successful!")
        logger.info(f"UAL: {result['ual']}")
        logger.info(f"Explorer Link: https://dkg-testnet.origintrail.io/explore?ual={result['ual']}")
        
    except Exception as e:
        logger.error(f"❌ Publish Failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
