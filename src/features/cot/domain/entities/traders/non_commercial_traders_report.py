from src.features.cot.domain.entities.traders.traders_report import TradersReport


class NonCommercialTradersReport(TradersReport):
    def __init__(self, longs: int, shorts: int, delta_longs: int, delta_shorts: int, spreads: int | None = None):
        super().__init__(longs, shorts, delta_longs, delta_shorts)
        self._spreads: int = spreads

    def __repr__(self):
        return super().__repr__().replace("TradersReport", "Non-Commercial Traders Report")

    @property
    def spreads(self) -> int:
        return self._spreads