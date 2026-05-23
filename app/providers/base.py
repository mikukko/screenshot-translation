from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class TextBlock:
    src: str
    dst: str
    rect: str
    line_count: int
    points: list[dict]
    paste_img: str | None = None


@dataclass
class TranslationResult:
    from_lang: str
    to_lang: str
    src: str
    dst: str
    contents: list[TextBlock]
    paste_img: str | None = None
    raw_response: dict = field(default_factory=dict)


class TranslationProvider(ABC):
    @abstractmethod
    async def translate_image(
        self,
        image_bytes: bytes,
        from_lang: str,
        to_lang: str,
        paste: int = 0,
    ) -> TranslationResult: ...

    async def close(self) -> None: ...
