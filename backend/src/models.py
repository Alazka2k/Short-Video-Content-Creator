from prisma import Prisma

db = Prisma()

# We don't need to define models here anymore, as they're defined in the Prisma schema
# Instead, we can add helper methods if needed

async def get_content_by_id(content_id: int):
    return await db.content.find_unique(where={"id": content_id})

async def create_content(data):
    return await db.content.create(data=data)

# Add more helper methods as needed