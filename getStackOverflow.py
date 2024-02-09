from flask import Flask, render_template, request
#from flask_caching import Cache
import requests, random
from bs4 import BeautifulSoup
from io import StringIO
from html.parser import HTMLParser

app = Flask(__name__)
#cache = Cache(config={'CACHE_TYPE': 'simple'}) # start with simple
#cache.init_app(app)

#@cache.cached(timeout=120,key_prefix='questions') # Cache main questions for 2 minutes
def get_recent_questions():
    url = "https://api.stackexchange.com/2.3/search/advanced"
    params = {
        "order": "desc",     # Most recent on top
        "sort": "creation",  # Get most recently created
        "accepted": "True",  # Only questions with accepted answers
        "answers": 2,        # Only questions with at least 2 answers
        "pagesize": 5,       # Limit to the top 5 results
        "site": "stackoverflow"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Error if not 200 status code
        data = response.json()
        return data['items']
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}. Error: {str(e)}")

# TODO: Add caching here
def get_question(question_id):
    url = f"https://api.stackexchange.com/2.3/questions/{question_id}"
    params = {
        #"order": "desc",
        #"sort": "activity",
        "site": "stackoverflow",
        "filter": "withbody"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Error if not 200 status code
        data = response.json()
        question = data['items'][0]
        if 'body' in question:
            question['correct_answer_id'] = question.get('accepted_answer_id')  # Extract accepted answer ID
        else:
            question['body'] = ""  # Set empty string if body doesn't exist
            question['correct_answer_id'] = None  # Set correct answer ID to None
        
        return question
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}. Error: {str(e)}")

# TODO: Add caching here 
def get_answers(question_id):
    url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
    params = {
        #"order": "desc",
        #"sort": "activity",
        "site": "stackoverflow",
        "filter": "withbody"
    }
    response = requests.get(url, params=params)
    data = response.json()
    answers = []
    for answer in data['items']:
        answer_text = BeautifulSoup(answer['body'], 'html.parser').get_text()
        answers.append({'answer_id': answer['answer_id'], 'body': answer_text})
    random_answers = random.sample(answers, len(answers)) # Return answers in random order
    return random_answers

@app.route('/')
def index():
    questions = get_recent_questions()
    return render_template('index.html', questions=questions)

@app.route('/answers/<question_id>')
def answers(question_id):
    question = get_question(question_id)
    answers = get_answers(question_id)
    return render_template('answers.html', question=question, answers=answers)

@app.route('/check_answer', methods=['POST']) # POST the answer to see if it's correct
def check_answer():
    selected_answer_id = request.form['selected_answer_id']
    correct_answer_id = request.form['correct_answer_id']

    if selected_answer_id == correct_answer_id:
        result = f"Correct! Answer ID: {correct_answer_id}"
    else:
        result = f"Incorrect! You chose {selected_answer_id} but the correct answer was {correct_answer_id}"
    return result

#@app.route('/clear_cache') # Clear cache manually if needed
#def clear_cache():
#    cache.clear()
#    return "Cache cleared!" 
 
if __name__ == '__main__':
    app.run(debug=True)
