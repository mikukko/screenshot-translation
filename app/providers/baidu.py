import base64

import httpx

from app.providers.base import TextBlock, TranslationProvider, TranslationResult


class TranslationError(Exception):
    pass


class BaiduTranslationProvider(TranslationProvider):
    API_URL = "https://fanyi-api.baidu.com/ait/api/picture/translate"

    def __init__(self, appid: str, token: str) -> None:
        self.appid = appid
        self.token = token
        self._client = httpx.AsyncClient(timeout=30.0)

    async def translate_image(
        self,
        image_bytes: bytes,
        from_lang: str,
        to_lang: str,
        paste: int = 0,
        view_type: int = 1,
        model_type: str = "nmt",
        need_intervene: int = 0,
    ) -> TranslationResult:
        content = base64.b64encode(image_bytes).decode("utf-8")

        payload = {
            "from": from_lang,
            "to": to_lang,
            "appid": self.appid,
            "content": content,
            "paste": paste,
            "view_type": view_type,
            "model_type": model_type,
            "need_intervene": need_intervene,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        resp = await self._client.post(
            self.API_URL, json=payload, headers=headers
        )
        resp.raise_for_status()
        result = resp.json()

        error_code = result.get("error_code", result.get("errno"))
        if error_code and str(error_code) != "0":
            error_msg = result.get("error_msg", result.get("errmsg", "unknown"))
            raise TranslationError(
                f"Baidu API error {error_code}: {error_msg}"
            )

        contents = [
            TextBlock(
                src=item.get("src", ""),
                dst=item.get("dst", ""),
                rect=item.get("rect", ""),
                line_count=item.get("line_count", 0),
                points=item.get("points", []),
                paste_img=item.get("paste_img"),
            )
            for item in result.get("contents", [])
        ]

        return TranslationResult(
            from_lang=result.get("from", from_lang),
            to_lang=result.get("to", to_lang),
            src=result.get("src", ""),
            dst=result.get("dst", ""),
            contents=contents,
            paste_img=result.get("paste_img"),
            raw_response=result,
        )

    async def close(self) -> None:
        await self._client.aclose()
