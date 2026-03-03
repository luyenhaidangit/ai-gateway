import asyncio
from app.database import async_session, init_db
from app.services.core import save_inference_result

async def main():
    print("Initiating DB...")
    await init_db()
    
    print("Testing save...")
    async with async_session() as db:
        try:
            result = await save_inference_result(
                text="Test from script",
                prediction="Positive",
                confidence=0.99,
                model_version="test-v1",
                db=db
            )
            print(f"Result ID: {result.id}")
        except Exception as e:
            print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(main())
