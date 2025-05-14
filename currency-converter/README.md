# Currency Converter Microservice

Este microservicio permite la conversión de monedas utilizando Flask, Redis y soporte multilenguaje.

## Estructura del proyecto

```
currency-converter/
│
├── app.py                 # Servidor principal con Flask
├── config.py              # Variables de entorno
├── cache.py               # Gestión de Redis
├── translator.py          # Manejador de idioma
├── logger.py              # Logs de auditoría
├── requirements.txt       # Dependencias
├── .env                   # Claves y configuración
└── README.md              # Instrucciones
```

## Instalación

1. Clona el repositorio y entra en la carpeta:
   ```bash
   git clone <repo_url>
   cd currency-converter
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura el archivo `.env` con tus variables de entorno.

## Ejecución

```bash
python app.py
```

## Uso de la API

### Endpoint: `/convert`

Convierte una cantidad de una moneda a otra.

**Método:** `GET`

**Parámetros:**
- `from`: Código de moneda origen (ej: `USD`)
- `to`: Código de moneda destino (ej: `EUR`)
- `amount`: Cantidad a convertir (ej: `100`)
- `lang`: (opcional) Idioma de la respuesta (`en` o `es`)

**Ejemplo de solicitud:**

```
GET http://localhost:5000/convert?from=USD&to=EUR&amount=100
```

**Ejemplo de respuesta:**
```json
{
  "result": "Conversion successful",
  "from": "USD",
  "to": "EUR",
  "amount": 100.0,
  "converted": 91.23,
  "rate": 0.9123
}
```

**Ejemplo en español:**
```
GET http://localhost:5000/convert?from=USD&to=EUR&amount=100&lang=es
```

**Respuesta:**
```json
{
  "result": "Conversión exitosa",
  "from": "USD",
  "to": "EUR",
  "amount": 100.0,
  "converted": 91.23,
  "rate": 0.9123
}
```

## Notas
- Asegúrate de tener un servidor Redis corriendo.
- Personaliza las traducciones y la lógica de conversión según tus necesidades.
- El microservicio utiliza [ExchangeRate-API](https://www.exchangerate-api.com/) por defecto. Puedes cambiar la URL en `app.py` si usas otro proveedor. 