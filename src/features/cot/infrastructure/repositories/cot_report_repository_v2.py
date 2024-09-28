import os
from datetime import datetime, timedelta

import pandas as pd
import pytz
import cot_reports as cot

from src.features.cot.domain.entities.cot_report import CotReport
from src.features.cot.domain.entities.reported_assets import ReportedAssets
from src.features.cot.domain.entities.traders.commercial_traders_report import CommercialTradersReport
from src.features.cot.domain.entities.traders.non_commercial_traders_report import NonCommercialTradersReport
from src.features.cot.domain.rules.cot_repository import CotRepository
from src.shared.entities.asset import Asset


def save_dataframe_locally_as_csv(dataframe: pd.DataFrame, csv_filename: str) -> None:
    dataframe.to_csv(csv_filename)

def get_asset_cot_report(asset: Asset, dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe[
        dataframe["Market and Exchange Names"] == asset.market_and_exchange_name
        ]

def only_reported_assets_cot_report(dataframe: pd.DataFrame, period: int = 5) -> pd.DataFrame:
    only_reported_assets: list[pd.DataFrame] = []
    for reported_asset in ReportedAssets:
        asset: Asset = Asset(reported_asset)
        asset_cot_report: pd.DataFrame = get_asset_cot_report(asset, dataframe)
        asset_cot_report = asset_cot_report.sort_values(by="As of Date in Form YYYY-MM-DD", ascending=False)
        asset_cot_report = asset_cot_report[: period]
        only_reported_assets.append(asset_cot_report)
    return pd.concat(only_reported_assets)

def is_local_cot_report_up_to_date(local_cot_report_csv_filename) -> bool:
    """
    The Commitments of Traders (COT) report is released every Friday at 3:30 p.m.
    Eastern Time but is already available every Tuesday. This method checks if the given locally stored cot report
    is up to date.
    """
    local_cot_report_dataframe: pd.DataFrame = pd.read_csv(local_cot_report_csv_filename)
    local_cot_report_recent_datetime: str = local_cot_report_dataframe.iloc[0]["As of Date in Form YYYY-MM-DD"]
    local_cot_report_recent_datetime: datetime = datetime.strptime(local_cot_report_recent_datetime, "%Y-%m-%d")
    local_cot_report_recent_date = local_cot_report_recent_datetime.date()

    eastern_time_zone = pytz.timezone(zone="US/Eastern")
    current_eastern_time: datetime = datetime.now(eastern_time_zone)

    # Calculates the latest release date, which is the previous Tuesday.
    latest_release_date: datetime = current_eastern_time - timedelta(days=(current_eastern_time.weekday() - 1) % 7)
    localized_eastern_time: datetime = eastern_time_zone.localize(datetime.combine(
        latest_release_date, datetime.min.time()
    ))

    # Adds 3 days 15 hours and 30 minutes to get to Friday at 3:30 PM and checks if current time is after
    # the latest release time.
    localized_eastern_time += timedelta(days=3, hours=15, minutes=30)
    latest_release_time = localized_eastern_time

    is_current_eastern_time_after_latest_release: bool = current_eastern_time >= latest_release_time

    return is_current_eastern_time_after_latest_release and local_cot_report_recent_date >= latest_release_date.date()

def is_local_cot_report_valid_to_return(local_cot_report_filename: str, period: int) -> bool:
    is_exist: bool = os.path.exists(local_cot_report_filename)
    is_up_to_date: bool = is_local_cot_report_up_to_date(local_cot_report_filename)
    is_period_in_range: bool = period <= len(pd.read_csv(local_cot_report_filename))
    return is_exist and is_up_to_date and is_period_in_range

def make_cot_report(data: dict) -> CotReport:
    release_date: str = data["As of Date in Form YYYY-MM-DD"]
    market_name: str = data["Market and Exchange Names"]
    open_interest: int = data["Open Interest (All)"]
    non_commercial_traders_report: NonCommercialTradersReport = NonCommercialTradersReport(
        longs=data["Noncommercial Positions-Long (All)"],
        shorts=data["Noncommercial Positions-Short (All)"],
        delta_longs=int(data["Change in Noncommercial-Long (All)"]),
        delta_shorts=int(data["Change in Noncommercial-Short (All)"])
    )
    commercial_traders_report: CommercialTradersReport = CommercialTradersReport(
        longs=data["Commercial Positions-Long (All)"],
        shorts=data["Commercial Positions-Short (All)"],
        delta_longs=int(data["Change in Commercial-Long (All)"]),
        delta_shorts=int(data["Change in Commercial-Short (All)"])
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


class CotReportRepositoryV2(CotRepository):

    def __init__(self, all_asset_local_cot_report_csv_file: str = "Local_COT_Reports.csv"):
        self._all_asset_local_cot_report_as_csv: str = all_asset_local_cot_report_csv_file

    def get_report(self, asset: Asset, period: int) -> list[CotReport]:
        cot_reports: list[CotReport] = []
        asset_local_cot_report_csv_filename: str = f"{asset.abbreviation}_COT_Report.csv"
        cot_report_dataframe: pd.DataFrame = self._fetch_cot_report(asset_local_cot_report_csv_filename)
        only_asset_reports: pd.DataFrame = get_asset_cot_report(asset, cot_report_dataframe)
        only_asset_reports = only_asset_reports[: period]
        for index, row in only_asset_reports.iterrows():
            cot_report: CotReport = make_cot_report(row.to_dict())
            cot_reports.append(cot_report)
        save_dataframe_locally_as_csv(only_asset_reports, asset_local_cot_report_csv_filename)
        return cot_reports

    def _fetch_cot_report(self, asset_local_cot_report_csv_filename: str, period: int = 5) -> pd.DataFrame:
        """
        This method fetches the cot report from the official cot report website then stores it locally only
        if the locally stored cot report is not up to date.
        """
        if is_local_cot_report_valid_to_return(asset_local_cot_report_csv_filename, period):
            return pd.read_csv(asset_local_cot_report_csv_filename)

        elif is_local_cot_report_valid_to_return(self._all_asset_local_cot_report_as_csv, period * len(ReportedAssets)):
            return pd.read_csv(self._all_asset_local_cot_report_as_csv)

        recently_released_cot_report: pd.DataFrame = cot.cot_all(cot_report_type="legacy_fut", verbose=False)
        only_reported_assets: pd.DataFrame = only_reported_assets_cot_report(recently_released_cot_report, period)
        save_dataframe_locally_as_csv(only_reported_assets, self._all_asset_local_cot_report_as_csv)
        return only_reported_assets
