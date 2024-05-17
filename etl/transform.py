from dataclasses import dataclass, field, asdict
from etl.extract import ExtractedFields

from constants import QUARTERS, Q_SALES, Q_EXPENSES, Q_OPM, Q_OPM_PERCENT, Q_OTHER_INCOME, Q_INTEREST, Q_DEPRECIATION, \
    Q_PBT, Q_TAX, Q_PAT, Q_EPS, \
    YEARS, A_SALES, A_EXPENSES, A_OPM, A_OPM_PERCENT, A_OTHER_INCOME, A_INTEREST, A_DEPRECIATION, \
    A_PBT, A_TAX, A_PAT, A_EPS


@dataclass
class QuarterlyData:
    quarters: list[str] = field(init=False)
    q_sales: list[int] = field(init=False)
    q_sales_percent: list[float] = field(init=False)
    q_expenses: list[int] = field(init=False)
    q_expenses_percent: list[float] = field(init=False)
    q_net_profit: list[int] = field(init=False)
    q_net_profit_percent: list[float] = field(init=False)


@dataclass
class AnnualData:
    years: list[str] = field(init=False)
    a_sales: list[int] = field(init=False)
    a_sales_percent: list[float] = field(init=False)
    a_expenses: list[int] = field(init=False)
    a_expenses_percent: list[float] = field(init=False)
    a_net_profit: list[int] = field(init=False)
    a_net_profit_percent: list[float] = field(init=False)


@dataclass
class TransformedFields:
    ticker: str = field(init=False)
    company_name: str = field(init=False)
    price: float = field(init=False)
    change: float = field(init=False)
    mcap: int = field(init=False, default=0)
    current_price: float = field(init=False, default=0)
    high: float = field(init=False, default=0)
    low: float = field(init=False, default=0)
    stock_pe: float = field(init=False, default=0)
    book_value: int = field(init=False, default=0)
    dividend_yield: float = field(init=False, default=0)
    roce: float = field(init=False, default=0)
    roe: float = field(init=False, default=0)
    fv: float = field(init=False, default=0)
    quarterlyData: QuarterlyData = field(init=False)
    annualData: AnnualData = field(init=False)

    def dict(self):
        return {k: v for k, v in asdict(self).items()}


