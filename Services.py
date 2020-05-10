
class Service:
    ...
    # for expansion if we want to have a base service for something

class FilesService(Service):
    def list(self, root=None):
        raise NotImplemented