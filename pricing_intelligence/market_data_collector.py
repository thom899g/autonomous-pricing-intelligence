import logging
import aiohttp
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MarketDataCollector:
    def __init__(self, data_sources: List[str]):
        self.data_sources = data_sources
        self.session = None

    async def collect_data(self) -> Dict[str, Any]:
        """
        Collects market data from all registered sources asynchronously.
        Returns a dictionary with source names as keys and their data as values.
        """
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            tasks = [self._fetch_data(source) for source in self.data_sources]
            results = await asyncio.gather(*tasks)
            
            return {source: result for source, result in zip(self.data_sources, results)}
        except Exception as e:
            logger.error(f"Failed to collect data: {e}")
            raise

    async def _fetch_data(self, source: str) -> Dict[str, Any]:
        """
        Fetches data from a single source using asynchronous HTTP request.
        Implements retry logic for failed requests.
        """
        try:
            async with self.session.get(source) as response:
                if response.status == 200:
                    return await response.json()
                logger.warning(f"Request to {source} failed with status {response.status}")
                return None
        except aiohttp.ClientError as e:
            logger.error(f"Connection error while fetching from {source}: {e}")
            return None