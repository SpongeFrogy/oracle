from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    API_BASE_URL: str = 'http://oracle:8000'



settings = Settings()
