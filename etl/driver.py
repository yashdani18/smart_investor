from etl.extract import ExtractedFields, extract
from etl.transform import TransformedFields, transform


def driver():
    url = 'https://www.screener.in/company/GPIL/consolidated/'
    extracted_fields: ExtractedFields = extract(url)
    transformed_fields: TransformedFields = transform(extracted_fields)
    print(extracted_fields)
    print(transformed_fields)


driver()