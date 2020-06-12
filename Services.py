
from .Credentials import Credentials
from googleapiclient.discovery import build

class DriveAPI:
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
            api = DriveAPI.load_drive(creds)
        self.api = api
        self.caller = getattr(self.api, name)()
    def wrap_call(self, name):
        method = getattr(self.caller, name)
        def _call(**params):
            return method(**params).execute()
        return _call
    def __getattr__(self, item):
        return self.wrap_call(item)

class FilesService(Service):
    def __init__(self, creds = None, api = None, **params):
        super().__init__('files', cred=creds, api=api, **params)

    def list(self,
             includeItemsFromAllDrives=True,
             supportsAllDrives=True,
             **params
             ):
        results = self.caller.list(
            includeItemsFromAllDrives=includeItemsFromAllDrives,
            supportsAllDrives=supportsAllDrives,
            **params
        ).execute()
        return results.get('files', [])
    def create(self,
             includeItemsFromAllDrives=True,
             supportsAllDrives=True,
             **params
             ):
        results = self.caller.create(
            includeItemsFromAllDrives=includeItemsFromAllDrives,
            supportsAllDrives=supportsAllDrives,
            **params
        ).execute()
        return results

class DriveService(Service):
    def __init__(self, creds = None, api = None, **params):
        super().__init__('drives', cred=creds, api=api, **params)

class AboutService(Service):
    def __init__(self, creds = None, api = None, **params):
        super().__init__('about', cred=creds, api=api, **params)

class ChildrenService(Service):
    def __init__(self, creds = None, api = None, **params):
        super().__init__('children', cred=creds, api=api, **params)
class ParentsService(Service):
    def __init__(self, creds = None, api = None, **params):
        super().__init__('parents', cred=creds, api=api, **params)
class PermissionsService(Service):
    def __init__(self, creds = None, api = None, **params):
        super().__init__('permissions', cred=creds, api=api, **params)
class RevisionsService(Service):
    def __init__(self, creds = None, api = None, **params):
        super().__init__('revisions', cred=creds, api=api, **params)
class AppsService(Service):
    def __init__(self, creds = None, api = None, **params):
        super().__init__('apps', cred=creds, api=api, **params)
class CommentsService(Service):
    def __init__(self, creds = None, api = None, **params):
        super().__init__('comments', cred=creds, api=api, **params)
class RepliesService(Service):
    def __init__(self, creds = None, api = None, **params):
        super().__init__('replies', cred=creds, api=api, **params)
class PropertiesService(Service):
    def __init__(self, creds = None, api = None, **params):
        super().__init__('properties', cred=creds, api=api, **params)