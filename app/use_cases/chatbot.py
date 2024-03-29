from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import cohere
from langdetect import detect
import os

# Clase para generar la respuesta del chatbot
class GenerateAnswer:
    def __init__(self, user_name: str, question: str):
        # Inicialización de los atributos de la instancia
        self.user_name = user_name
        self.question = question
        # Inicialización de modelos y servicios externos
        self.__model = SentenceTransformer('all-MiniLM-L6-v2') #384 dimensional
        self.__index = self.__init_pinecone()
        self.__co = cohere.Client(os.environ.get('COHERE_API_KEY'))

    # Llamada a la función para generar la respuesta
    def execute(self) -> str:
        result = self.__ask(self.question, self.user_name)
        return result
    
    # Inicialización del pinecone
    def __init_pinecone(self):
        pc = Pinecone(api_key=os.environ.get('PINECONE_API_KEY'),)
        return pc.Index(os.environ.get('PINECONE_INDEX'))

    #Embbeding de la pregunta y busqueda de similitudes
    def __find_match(self, question: str):
        input_em = self.__model.encode(question).tolist()
        result = self.__index.query(vector=input_em, top_k=1, includeMetadata=True)
        return result["matches"][0]["metadata"]["text"]

    # Generación de la respuesta a traves del LLM
    def __generate_answer(self, prompt: str):
        response = self.__co.chat(
            message=prompt,
            model="command",
            temperature=0.1,
            max_tokens=50
        )
        return response.text
        
    #Llamada para iniciar el proceso de generación de respuesta
    def __ask(self, question: str, user_name: str) -> str:
        context = self.__find_match(question)
        language = self.__detect_language(question)
        prompt = self.__generate_header(question, user_name, context, language)
        result = self.__generate_answer(prompt)
        return result

    # Generación del prompt
    def __generate_header(self, question: str, user_name: str, context: str, language: str) -> str:
        return f"""Tu tarea es responder la siguiente pregunta: '{question}' del usuario '{user_name}',
                    utiliza emojis en tus respuestas y responde siempre en base a la información proporcionada
                    en el siguiente contexto: '{context}'. La respuesta debe ser corta, sólo una oración, sé consistente.
                    Responde en {language}.
                    Ejemplos de respuestas:
                    - user: ¿Quién es Maria? answer: Maria es una artista.
                    - user: ¿Cómo se llama el perro? answer: El perro se llama Beto.
                    - user: ¿Where is she from? answer: She is from Canadá.
                   """
    #Detección del lenguaje para mejorar el prompt
    def __detect_language(self, text: str) -> str:
        try:
            return detect(text)
        except:
            return "es"

