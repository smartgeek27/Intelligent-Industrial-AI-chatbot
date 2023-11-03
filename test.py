from flask import Flask, render_template, jsonify, request
import config
import openai
import aiapi
import notebook

prompt = 'hey man whoc is elon musk ?'
print(notebook.customChatGPTAnswer(prompt))