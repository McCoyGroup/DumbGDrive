
from .Credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

class Drive:
    _cache = {}
    version='v3'
    root='drive'
    @classmethod
    def load_drive(cls, credentials, root=None, version=None):
        if root is None:
            root = cls.root
        if version is None:
            version = cls.version
        key = (root, version, credentials)
        if key in cls._cache:
            return cls._cache[key]
        else:
            service = build(root, version, credentials=credentials.credentials)
            cls._cache[key] = service
            return service

class Service:
    # might have other uses for this, but in any case a base class doesn't hurt
    def __init__(self, name, creds = None, api = None, **params):
        self.name = name
        if creds is None:
            creds = Credentials()
        self.creds = creds
        if api is None:
            api = Drive.load_drive(creds)
        self.api = api
        self.caller = getattr(self.api, name)()

class FilesService(Service):
    def __init__(self, creds = None, api = None, **params):
        super().__init__('files', cred=creds, api=api, **params)
    def list(self, root=None, **params):
        results = self.caller.list(
            **params
        ).execute()
        return results.get('files', [])