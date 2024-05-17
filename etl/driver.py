from etl.extract import ExtractedFields, extract
from etl.load import load
from etl.transform import TransformedFields, transform

from constants import URL_ROOT, URL_CONSOLIDATED


def driver():
    # ticker = 'GPIL'
    ticker = 'NSLNISP'
    tickers = []
    # url = 'https://www.screener.in/company/GPIL/consolidated/'
    url = f'{URL_ROOT}/{ticker}/{URL_CONSOLIDATED}'

    extracted_fields: ExtractedFields | bool = extract(url, ticker)
    if type(extracted_fields) == bool:
        url = f'{URL_ROOT}/{ticker}'
        extracted_fields: ExtractedFields | bool = extract(url, ticker)
        if type(extracted_fields) == bool:
            print('Data extraction failed')
            exit(1)

    transformed_fields: TransformedFields = transform(extracted_fields)
    print(extracted_fields)
    print(transformed_fields)
    if load(transformed_fields):
        print('Data inserted successfully')
    else:
        print('Data insertion failed')


driver()
