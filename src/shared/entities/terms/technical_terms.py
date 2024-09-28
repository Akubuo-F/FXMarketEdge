from enum import Enum


class TechnicalTerm(Enum):
    OVERSOLD = 1
    OVERBOUGHT = -1
    BEARISH_DIVERGENCE = -1
    BULLISH_DIVERGENCE = 1
