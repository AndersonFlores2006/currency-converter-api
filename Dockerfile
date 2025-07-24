# Dockerfile para Currency Converter API
FROM python:3.10-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Crea el directorio de la app
WORKDIR /app

# Copia los archivos de dependencias
COPY requirements.txt ./

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copia el resto del código fuente
COPY . .

# Expone el puerto 8080 para Cloud Run
EXPOSE 8080

# Comando para ejecutar la app en producción con Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"] 