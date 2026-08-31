import asyncio
import getpass

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.role import Role
from app.models.user import User
from app.security.password import hash_password


async def main():
    username = input("Admin username: ").strip()
    email = input("Admin email (optional): ").strip() or None
    password = getpass.getpass("Admin password: ")
    password_confirm = getpass.getpass("Confirm password: ")

    if password != password_confirm:
        raise SystemExit("Passwords do not match.")

    if not username:
        raise SystemExit("Username is required.")

    if not password:
        raise SystemExit("Password is required.")

    async with AsyncSessionLocal() as session:
        existing = await session.execute(
            select(User).where(User.username == username)
        )

        if existing.scalar_one_or_none():
            raise SystemExit("Username already exists.")

        role_result = await session.execute(
            select(Role).where(Role.name == "Admin")
        )

        role = role_result.scalar_one_or_none()

        if role is None:
            raise SystemExit("Admin role not found.")

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            role_id=role.id,
            status="ACTIVE",
        )

        session.add(user)

        await session.commit()

        print()
        print("ADMIN USER CREATED")
        print("username:", user.username)
        print("role:", role.name)
        print("status:", user.status)


if __name__ == "__main__":
    asyncio.run(main())