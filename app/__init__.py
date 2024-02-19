import os



if os.environ.get('DEVELOPMENT_ENV'):
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
