from src.features.cot.domain.entities.reported_assets import ReportedAssets
from src.shared.entities.asset import Asset
from src.features.cot.domain.entities.cot_report import CotReport
from src.features.cot.infrastructure.repositories.pycot_cot_repository import PycotCotRepository


def main():
    pycot_cot_repository: PycotCotRepository = PycotCotRepository()
    asset: Asset = Asset(ReportedAssets.AUD)
    cot_reports: list[CotReport] = pycot_cot_repository.get_report(asset, 4)
    print("\n".join(map(lambda x: str(x), cot_reports)))


if __name__ == '__main__':
    main()