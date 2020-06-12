
__all__ = [
    "Downloader",
    "Uploader"
]

from .Services import *
import io, os
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

class Downloader:
    def __init__(self, id=None, export_format=None, mimeType=None, name=None, files_service=None):
        if id is None:
            raise ValueError("{} needs a 'fileId' to work".format(
                type(self).__name__
            ))
        self.mime=mimeType
        self.name=name
        self.file_id = id
        if export_format is None:
            export_format = self.get_export_fmt(mimeType)
        self.export_fmt = export_format #maybe I should handle the MIME-Typing for people...?
        if files_service is None:
            files_service = FilesService()
        self.service = files_service

    mimeMap = {
        'application/vnd.google-apps.spreadsheet':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.google-apps.document':'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.google-apps.presentation':'application/vnd.openxmlformats-officedocument.presentationml.document',
        'application/vnd.google-apps.audio':'audio/mp4'
    }
    @classmethod
    def get_export_fmt(self, mime):
        if mime in self.mimeMap:
            mime = self.mimeMap[mime]
        return mime

    def download_buffer(self, fmt=None):
        if fmt is None:
            fmt = self.export_fmt
        if fmt is not None:
            request = self.service.export_media(fileId=self.file_id, mimeType=fmt)
        else:
            request = self.service.get_media(fileId=self.file_id)
        if isinstance(request, bytes):
            return request
        else:
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                # should probably do something with the status?
                status, done = downloader.next_chunk()
            return bytes(fh)

    def download(self, path=None, fmt=None):
        if path is not None:
            with open(path, 'wb') as out:
                buf = self.download_buffer(fmt=fmt)
                out.write(buf)
            return out
        else:
            return self.download_buffer(fmt=fmt)

class Uploader:
    def __init__(self, file_path, files_service=None, mimeType = None, resumable=True, folder=None, **params):
        if files_service is None:
            files_service = FilesService()
        self.service = files_service
        self.fp = file_path
        self.mimeType = mimeType
        self.resumable = resumable
        if 'name' not in params:
            params['name'] = os.path.basename(file_path)
            if folder is not None:
                params['name'] = os.path.join(folder, params['name'])
        self.opts = params
    def upload(self, fields='*'):
        # I should probably try to find the parent folder, first, and upload there if possible and otherwise
        # create a folder
        upops = {'resumable':self.resumable}
        if self.mimeType is not None:
            upops['mimetype'] = self.mimeType
        media = MediaFileUpload(self.fp, **upops)
        req = self.service.create(body=self.opts, media_body=media, fields=fields, supportsAllDrives=True)
        if isinstance(req, dict):
            return req
        else:
            return req.execute()

class GDObject:
    _cache = {}
    def __init__(self, name=None, id=None, **props):
        self.name = name
        self.id = id
        self.props = props
    def __repr__(self):
        return "{}(name='{}', id={})".format(type(self).__name__, self.name, self.id)
    @classmethod
    def load(cls, name=None, id=None, **props):
        if id is None:
            raise ValueError("ID can't be None")
        if id in cls._cache:
            obj = cls._cache[id]
            if name is not None:
                obj.name = name
            obj.props.update(**props)
        else:
            obj = cls(name=name, id=id, **props)
            cls._cache[id] = obj
        return obj
    _fs = None
    @classmethod
    def FilesAPI(cls):
        if cls._fs is None:
            cls._fs = FilesService()
        return cls._fs
    _ds = None
    @classmethod
    def DrivesAPI(cls):
        if cls._ds is None:
            cls._ds = DriveService()
        return cls._ds
    def get_metadata(self):
        raise NotImplemented
class Drive(GDObject): # might be worth doing some stuff to cache a file tree?
    _api = GDObject.DrivesAPI
    def __init__(self, name=None, id=None, **props):
        super().__init__(name=name, id=id, **props)
        self._folders = None
        self._files = None
    @classmethod
    def list(cls):
        drives = cls._api().list()['drives']
        return [Drive.load(**drive) for drive in drives]
    @property
    def folders(self):
        if self._folders is None:
            self._folders = Folder.search(driveId=self.id, corpora='drive', q="'{}' in parents".format(self.id))
        return self._folders
    @property
    def files(self):
        if self._files is None:
            self._files = File.search(driveId=self.id, corpora='drive', spaces='drive', q="'{}' in parents".format(self.id))
        return self._files
    def upload(self, path, **params):
        return File.upload(path, parent=self, **params)
    def get_metadata(self):
        fields = self._api().get(driveId=self.id, fields='*')
        self.props.update(**fields)
class File(GDObject):
    _api = GDObject.FilesAPI
    def __init__(self, name=None, id=None, path=None, **props):
        super().__init__(name=name, id=id, **props)
        self.path = path
        self._drive = None
        self._folder = None
    def get_metadata(self):
        fields = self._api().get(fileId=self.id, fields='*')
        self.props.update(**fields)
    @classmethod
    def upload(cls, path, parent = None, drive=None, **params):
        if parent is not None and 'parents' not in params:
            params['parents'] = [parent.id]
        if drive is not None:
            params['driveId'] = drive.id
        up = Uploader(path, **params).upload()
        return cls.load(**up, path=path)
    def download(self, parent=None):
        if parent is None:
            parent=os.getcwd()
        Downloader(id=self.id).download(os.path.join(parent, self.name))
    @classmethod
    def load(cls, name=None, id=None, **props):
        if 'mimeType' in props and props['mimeType'] == Folder.MIMEType:
            props['mimeType'] = None
            return Folder.load(name=name, id=id, **props)
        else:
            return super().load(name=name, id=id, **props)
    @property
    def folder(self):
        if self._folder is None:
            if 'parents' in self.props:
                self._folder = Folder.load(id=self.props['parents'])
            else:
                self.get_metadata()
                self._folder = Folder.load(id=self.props['parents'])
        return self._folder
    @property
    def drive(self):
        if self._drive is None:
            if 'driveId' in self.props:
                self._drive = Drive.load(id=self.props['driveId'])
            else:
                self.get_metadata()
                self._drive = Drive.load(id=self.props['driveId'])
        return self._drive
    @classmethod
    def search(cls, fields="files(name,id,parents,mimeType)", **params):
        return [cls.load(**f) for f in cls._api().list(fields=fields, **params)]
class Folder(File):
    _api = GDObject.FilesAPI
    MIMEType='application/vnd.google-apps.folder'
    def __init__(self, name=None, id=None, path=None, **props):
        super().__init__(name=name, id=id, **props)
        self.path = path
        self._drive = None
        self._files = None
        self.props['mimeType']=self.MIMEType
    def upload(self, path, **params):
        return super().upload(path, parent=self, drive=self.drive, **params)
    @classmethod
    def new(cls, name, parent=None, drive=None, **opts):
        metadata = opts
        metadata.update(
            name=name,
            mimeType='application/vnd.google-apps.folder'
        )
        if parent is not None:
            metadata['parents'] = [parent.id]
        if drive is not None:
            metadata['driveId'] = drive.id
        ret = cls.FilesAPI().create(
            body=metadata,
            fields='name,id'
        )
        return cls.load(**ret)
    @classmethod
    def search(cls, fields="*", **params):
        if 'q' in params:
            params['q'] = params['q']+" and mimeType='{}'".format(cls.MIMEType)
        else:
            params['q'] = "mimeType='{}'".format(cls.MIMEType)
        return super().search(fields=fields, **params)
    @property
    def files(self):
        if self._files is None:
            self._files = File.search(q="'{}' in parents".format(self.id))
        return self._files