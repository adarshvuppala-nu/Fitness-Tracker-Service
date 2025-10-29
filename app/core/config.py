from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "postgresql://fitness_user:password@localhost:5432/fitness_tracker"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "fitness_tracker"
    DATABASE_USER: str = "fitness_user"
    DATABASE_PASSWORD: str = "password"

    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Fitness Tracker API"
    VERSION: str = "1.0.0"

    # Day 2: AI & LangChain Configuration
    OPENAI_API_KEY: str = ""
    OPENWEATHER_API_KEY: str = ""

    # Langfuse Observability
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()
