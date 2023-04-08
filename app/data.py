from os import getenv

from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient


class Database:
    load_dotenv()
    database = MongoClient(getenv("DB_URL"), tlsCAFile=where())["Database"]

    def __init__(self, collection: str):
        self.collection = self.database[collection]

    def seed(self, amount):
        doc = [Monster().to_dict() for _ in range(amount)]
        return self.collection.insert_many(doc).acknowledged

    def reset(self):
        self.collection.delete_many({})

    def count(self) -> int:
        return self.collection.count_documents({})

    def dataframe(self) -> DataFrame:
        documents = self.collection.find({}, {'_id': False})
        return DataFrame(documents)

    def html_table(self) -> str:
        return self.dataframe().to_html()


if __name__ == '__main__':
    db = Database('BanderSnatch')
    db.reset()
    db.seed(3000)
    print(db.count())