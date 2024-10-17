from fastapi import APIRouter

from task.models import Plate, User
from task.schemas import PlatePydantic, pydantic_create_plate, PlatePydantic
from utils.R import R

# @RequestMapping("/plate")
plate_api = APIRouter(prefix='/plate', tags=['任务--板块'])


@plate_api.get("/", name='获取所有-板块')
async def getAllPlate():
    plates = await Plate.all().prefetch_related('dutyuser')
    pps = []
    for plate in plates:
        pp = PlatePydantic(
            id=plate.id,
            name=plate.name,
            uid=plate.dutyuser.id
        )
        pps.append(pp)
    return R.success(data=pps)


@plate_api.get("/{pid}", name='获取一个-板块')
async def getPlateById(pid: int):
    plate = await Plate.filter(id=pid).prefetch_related('dutyuser').first()  # 使用 first() 获取单个对象
    if plate is None:
        return R.error(msg="没有这条记录")  # 处理找不到的情况
    pp = PlatePydantic(
        id=plate.id,
        name=plate.name,
        uid=plate.dutyuser.id
    )
    return R.success(data=pp)


@plate_api.post('/', name='新增一个-板块')
async def createPlate(plate: pydantic_create_plate):
    existing_plate = await Plate.filter(name=plate.name).first()
    if existing_plate:
        return R.error(msg="该名称的 Plate 已存在")

    user = await User.filter(id=plate.uid).first()
    if not user:
        return R.error(msg="用户不存在")
    plate_obj = await Plate.create(
        name=plate.name,
        dutyuser_id=plate.uid
    )
    await plate_obj.save()
    return R.success()


@plate_api.delete('/{pid}', name='删除一个-板块')
async def deletePlate(pid: int):
    plate = await Plate.filter(id=pid).first()
    if plate is None:
        return R.error(msg="该记录不存在")
    await Plate.filter(id=pid).delete()
    return R.success()


@plate_api.put('/', name='更新一个-板块')
async def updatePlate(updateObj: PlatePydantic):
    if updateObj.id is None:
        return R.error(msg="id为空")
    user = await User.filter(id=updateObj.uid).first()
    if not user:
        return R.error(msg='用户不存在')
    existing_plate = await Plate.filter(id=updateObj.id).first()
    if not existing_plate:
        return R.error(msg='未找到这条记录')
    existing_plate.name = updateObj.name
    existing_plate.dutyuser_id = updateObj.uid
    await existing_plate.save()
    return R.success()
