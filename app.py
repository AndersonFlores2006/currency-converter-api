"""
Currency Converter Service - API

Este microservicio expone una API REST para convertir montos entre diferentes monedas utilizando tasas de cambio en tiempo real. Permite especificar el idioma de los mensajes de respuesta.

Endpoints disponibles:

- `/` — Endpoint raíz, responde con un mensaje simple para verificar que el servicio está activo.
- `/convert` — Realiza la conversión de un monto entre dos monedas.
- `/swagger` — Interfaz Swagger UI para probar la API.
- `/dashboard` — Dashboard web con ejemplos y enlaces.
- `/static/swagger.json` — Especificación OpenAPI en formato JSON.

"""
from flask import Flask, request, jsonify, render_template_string, redirect
from config import Config
from cache import get_cache, set_cache
from translator import translate
from logger import log_event
import requests
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Configuración de Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Currency Converter Service"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/static/swagger.json')
def swagger_json():
    swagger_doc = {
        "swagger": "2.0",
        "info": {
            "title": "Currency Converter Service API",
            "description": "API para convertir montos entre monedas.",
            "version": "1.0.0"
        },
        "basePath": "/",
        "schemes": ["http"],
        "paths": {
            "/convert": {
                "get": {
                    "summary": "Convertir monedas",
                    "description": "Convierte un monto de una moneda a otra usando tasas de cambio en tiempo real.",
                    "parameters": [
                        {"name": "from", "in": "query", "description": "Código de moneda origen (ej: USD)", "required": True, "type": "string"},
                        {"name": "to", "in": "query", "description": "Código de moneda destino (ej: EUR)", "required": True, "type": "string"},
                        {"name": "amount", "in": "query", "description": "Monto a convertir", "required": True, "type": "number"},
                        {"name": "lang", "in": "query", "description": "Idioma de la respuesta (opcional)", "required": False, "type": "string"}
                    ],
                    "responses": {
                        "200": {"description": "Conversión exitosa"},
                        "400": {"description": "Parámetros inválidos"},
                        "502": {"description": "Error en API externa"}
                    }
                }
            }
        }
    }
    return jsonify(swagger_doc)

