
class DataCorruptionError(Exception):
    """ Raised when MD5 calculated does not match the saved database md5 for the file resource """


class FileDoesNotExist(Exception):
    """ Raised when the file does not actually exist,
    although there is a FileInstance object in the database that says the file exists """


class FileAlreadyExists(Exception):
    """ Raised when the file already exists,
    although there is no FileInstance object in the database that says the file exists """


class RecoverableFileTransferError(Exception):
    """ Raised when file transfer failed within celery worker,
    but should be given another chance to complete """


class DeploymentUnnecessary(Exception):
    """ Raised when a deployment does not require any transfers. """


