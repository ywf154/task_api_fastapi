from fastapi import APIRouter

from task.apis.kind_api import kind_api
from task.apis.plate_api import plate_api
from task.apis.task_api import task_api
from task.apis.user_api import user_api

task = APIRouter()

task.include_router(plate_api)
task.include_router(kind_api)
task.include_router(task_api)
task.include_router(user_api)