@app.route('/')
def home():
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Currency Converter Dashboard</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 900px; margin: 0 auto; padding: 30px; background: #f9f9f9; color: #333; }
            h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 15px; font-size: 2.2em; text-align: center; margin-bottom: 30px; }
            .container { display: flex; flex-wrap: wrap; gap: 20px; justify-content: space-between; }
            .endpoint { background: white; padding: 22px; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.08); flex: 1 1 45%; border-left: 5px solid #3498db; }
            .endpoint h2 { color: #3498db; margin-top: 0; font-size: 1.3em; }
            .endpoint p { margin-bottom: 10px; font-size: 1.05em; }
            .example-link { display: inline-block; background: #f2f2f2; padding: 7px 13px; border-radius: 4px; text-decoration: none; color: #333; font-family: monospace; font-size: 1em; border: 1px solid #ddd; }
            .example-link:hover { background: #e6e6e6; }
            .btn { display: block; background: #3498db; color: white; padding: 13px 20px; text-decoration: none; border-radius: 6px; margin: 30px auto 0; text-align: center; font-size: 1.1em; font-weight: bold; transition: background 0.3s; width: 260px; box-shadow: 0 4px 6px rgba(0,0,0,0.08); }
            .btn:hover { background: #2980b9; }
            .api-info { text-align: center; margin-bottom: 30px; font-size: 1.1em; line-height: 1.7; color: #555; background: white; padding: 18px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.07); }
            .btn-group { display: flex; justify-content: center; gap: 20px; margin-top: 30px; }
        </style>
    </head>
    <body>
        <h1>💱 Currency Converter Dashboard</h1>
        <div class="api-info">
            <p>Bienvenido al microservicio de conversión de monedas. Convierte montos entre diferentes monedas usando tasas de cambio en tiempo real.</p>
            <p>Incluye soporte multilenguaje y caché para mejorar el rendimiento.</p>
        </div>
        <div class="container">
            <div class="endpoint">
                <h2>🔄 Conversión de Monedas</h2>
                <p>Convierte una cantidad de una moneda a otra.</p>
                <p><strong>Endpoint:</strong> /convert?from=USD&to=EUR&amount=100</p>
                <p><strong>Ejemplo:</strong> <a class="example-link" href="/convert?from=USD&to=EUR&amount=100">/convert?from=USD&to=EUR&amount=100</a></p>
            </div>
        </div>
        <div class="btn-group">
            <a href="/swagger" class="btn">📚 Explorar Swagger UI</a>
            <a href="/docs" class="btn" style="background: #27ae60;">📖 Guía de la API</a>
        </div>
    </body>
    </html>
    ''')

@app.route('/docs')
def docs():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Guía de la API - Currency Converter</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 900px; margin: 0 auto; padding: 30px; background: #f9f9f9; color: #333; }
            h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 15px; font-size: 2.2em; text-align: center; margin-bottom: 30px; }
            h2 { color: #3498db; margin-top: 30px; }
            code, pre { background: #f2f2f2; border-radius: 4px; padding: 2px 6px; font-size: 1em; }
            .section { background: white; padding: 22px; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.08); }
            ul { margin-left: 20px; }
            .btn { display: inline-block; background: #3498db; color: white; padding: 10px 18px; text-decoration: none; border-radius: 6px; margin: 20px 0; font-size: 1.1em; font-weight: bold; transition: background 0.3s; }
            .btn:hover { background: #2980b9; }
        </style>
    </head>
    <body>
        <h1>📖 Guía de la API - Currency Converter</h1>
        <div class="section">
            <h2>¿Qué es este microservicio?</h2>
            <p>Permite convertir montos entre diferentes monedas usando tasas de cambio en tiempo real. Incluye soporte multilenguaje y caché para mejorar el rendimiento.</p>
        </div>
        <div class="section">
            <h2>Endpoints principales</h2>
            <ul>
                <li><b>/</b> — Mensaje de bienvenida.</li>
                <li><b>/convert</b> — Conversión de monedas (<code>GET</code>).</li>
                <li><b>/swagger</b> — Interfaz Swagger UI.</li>
                <li><b>/dashboard</b> — Dashboard web con ejemplos.</li>
                <li><b>/static/swagger.json</b> — Especificación OpenAPI.</li>
            </ul>
        </div>
        <div class="section">
            <h2>Uso del endpoint <code>/convert</code></h2>
            <p><b>Parámetros:</b></p>
            <ul>
                <li><b>from</b> (requerido): Código de moneda origen (ej: <code>USD</code>).</li>
                <li><b>to</b> (requerido): Código de moneda destino (ej: <code>EUR</code>).</li>
                <li><b>amount</b> (requerido): Monto a convertir (ej: <code>100</code>).</li>
                <li><b>lang</b> (opcional): Idioma de la respuesta (<code>en</code> o <code>es</code>).</li>
            </ul>
            <p><b>Ejemplo de solicitud:</b></p>
            <pre>GET /convert?from=USD&to=EUR&amount=100</pre>
            <p><b>Respuesta de ejemplo:</b></p>
            <pre>{
  "result": "Conversion successful",
  "from": "USD",
  "to": "EUR",
  "amount": 100.0,
  "converted": 91.23,
  "rate": 0.9123
}</pre>
            <p><b>En español:</b></p>
            <pre>GET /convert?from=USD&to=EUR&amount=100&lang=es</pre>
            <pre>{
  "result": "Conversión exitosa",
  "from": "USD",
  "to": "EUR",
  "amount": 100.0,
  "converted": 91.23,
  "rate": 0.9123
}</pre>
        </div>
        <div class="section">
            <h2>Notas y recomendaciones</h2>
            <ul>
                <li>El microservicio utiliza una API externa para obtener las tasas de cambio. Si la API externa falla, se devolverá un error 502.</li>
                <li>Prueba con códigos de moneda inválidos o sin parámetros para ver las respuestas de error.</li>
                <li>El endpoint <b>/convert</b> soporta los idiomas <code>en</code> y <code>es</code> para los mensajes de respuesta.</li>
            </ul>
        </div>
        <a href="/dashboard" class="btn">⬅️ Volver al Dashboard</a>
        <a href="/swagger" class="btn">📚 Ir a Swagger UI</a>
    </body>
    </html>
    ''')

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