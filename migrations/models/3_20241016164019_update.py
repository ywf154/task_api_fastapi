from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `task` ADD `createTime` DATETIME(6) NOT NULL;
        ALTER TABLE `task` ADD `status` BOOL NOT NULL  DEFAULT 0;
        ALTER TABLE `task` ADD `finishTime` DATETIME(6);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `task` DROP COLUMN `createTime`;
        ALTER TABLE `task` DROP COLUMN `status`;
        ALTER TABLE `task` DROP COLUMN `finishTime`;"""
