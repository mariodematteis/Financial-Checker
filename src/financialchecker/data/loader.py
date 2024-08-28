from financialchecker.database.mongodb.database import MongoDBCrud


class DataLoader:
    def __init__(self) -> None:
        self._mongo_instance = MongoDBCrud()