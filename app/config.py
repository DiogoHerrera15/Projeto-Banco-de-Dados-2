from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "Ecommerce Deferente API"
    debug: bool = True

    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "ecommerce_deferente"
    db_user: str = "admin_deferente"
    db_password: str = "Admin@123"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
            f"?charset=utf8mb4"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
    )


settings = Settings()
