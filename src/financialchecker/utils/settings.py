from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from omegaconf import OmegaConf
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="FINANCIALCHECKER_",
        case_sensitive=False,
    )

    ACCOUNT: int
    PASSWORD: str
    SERVER: str


@dataclass
class MongoDBCollections:
    Log: str
    Transaction: str
    Utility: str


@dataclass
class MongoDB:
    """
    Data class representing the configuration details for connecting to a MongoDB
    database.

    Attributes:
        PROTOCOL (str): Protocol used for the connection (e.g., "mongodb" or
        "mongodb+srv").
        USERNAME (str): Username for authenticating the MongoDB connection.
        PASSWORD (str): Password for authenticating the MongoDB connection.
        HOSTNAME (str): Hostname or IP address of the MongoDB server.
        PORT (int): Port number on which the MongoDB server is listening.
        DATABASE (str): Name of the MongoDB database to connect to.
        PARAMETERS (str): Additional connection parameters as a string.
        TLS (bool): Flag indicating whether to use TLS/SSL for the connection.

        COLLECTIONS (MongoDBCollections): An instance of the MongoDBCollections class,
            representing the collections within the MongoDB database.

    Note:
        This class is designed to hold the configuration details required for connecting
        to a MongoDB database. It includes information such as the protocol, username,
        password, hostname, port, database name, parameters, TLS usage, and collections.
    """

    PROTOCOL: str
    USERNAME: str
    PASSWORD: str
    HOSTNAME: str
    PORT: int
    DATABASE: str
    PARAMETERS: str
    TLS: bool

    COLLECTIONS: MongoDBCollections


@dataclass
class Settings:
    MongoDB: MongoDB

    PaymentMethods: list[str]
    Categories: list[str]


@lru_cache
def get_environmental_settings() -> EnvSettings:
    return EnvSettings()


@lru_cache
def get_settings() -> Settings:

    settings_import = OmegaConf.load(
        Path(__file__)
        .absolute()
        .parent.parent.parent.parent.joinpath(
            "config.yaml",
        ),
    )

    return OmegaConf.structured(
        Settings(**settings_import),
    )


@lru_cache
def get_mongodb_settings() -> MongoDB:
    """
    Get the MongoDB configuration settings.

    Returns:
        MongoDB: An instance of the MongoDB configuration settings obtained from the
            overall application settings.

    Note:
        This function is decorated with the LRU (Least Recently Used) cache,
        which helps in caching the result of the function to improve performance.
    """

    return get_settings().MongoDB


@lru_cache
def get_mongodb_collection() -> MongoDBCollections:
    """
    Retrieve the MongoDB collection from the application settings.

    Returns:
        MongoDBCollections: An instance of the MongoDBCollections class representing
            the MongoDB collection.
    """

    return get_mongodb_settings().COLLECTIONS


@lru_cache
def get_mongodb_url(no_port: bool = False) -> str:
    """
    Get the MongoDB connection URL from the configuration settings.

    Returns:
        str: The MongoDB connection URL constructed from the configuration settings.

    Note:
        This function is decorated with the LRU (Least Recently Used) cache,
        which helps in caching the result of the function to improve performance.

        The function retrieves MongoDB configuration settings from the overall
        application settings using `get_settings()`. It then constructs the MongoDB
        connection URL by combining the protocol, username, password, hostname, port,
        and parameters information from the configuration settings.

        Returns the constructed MongoDB connection URL as a string.
    """

    mongodb_settings = get_settings().MongoDB

    return (
        f"{mongodb_settings.PROTOCOL}://"
        f"{mongodb_settings.USERNAME}:"
        f"{mongodb_settings.PASSWORD}@"
        f"{mongodb_settings.HOSTNAME}"
        f"{':' + str(mongodb_settings.PORT) if not no_port else ''}/"
        f"{mongodb_settings.PARAMETERS}"
    )


@lru_cache
def get_categories() -> list[str]:
    return get_settings().Categories


@lru_cache
def get_payment_methods() -> list[str]:
    return get_settings().PaymentMethods
