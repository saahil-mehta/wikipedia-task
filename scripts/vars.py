from google.cloud import secretmanager


CLIENT = secretmanager.SecretManagerServiceClient()
PROJECT_ID = advancedml-saahil
NAME = f"projects/{PROJECT_ID}/secrets/wikiSecret/versions/latest"
response = CLIENT.access_secret_version(request={"name": NAME})
SECRETKEY = response.payload.data.decode('UTF-8')

APP_NAME = 'mobkoiTask'
ACCESS_TOKEN = SECRETKEY
WIKI_API = "https://en.wikipedia.org/w/api.php"
