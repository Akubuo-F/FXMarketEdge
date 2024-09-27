from src.features.cot.domain.entities.traders.traders_report import TradersReport


class CotReport:

    def __init__(
            self,
            release_date: str,
            market_name: str,
            open_interest: int,
            non_commercial_traders_report: TradersReport,
            commercial_traders_report: TradersReport,
            delta_open_interest: int,
    ):
        self._release_date: str = release_date
        self._market_name: str = market_name
        self._open_interest: int = open_interest
        self._non_commercial_traders_report: TradersReport = non_commercial_traders_report
        self._commercial_traders_report: TradersReport = commercial_traders_report
        self._delta_open_interest: int = delta_open_interest

    def __repr__(self) -> str:
        release_date: str = f"Release Date = {self._release_date}"
        market_name: str = f"Market Name = {self._market_name}"
        open_interest: str = f"Open Interest = {self._open_interest}"
        delta_open_interest: str = f"Open Interest Change= {self._delta_open_interest}"
        joined: str = ", ".join([
            release_date,
            market_name,
            open_interest,
            str(self._non_commercial_traders_report),
            str(self._commercial_traders_report),
            delta_open_interest
        ])
        return f"CotReport({joined})"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def release_date(self) -> str:
        return self._release_date

    @property
    def market_name(self) -> str:
        return self._market_name

    @property
    def open_interest(self) -> int:
        return self._open_interest

    @property
    def non_commercial_traders_report(self) -> TradersReport:
        return self._non_commercial_traders_report

    @property
    def commercial_traders_report(self) -> TradersReport:
        return self._commercial_traders_report

    @property
    def delta_open_interest(self) -> int:
        return self._delta_open_interest