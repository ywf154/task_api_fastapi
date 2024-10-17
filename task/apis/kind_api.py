from fastapi import APIRouter

from task.models import Kind, User, Plate
from task.schemas import KindPydantic, pydantic_create_kind
from utils.R import R

# @RequestMapping("/kind")
kind_api = APIRouter(prefix='/kind', tags=['任务--种类'])


@kind_api.get("/", name='获取所有-种类')
async def getAllKind():
    kinds = await Kind.all().prefetch_related('douser','plate')
    kps = []
    for kind in kinds:
        kp = KindPydantic(  # 在每次迭代中创建新的实例
            id=kind.id,
            name=kind.name,
            pid=kind.plate_id,
            uid=kind.douser_id
        )
        kps.append(kp)
    return R.success(data=kps)


@kind_api.get("/{kid}", name='获取一个-种类')
async def getKindById(kid: int):
    kind = await Kind.filter(id=kid).prefetch_related('douser').first()
    if kind is None:
        return R.error(msg="没有这条记录")  # 处理找不到的情况
    kp = KindPydantic(
        id=kind.id,
        name=kind.name,
        pid=kind.plate_id,
        uid=kind.douser_id
    )
    return R.success(data=kp)


@kind_api.post('/', name='新增一个-种类')
async def createKind(kp: pydantic_create_kind):
    ex_kind = await Kind.filter(name=kp.name).first()
    if ex_kind:
        return R.error('该种类已存在')

    user = await User.filter(id=kp.uid).first()
    if user is None:
        return R.error(msg="用户不存在")

    ex_plate = await Plate.filter(id=kp.pid).first()
    if ex_plate is None:
        return R.error(msg="板块不存在")
    kind_obj = await Kind.create(
        plate_id=kp.pid,
        name=kp.name,
        douser_id=kp.uid
    )
    await kind_obj.save()
    return R.success()


@kind_api.delete('/{kid}', name='删除一个-种类')
async def deleteKind(kid: int):
    kind = await Kind.filter(id=kid).first()
    if kind is None:
        return R.error(msg="该记录不存在")
    await kind.filter(id=kid).delete()
    return R.success()


@kind_api.put('/', name='更新一个-种类')
async def updateKind(updateObj: KindPydantic):
    if updateObj.id is None:
        return R.error(msg="id为空")
    existing_kind = await Kind.filter(id=updateObj.id).first()
    if not existing_kind:
        return R.error(msg='未找到这条记录')
    user = await User.filter(id=updateObj.uid).first()
    if user is None:
        return R.error(msg="用户不存在")

    ex_plate = await Plate.filter(id=updateObj.pid).first()
    if ex_plate is None:
        return R.error(msg="板块不存在")
    existing_kind.plate_id = updateObj.pid
    existing_kind.name = updateObj.name
    existing_kind.douser_id = updateObj.uid
    await existing_kind.save()
    return R.success()
