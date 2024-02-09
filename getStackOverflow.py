from flask import Flask, render_template, request
import requests

app = Flask(__name__)
#cache = Cache(config={'CACHE_TYPE': 'simple'}) # start simple
#cache.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')
 
if __name__ == '__main__':
    app.run(debug=True)
