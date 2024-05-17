from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config.mongodb import MONGO_CONNECTION_URL
from etl.transform import TransformedFields


def connect():
    # Create a new client and connect to the server
    client = MongoClient(MONGO_CONNECTION_URL, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        exit(1)

    database = client['smart_investor']

    return client, database


def search():
    client, database = connect()

    collection_tickers = database['col_tickers']
    collection_details = database['col_details']

    print(client.list_database_names())

    if collection_details.find_one({'ticker': 'GPIL'}):
        print('Record for GPIL exists')
    else:
        print('Record for GPIL does not exist')


def ticker_exists(collection, ticker):
    return collection.find_one({'ticker': ticker})


def details_exist(collection, ticker):
    return collection.find_one({'ticker': ticker})


def load(transformed_fields: TransformedFields) -> bool:
    client, database = connect()
    collection_tickers = database['col_tickers']
    collection_details = database['col_details']

    print(transformed_fields.dict())

    ticker = transformed_fields.ticker
    if ticker_exists(collection_tickers, ticker) or details_exist(collection_details, ticker):
        print('Data already exists for', transformed_fields.ticker)
        return False

    status_insertion_col_details = collection_details.insert_one(transformed_fields.dict())
    status_insertion_col_tickers = collection_tickers.insert_one({'ticker': transformed_fields.ticker})

    if status_insertion_col_tickers.acknowledged and status_insertion_col_details.acknowledged:
        print('Both tables updated successfully')
        return True
    else:
        print('One or both of the insertions failed')

    return False


# tf = TransformedFields()
# print(load(tf))

# search()
