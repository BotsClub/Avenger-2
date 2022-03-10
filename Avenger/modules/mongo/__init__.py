from motor.motor_asyncio import AsyncIOMotorClient as AvengerMongoClient
from Avenger import MONGO_DB_URI

avengermongo = AvengerMongoClient(MONGO_DB_URI)
avengerdb = avengermongo.avenger

anitcdb = avengerdb.antichnl
