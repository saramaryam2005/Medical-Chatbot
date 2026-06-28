from flask import Flask, render_template, request, jsonify

from src.chatbot import get_response

app = Flask(__name__)


