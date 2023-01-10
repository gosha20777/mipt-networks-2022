from enum import Enum


class FileStatus(str, Enum):
    available = 'available'
    not_found = 'not_found'


class TaskStatus(str, Enum):
    queued = 'queued'
    started = 'started'
    finished = 'finished'
    failed = 'failed'


class OrchestratorType(str, Enum):
    thread = 'thread'
    docker = 'docker'
    docker_gpu = 'docker_gpu'


class EngineType(str, Enum):
    vision_labs = 'vision_labs'
    ntech = 'ntech'
    tevian = 'tevian'
    facenet = 'facenet'
