import certifi
from bson import ObjectId
from pymongo import MongoClient
from pymongo.database import Collection, Database

from financialchecker.log.log import Logger
from financialchecker.transactions._transactions import Transaction, TransactionType
from financialchecker.utils.settings import (
    get_categories,
    get_mongodb_collection,
    get_mongodb_settings,
    get_mongodb_url,
    get_payment_methods,
)

logger = Logger(module_name="MongoDBDatabase", package_name="mongodb", database=False)


class DatabaseInstanceSingleton(type):
    """
    Singleton metaclass for managing a database connection instance.
    """

    _instance = None

    def __call__(
        cls,
        *args,
        **kwargs,
    ):
        """
        Override the __call__ method to implement the singleton pattern.

        Args:
            cls: The class.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The database connection instance.
        """

        if not cls._instance or not cls._instance.is_connected():
            cls._instance = super(
                type(
                    cls,
                ),
                cls,
            ).__call__(
                *args,
                **kwargs,
            )

        return cls._instance


class MongoDBInstance(metaclass=DatabaseInstanceSingleton):
    """
    Singleton class for managing a connection to a MongoDB database.
    """

    client: MongoClient = None
    database: Database = None

    def __init__(
        self,
    ) -> None:
        """
        Initialize the MongoDBInstance.

        Raises:
            MongoConnectionError: If unable to establish a connection with the MongoDB
            Instance.
        """

        try:
            if get_mongodb_settings().TLS:
                self.client = MongoClient(
                    get_mongodb_url(
                        True if "srv" in get_mongodb_settings().PROTOCOL else False
                    ),
                    tlsCAFile=certifi.where(),
                )
            else:
                self.client = MongoClient(
                    get_mongodb_url(
                        True if "srv" in get_mongodb_settings().PROTOCOL else False
                    ),
                )

            self.client.admin.command(
                "ping",
            )
            self.database = self.client[get_mongodb_settings().DATABASE]
        except Exception as error:
            logger.error(
                message=(
                    "Unable to establish with the MongoDB Instance. Error occurred:"
                    f" {error}"
                )
            )
            return

    def is_connected(
        self,
    ) -> bool:
        """
        Check if the MongoDB instance is connected.

        Returns:
            bool: True if connected, False otherwise.
        """

        try:
            if not isinstance(
                self.client,
                MongoClient,
            ):
                return False

            self.client.admin.command(
                "ping",
            )
        except Exception:
            return False

        return True

    def close_database_connection(
        self,
    ) -> None:
        """
        Close the connection to the MongoDB database.
        """

        self.client.close()


class MongoDBCrud:
    def __init__(self) -> None:
        self.mongodb_instance = MongoDBInstance()

    def get_categories(self) -> list[str]:
        utilities_collection: Collection = self.mongodb_instance.database[
            get_mongodb_collection().Utility
        ]

        result: list[dict] = list(
            utilities_collection.aggregate([
                {
                    '$match': {
                        'type': 'Category'
                    }
                },
                {
                    '$sort': {
                        'value': 1
                    }
                }
            ])
        )

        if len(result):
            return [_dict.get("value", "") for _dict in result]
        else:
            get_categories()

    def get_income_categories(self,) -> list[str]:
        utilities_collection: Collection = self.mongodb_instance.database[
            get_mongodb_collection().Utility
        ]

        result: list[dict] = list(
            utilities_collection.aggregate([
                {
                    '$match': {
                        'type': 'IncomeCategory'
                    }
                },
                {
                    '$sort': {
                        'value': 1
                    }
                }
            ])
        )

        if len(result):
            return [_dict.get("value", "") for _dict in result]
        else:
            get_categories()

    def get_payment_methods(self) -> list[str]:
        utilities_collection: Collection = self.mongodb_instance.database[
            get_mongodb_collection().Utility
        ]

        result: list[dict] = list(
            utilities_collection.aggregate([
                {
                    '$match': {
                        'type': 'PaymentMethod'
                    }
                },
                {
                    '$sort': {
                        'value': 1
                    }
                }
            ])
        )

        if len(result):
            return [_dict.get("value", "") for _dict in result]
        else:
            return get_payment_methods()

    def get_firms(self) -> list[str]:
        utilities_collection: Collection = self.mongodb_instance.database[
            get_mongodb_collection().Utility
        ]

        result: list[dict] = list(
            utilities_collection.aggregate([
                {
                    '$match': {
                        'type': 'Firm'
                    }
                },
                {
                    '$sort': {
                        'value': 1
                    }
                }
            ])
        )

        if len(result):
            return [_dict.get("value", "") for _dict in result]
        else:
            return [""]

    def get_locations(self) -> list[str]:
        utilities_collection: Collection = self.mongodb_instance.database[
            get_mongodb_collection().Utility
        ]

        result: list[dict] = list(
            utilities_collection.aggregate([
                {
                    '$match': {
                        'type': 'Location'
                    }
                },
                {
                    '$sort': {
                        'value': 1
                    }
                }
            ])
        )

        if len(result):
            return [_dict.get("value", "") for _dict in result]
        else:
            return [""]

    def add_transaction(self, transaction: Transaction) -> ObjectId:
        transactions_collection = self.mongodb_instance.database[
            get_mongodb_collection().Transaction
        ]

        result = transactions_collection.insert_one(
            dict(transaction)
        )
        return result.inserted_id

    def get_all_transactions(self, transaction_type: str | None = None) -> list[dict]: # noqa E507
        transactions_collection = self.mongodb_instance.database[
            get_mongodb_collection().Transaction
        ]
        request: list[dict] = []

        if transaction_type is not None and TransactionType.has(transaction_type):
            request.append({
                '$match' : {
                    'type': transaction_type
                }
            })

        request.append(
            {
                '$addFields': {
                    'id': {
                        '$toString' : "$_id"
                    }
                }
            }
        )
        request.append(
            {
                '$project': {
                    '_id': 0
                }
            }
        )

        result: list[dict] = list(transactions_collection.aggregate(request))

        return result
