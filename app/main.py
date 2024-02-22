from fastapi import FastAPI
from .use_cases.chatbot import GenerateAnswer

app = FastAPI()

# Definición de la ruta POST para el endpoint
@app.post(
        "/askme",
        operation_id= 'askme_chatbot'
)
async def generate_answer(
    user_name : str,
    question : str
):
    # Llamada a la función para generar la respuesta
    result = GenerateAnswer(user_name, question).execute()

    return result