# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
from typing import List, Optional

__all__ = ('celery_app',)

TRUE = ("1", "true", "True", "TRUE", "on", "yes")


def is_true(val: Optional[str]) -> bool:
    return val in TRUE


def split_with_comma(val: str) -> List[str]:
    return list(filter(None, map(str.strip, val.split(","))))
