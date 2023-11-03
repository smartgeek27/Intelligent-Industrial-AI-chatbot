import openai
import os
import requests
import numpy as np
import pandas as pd
from typing import Iterator
import tiktoken
import textract
from numpy import array, average
from pdfminer.high_level import extract_text

from database import get_redis_connection, get_redis_results
from transformers import handle_file_string

# Set our default models and chunking size
from config import COMPLETIONS_MODEL, EMBEDDINGS_MODEL, CHAT_MODEL, TEXT_EMBEDDING_CHUNK_SIZE, VECTOR_FIELD_NAME, PREFIX, INDEX_NAME


##Additional Line
import config
openai.api_key = config.DevelopmentConfig.OPENAI_KEY


# Setup Redis
from redis import Redis
from redis.commands.search.query import Query
from redis.commands.search.field import (
    TextField,
    VectorField,
    NumericField
)
from redis.commands.search.indexDefinition import (
    IndexDefinition,
    IndexType
)

redis_client = get_redis_connection() ## connect to redis database 
VECTOR_DIM = 1536
DISTANCE_METRIC = "euclidean"
location = 'data' # location of all your pdf's on which you need to ask the questions
query = 'what is L-27 ? ' ## this is the query you wanna ask for testing purpose. 

def getPDFFiles():
    data_dir = os.path.join(os.curdir,location)
    pdf_files = sorted([x for x in os.listdir(data_dir) if 'DS_Store' not in x])
    return pdf_files,data_dir


def createDatabaseIndex():
    # Define RediSearch fields for each of the columns in the dataset
    # This is where you should add any additional metadata you want to capture
    filename = TextField("filename")
    text_chunk = TextField("text_chunk")
    file_chunk_index = NumericField("file_chunk_index")

    # define RediSearch vector fields to use HNSW index

    text_embedding = VectorField(VECTOR_FIELD_NAME,
        "HNSW", {
            "TYPE": "FLOAT32",
            "DIM": VECTOR_DIM,
            "DISTANCE_METRIC": DISTANCE_METRIC
        }
    )
    # Add all our field objects to a list to be created as an index
    fields = [filename,text_chunk,file_chunk_index,text_embedding]

    # print(redis_client.ping())
    try:
        redis_client.ft(INDEX_NAME).info()
        print(f"Index {INDEX_NAME} already exists")
    except Exception as e:
        redis_client.ft(INDEX_NAME).create_index(fields = fields,
        definition = IndexDefinition(prefix=[PREFIX],
        index_type=IndexType.HASH))
        print(f"Index {INDEX_NAME} was created succesfully")

    return True


def addDocumentsToIndex(out):
    
    pdf_files = out[0]
    data_dir = out[1]

    # Initialise tokenizer
    tokenizer = tiktoken.get_encoding("cl100k_base")

    # Process each PDF file and prepare for embedding
    for pdf_file in pdf_files:
        pdf_path = os.path.join(data_dir,pdf_file)
       
        if not os.path.isfile(pdf_path):
            print(f'No file exists at {pdf_path}')
            continue

        text = extract_text(pdf_path)
      
        # Chunk each document, embed the contents and load to Redis
        handle_file_string((pdf_file,text),tokenizer,redis_client,VECTOR_FIELD_NAME,INDEX_NAME)



def queryRedisDatabase(query):
    result_df = get_redis_results(redis_client,query,index_name=INDEX_NAME)
    redis_result = result_df['result'][0]
    # print(redis_result, "i am redis resul")
    messages = []
    # your prompt here Probabaly the most important part of the code. 
    messages.append({"role": "system", "content": "You are an advanced AI chatbot developed for Sabin, designed to assist users by providing answers to their queries related to Sabin's products. Only answer questions asked, provide no information about the source."})

    ENGINEERING_PROMPT = f"""
    Answer this question: {query}
    Using this information: {redis_result}
    """
    question = {}
    question['role'] = 'user'
    question['content'] = ENGINEERING_PROMPT
    messages.append(question)
    response = openai.ChatCompletion.create(model=CHAT_MODEL,messages=messages,temperature =0.2)
    # response = openai.ChatCompletion.create(model=COMPLETIONS_MODEL,messages=messages)

    print(" ####################################################")
    try:
        answer = response['choices'][0]['message']['content'].replace('\n', '<br>')
    except:
        answer = 'Oops you beat the AI, try a different question, if the problem persists, come back later.'

    return answer


### storing all the previous chats and adding memory to the AI chatbot. 
history = []
# history.append({"role": "system", "content": "You are an advanced AI chatbot representing our company Sabin, you are designed to assist users by providing answers to their queries related to Sabin's products. Only answer the sepecific questions, provide no other information "})

def customChatGPTAnswer(the_query, new_conversation=False):
    result_df = get_redis_results(redis_client,the_query,index_name=INDEX_NAME)
    redis_result = result_df['result'][0]

    history.append({"role": "system", "content": "You are Wallace, an advanced AI chatbot created to represent Sabin."})
    # history.append({"role": "user", "content": " Introduce yourself "})

    ENGINEERING_PROMPT = f"""
    Answer this question: {the_query}
    Using this information: {redis_result}
    """

    history.append({"role": "user", "content": ENGINEERING_PROMPT})
    messages = history

    response = openai.ChatCompletion.create(model=CHAT_MODEL,messages=messages,temperature = 0.2)
    # response = openai.Completion.create(model=COMPLETIONS_MODEL,prompt=messages)
    try:
        answer = response['choices'][0]['message']['content'].replace('\n', '<br>')
    except:
        answer = 'Oops you beat the AI, try a different question, if the problem persists, come back later.'

    # try:
    #     answer_content = response['choices'][0]['message']['content'].replace('\n', '<br>')
    #     if new_conversation:
    #         answer_content = "I am Wallace, here to assist you: " + answer_content
    #     answer = answer_content
    # except:
    #     answer = 'Oops, you beat the AI. Try a different question, or if the problem persists, come back later.'

    # Store the bot's response in the history
    history.append({"role": "assistant", "content": answer})

    # Once again, only keep the last 5 messages
    # history = history[-5:]
    # print(len(messages), " here is the length")

    if len(history) > 25:
        history.clear()

    return answer


if __name__ == '__main__':


    out = getPDFFiles()
    ## create database index 
    createDatabaseIndex()
    # Check that our docs have been inserted
    addDocumentsToIndex(out)
    # check if redis client is connected
    print(redis_client.ft(INDEX_NAME).info()['num_docs'])
    print(customChatGPTAnswer(Query))
    # print(queryRedisDatabase(query))

