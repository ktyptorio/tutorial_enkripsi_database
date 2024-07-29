# Enkripsi dan Keamanan Data

Panduan ini akan membimbing Anda melalui proses penyiapan dan penggunaan sistem basis data terenkripsi menggunakan Vault, MariaDB, dan layanan API kustom.

## Persiapan Teknis

1. Pastikan Anda memiliki Virtual Box atau VMWare terinstal.
2. Siapkan VM dengan Ubuntu Server 22.04 LTS.
3. Instal Docker:
   ```bash
   sudo nano docker-install.sh
   ```
   Salin dan tempel skrip berikut:
   ```bash
   #!/bin/bash
   for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
   sudo apt-get update
   sudo apt-get install -y ca-certificates curl gnupg
   sudo install -m 0755 -d /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   sudo chmod a+r /etc/apt/keyrings/docker.gpg
   echo \
   "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
   "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt-get update
   sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```
   Jalankan skrip:
   ```bash
   sudo bash docker-install.sh
   ```

## Instalasi Service

1. Clone repository:
   ```bash
   sudo git clone https://github.com/ktyptorio/tutorial_enkripsi_database.git
   ```

2. Masuk ke direktori yang telah di-clone dan jalankan Docker Compose:
   ```bash
   sudo docker compose up -d --build
   ```

3. Verifikasi instalasi:
   ```bash
   sudo docker container ls
   ```

## Persiapan Vault

1. Akses Vault melalui browser di `http://<IP>:8200`
2. Masukkan token: `12345678`

## Proses Enkripsi-Dekripsi dengan CLI

1. Akses container Vault:
   ```bash
   sudo docker container exec -it <CONTAINER_ID> sh
   ```

2. Atur variabel lingkungan Vault:
   ```bash
   export VAULT_ADDR='http://127.0.0.1:8200'
   export VAULT_TOKEN="12345678"
   ```

3. Buat Transit Engine:
   ```bash
   vault secrets enable -path=transit-cli transit
   ```

4. Buat kunci:
   ```bash
   vault write -f transit-cli/keys/my-key-0
   ```

5. Enkripsi data:
   ```bash
   vault write transit-cli/encrypt/my-key-0 plaintext=$(echo "informasi rahasia" | base64)
   ```

6. Dekripsi data:
   ```bash
   vault write transit-cli/decrypt/my-key-0 ciphertext=<value>
   base64 -d <<EOF
   "<value>"
   EOF
   ```

## Persiapan Database

1. Akses container MariaDB:
   ```bash
   sudo docker exec -it <container_id> bash
   ```

2. Masuk ke MariaDB:
   ```bash
   mariadb -u root -p
   ```
   (password: secret)

3. Buat database contoh:
   ```sql
   CREATE DATABASE IF NOT EXISTS my_database;
   USE my_database;
   CREATE TABLE IF NOT EXISTS encrypted_personal_data (
     id INT AUTO_INCREMENT PRIMARY KEY,
     name VARCHAR(255),
     gender VARCHAR(255),
     age VARCHAR(255),
     address VARCHAR(255),
     phone_number VARCHAR(255),
     credit_card_number VARCHAR(255)
   );
   ```

## Penggunaan API Service

Akses dokumentasi API di `http://<IP>:8000/docs`

1. Enkripsi data:
   ```bash
   curl -X 'POST' \
     'http://localhost:8000/write' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
       "data":{
         "name": "Andi",
         "gender": "Male",
         "age": 35,
         "address": "Jl. Diponegoro No. 321, Bandung",
         "phone_number": "+628987654321",
         "credit_card_number": "7890-1234-5678-9012"
       },
       "table":"encrypted_personal_data"
     }'
   ```

2. Dekripsi semua data:
   ```bash
   curl -X 'GET' \
     'http://localhost:8000/read_all?table=encrypted_personal_data' \
     -H 'accept: application/json'
   ```

3. Dekripsi data spesifik:
   ```bash
   curl -X 'GET' \
     'http://localhost:8000/read/4?table=encrypted_personal_data' \
     -H 'accept: application/json'
   ```

4. Rewrap data:
   ```bash
   curl -X 'POST' \
     'http://localhost:8000/rewrap?table=encrypted_personal_data' \
     -H 'accept: application/json'
   ```

README ini memberikan panduan dasar untuk menyiapkan dan menggunakan sistem basis data terenkripsi. Pastikan untuk mengganti `<IP>` dan `<container_id>` dengan nilai yang sesuai untuk setup Anda.