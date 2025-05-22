import oss2
from config.config import settings
from clickhouse_driver import Client
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


class Calculator():
    def __init__(self):
        self.auth = oss2.Auth(settings.ACCESS_KEY, settings.ACCESS_KEY_SECRET)
        self.bucket = oss2.Bucket(self.auth, settings.OSS.ENDPOINT, settings.OSS.BUCKET)
        self.client = Client(host=settings.CLICKHOUSE.HOST, port=settings.CLICKHOUSE.PORT,
                             user=settings.CLICKHOUSE.USER, password=settings.CLICKHOUSE.PASSWORD,
                             database=settings.CLICKHOUSE.DATABASE, settings={'use_numpy': True})

    def clickhouse_get_leaf(self):
        sql = """
            SELECT * FROM categories WHERE hierarchy=='3'
        """
        return [list(i) for i in self.client.execute(sql)]

    def clickhouse_get_base_report_price(self, start_date, end_date):
        sql_delete_table = """
            DROP TABLE IF EXISTS price_data
        """
        self.client.execute(sql_delete_table)
        sql = """
            CREATE TABLE price_data 
            ENGINE=MergeTree()
            ORDER BY product_id
            AS (
                SELECT 
                    product_id,
                    MAX(CASE WHEN date = '{start_date}' THEN price END) AS base_price,
                    MAX(CASE WHEN date = '{end_date}' THEN price END) AS report_price
                FROM prices
                WHERE date IN ('{start_date}', '{end_date}')
                GROUP BY product_id
            )
        """
        return [list(i) for i in self.client.execute(sql.format(start_date=start_date, end_date=end_date))]

    def clickhouse_calculate_cpi(self):
        sql_delete_table = """
            FROP  TABLE IF EXISTS category_cpi
        """
        self.client.execute(sql_delete_table)
        sql = """
            CREATE TABLE category_cpi
            ENGINE=MergeTree()
            ORDER BY p.category_id
            AS (
                SELECT 
                    p.category_id,
                    EXP(AVG(LN(pd.report_price / pd.base_price))) AS price_index
                FROM products p
                JOIN price_data pd ON p.product_id = pd.product_id
                JOIN leaf_categories lc ON p.category_id = lc.category_id
                WHERE pd.base_price > 0
                  AND pd.report_price IS NOT NULL
                GROUP BY p.category_id
            )
        """
        return [list(i) for i in self.client.execute(sql)]

    def clickhouse_get_cpi(self):
        sql = """
            SELECT * FROM category_cpi
        """
        return [list(i) for i in self.client.execute(sql)]


def main():
    calculator = Calculator()
    # print(calculator.clickhouse_get_leaf())
    # print(calculator.clickhouse_get_base_report_price('2025-05-19', '2025-05-20'))
    # calculator.clickhouse_get_base_report_price('2025-05-20', '2025-05-21')
    # print(calculator.clickhouse_get_cpi())
    start_date = datetime.strptime('2025-05-19', '%Y-%m-%d')
    end_date = datetime.strptime('2028-05-15', '%Y-%m-%d')
    for i in range((end_date.date() - start_date.date()).days):
        today = start_date + timedelta(days=i)
        tomorrow = today + timedelta(days=1)
        today = today.strftime('%Y-%m-%d')
        tomorrow = tomorrow.strftime('%Y-%m-%d')
        calculator.clickhouse_get_base_report_price(today, tomorrow)
        # print(today)


if __name__ == '__main__':
    main()
