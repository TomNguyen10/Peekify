from pymongo.mongo_client import MongoClient
from config import MONGODB_SOURCE

mongo_client = MongoClient(MONGODB_SOURCE)
mongo_db = mongo_client['peekify']
