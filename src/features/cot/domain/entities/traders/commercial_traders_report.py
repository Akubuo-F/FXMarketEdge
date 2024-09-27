from src.features.cot.domain.entities.traders.traders_report import TradersReport


class CommercialTradersReport(TradersReport):
    def __init__(self, longs: int, shorts: int, delta_longs: int, delta_shorts: int):
        super().__init__(longs, shorts, delta_longs, delta_shorts)

    def __repr__(self):
        return super().__repr__().replace("TradersReport", "Commercial Traders Report")