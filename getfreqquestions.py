from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
import logging
import json

from mcp.client.sse import sse_client
from mcp import ClientSession

router = APIRouter()

# Setup logger
logger = logging.getLogger("frequent_questions")
logging.basicConfig(level=logging.INFO)

@router.get("/frequent_questions/{aplctn_cd}")
async def get_frequent_questions(aplctn_cd: str):
    """
    Fetch and return the raw frequent questions JSON from the MCP resource
    """
    try:
        async with sse_client("http://localhost:8000/sse") as connection:
            async with ClientSession(*connection) as session:
                await session.initialize()

                resource_uri = f"genaiplatform://{aplctn_cd}/frequent_questions/hedis-question"
                logger.info(f"🔍 Fetching resource: {resource_uri}")

                result = await session.read_resource(resource_uri)

                if not result:
                    raise HTTPException(status_code=404, detail="No frequent questions found.")

                # Return raw JSON string with correct MIME type
                return Response(content=json.dumps(result), media_type="application/json")

    except HTTPException as e:
        logger.error(f"Request error: {e}")
        raise e

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
