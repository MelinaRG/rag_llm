from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import cohere

class GenerateAnswer:
    def __init__(self, user_name: str, question: str):
        self.user_name = user_name
        self.question = question
        self.__model = SentenceTransformer('all-MiniLM-L6-v2') #384 dimensional
        self.__index = self.__init_pinecone()
        self.__co = cohere.Client('')

    def __init_pinecone(self):
        pc = Pinecone(api_key="")
        return pc.Index("")

    def __find_match(self, question: str):
        input_em = self.__model.encode(question).tolist()
        result = self.__index.query(vector=input_em, top_k=1, includeMetadata=True)
        return result["matches"][0]["metadata"]["text"]

    def __generate_answer(self, question: str):

        
        response = self.__co.chat(
            message=question,
            model="command",
            temperature=0.2,
        )

        return response.text
        

    def execute(self) -> str:
        result = self.ask(self.question)
        return result

    def ask(self, question: str) -> str:
        context = self.__find_match(question)
        headers = self.generate_header(question)
        prompt = f"{headers}\n{context}"
        result = self.__generate_answer(prompt)
    
        return result


    def generate_header(self, question: str) -> str:
        # Prompt simplificado para mantener la coherencia en las respuestas
        prompt = ("Por favor, responda a la pregunta en una sola oración, utilizando el mismo idioma que se utilizó para formular la pregunta.\n"
                "Asegúrese de que su respuesta sea consistente ante la misma pregunta y añada emojis que reflejen el contenido.\n"
                "Además, formule su respuesta en tercera persona.\n"
                "A continuación, por favor, proporcione su respuesta:")

        return f"{question}\n\n{prompt}"

