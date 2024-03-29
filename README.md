# getStackOverflow

This script will pull the five most recent questions from StackOverflow and give the user the ability to choose a question. The answers to that question will then be shown and the user can select the one they think was marked as correct. The user will be shown if they are correct.

## Hosted URL

You can access a hosted version of this script at: [https://cduff123.pythonanywhere.com/](https://cduff123.pythonanywhere.com/)  
Note that this URL will need to be recreated every 30 days.

## TODOs: 
- Fix caching to reduce API calls
- Better error handling
- Separate CSS
- Nicer UI

### Local Install Instructions:

1. Install the latest version of Python: [Download Python](https://www.python.org/downloads/)
   
2. Install Flask:
    ```
    python -m pip install flask
    ```

3. Install BeautifulSoup4:
    ```
    python -m pip install beautifulsoup4
    ```

4. Open a command line and run:
    ```
    python getStackOverflow.py
    ```

5. Open a browser and go to the URL [http://localhost:5000/](http://localhost:5000/)
