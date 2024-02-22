# Proyecto RAG con LLMs 🤖

Este es un proyecto que busca desarrollar una solución simple de tipo RAG (retrieved augmented generation). Con esta solución, a través de una API, se permite interactuar con un LLM con el fin de generar una respuesta a partir de una pregunta dada por el usuario, en relación a un documento específico.

## Estructura del Repositorio 📁

El repositorio está organizado de la siguiente manera:

- **app**: Esta carpeta contiene el archivo `main.py`, donde se encuentra la estructura de la API.
  
- **use_cases**: En esta carpeta se encuentra el archivo `chatbot.py`, que contiene la clase que desarrolla toda la lógica para embeber la pregunta del usuario, hacer coincidir la pregunta con la similaridad del coseno, y devolver la respuesta utilizando el LLM de Coherence.

- **data**: Contiene el documento necesario para generar el RAG.

- **scripts**: Incluye un Jupyter Notebook para generar el embedding del documento y guardarlo en la base de datos de Pinecone.

- **tests**: Aquí se encuentran los archivos de prueba utilizando pytest para verificar el funcionamiento de la API.

- **gitignore**: Archivo que especifica patrones de archivos (como pycache o archivos de registro) que deben ser ignorados por Git.

- **requirements.txt**: Archivo que especifica las dependencias del proyecto.

## Pasos para Ejecutar Localmente 🛠️
### 0. Antes de Comenzar
Asegúrate de tener instalado:
    - Python >3.10

### 1. Clonar el Proyecto
```
git clone https://github.com/MelinaRG/rag_llm.git
```

### 2. Crear Entorno Virtual
```
python -m venv env  
```

### 3. Crear Archivo .env
Solicita las variables de entorno al equipo/profesional a cargo.

### 4. Activar Entorno Virtual
(NOTA: Esto debe hacerse cada vez que se abre una nueva terminal).
```
.\env\Scripts\activate
set DEVELOPMENT_ENV=1   

```

### 5. Instalar Dependencias
```
pip install -r requirements.txt
```

### 6. Ejecutar Localmente
```
uvicorn app.main:app --reload

```
## Test

Se utilizan pruebas unitarias con pytest.
Puedes ejecutar todas las pruebas con:

```
python -m pytest tests -s -v
```
