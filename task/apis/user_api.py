from fastapi import APIRouter

from task.models import Kind, User, Plate
from task.schemas import KindPydantic, pydantic_create_kind, UserPydantic, info_user
from utils.R import R

# @RequestMapping("/User")
user_api = APIRouter(prefix='/user', tags=['任务--用户'])


@user_api.get("/", name='获取所有-用户')
async def getAllUser():
    users = await User.all()
    ups = []
    for user in users:
        kp = UserPydantic(
            id=user.id,
            name=user.name,
            password=user.password
        )
        ups.append(kp)
    return R.success(data=ups)


@user_api.get("/{uid}", name='获取一个-用户')
async def getUserById(uid: int):
    user = await User.filter(id=uid).first()
    if user is None:
        return R.error(msg="没有这条记录")  # 处理找不到的情况
    kp = UserPydantic(
        id=user.id,
        name=user.name,
        password=user.password
    )
    return R.success(data=kp)


@user_api.post('/{name}', name='新增一个-用户')
async def createUser(name: str):
    user = await User.filter(name=name).first()
    if user:
        return R.error('该用户已存在')
    uObj = await User.create(name=name)
    await uObj.save()
    return R.success()


@user_api.delete('/{uid}', name='删除一个-用户')
async def deleteUser(uid: int):
    user = await User.filter(id=uid).first()
    if user is None:
        return R.error(msg="用户不存在")
    await User.filter(id=uid).delete()
    return R.success()


@user_api.put('/', name='更新一个-用户')
async def updateUser(updateObj: UserPydantic):
    if updateObj.id is None:
        return R.error(msg="id为空")
    user_in = await User.filter(id=updateObj.id).first()
    if not user_in:
        return R.error(msg='用户不存在')
    user_in.name = updateObj.name
    user_in.password = updateObj.password
    await user_in.save()
    return R.success()


@user_api.get('/info/{uid}', name='获取用户相关任务信息')
async def getUserInfo(uid: int):
    user = await User.filter(id=uid).first()
    if user is None:
        return R.error(msg="用户不存在")
    plates = await Plate.filter(dutyuser_id=uid).all()
    kinds = await Kind.filter(douser_id=uid).all()
    info_p = []
    info_k = []
    for plate, kind in zip(plates, kinds):
        info_p.append(plate.name)
        info_k.append(kind.name)
    infos = info_user(
        pNames=info_p,
        kNames=info_k
    )
    return R.success(data=infos)
