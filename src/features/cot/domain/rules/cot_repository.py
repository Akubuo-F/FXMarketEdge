from abc import ABC, abstractmethod

from src.shared.entities.asset import Asset
from src.features.cot.domain.entities.cot_report import CotReport


class CotRepository(ABC):

    @abstractmethod
    def get_report(self, asset: Asset, period: int) -> list[CotReport]:
        ...