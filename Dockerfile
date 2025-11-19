FROM python:3.11-slim
WORKDIR /app
COPY . /app/
# RUN pip install --no-cache-dir -e .

# Install minimal deps
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy project
COPY . /app

EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
