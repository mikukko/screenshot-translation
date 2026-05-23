from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.dependencies import get_baidu_provider, verify_api_key
from app.models.schemas import (
    TextBlockResponse,
    TranslateResponse,
    TranslateResponseData,
)
from app.providers.baidu import BaiduTranslationProvider, TranslationError

router = APIRouter(prefix="/api/v1/translate", tags=["translate"])


@router.post("/image", response_model=TranslateResponse)
async def translate_image(
    image: UploadFile = File(...),
    from_lang: str = Form(..., alias="from"),
    to_lang: str = Form(..., alias="to"),
    paste: int = Form(0),
    api_key: str = Depends(verify_api_key),
    provider: BaiduTranslationProvider = Depends(get_baidu_provider),
):
    image_bytes = await image.read()
    if not image_bytes:
        return TranslateResponse(
            success=False,
            data=TranslateResponseData(
                from_lang=from_lang,
                to_lang=to_lang,
                src="",
                dst="",
                contents=[],
            ),
        )

    try:
        result = await provider.translate_image(
            image_bytes=image_bytes,
            from_lang=from_lang,
            to_lang=to_lang,
            paste=paste,
        )
    except TranslationError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e),
        )

    contents = [
        TextBlockResponse(
            src=block.src,
            dst=block.dst,
            rect=block.rect,
            line_count=block.line_count,
            points=block.points,
            paste_img=block.paste_img,
        )
        for block in result.contents
    ]

    return TranslateResponse(
        success=True,
        data=TranslateResponseData(
            from_lang=result.from_lang,
            to_lang=result.to_lang,
            src=result.src,
            dst=result.dst,
            contents=contents,
            paste_img=result.paste_img,
        ),
    )
