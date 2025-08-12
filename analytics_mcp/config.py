# Copyright 2025 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Configuration module for MCP server with environment variable management."""

import os
from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Configuration for MCP server."""
    
    # Google OAuth2 settings
    refresh_token: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        config = cls()
        
        # Load Google OAuth2 settings
        refresh_token_path = os.getenv("GOOGLE_REFRESH_TOKEN_PATH")
        if refresh_token_path:
            try:
                with open(refresh_token_path, "r") as f:
                    config.refresh_token = f.read().strip()
                logger.info(f"Refresh token loaded from {refresh_token_path}")
            except FileNotFoundError:
                logger.warning(f"Refresh token file not found: {refresh_token_path}")
            except Exception as e:
                logger.error(f"Error loading refresh token: {e}")
        
        config.client_id = os.getenv("GOOGLE_CLIENT_ID")
        config.client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        
        # Validate OAuth2 configuration if refresh token is provided
        if config.refresh_token:
            if not config.client_id or not config.client_secret:
                raise ValueError(
                    "GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set "
                    "when using refresh token authentication"
                )
        
        # Load logging settings
        config.log_level = os.getenv("MCP_LOG_LEVEL", config.log_level).upper()
        if config.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            logger.warning(f"Invalid log level: {config.log_level}, using INFO")
            config.log_level = "INFO"
        
        return config
    
    def has_refresh_token_auth(self) -> bool:
        """Check if refresh token authentication is configured."""
        return bool(self.refresh_token and self.client_id and self.client_secret)
    
    def get_token_uri(self) -> str:
        """Get the OAuth2 token endpoint URI."""
        return "https://oauth2.googleapis.com/token"


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config.from_env()
    return _config