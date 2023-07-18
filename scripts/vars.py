from google.cloud import secretmanager
import os

SECRETKEY = os.environ.get('SECRETKEY')

APP_NAME = 'mobkoiTask'
ACCESS_TOKEN = SECRETKEY
WIKI_API = "https://en.wikipedia.org/w/api.php"
