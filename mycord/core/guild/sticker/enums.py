from typing import Dict

from ....utils.enums import Enum

class StickerType(Enum):
    standard = 1
    guild = 2


class StickerFormatType(Enum):
    png = 1
    apng = 2
    lottie = 3
    gif = 4

    @property
    def file_extension(self) -> str:
        # fmt: off
        lookup: Dict[StickerFormatType, str] = {
            StickerFormatType.png: 'png',
            StickerFormatType.apng: 'png',
            StickerFormatType.lottie: 'json',
            StickerFormatType.gif: 'gif',
        }
        # fmt: on
        return lookup.get(self, 'png')