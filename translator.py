from config import Config

TRANSLATIONS = {
    'en': {
        'conversion_success': 'Conversion successful',
        'invalid_currency': 'Invalid currency code',
    },
    'es': {
        'conversion_success': 'Conversión exitosa',
        'invalid_currency': 'Código de moneda inválido',
    }
}

def translate(key, lang=None):
    lang = lang or Config.DEFAULT_LANGUAGE
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key) 