"""
Configuration management for PTNutritionAI
"""
import os
from typing import Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings with Azure integration"""
    
    # Application settings
    app_name: str = "PTNutritionAI"
    debug: bool = Field(default=False, env="DEBUG")
    
    # Azure OpenAI Configuration
    azure_openai_endpoint: Optional[str] = Field(None, env="AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key: Optional[str] = Field(None, env="AZURE_OPENAI_API_KEY")
    azure_openai_api_version: str = Field("2024-02-15-preview", env="AZURE_OPENAI_API_VERSION")
    
    # Azure AI Foundry Configuration
    ai_foundry_project_name: Optional[str] = Field(None, env="AI_FOUNDRY_PROJECT_NAME")
    ai_foundry_endpoint: Optional[str] = Field(None, env="AI_FOUNDRY_ENDPOINT")
    
    # Model configurations
    pt_coach_model: str = Field("gpt-4", env="PT_COACH_MODEL")
    nutrition_coach_model: str = Field("gpt-4", env="NUTRITION_COACH_MODEL")
    
    # Azure Computer Vision (for meal analysis)
    azure_vision_endpoint: Optional[str] = Field(None, env="AZURE_VISION_ENDPOINT")
    azure_vision_api_key: Optional[str] = Field(None, env="AZURE_VISION_API_KEY")
    
    # Azure Cosmos DB
    cosmos_endpoint: Optional[str] = Field(None, env="COSMOS_ENDPOINT")
    cosmos_key: Optional[str] = Field(None, env="COSMOS_KEY")
    cosmos_database: str = Field("PTNutritionAI", env="COSMOS_DATABASE")
    
    # Azure Blob Storage
    storage_account_name: Optional[str] = Field(None, env="STORAGE_ACCOUNT_NAME")
    storage_account_key: Optional[str] = Field(None, env="STORAGE_ACCOUNT_KEY")
    storage_container: str = Field("user-images", env="STORAGE_CONTAINER")
    
    # JWT Configuration
    secret_key: str = Field("your-secret-key-change-in-production", env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Regional settings
    azure_region: str = Field("westeurope", env="AZURE_REGION")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
