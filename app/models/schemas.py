from pydantic import BaseModel


class TextBlockResponse(BaseModel):
    src: str
    dst: str
    rect: str
    line_count: int
    points: list[dict]
    paste_img: str | None = None


class TranslateResponseData(BaseModel):
    from_lang: str
    to_lang: str
    src: str
    dst: str
    contents: list[TextBlockResponse]
    paste_img: str | None = None


class TranslateResponse(BaseModel):
    success: bool
    data: TranslateResponseData
