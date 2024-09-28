from src.features.cot.domain.entities.reported_assets import ReportedAssets


class Asset:

    def __init__(self, reported_asset: ReportedAssets):
        self._market_and_exchange_name: str = reported_asset.value
        self._abbreviation: str = reported_asset.name

    def __repr__(self) -> str:
        return f"Asset(Abbreviation={self._abbreviation}, Market_and_Exchange_Name={self._market_and_exchange_name})"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def market_and_exchange_name(self) -> str:
        return self._market_and_exchange_name

    @property
    def abbreviation(self) -> str:
        return self._abbreviation