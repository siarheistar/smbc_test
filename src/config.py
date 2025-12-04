"""
Configuration management using environment variables
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application Configuration
    app_name: str = "Anagram Checker API"
    app_version: str = "1.0.0"
    app_description: str = "API to check if two strings are anagrams"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True

    # API Configuration
    api_prefix: str = "/api"
    api_check_endpoint: str = "/api/check"
    health_endpoint: str = "/health"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"

    # CORS Configuration
    cors_origins: str = "*"
    cors_allow_credentials: bool = True
    cors_allow_methods: str = "*"
    cors_allow_headers: str = "*"

    # Application URLs
    base_url: str = "http://localhost:8000"
    api_url: str = "http://localhost:8000/api"

    # UI Configuration
    ui_title: str = "Anagram Checker"
    ui_primary_color: str = "#4CAF50"
    ui_primary_color_hover: str = "#45a049"
    copyright_name: str = "Siarhei Staravoitau"

    # Testing Configuration
    test_server_url: str = "http://localhost:8000"
    test_timeout: int = 30000
    test_browser: str = "firefox"
    test_headed: bool = False

    # Validation Configuration
    min_input_length: int = 2
    max_input_length: int = 1000

    # Environment
    environment: str = "development"
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS origins string to list"""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Create global settings instance
settings = Settings()
