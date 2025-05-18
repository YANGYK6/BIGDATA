import oss2
from config.config import settings
from clickhouse_driver import Client
import pandas as pd


class DataLoader():
    def __init__(self):
        self.auth = oss2.Auth(settings.ACCESS_KEY, settings.ACCESS_KEY_SECRET)
        self.bucket = oss2.Bucket(self.auth, settings.OSS.ENDPOINT, settings.OSS.BUCKET)
        self.client = Client(host=settings.CLICKHOUSE.HOST, port=settings.CLICKHOUSE.PORT,
                             user=settings.CLICKHOUSE.USER, password=settings.CLICKHOUSE.PASSWORD,
                             database=settings.CLICKHOUSE.DATABASE, settings={'use_numpy': True})
        self.prepare_queries = """
            SELECT *
            FROM price
            WHERE date BETWEEN %(start)s AND %(end)s
        """




def main():
    loader = DataLoader()
    loaders = loader.load_price_data('2025-05-01', '2025-05-02')
    print(loaders)


if __name__ == '__main__':
    main()
