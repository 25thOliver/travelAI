from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Destination

class DestinationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> Destination:
        destination = Destination(**kwargs)
        self.db.add(destination)
        await self.db.commit()
        await self.db.refresh(destination)
        return destination
    
    async def list_all(self) -> list[Destination]:
        result = await self.db.execute(select(Destination))
        return result.scalars().all()
    