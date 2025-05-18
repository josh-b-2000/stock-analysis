from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=find_dotenv(usecwd=True), extra="ignore")

    alpha_vantage_base_url: str
    alpha_vantage_api_key: str
