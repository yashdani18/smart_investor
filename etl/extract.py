import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from constants import QUARTERS, Q_SALES, Q_EXPENSES, Q_OPM, Q_OPM_PERCENT, Q_OTHER_INCOME, Q_INTEREST, Q_DEPRECIATION, \
    Q_PBT, Q_TAX, Q_PAT, Q_EPS, \
    YEARS, A_SALES, A_EXPENSES, A_OPM, A_OPM_PERCENT, A_OTHER_INCOME, A_INTEREST, A_DEPRECIATION, \
    A_PBT, A_TAX, A_PAT, A_EPS


@dataclass
class ExtractedQuarter:
    q_name: str
    q_sales: list[int]
    q_expenses: list[int]
    q_opm: list[int]
    q_opm_percent: list[int]
    q_other_income: int
    q_interest: int
    q_dep: int
    q_pbt: int
    q_tax: int
    q_pat: int
    q_eps: float


@dataclass
class ExtractedFields:
    company_name: str = field(init=False)
    price: str = field(init=False)
    change: str = field(init=False)
    mcap: str = field(init=False)
    current_price: str = field(init=False)
    high_low: str = field(init=False)
    stock_pe: str = field(init=False)
    book_value: str = field(init=False)
    dividend_yield: str = field(init=False)
    roce: str = field(init=False)
    roe: str = field(init=False)
    fv: str = field(init=False)
    results: dict = field(init=False)
    # quarters: ExtractedQuarter


def extract(url):
    # url = 'https://www.screener.in/company/GPIL/consolidated/'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')

    ef = ExtractedFields()

    company_name = soup.find(False, {'class': ['margin-0 show-from-tablet-landscape']}).text
    # print(company_name)
    ef.company_name = company_name

    price_fields = soup.find(False, {'class': ['font-size-18 strong line-height-14']}).find_all('span')
    ef.price = price_fields[0].text.strip()
    ef.change = price_fields[1].text.strip()

    list_vals = []

    top_ratios = soup.find(id="top-ratios").find_all('li')
    for ratio in top_ratios:
        key_value = ratio.find_all('span')
        # key = key_value[0].text.strip()
        val = key_value[1].text.strip()
        list_vals.append(val)

    ef.mcap = list_vals[0]
    ef.current_price = list_vals[1]
    ef.high_low = list_vals[2]
    ef.stock_pe = list_vals[3]
    ef.book_value = list_vals[4]
    ef.dividend_yield = list_vals[5]
    ef.roce = list_vals[6]
    ef.roe = list_vals[7]
    ef.fv = list_vals[8]

    table_metadata = [
        [QUARTERS, Q_SALES, Q_EXPENSES, Q_OPM, Q_OPM_PERCENT, Q_OTHER_INCOME, Q_INTEREST, Q_DEPRECIATION,
         Q_PBT, Q_TAX, Q_PAT, Q_EPS],
        [YEARS, A_SALES, A_EXPENSES, A_OPM, A_OPM_PERCENT, A_OTHER_INCOME, A_INTEREST, A_DEPRECIATION,
         A_PBT, A_TAX, A_PAT, A_EPS],
    ]

    dictionary = {}

    tables = soup.find_all(False, {'class': ['responsive-holder fill-card-width']})[:2]
    for t_index, table in enumerate(tables):
        header_cols = table.find('thead').find('tr').find_all('th')[1:]
        # print([col.text.strip() for col in header_cols])
        dictionary[table_metadata[t_index][0]] = [col.text.strip() for col in header_cols]

        body_rows = table.find('tbody').find_all('tr')
        for r_index, row in enumerate(body_rows[:-1]):
            cols = row.find_all('td')
            # print(cols[0].text.strip(), [col.text.strip().replace(',', '') for col in cols[1:]])

            # dictionary[table_metadata[t_index][r_index + 1]] = [col.text.strip().replace(',', '') for col in cols[1:]]
            dictionary[table_metadata[t_index][r_index + 1]] = [col.text.strip() for col in cols[1:]]

        # print()

    # print(dictionary)

    ef.results = dictionary
    return ef
    # print(ef)
