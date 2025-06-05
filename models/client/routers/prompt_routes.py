from fastapi import APIRouter, HTTPException, status
from loguru import logger
from models.schemas import PromptModel, FrequentQuestionModel
from client.mcp_client import get_client
from mcp import ClientSession

route = APIRouter()

@route.get("/prompts/{aplctn_cd}")
async def get_prompts(aplctn_cd: str):
    try:
        async with get_client() as connection:
            async with ClientSession(*connection) as session:
                await session.initialize()
                result = await session.read_resource(f"genaiplatform://{aplctn_cd}/prompts/hedis-prompt")
                return result
    except Exception as e:
        logger.error(f"Unexpected error in get_prompts: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@route.get("/frequent_questions/{aplctn_cd}")
async def get_frequent_questions(aplctn_cd: str):
    try:
        async with get_client() as connection:
            async with ClientSession(*connection) as session:
                await session.initialize()
                result = await session.read_resource(f"genaiplatform://{aplctn_cd}/frequent_questions/hedis-question")
                return result
    except Exception as e:
        logger.error(f"Unexpected error in get_frequent_questions: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@route.post("/add_prompt")
async def add_prompt(data: PromptModel):
    try:
        async with get_client() as connection:
            async with ClientSession(*connection) as session:
                await session.initialize()
                result = await session.call_tool(name="add-prompts", arguments={
                    "uri": data.uri,
                    "prompt": data.prompt
                })
                return result
    except Exception as e:
        logger.error(f"Unexpected error in add_prompt: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@route.post("/add_frequent_question")
async def add_frequent_question(data: FrequentQuestionModel):
    try:
        async with get_client() as connection:
            async with ClientSession(*connection) as session:
                await session.initialize()
                result = await session.call_tool(name="add-frequent-questions", arguments={
                    "uri": data.uri,
                    "question": data.question
                })
                return result
    except Exception as e:
        logger.error(f"Unexpected error in add_frequent_question: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
