from abc import ABC, abstractmethod

from plaatisfinder.models import CamperAd


class BaseScraper(ABC):

    @abstractmethod
    def get_ads(self) -> list[CamperAd]:
        pass