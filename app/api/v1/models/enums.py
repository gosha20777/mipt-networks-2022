from enum import Enum


class RoleType(str, Enum):
    user = 'user'
    admin = 'admin'
    root = 'root'


class EngineType(str, Enum):
    vision_labs = 'vision_labs'
    ntech = 'ntech'
    tevian = 'tevian'
    facenet = 'facenet'


class TaskStatus(str, Enum):
    queued = 'queued'
    started = 'started'
    finished = 'finished'
    failed = 'failed'


class FileStatusType(str, Enum):
    available = 'available'
    not_found = 'not_found'
