from src.features.cot.applications.cot_report_analyser import CotReportAnalyser
from src.features.cot.domain.entities.cot_report import CotReport
from src.features.cot.domain.entities.reported_assets import ReportedAssets
from src.features.cot.domain.rules.cot_repository import CotRepository
from src.features.cot.infrastructure.repositories.cot_report_repository import CotReportRepository
from src.shared.entities.asset import Asset
from src.shared.entities.terms.sentiment_terms import Sentiment
from src.shared.entities.terms.technical_terms import TechnicalTerm
from src.shared.entities.terms.trend_terms import Trend


def main():
    cot_repository: CotRepository = CotReportRepository(save_report=True)
    asset: Asset = Asset(ReportedAssets.XAG)
    cot_report: CotReport = cot_repository.get_report(asset, 2)[0]
    print(cot_report)
    cot_report_analyser: CotReportAnalyser = CotReportAnalyser(cot_report)

    sentiment: Sentiment = cot_report_analyser.analyse_sentiment()
    trend: Trend = cot_report_analyser.analyse_trend()
    technicals: list[TechnicalTerm] = cot_report_analyser.analyse_technicals()

    print(sentiment.name)
    print(trend.name)
    for term in technicals:
        print(term.name)


if __name__ == '__main__':
    main()