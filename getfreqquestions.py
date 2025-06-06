from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
import json
import logging

from mcp.client.sse import sse_client
from mcp import ClientSession

route = APIRouter()

# Logger setup
logger = logging.getLogger("mcp_resource_reader")
logging.basicConfig(level=logging.INFO)

@route.get("/prompts/{aplctn_cd}")
async def get_prompts(aplctn_cd: str):
    """
    Fetch and return the full prompt JSON from MCP resource URI.
    URI pattern: genaiplatform://{aplctn_cd}/prompts/hedis-prompt
    """
    try:
        async with sse_client("http://localhost:8000/sse") as connection:
            async with ClientSession(*connection) as session:
                await session.initialize()

                # Define resource URI
                uri = f"genaiplatform://{aplctn_cd}/prompts/hedis-prompt"
                logger.info(f"📥 Fetching MCP resource: {uri}")

                # Read from MCP resource registry
                result = await session.read_resource(uri)

                if not result:
                    raise HTTPException(status_code=404, detail="MCP resource not found.")

                # Return as raw JSON
                return Response(
                    content=json.dumps(result, indent=2),
                    media_type="application/json"
                )

    except HTTPException as e:
        logger.error(f"HTTP error: {e}")
        raise e

    except Exception as e:
        logger.exception("Unexpected error while reading MCP resource.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
