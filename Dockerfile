# Gunakan image dasar python
FROM python:3.11

# Tentukan working directory
WORKDIR /app

# Salin file requirements.txt ke dalam container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file aplikasi ke dalam container
COPY api_service/ .

# Eksekusi perintah untuk menjalankan FastAPI dengan uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
