from abc import ABC, abstractmethod

from src.shared.entities.terms.sentiment_terms import Sentiment
from src.shared.entities.terms.technical_terms import TechnicalTerm
from src.shared.entities.terms.trend_terms import Trend


class CotAnalyser(ABC):
    @abstractmethod
    def analyse_sentiment(self) -> Sentiment:
        ...

    @abstractmethod
    def analyse_trend(self) -> Trend:
        ...

    @abstractmethod
    def analyse_technicals(self) -> list[TechnicalTerm]:
        ...