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
    url = "https://api.stackexchange.com/2.3/search/advanced"
    params = {
        "order": "desc",     # Most recent on top
        "sort": "creation",  # Get most recently created
        "accepted": "True",  # Filter for questions with accepted answers
        "answers": 2,        # Filter for questions with at least 2 answers
        "pagesize": 5,       # Limit the results
        "site": "stackoverflow"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Error if not 200 status code
        data = response.json()
        return data['items']
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}. Error: {str(e)}")

def get_question(question_id):
    url = f"https://api.stackexchange.com/2.3/questions/{question_id}"
    params = {
        "order": "desc",
        "sort": "activity",
        "site": "stackoverflow",
        "filter": "withbody"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Error if not 200 status code
        data = response.json()
        question = data['items'][0]
        
        question['body'] = BeautifulSoup(question['body'], 'html.parser').get_text()
        question['body']=strip_tags(question['body'])
        question['correct_answer_id'] = question.get('accepted_answer_id')  # Extract accepted answer ID
        
        return question
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}. Error: {str(e)}")


def get_answers(question_id):
    url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
    params = {
        #"order": "desc",
        #"sort": "votes",
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