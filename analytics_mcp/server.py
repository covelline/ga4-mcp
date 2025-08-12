#!/usr/bin/env python

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

"""Entry point for the Google Analytics MCP server."""

import logging
from analytics_mcp.coordinator import mcp
from analytics_mcp.config import get_config

# The following imports are necessary to register the tools with the `mcp`
# object, even though they are not directly used in this file.
# The `# noqa: F401` comment tells the linter to ignore the "unused import"
# warning.
from analytics_mcp.tools.admin import info  # noqa: F401
from analytics_mcp.tools.reporting import realtime  # noqa: F401
from analytics_mcp.tools.reporting import core  # noqa: F401


def run_server() -> None:
    """Runs the server.

    Serves as the entrypoint for the 'google-analytics-mcp' command.
    Uses STDIO transport for communication.
    """
    config = get_config()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Google Analytics MCP server with STDIO transport")
    
    if config.has_refresh_token_auth():
        logger.info("Using refresh token authentication")
    else:
        logger.info("Using Application Default Credentials")
    
    # Run with STDIO transport (default)
    mcp.run()


if __name__ == "__main__":
    run_server()
