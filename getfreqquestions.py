from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
import json
import logging

from mcp.client.sse import sse_client
from mcp import ClientSession

route = APIRouter()

logger = logging.getLogger("frequent_questions")
logging.basicConfig(level=logging.INFO)

@route.get("/frequent_questions/{aplctn_cd}")
async def get_frequent_questions(aplctn_cd: str):
    """
    Runs the 'get-frequent-questions' MCP tool with the given application code and returns the raw JSON.
    """
    try:
        async with sse_client("http://localhost:8000/sse") as connection:
            async with ClientSession(*connection) as session:
                await session.initialize()

                # Input to the MCP tool
                tool_input = {"aplctn_cd": aplctn_cd}

                logger.info(f"🚀 Running MCP tool 'get-frequent-questions' with input: {tool_input}")
                result = await session.run_tool("get-frequent-questions", input=tool_input)

                if not result:
                    raise HTTPException(status_code=404, detail="Tool returned no result")

                return Response(content=json.dumps(result), media_type="application/json")

    except HTTPException as e:
        logger.error(f"❌ HTTP error in get_frequent_questions: {e}")
        raise e

    except Exception as e:
        logger.error(f"❌ Unexpected error in get_frequent_questions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
