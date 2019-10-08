# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery_app import app as celery_app

__all__ = ("celery_app",)

import pymysql  # 导入pymysql模块

pymysql.install_as_MySQLdb()  # 兼容mysqldb
