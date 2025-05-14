from flask import Flask, request, jsonify
from config import Config
from cache import get_cache, set_cache
from translator import translate
from logger import log_event
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'Currency Converter Service'

@app.route('/convert', methods=['GET'])
def convert():
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    amount = request.args.get('amount', type=float)
    lang = request.args.get('lang', Config.DEFAULT_LANGUAGE)

    if not from_currency or not to_currency or not amount:
        return jsonify({'error': translate('invalid_currency', lang)}), 400

    cache_key = f'{from_currency}_{to_currency}'
    rate = get_cache(cache_key)
    if rate is None:
        # Ejemplo usando ExchangeRate-API (puedes cambiar la URL según tu proveedor)
        url = f'https://v6.exchangerate-api.com/v6/{Config.API_KEY}/pair/{from_currency}/{to_currency}'
        response = requests.get(url)
        if response.status_code != 200:
            log_event('API error', response.text)
            return jsonify({'error': 'External API error'}), 502
        data = response.json()
        if data.get('result') != 'success':
            log_event('API error', data)
            return jsonify({'error': translate('invalid_currency', lang)}), 400
        rate = data['conversion_rate']
        set_cache(cache_key, rate, ex=3600)  # Cache por 1 hora
    else:
        rate = float(rate)

    converted = amount * rate
    log_event('conversion', f'{amount} {from_currency} -> {converted} {to_currency}')
    return jsonify({
        'result': translate('conversion_success', lang),
        'from': from_currency,
        'to': to_currency,
        'amount': amount,
        'converted': round(converted, 2),
        'rate': rate
    })

if __name__ == '__main__':
    app.run(debug=True) 