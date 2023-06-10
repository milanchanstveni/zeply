from typing import Iterable
from pathlib import Path
import sys


async def async_iter(loop: Iterable):
    for i in loop:
        yield i


def load_project_modules():
    base = Path(__file__).resolve().parent.parent
    sys.path.append(str(base))


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance
