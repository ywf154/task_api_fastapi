from datetime import datetime

from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=255,default='123456')
    # kinds = fields.ReverseRelation["Kind"]  # 反向关系定义
    # plates = fields.ReverseRelation["Plate"]  # 反向关系定义


class Plate(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    dutyuser = fields.ForeignKeyField("models.User", related_name="dutyuser")
    kinds = fields.ReverseRelation["Kind"]  # 反向关系定义


class Kind(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    douser = fields.ForeignKeyField("models.User", related_name="douser")
    plate = fields.ForeignKeyField("models.Plate", related_name="plate")


#     @TableId(type = IdType.AUTO)
#     private Integer id;
#     private String name;
#     private String douser;
#     private Long plateId;
#     @TableField(exist = false)
#     private Plate plate;
#     @TableField(exist = false)


class Task(Model):
    id = fields.IntField(pk=True)
    kind = fields.ForeignKeyField("models.Kind", related_name="kind")
    name = fields.CharField(max_length=255)
    toWho = fields.CharField(max_length=255, null=True, blank=True)
    endTime = fields.DatetimeField(null=True, blank=True)
    wxNoticeTo = fields.TextField(null=True, blank=True)
    wxNoticeFrom = fields.TextField(null=True, blank=True)
    status = fields.BooleanField(default=False)
    createTime = fields.DatetimeField(default=datetime.now)
    finishTime = fields.DatetimeField(null=True, blank=True)

