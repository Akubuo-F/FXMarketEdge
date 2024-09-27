from src.asset import Asset
from src.exchange import Exchange
from src.features.cot.domain.entities.cot_report import CotReport
from src.features.cot.infrastructure.repositories.cot_reports_repository import CotReportsRepository


def main():
    asset: Asset = Asset("CANADIAN DOLLAR", "CAD", Exchange.FOREX.value)
    cot_report_repository: CotReportsRepository = CotReportsRepository()
    cot_reports: list[CotReport] = cot_report_repository.get_report(asset, 5)
    print("\n".join(map(lambda x: str(x), cot_reports)))

if __name__ == '__main__':
    main()