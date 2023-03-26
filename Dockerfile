# Python tabanlı resmi Docker görüntüsü seçin
FROM python:3.8-slim-buster

# Uygulamanızın çalışması için gerekli tüm dosyaları kopyalayın
COPY . /app
COPY . /unittest
COPY . /scraper
WORKDIR /app

# Uygulamanızın bağımlılıklarını yükleyin
RUN pip install --no-cache-dir -r requirements.txt

# Uygulamanızı çalıştırın
CMD ["python", "./app.py"]