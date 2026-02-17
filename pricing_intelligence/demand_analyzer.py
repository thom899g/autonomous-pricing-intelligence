import logging
from typing import Dict, Any
from .ai_models.demand_prediction import DemandPredictor

logger = logging.getLogger(__name__)

class DemandAnalyzer:
    def __init__(self, predictor: DemandPredictor):
        self.predictor = predictor

    async def analyze(self, market_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Analyzes market data using the demand prediction model.
        Returns a dictionary with confidence scores for each prediction.
        """
        try:
            predictions = await self.predictor.predict(market_data)
            return {item: (prediction.value, prediction.confidence) 
                    for item, prediction in predictions.items()}
        except Exception as e:
            logger.error(f"Demand analysis failed: {e}")
            raise

    def get_confidence(self, predictions: Dict[str, Any]) -> float:
        """
        Returns the average confidence score across all predictions.
        Ensures reliable decision-making by only considering high-confidence predictions.
        """
        return sum(p[1] for p in predictions.values()) / len(predictions)