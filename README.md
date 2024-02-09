# getStackOverflow

This script will pull the five most recent questions from StackOverflow and give the user the ability to choose a question. The answers to that question will then be shown, and the user can select the one they think was marked as correct.

## TODOs: 
- Fix caching to reduce API calls
- Better error handling
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
