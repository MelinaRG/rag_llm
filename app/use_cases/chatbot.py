from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import cohere
from langdetect import detect

class GenerateAnswer:
    def __init__(self, user_name: str, question: str):
        self.user_name = user_name
        self.question = question
        self.__model = SentenceTransformer('all-MiniLM-L6-v2') #384 dimensional
        self.__index = self.__init_pinecone()
        self.__co = cohere.Client('8e99EgyI6c94jF0Q9KEARQDHfZAZC03xDODJx4ks')

    def __init_pinecone(self):
        pc = Pinecone(api_key="1dd271a4-8d83-4a45-b744-a883e412d992")
        return pc.Index("chatbot")

    def __find_match(self, question: str):
        input_em = self.__model.encode(question).tolist()
        result = self.__index.query(vector=input_em, top_k=1, includeMetadata=True)
        return result["matches"][0]["metadata"]["text"]

    def __generate_answer(self, prompt: str):

        response = self.__co.chat(
            message=prompt,
            model="command",
            temperature=0.1,
            max_tokens=50
        )

        return response.text
        

    def execute(self) -> str:
        result = self.ask(self.question, self.user_name)
        return result

    def ask(self, question: str, user_name: str) -> str:
        context = self.__find_match(question)
        language = self.detect_language(question)
        prompt = self.generate_header(question, user_name, context, language)
        result = self.__generate_answer(prompt)
        return result


    def generate_header(self, question: str, user_name: str, context: str, language: str) -> str:
        return f"""Tu tarea es responder la siguiente pregunta: '{question}' del usuario '{user_name}',
                    utiliza emojis en tus respuestas y responde siempre en base a la información proporcionada
                    en el siguiente contexto: '{context}'. La respuesta debe ser corta, sólo una oración, sé consistente.
                    Responde en {language}.
                    Ejemplos de respuestas:
                    - user: ¿Quién es Maria? answer: Maria es una artista.
                    - user: ¿Cómo se llama el perro? answer: El perro se llama Beto.
                    - user: ¿Where is she from? answer: She is from Canadá.
                   """
    def detect_language(self, text: str) -> str:
        try:
            return print(detect(text))
        except:
            return "es"

