"""Application configuration loaded from environment variables.

Uses pydantic-settings to validate and type-check settings on startup.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable mapping."""

    # Application environment
    environment: str = Field(
        default="development",
        description="Deployment environment",
    )
    host: str = Field(default="0.0.0.0", description="Host to bind the server")
    port: int = Field(default=8000, description="Port to bind the server")
    log_level: str = Field(default="INFO", description="Logging level")

    # Security & CORS
    cors_origins: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        description="Comma-separated allowed frontend origins",
    )

    # Database
    database_url: str = Field(
        default="postgresql://agrivision_user:example_password@localhost/agrivision",
        description="Neon PostgreSQL connection URL",
    )

    # ML Inference
    model_path: str = Field(
        default="ml/models/agrivision_mobilenetv2.onnx",
        description="Path to ONNX model file",
    )
    confidence_threshold: float = Field(
        default=0.70,
        description="Minimum confidence for accepting predictions",
    )
    max_image_size_mb: int = Field(
        default=5,
        description="Maximum allowed image upload size in MB",
    )

    # Frontend
    vite_api_url: str = Field(
        default="http://localhost:8000",
        description="API URL for frontend",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [
            origin.strip() for origin in self.cors_origins.split(",") if origin.strip()
        ]

    @property
    def max_image_size_bytes(self) -> int:
        """Maximum image size in bytes."""
        return self.max_image_size_mb * 1024 * 1024


settings = Settings()
