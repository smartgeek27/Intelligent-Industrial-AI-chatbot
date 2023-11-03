class Config(object):
    DEBUG = True
    TESTING = False

class DevelopmentConfig(Config):
    SECRET_KEY = "this-is-a-super-secret-key"
    OPENAI_KEY = 'your_open_ai_key'

config = {
    'development': DevelopmentConfig,
    'testing': DevelopmentConfig,
    'production': DevelopmentConfig
}


COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDINGS_MODEL = "text-embedding-ada-002"
CHAT_MODEL = 'gpt-3.5-turbo'
# CHAT_MODEL = 'gpt-3.5-turbo-0613'

TEXT_EMBEDDING_CHUNK_SIZE=300
VECTOR_FIELD_NAME='content_vector'

PREFIX = "rishidoc"
INDEX_NAME = "rishi-index" # your index name used in indexing 