def transform(ef: ExtractedFields) -> TransformedFields:
    print(ef)
    tf = TransformedFields()
    try:
        tf.ticker = ef.ticker
        tf.company_name = ef.company_name
        tf.price = float(ef.price[1:].replace(',', '').strip())
        tf.change = float(ef.change[:-1])
        tf.mcap = int(ef.mcap[1:-3].replace('\n', '').strip().replace(',', ''))
        tf.current_price = tf.price
        high_low = ef.high_low[1:].split(' / ')
        tf.high = float(high_low[0].replace(',', ''))
        tf.low = float(high_low[1].replace(',', ''))
        if ef.stock_pe == '':
            tf.stock_pe = 0
        else:
            tf.stock_pe = float(ef.stock_pe)
        if ef.book_value[1:] == '':
            tf.book_value = 0
        else:
            tf.book_value = int(ef.book_value[1:].replace('\n', '').strip())
        tf.dividend_yield = float(ef.dividend_yield[:-1].replace('\n', '').strip())

        temp_roce = ef.roce[:-1].replace('\n', '').strip()
        if temp_roce == '':
            tf.roce = 0
        else:
            tf.roce = float(temp_roce)
        tf.roe = float(ef.roe[:-1].replace('\n', '').strip())
        tf.fv = float(ef.fv[1:].replace('\n', '').strip())
    except Exception as e:
        print('Exception while transforming fundamental ratios for', tf.ticker)
        print(str(e))
        exit(1)

    quarterly_data = QuarterlyData()
    q_sales = ef.results[Q_SALES]
    q_expenses = ef.results[Q_EXPENSES]
    q_net_profit = ef.results[Q_PAT]

    quarterly_data.quarters = ef.results[QUARTERS]
    quarterly_data.q_sales = [int(val.replace(',', '')) for val in q_sales]
    quarterly_data.q_expenses = [int(val.replace(',', '')) for val in q_expenses]
    quarterly_data.q_net_profit = [int(val.replace(',', '')) for val in q_net_profit]

    temp_q_sales = quarterly_data.q_sales
    temp_q_expenses = quarterly_data.q_expenses
    temp_q_net_profit = quarterly_data.q_net_profit

    try:
        quarterly_data.q_sales_percent = \
            [round(((temp_q_sales[index + 1] - val) / val * 100), 2) for index, val in enumerate(temp_q_sales[:-1])]
        quarterly_data.q_expenses_percent = \
            [round(((temp_q_expenses[index + 1] - val) / val * 100), 2) for index, val in
             enumerate(temp_q_expenses[:-1])]
        quarterly_data.q_net_profit_percent = \
            [round(((temp_q_net_profit[index + 1] - val) / val * 100), 2)
             for index, val in enumerate(temp_q_net_profit[:-1])]
    except ZeroDivisionError as e:
        print('ZeroDivisionError while transforming data for', tf.ticker)
        exit(1)

    annual_data = AnnualData()
    a_sales = ef.results[A_SALES]
    a_expenses = ef.results[A_EXPENSES]
    a_net_profit = ef.results[A_PAT]

    annual_data.years = ef.results[YEARS]
    annual_data.a_sales = [int(val.replace(',', '')) for val in a_sales]
    annual_data.a_expenses = [int(val.replace(',', '')) for val in a_expenses]
    annual_data.a_net_profit = [int(val.replace(',', '')) for val in a_net_profit]

    temp_a_sales = annual_data.a_sales
    temp_a_expenses = annual_data.a_expenses
    temp_a_net_profit = annual_data.a_net_profit
    try:
        annual_data.a_sales_percent = \
            [round(((temp_a_sales[index + 1] - val) / val * 100), 2) for index, val in enumerate(temp_a_sales[:-1])]
        annual_data.a_expenses_percent = \
            [round(((temp_a_expenses[index + 1] - val) / val * 100), 2) for index, val in
             enumerate(temp_a_expenses[:-1])]
        annual_data.a_net_profit_percent = \
            [round(((temp_a_net_profit[index + 1] - val) / val * 100), 2)
             for index, val in enumerate(temp_a_net_profit[:-1])]
    except ZeroDivisionError as e:
        print('ZeroDivisionError while transforming data for', tf.ticker)
        exit(1)

    tf.quarterlyData = quarterly_data
    tf.annualData = annual_data

    return tf

# ['1,132', '1,237', '1,160', '1,274', '1,607', '1,438', '1,666', '1,307', '1,463', '1,317', '1,326', '1,291', '1,309']
# [9.28, -6.22, 9.83, 26.14, -10.52, 15.86, -21.55, 11.94, -9.98, 0.68, -2.64, 1.39]

# Load this data into mongodb, repeat for 40-50 other tickers
# create a link between backend and db, fetch data from db into backend, fetch data from frontend to backend
# create two collections in mongodb,
# 1. tbl_tickers - only the names of the tickers
# 2. tbl_details - all tickers with details
# 3. tbl_users - all users with fields: username (email), password, tickers
# when user creates an account, he/she will be able to create custom watchlist by selecting tickers

# fetch and load all data into mongodb's two collections - tbl_tickers, tbl_details
# code register, login and jwt part
# code manage profile (where user can add tickers to watchlist)
# code landing page, where user can view all the numbers - ratios and results
# use cypress to test login flow and manage profile flow

# Expense tracker
# create a python function to fetch data from splitwise (day by day) and load into mysql
# s3 is for storage of monthly expenses
# UI? fetch expenses for last few days (set duration)

# If time remains, start learning about Next.js
