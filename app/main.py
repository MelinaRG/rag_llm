from fastapi import FastAPI
from .use_cases.chatbot import GenerateAnswer

app = FastAPI()

@app.post(
        "/askme",
        operation_id= 'askme_chatbot'
)
async def generate_answer(
    user_name : str,
    question : str
):
    result = GenerateAnswer(user_name, question).execute()

    return result