# import pandas as pd
# import json

# curr = ['USD', 'AED', 'ARS', 'AUD', 'BGN', 'BRL', 'BSD', 'CAD', 'CHF', 'CLP', 'CNY', 'COP', 'CZK', 'DKK', 'DOP', 'EGP', 'EUR', 'FJD', 'GBP', 'GTQ', 'HKD', 'HRK', 'HUF', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'KZT', 'MVR', 'MXN', 'MYR', 'NOK', 'NZD', 'PAB', 'PEN', 'PHP', 'PKR', 'PLN', 'PYG', 'RON', 'RUB', 'SAR', 'SEK', 'SGD', 'THB', 'TRY', 'TWD', 'UAH', 'UYU', 'ZAR']

# df = pd.read_excel('records.xlsx', header=None)
# print(df)

# d = {}
# for name in curr:
#     d[name] = df[df[0] == name].iloc[0, 2]

# with open("namerates.json", "w") as outfile:
#     json.dump(d, outfile, indent=2)

# with open('cconverter/namerates.json') as f:
#     print(f)

from loguru import logger

logger.debug('Hello')
