# Usa una imagen oficial de Python como base
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Expone el puerto requerido por Cloud Run
EXPOSE 8080

# Comando para ejecutar la app usando Gunicorn
CMD ["gunicorn", "hound_express_be.wsgi:application", "--bind", "0.0.0.0:8080"]