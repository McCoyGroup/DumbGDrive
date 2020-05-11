#
# I'll leave this here in case I want to make a 'simplified' caller where we don't have to explicity route through
#   a Service object in the script
#

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
    def upload(self, fields='name,id'):
        upops = {'resumable':self.resumable}
        if self.mimeType is not None:
            upops['mimetype'] = self.mimeType
        media = MediaFileUpload(self.fp, **upops)
        req = self.service.create(body=self.opts, media_body=media, fields=fields)
        if isinstance(req, dict):
            return req
        else:
            return req.execute()