from datetime import datetime
from typing import List

from fastapi import APIRouter

from task.models import Task, User, Plate, Kind
from task.schemas import TaskPydantic, quick_create_task
from utils.R import R

# @RequestMapping("/task")
task_api = APIRouter(prefix='/task', tags=['任务--任务'])


@task_api.get("/", name='获取所有-任务')
async def getAllTask():
    tasks = await Task.all().prefetch_related('kind')
    tps = []
    for task in tasks:
        tp = TaskPydantic(
            id=task.id,
            name=task.name,
            kid=task.kind_id,
            endTime=task.endTime,
            toWho=task.toWho,
            wxNoticeTo=task.wxNoticeTo,
            wxNoticeFrom=task.wxNoticeFrom,
            status=task.status,
            createTime=task.createTime,
            finishTime=task.finishTime
        )
        tps.append(tp)
    return R.success(data=tps)


@task_api.get("/{tid}", name='获取一个-任务')
async def getTaskById(tid: int):
    task = await Task.filter(id=tid).prefetch_related('kind').first()
    if task is None:
        return R.error(msg="没有这条记录")
    tp = TaskPydantic(
        id=task.id,
        name=task.name,
        kid=task.kind_id,
        endTime=task.endTime,
        toWho=task.toWho,
        wxNoticeTo=task.wxNoticeTo,
        wxNoticeFrom=task.wxNoticeFrom,
        status=task.status,
        createTime=task.createTime,
        finishTime=task.finishTime
    )
    return R.success(data=tp)


@task_api.post('/', name='新增一个-任务')
async def createTask(kp: quick_create_task):
    kind = await Kind.filter(id=kp.kid).first()
    if kind is None:
        return R.error(msg="种类不存在")
    task_obj = await Task.create(
        name=kp.name,
        kind_id=kp.kid,
        endTime=kp.endTime
    )
    await task_obj.save()
    return R.success()


@task_api.delete('/{kid}', name='删除一个-任务')
async def deleteTask(kid: int):
    task = await Task.filter(id=kid).first()
    if task is None:
        return R.error(msg="该记录不存在")
    await task.filter(id=kid).delete()
    return R.success()


@task_api.put('/', name='更新一个-任务')
async def updateTask(updateObj: TaskPydantic):
    if updateObj.id is None:
        return R.error(msg="id为空")
    existing_task = await Task.filter(id=updateObj.id).first()
    if not existing_task:
        return R.error(msg='未找到这条记录')
    kind = await Kind.filter(id=updateObj.kid).first()
    if kind is None:
        return R.error('种类不存在')
    existing_task.kind_id = updateObj.kid
    existing_task.name = updateObj.name
    existing_task.endTime = updateObj.endTime
    existing_task.status = updateObj.status
    existing_task.toWho = updateObj.toWho
    existing_task.wxNoticeTo = updateObj.wxNoticeTo
    existing_task.wxNoticeFrom = updateObj.wxNoticeFrom
    existing_task.finishTime = updateObj.finishTime
    await existing_task.save()
    return R.success()


@task_api.get('/f/{tid}', name='完成一个任务')
async def fTask(tid: int):
    if tid is None:
        return R.error('id为空')
    task = await Task.filter(id=tid).first()
    if task is None:
        return R.error('记录不存在')
    task.finishTime = datetime.now()
    task.status = True
    await task.save()
    return R.success()


@task_api.get('/uf/{tid}', name='取消完成一个任务')
async def fTask(tid: int):
    if tid is None:
        return R.error('id为空')
    task = await Task.filter(id=tid).first()
    if task is None:
        return R.error('记录不存在')
    task.finishTime = None
    task.status = False
    await task.save()
    return R.success()


@task_api.get('/search/{name}', name='模糊搜索')
async def fSearch(name: str):
    if not name:
        return R.error('搜索字段为空')
    tasks = await Task.filter(name__icontains=name).all()
    if not tasks:
        return R.error(msg='未找到相关任务')
    tps = []
    for task in tasks:
        tp = TaskPydantic(
            id=task.id,
            name=task.name,
            kid=task.kind_id,
            endTime=task.endTime,
            toWho=task.toWho,
            wxNoticeTo=task.wxNoticeTo,
            wxNoticeFrom=task.wxNoticeFrom,
            status=task.status,
            createTime=task.createTime,
            finishTime=task.finishTime
        )
        tps.append(tp)
    return R.success(data=tps)
