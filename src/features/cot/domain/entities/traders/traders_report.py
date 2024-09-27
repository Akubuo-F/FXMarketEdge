class TradersReport:

    def __init__(self, longs: int, shorts: int, delta_longs: int, delta_shorts: int):
        self._longs: int = abs(longs)
        self._shorts: int = abs(shorts)
        self._delta_longs: int = delta_longs
        self._delta_shorts: int = delta_shorts

    def __repr__(self) -> str:
        longs: str = f"Longs = {self._longs}"
        shorts: str = f"Shorts = {self._shorts}"
        net_position: str = f"Net_Position = {self.net_position}"
        longs_percentage: str = f"Longs% = {self.longs_percentage}"
        shorts_percentage: str = f"Shorts% = {self.shorts_percentage}"
        delta_longs: str = f"Change in Longs = {self._delta_longs}"
        delta_shorts: str = f"Change in Shorts = {self._delta_shorts}"
        joined: str = ", ".join([
            longs,
            shorts,
            net_position,
            longs_percentage,
            shorts_percentage,
            delta_longs,
            delta_shorts
        ])
        return f"TradersReport({joined})"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def longs(self) -> int:
        return self._longs

    @property
    def shorts(self) -> int:
        return self._longs

    @property
    def delta_longs(self) -> int:
        return self._delta_longs

    @property
    def delta_shorts(self) -> int:
        return self._delta_longs

    @property
    def net_position(self) -> int:
        return self._longs - self._shorts

    @property
    def longs_percentage(self) -> float:
        return self._get_percentage(self._longs)

    @property
    def shorts_percentage(self) -> float:
        return self._get_percentage(self._shorts)

    def _get_percentage(self, value: int) -> float:
        percentage: float = (value / (self._longs + self._shorts)) * 100
        return round(percentage, 1)