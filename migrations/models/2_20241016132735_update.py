from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `task` ADD `kind_id` INT NOT NULL;
        ALTER TABLE `task` ADD CONSTRAINT `fk_task_kind_b67278eb` FOREIGN KEY (`kind_id`) REFERENCES `kind` (`id`) ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `task` DROP FOREIGN KEY `fk_task_kind_b67278eb`;
        ALTER TABLE `task` DROP COLUMN `kind_id`;"""
