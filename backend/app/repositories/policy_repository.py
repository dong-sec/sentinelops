from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.policy import Policy, PolicyRule


class PolicyRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Policy]:
        result = await self.session.execute(
            select(Policy)
            .options(
                selectinload(Policy.rules)
            )
            .order_by(
                Policy.priority.asc(),
                Policy.created_at.desc(),
            )
        )

        return list(result.scalars().unique().all())

    async def get_by_id(
        self,
        policy_id: UUID,
    ) -> Policy | None:
        result = await self.session.execute(
            select(Policy)
            .options(
                selectinload(Policy.rules)
            )
            .where(Policy.id == policy_id)
        )

        return result.scalar_one_or_none()

    async def get_by_name(
        self,
        name: str,
    ) -> Policy | None:
        result = await self.session.execute(
            select(Policy)
            .options(
                selectinload(Policy.rules)
            )
            .where(Policy.name == name)
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        policy: Policy,
    ) -> Policy:
        self.session.add(policy)

        await self.session.flush()
        await self.session.refresh(policy)

        return policy

    async def update(
        self,
        policy: Policy,
    ) -> Policy:
        await self.session.flush()
        await self.session.refresh(policy)

        return policy

    async def delete(
        self,
        policy: Policy,
    ) -> None:
        await self.session.delete(policy)
        await self.session.flush()

    async def create_rule(
        self,
        rule: PolicyRule,
    ) -> PolicyRule:
        self.session.add(rule)

        await self.session.flush()
        await self.session.refresh(rule)

        return rule

    async def delete_rules(
        self,
        policy_id: UUID,
    ) -> None:
        result = await self.session.execute(
            select(PolicyRule)
            .where(PolicyRule.policy_id == policy_id)
        )

        rules = result.scalars().all()

        for rule in rules:
            await self.session.delete(rule)

        await self.session.flush()