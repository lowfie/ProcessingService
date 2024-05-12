import asyncio
import logging

from src.models import User
from src.config import config
from src.database.actions import db_session


async def main() -> None:
    async with db_session() as db:
        user, created = await User.get_or_create(
            db=db,
            username=config.admin.name,
            defaults=dict(password=config.admin.password, is_admin=True)
        )
        if not created:
            logging.info(f"Admin {user} already exists")
            return None

        logging.info(f"Admin was created: {user}")


if __name__ == '__main__':
    asyncio.run(main())
