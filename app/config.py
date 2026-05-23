from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    baidu_appid: str
    baidu_token: str  # API Key from Baidu console (管理控制台 → APIKey管理)

    api_keys: str  # comma-separated, e.g. "sk-key1,sk-key2"

    host: str = "0.0.0.0"
    port: int = 8000
    rate_limit_per_minute: int = 60

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def api_keys_list(self) -> list[str]:
        return [k.strip() for k in self.api_keys.split(",") if k.strip()]


settings = Settings()
