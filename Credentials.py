
import os, pickle, enum
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GoogleDriveScope(enum.Enum):
    All='https://www.googleapis.com/auth/drive'
    MetadataRO='https://www.googleapis.com/auth/drive.metadata.readonly'

class Credentials:
    default_root = 'gdrive'
    default_cfig = 'client_id.json'
    default_cache='token_{scopes}.pickle'
    default_scopes=[GoogleDriveScope.All]
    default_auth_mode='OAuth2'
    def __init__(self, cfig = None, cache=None, scopes=None, mode=None):
        if scopes is None:
            scopes = self.default_scopes
        if isinstance(scopes, str):
            scopes=[scopes]
        scopes = [getattr(GoogleDriveScope, s) if isinstance(s, str) else s for s in scopes]
        self.scopes = scopes
        if mode is None:
            mode=self.default_auth_mode
        self.mode = mode
        self.creds = None
        if cfig is None:
            cfig = os.path.join(self.default_root, self.default_cfig)
        self.creds_file = cfig.format(scopes=self.scope_string)
        if cache is None:
            cache = os.path.join(self.default_root, self.default_cache)
        self.cache_file = cache.format(scopes=self.scope_string)
    @property
    def scope_string(self):
        return '+'.join(s.name if isinstance(s, GoogleDriveScope) else s[0] for s in self.scopes)

    @property
    def scope_list(self):
        return [s.value if isinstance(s, GoogleDriveScope) else s[1] for s in self.scopes]

    def load_credentials(self):
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        creds = None
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            elif self.mode == 'service_account':
                creds = service_account.Credentials.from_service_account_file(self.creds_file, scopes=self.scope_list)
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.creds_file, self.scope_list)
                creds = flow.run_console(port=0)
                # Save the credentials for the next run
                with open(self.cache_file, 'wb') as token:
                    pickle.dump(creds, token)
        return creds
    @property
    def credentials(self):
        if self.creds is None:
            self.creds = self.load_credentials()
        return self.creds