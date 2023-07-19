from google.cloud import secretmanager
import os

APP_NAME = 'mobkoiTask'
ACCESS_TOKEN = os.environ.get('SECRETKEY')
WIKI_API = "https://en.wikipedia.org/w/api.php"