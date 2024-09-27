from src.asset import Asset
from src.features.cot.domain.entities.traders.commercial_traders_report import CommercialTradersReport
from src.features.cot.domain.entities.cot_report import CotReport
from src.features.cot.domain.entities.traders.non_commercial_traders_report import NonCommercialTradersReport
from src.features.cot.domain.repositories.cot_repository import CotRepository

from pycot.reports import CommitmentsOfTraders
import pandas as pd


def make_cot_report(data: dict) -> CotReport:
    open_interest: int = data["Open Interest"]
    non_commercial_traders_report: NonCommercialTradersReport = NonCommercialTradersReport(
        longs=data["Noncommercial Long"],
        shorts=data["Noncommercial Short"],
        delta_longs=0,
        delta_shorts=0
    )
    commercial_traders_report: CommercialTradersReport = CommercialTradersReport(
        longs=-1,
        shorts=-1,
        delta_longs=0,
        delta_shorts=0
    )
    delta_open_interest: int = data["Open Interest, Change"]
    return CotReport(
        "",
        "",
        open_interest,
        non_commercial_traders_report,
        commercial_traders_report,
        delta_open_interest
    )

class PycotCotRepository(CotRepository):

    def __init__(self):
        self._api: CommitmentsOfTraders = CommitmentsOfTraders("legacy_fut")

    def get_report(self, asset: Asset, period: int) -> list[CotReport]:
        cot_reports: list[CotReport] = []
        asset_contract_name: str = f"{asset.name.upper()} - {asset.exchange_name.upper()}"
        dataframe: pd.DataFrame = self._api.report(asset_contract_name)
        dataframe = dataframe[:period]
        for index, row in dataframe.iterrows():
            cot_report: CotReport = make_cot_report(row.to_dict())
            cot_reports.append(cot_report)
        dataframe.to_csv("cot_report.csv")
        return cot_reports