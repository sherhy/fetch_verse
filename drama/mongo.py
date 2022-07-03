from pymongo import MongoClient


class Mongo:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Mongo, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def init_mongo() -> None:
        mongo = Mongo()
        mongo.client = MongoClient("mongodb://localhost:27017")
        mongo.db = mongo.client.drama_bible
