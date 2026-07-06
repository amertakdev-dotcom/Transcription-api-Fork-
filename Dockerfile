# [span_11](start_span)Usar una imagen oficial de Python[span_11](end_span)
[span_12](start_span)FROM python:3.9[span_12](end_span)

# [span_13](start_span)Establecer el directorio de trabajo[span_13](end_span)
[span_14](start_span)WORKDIR /app[span_14](end_span)

# [span_15](start_span)Copiar los archivos necesarios[span_15](end_span)
[span_16](start_span)COPY requirements.txt .[span_16](end_span)
[span_17](start_span)COPY main.py .[span_17](end_span)
[span_18](start_span)COPY transcription.py .[span_18](end_span)
[span_19](start_span)COPY .env .env[span_19](end_span)

# [span_20](start_span)Instalar dependencias[span_20](end_span)
[span_21](start_span)RUN pip install --no-cache-dir -r requirements.txt[span_21](end_span)

# [span_22](start_span)Exponer el puerto de FastAPI[span_22](end_span)
[span_23](start_span)EXPOSE 8000[span_23](end_span)

# បញ្ជាដំណើរការ៖ ប្រើប្រាស់ dynamic port របស់ Render
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
