import click
from loguru import logger
from pymongo import MongoClient
from pymongo.database import Database

from philoagents.config import settings


@click.command()
@click.option(
    "--collection-name",
    "-c",
    default=settings.MONGO_LONG_TERM_MEMORY_COLLECTION,
    help="Name of the collection to delete",
)
@click.option(
    "--mongo-uri",
    "-u",
    default=settings.MONGO_URI,
    help="MongoDB connection URI",
)
@click.option(
    "--db-name",
    "-d",
    default=settings.MONGO_DB_NAME,
    help="Name of the database",
)
def main(collection_name: str, mongo_uri: str, db_name: str) -> None:
    """CLI to delete a MongoDB collection.

    Args:
        collection_name (str): Name of the collection to delete.
        mongo_uri (str): The MongoDB collection URI string.
        db_name (str): The name of the database containing the collection.
    """

    client = MongoClient(mongo_uri)

    db: Database = client[db_name]

    # Delete collection if it exists
    if collection_name in db.list_collection_names():
        db.drop_collection(collection_name)
        logger.info(f"Successfully deleted '{collection_name}' collection.")
    else:
        logger.info(f"'{collection_name}' collection does not exist.")

    client.close()


if __name__ == "__main__":
    main()
