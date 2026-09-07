from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.policy import Policy, PolicyRule
from app.repositories.policy_repository import PolicyRepository


class PolicyService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = PolicyRepository(session)

    async def get_all(self) -> list[Policy]:
        return await self.repository.get_all()

    async def get_by_id(
        self,
        policy_id: UUID,
    ) -> Policy | None:
        return await self.repository.get_by_id(policy_id)

    async def create_policy(
        self,
        name: str,
        description: str | None,
        enabled: bool,
        priority: int,
        action: str,
        duration_seconds: int | None,
        rules: list[dict],
        user_id: UUID,
    ) -> Policy:
        existing_policy = await self.repository.get_by_name(name)

        if existing_policy:
            raise ValueError("Policy name already exists.")

        policy = Policy(
            name=name,
            description=description,
            enabled=enabled,
            priority=priority,
            action=action,
            duration_seconds=duration_seconds,
            created_by=user_id,
            updated_by=user_id,
        )

        try:
            policy = await self.repository.create(policy)

            for rule_data in rules:
                rule = PolicyRule(
                    policy_id=policy.id,
                    field=rule_data["field"],
                    operator=rule_data["operator"],
                    value=rule_data["value"],
                    logical_operator=rule_data.get(
                        "logical_operator",
                        "AND",
                    ),
                )

                await self.repository.create_rule(rule)

            await self.session.commit()

            return await self.repository.get_by_id(policy.id)

        except Exception:
            await self.session.rollback()
            raise

    async def update_policy(
        self,
        policy_id: UUID,
        name: str | None,
        description: str | None,
        enabled: bool | None,
        priority: int | None,
        action: str | None,
        duration_seconds: int | None,
        rules: list[dict] | None,
        user_id: UUID,
    ) -> Policy:
        policy = await self.repository.get_by_id(policy_id)

        if policy is None:
            raise ValueError("Policy not found.")

        if name is not None and name != policy.name:
            existing_policy = await self.repository.get_by_name(name)

            if existing_policy:
                raise ValueError("Policy name already exists.")

            policy.name = name

        if description is not None:
            policy.description = description

        if enabled is not None:
            policy.enabled = enabled

        if priority is not None:
            policy.priority = priority

        if action is not None:
            policy.action = action

        if duration_seconds is not None:
            policy.duration_seconds = duration_seconds

        policy.updated_by = user_id

        try:
            if rules is not None:
                await self.repository.delete_rules(policy.id)

                for rule_data in rules:
                    rule = PolicyRule(
                        policy_id=policy.id,
                        field=rule_data["field"],
                        operator=rule_data["operator"],
                        value=rule_data["value"],
                        logical_operator=rule_data.get(
                            "logical_operator",
                            "AND",
                        ),
                    )

                    await self.repository.create_rule(rule)

            policy = await self.repository.update(policy)

            await self.session.commit()

            return await self.repository.get_by_id(policy.id)

        except Exception:
            await self.session.rollback()
            raise

    async def enable_policy(
        self,
        policy_id: UUID,
        user_id: UUID,
    ) -> Policy:
        policy = await self.repository.get_by_id(policy_id)

        if policy is None:
            raise ValueError("Policy not found.")

        if policy.enabled:
            raise ValueError("Policy already enabled.")

        try:
            policy.enabled = True
            policy.updated_by = user_id

            await self.repository.update(policy)
            await self.session.commit()

            return await self.repository.get_by_id(policy.id)

        except Exception:
            await self.session.rollback()
            raise

    async def disable_policy(
        self,
        policy_id: UUID,
        user_id: UUID,
    ) -> Policy:
        policy = await self.repository.get_by_id(policy_id)

        if policy is None:
            raise ValueError("Policy not found.")

        if not policy.enabled:
            raise ValueError("Policy already disabled.")

        try:
            policy.enabled = False
            policy.updated_by = user_id

            await self.repository.update(policy)
            await self.session.commit()

            return await self.repository.get_by_id(policy.id)

        except Exception:
            await self.session.rollback()
            raise

    async def delete_policy(
        self,
        policy_id: UUID,
    ) -> None:
        policy = await self.repository.get_by_id(policy_id)

        if policy is None:
            raise ValueError("Policy not found.")

        try:
            await self.repository.delete(policy)
            await self.session.commit()

        except Exception:
            await self.session.rollback()
            raise

    async def validate_policy(
        self,
        condition: dict,
        action: dict,
    ) -> tuple[bool, list[str]]:
        warnings: list[str] = []

        if not condition:
            warnings.append("Condition is empty.")

        if not action:
            warnings.append("Action is empty.")

        return len(warnings) == 0, warnings