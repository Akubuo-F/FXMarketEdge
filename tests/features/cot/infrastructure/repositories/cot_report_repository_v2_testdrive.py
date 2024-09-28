from src.features.cot.domain.entities.reported_assets import ReportedAssets
from src.features.cot.infrastructure.repositories.cot_report_repository_v2 import CotReportRepositoryV2
from src.shared.entities.asset import Asset
from src.features.cot.domain.entities.cot_report import CotReport


def main():
    assets: list[Asset] = make_assets()
    cot_report_repository_v2: CotReportRepositoryV2 = CotReportRepositoryV2()

    for asset in assets:
        cot_reports: list[CotReport] = cot_report_repository_v2.get_report(asset, 5)
        print("\n".join(map(lambda x: str(x), cot_reports)))

def make_assets() -> list[Asset]:
    assets: list[Asset] = []
    for report_asset in ReportedAssets:
        asset: Asset = Asset(report_asset)
        assets.append(asset)
    return assets


if __name__ == '__main__':
    main()