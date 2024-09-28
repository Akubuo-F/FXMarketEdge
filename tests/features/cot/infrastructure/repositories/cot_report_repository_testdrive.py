from src.features.cot.domain.entities.reported_assets import ReportedAssets
from src.shared.entities.asset import Asset
from src.features.cot.domain.entities.cot_report import CotReport
from src.features.cot.infrastructure.repositories.cot_report_repository import CotReportRepository


def main():
    asset: Asset = Asset(ReportedAssets.CAD)
    cot_report_repository: CotReportRepository = CotReportRepository()
    cot_reports: list[CotReport] = cot_report_repository.get_report(asset, 5)
    print("\n".join(map(lambda x: str(x), cot_reports)))

if __name__ == '__main__':
    main()