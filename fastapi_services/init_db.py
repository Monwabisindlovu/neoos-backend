# init_db.py - Database initialization script
from models import Base
from utils.config import engine

async def init_models():
    """Create all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import asyncio
    
    async def main():
        print("Creating database tables...")
        await init_models()
        print("Tables created successfully!")
    
    asyncio.run(main())
