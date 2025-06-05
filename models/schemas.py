from pydantic import BaseModel

class PromptModel(BaseModel):
    uri: str
    prompt: str

class FrequentQuestionModel(BaseModel):
    uri: str
    question: str
