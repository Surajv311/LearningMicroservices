cd $APP_HOME # Changing directory to app/ folder inside which all our source code is copied and has our logic files app.py, database folder, etc etc.

uvicorn app:app --port 8000 --reload