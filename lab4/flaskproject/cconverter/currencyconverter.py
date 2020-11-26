from flask import Blueprint, render_template, request, redirect, url_for
import requests
import json
from .. import cache
from .parser import get_full_names_currencies

currencyconverter = Blueprint('currencyconverter', __name__)

url = "https://api.exchangerate-api.com/v4/latest/"
names_url = "https://open.exchangerate-api.com/v6/latest"
rates_names = get_full_names_currencies()


@currencyconverter.route('/converter', defaults={
    "from_to": None,
    "currencies": '["USD", "UAH"]'
})
@currencyconverter.route('/converter/<currencies>/<from_to>')
def converter(from_to, currencies):
    if not from_to:
        ft = {"from": 0, "to": 0}
    else:
        ft = json.loads(from_to)

    currencies = [rates_names[key] for key in json.loads(currencies)]

    return render_template('converter.html',
                           currencies=rates_names.values(),
                           curr_curr=currencies,
                           values=ft)


@currencyconverter.route('/converter', methods=['POST'])
def converter_post():
    try:
        c_from = float(request.form.get('c_from'))
    except ValueError:
        c_from = 0
    currency_from = request.form.get('currency_from').split()[0]
    currency_to = request.form.get('currency_to').split()[0]

    c_to = get_list_of_currencies_for_given_currency(currency_from)[currency_to]

    from_to = json.dumps({"from": c_from, "to": c_to*c_from})
    currencies = json.dumps([currency_from, currency_to])
    return redirect(url_for('currencyconverter.converter',
                            from_to=from_to,
                            currencies=currencies))


@cache.memoize(3600)
def get_list_of_currencies_for_given_currency(currency):
    return requests.get(url+currency).json()['rates']
