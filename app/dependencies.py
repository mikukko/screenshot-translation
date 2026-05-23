from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings
from app.providers.baidu import BaiduTranslationProvider

_bearer = HTTPBearer()

_baidu_provider: BaiduTranslationProvider | None = None


def get_baidu_provider() -> BaiduTranslationProvider:
    global _baidu_provider
    if _baidu_provider is None:
        _baidu_provider = BaiduTranslationProvider(
            appid=settings.baidu_appid,
            token=settings.baidu_token,
        )
    return _baidu_provider


async def close_providers() -> None:
    global _baidu_provider
    if _baidu_provider is not None:
        await _baidu_provider.close()
        _baidu_provider = None


async def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> str:
    key = credentials.credentials
    if key not in settings.api_keys_list:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return key
