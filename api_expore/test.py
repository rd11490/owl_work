import requests
from requests.auth import HTTPBasicAuth

token = '*'

class OWLApiClient:

    def __init__(self, token=None):
        self.user = '*'
        self.secret = '*'

        self.base_url = 'https://us.api.blizzard.com'
        self.oauth_url = 'https://oauth.battle.net/token'
        self.token = token

        self.__get_token()


    def __create_headers(self):
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def __get_token(self):
        if self.token is None:
            response = requests.post(self.oauth_url, auth=HTTPBasicAuth(self.user, self.secret), data={'grant_type':'client_credentials'})
            self.token = response.json()['access_token']
        self.__create_headers()

    def get_match(self, match_id):
        response = requests.get(f'{self.base_url}/owl/v1/matches/{match_id}', headers=self.headers)
        return response.json()

    def get_summary(self):
        response = requests.get(f'{self.base_url}/owl/v1/owl2', headers=self.headers)
        return response.json()

# token = get_token()
print(token)

client = OWLApiClient(token)
resp_json = client.get_summary()
for k in resp_json.keys():
    print(k)

matches = resp_json.get('matches')
print(matches)
for match_id in matches.keys():
    print(match_id)
    print(matches.get(match_id))
    match_resp = client.get_match(match_id)
    print(match_resp)
    for k in match_resp.keys():
        print(k)
    print('')
    break
