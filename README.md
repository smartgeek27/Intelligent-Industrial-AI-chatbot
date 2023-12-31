# Industry specific Chatbot using OpenAI LLM api's and Redis Database. 
Starting template for a the Custom ChatGPT Chatbot Application. 

This repository provides a comprehensive guide for building a custom chatbot powered by your data, Redis Search, and the openAI API's, all integrated into a Python Flask application.

This youtube guide will act as a good starting point for your Industry Specific Chatbot

## YouTube Channel
Check out out [YouTube Channel here](https://www.youtube.com/c/SkoloOnline)

## Set up the project
Start by installing virtual environment if you do not already have it.

```sh
sudo -H pip3 install --upgrade pip

sudo -H pip3 install virtualenv
```

Create and activate the virtual environment

```sh
virtualenv chatgptenv
souce chatgptenv/bin/activate
```

## Create a folder called data
Put your PDF files in there, note this project will only work with PDF files. Can also work with text and csv files. Use Langchain dataloader to make it work with your desired format. 

https://python.langchain.com/docs/integrations/document_loaders/ 
## Install required python packages

```sh
pip install Flask
pip install openai
pip install numpy==1.24.2
pip install openai==0.27.1
pip install pandas==1.5.3
pip install redis==4.5.1
pip install requests==2.28.2
pip install ipykernel
pip install textract
pip install tiktoken
```

## Instal Redis Stack Server
In your Ubuntu Virtual server
```sh
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
sudo apt-get install redis-stack-server
```

### Check Redis Stack Server Installation
```sh
sudo systemctl status redis-stack-server
```

## Check that there is document in the index
Run this line inside of a python shell to check that the index was created successfully, and there are documents in the index

```py
#RUN THIS TEST FUNCTION
redis_client.ft(INDEX_NAME).info()['num_docs']
```


You should get this output:
```sh
● redis-stack-server.service - Redis stack server
     Loaded: loaded (/etc/systemd/system/redis-stack-server.service; enabled; vendor preset: ......
     Active: active (running) since Fri 2023-04-21 13:45:42 CEST; 20h ago
       Docs: https://redis.io/
   Main PID: 365056 (redis-server)
      Tasks: 17 (limit: 2282)
     Memory: 195.0M
     CGroup: /system.slice/redis-stack-server.service
             └─365056 /opt/redis-stack/bin/redis-server *:6379
````

