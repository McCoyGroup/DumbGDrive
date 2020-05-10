
import os, pickle
from google_auth_oauthlib.flow import InstalledAppFlow

class Credentials:

    default_cfig='credentials.json'
    default_cache='token.pickle'
    def __init__(self, cfig = None, cache=None):
        self.creds = None
        if cfig is None:
            cfig = self.default_cfig
        self.creds_file = cfig
        if cache is None:
            cache = self.default_cache
        self.cache_file = cache

    def load_credentials(self):
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds
    @property
    def credentials(self):
        if self.creds is None:
            self.creds = self.load_credentials()


    # def call(self):
    # service = build('drive', 'v3', credentials=creds)