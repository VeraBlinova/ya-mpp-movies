import argparse
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import select
from werkzeug.security import generate_password_hash

from core.config import settings
from models.role import Role
from models.user import User
from models.history import History
from models.social import social_account

db_engine = create_async_engine(
    settings.db.url,
    future=True,
)

async_session = sessionmaker(
    db_engine, class_=AsyncSession, expire_on_commit=False
)

parser = argparse.ArgumentParser()
parser.add_argument('-l', help='Login', type=str, required=True, default='admin')
parser.add_argument('-p', help='Password', type=str, required=True)
parser.add_argument('-fn', help='First name', type=str, required=True, default='admin')
parser.add_argument('-ln', help='Last name', type=str, required=True, default='admin')
args = parser.parse_args()


async def create_superuser():
    async with async_session() as session:
        #Creat subscriber role 
        role = Role(name='subscriber',
                        description='subscriber',
                        created_at=datetime.now()
                        )
        session.add(role)
        # Get admin role
        query = select(Role).where(Role.name == 'admin')
        result = await session.execute(query)
        role = result.scalar_one_or_none()
        if role is None:

            # Create a role record
            role = Role(name='admin',
                        description='Super user',
                        is_superuser=True,
                        is_staff=True,
                        created_at=datetime.now()
                        )
            session.add(role)

            await session.flush()
        # Create a user record with the role 'grand'
        user = User(login=args.l,
                    password=generate_password_hash(args.p),
                    first_name=args.fn,
                    last_name=args.ln,
                    created_at=datetime.now(),
                    is_active=True,
                    role=role)
        session.add(user)

        # Commit the changes to the database
        await session.commit()
    # Close the session
        await session.close()

if __name__ == '__main__':
    import asyncio
    asyncio.run(create_superuser())
