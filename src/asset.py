class Asset:

    def __init__(self, name: str, abbreviation: str, exchange_name: str):
        self._name: str = name
        self._abbreviation: str = abbreviation
        self._exchange_name: str = exchange_name

    def __repr__(self) -> str:
        return f"Asset(Name={self._name}, Abbreviation={self._abbreviation})"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def name(self) -> str:
        return self._name

    @property
    def abbreviation(self) -> str:
        return self._abbreviation

    @property
    def exchange_name(self) -> str:
        return self._exchange_name