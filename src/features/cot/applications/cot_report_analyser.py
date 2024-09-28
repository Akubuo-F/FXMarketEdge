from src.features.cot.domain.entities.cot_report import CotReport
from src.features.cot.domain.entities.traders.commercial_traders_report import CommercialTradersReport
from src.features.cot.domain.entities.traders.non_commercial_traders_report import NonCommercialTradersReport
from src.features.cot.domain.rules.cot_analyser import CotAnalyser
from src.shared.entities.terms.sentiment_terms import Sentiment
from src.shared.entities.terms.technical_terms import TechnicalTerm
from src.shared.entities.terms.trend_terms import Trend


class CotReportAnalyser(CotAnalyser):

    def __init__(self, cot_report: CotReport):
        self._cot_report: CotReport = cot_report

    def analyse_sentiment(self, threshold: float = 20.0) -> Sentiment:
        # use a threshold of 10-15% to capture more changes
        non_commercial_report: NonCommercialTradersReport = self._cot_report.non_commercial_traders_report
        longs_percentage: float = non_commercial_report.longs_percentage
        shorts_percentage: float = non_commercial_report.shorts_percentage
        difference: float = abs(longs_percentage - shorts_percentage)
        if longs_percentage > shorts_percentage and difference >= threshold:
            return Sentiment.BULLISH
        elif longs_percentage < shorts_percentage and difference >= threshold:
            return Sentiment.BEARISH
        return Sentiment.NEUTRAL

    def analyse_trend(self, threshold: float = 20.0) -> Trend:
        # Use a threshold of 10-15% to capture more changes
        commercial_report: CommercialTradersReport = self._cot_report.commercial_traders_report
        longs_percentage: float = commercial_report.longs_percentage
        shorts_percentage: float = commercial_report.shorts_percentage
        difference: float = abs(longs_percentage - shorts_percentage)
        if longs_percentage > shorts_percentage and difference >= threshold:
            return Trend.UPTREND
        elif longs_percentage < shorts_percentage and difference >= threshold:
            return Trend.DOWNTREND
        return Trend.NEUTRAL

    def analyse_technicals(self) -> list[TechnicalTerm]:
        result: list[TechnicalTerm] = []
        result += [TechnicalTerm.OVERSOLD] if self._is_oversold() else []
        result += [TechnicalTerm.OVERBOUGHT] if self._is_overbought() else []
        result += [TechnicalTerm.BEARISH_DIVERGENCE] if self._is_bearish_diverging() else []
        result += [TechnicalTerm.BULLISH_DIVERGENCE] if self._is_bullish_diverging() else []
        return result

    def _is_overbought(self, threshold: float = 80.0) -> bool:
        # Use a threshold of 70-75% to identify overextended conditions.
        non_commercial_report: NonCommercialTradersReport = self._cot_report.non_commercial_traders_report
        longs_percentage: float = non_commercial_report.longs_percentage
        return longs_percentage >= threshold

    def _is_oversold(self, threshold: float = 80.0) -> bool:
        # Use a threshold of 70-75% to identify overextended conditions.
        non_commercial_report: NonCommercialTradersReport = self._cot_report.non_commercial_traders_report
        shorts_percentage: float = non_commercial_report.shorts_percentage
        return shorts_percentage >= threshold

    def _is_bullish_diverging(self) -> bool:
        non_commercial_report: NonCommercialTradersReport = self._cot_report.non_commercial_traders_report
        delta_shorts: int = non_commercial_report.delta_shorts
        delta_longs: int = non_commercial_report.delta_longs
        return delta_shorts < 0 < delta_longs

    def _is_bearish_diverging(self) -> bool:
        non_commercial_report: NonCommercialTradersReport = self._cot_report.non_commercial_traders_report
        delta_shorts: int = non_commercial_report.delta_shorts
        delta_longs: int = non_commercial_report.delta_longs
        return delta_longs < 0 < delta_shorts