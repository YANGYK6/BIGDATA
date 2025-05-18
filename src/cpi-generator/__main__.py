from calculator import CPICalculator, plot_cpi_trend
from config.config import settings
from visualize import visualize
from datetime import date
import pandas as pd


def main():
    settings.from_env('prod')
    calculator = CPICalculator(db_config=settings.CLICKHOUSE)

    start_date = date(2025, 5, 17)
    end_date = date(2028, 5, 15)

    daily_cpi = calculator.compute_daily_cpi(start_date, end_date)
    # print(daily_cpi)
    plot_cpi_trend(daily_cpi)


if __name__ == '__main__':
    main()
