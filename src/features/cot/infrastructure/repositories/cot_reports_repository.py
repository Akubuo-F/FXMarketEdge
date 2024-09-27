from src.asset import Asset
from src.features.cot.domain.entities.traders.commercial_traders_report import CommercialTradersReport
from src.features.cot.domain.entities.cot_report import CotReport
from src.features.cot.domain.entities.traders.non_commercial_traders_report import NonCommercialTradersReport
from src.features.cot.domain.repositories.cot_repository import CotRepository

import pandas as pd
import cot_reports as cot


def get_asset_cot_report(asset: Asset, dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe[
        dataframe["Market and Exchange Names"] == f"{asset.name} - {asset.exchange_name}"
        ]

def make_cot_report(data: dict) -> CotReport:
    release_date: str = data["As of Date in Form YYYY-MM-DD"]
    market_name: str = data["Market and Exchange Names"]
    open_interest: int = data["Open Interest (All)"]
    non_commercial_traders_report: NonCommercialTradersReport = NonCommercialTradersReport(
        longs=data["Noncommercial Positions-Long (All)"],
        shorts=data["Noncommercial Positions-Short (All)"],
        delta_longs=data["Change in Noncommercial-Long (All)"],
        delta_shorts=data["Change in Noncommercial-Short (All)"]
    )
    commercial_traders_report: CommercialTradersReport = CommercialTradersReport(
        longs=data["Commercial Positions-Long (All)"],
        shorts=data["Commercial Positions-Short (All)"],
        delta_longs=data["Change in Commercial-Long (All)"],
        delta_shorts=data["Change in Commercial-Short (All)"]
    )
    delta_open_interest: int = data["Change in Open Interest (All)"]
    return CotReport(
        release_date=release_date,
        market_name=market_name,
        open_interest=open_interest,
        non_commercial_traders_report=non_commercial_traders_report,
        commercial_traders_report=commercial_traders_report,
        delta_open_interest=delta_open_interest
    )


class CotReportsRepository(CotRepository):

    def __init__(self, csv_output_filename: str = "CotReports.csv"):
        self._csv_output_filename: str = csv_output_filename

    def get_report(self, asset: Asset, period: int) -> list[CotReport]:
        cot_reports: list[CotReport] = []
        dataframe: pd.DataFrame = cot.cot_all(cot_report_type="legacy_fut", verbose=False)
        dataframe = get_asset_cot_report(asset, dataframe)
        dataframe = dataframe.sort_values(by="As of Date in Form YYYY-MM-DD", ascending=False)
        dataframe = dataframe[: period]
        for index, row in dataframe.iterrows():
            cot_report: CotReport = make_cot_report(row.to_dict())
            cot_reports.append(cot_report)
        dataframe.to_csv(self._csv_output_filename)
        return cot_reports