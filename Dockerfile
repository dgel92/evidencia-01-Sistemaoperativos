FROM python:3.11-slim
WORKDIR /app
COPY prueba1.py .
CMD ["python", "prueba1.py"]