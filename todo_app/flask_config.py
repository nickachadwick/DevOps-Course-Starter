import os
from dotenv import find_dotenv, load_dotenv

class Config():

        """Base configuration variables."""
        SECRET_KEY = os.environ.get('SECRET_KEY')
        if not SECRET_KEY:
            raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")

        API_KEY = os.environ.get('API_KEY')
        if not API_KEY:
            raise ValueError("No API_KEY set for Flask application. Did you follow the setup instructions?")
        
        TOKEN = os.environ.get('TOKEN')
        if not TOKEN:
            raise ValueError("No TOKEN set for Flask application. Did you follow the setup instructions?")

        TRELLO_BOARD = os.environ.get('TRELLO_BOARD')
        if not TRELLO_BOARD:
            raise ValueError("No TRELLO_BOARD set for Flask application. Did you follow the setup instructions?")