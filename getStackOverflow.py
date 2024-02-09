from flask import Flask, render_template, request
#from flask_caching import Cache
import requests
from bs4 import BeautifulSoup
from io import StringIO
from html.parser import HTMLParser


app = Flask(__name__)
#cache = Cache(config={'CACHE_TYPE': 'simple'}) # start simple
#cache.init_app(app)

def get_recent_questions():
    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        "order": "desc",
        "sort": "creation",
        "site": "stackoverflow",
        "pagesize": 5
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['items']

def get_answers(question_id):
    url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
    params = {
        "order": "desc",
        "sort": "votes",
        "site": "stackoverflow",
        "filter": "withbody"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['items']

@app.route('/')
def index():
    questions = get_recent_questions()
    return render_template('index.html', questions=questions)

@app.route('/answers', methods=['POST'])
def answers():
    question_id = request.form['question_id']
    answers = get_answers(question_id)
    return render_template('answers.html', answers=answers)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    selected_answer = request.form['selected_answer']
    correct_answer = request.form['correct_answer']
    if selected_answer == correct_answer:
        result = "Correct!"
    else:
        result = "Incorrect!"
    return result

if __name__ == '__main__':
    app.run(debug=True)