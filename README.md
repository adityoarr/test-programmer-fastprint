# Test Kerja - Fast Print

### Tentang project
Projek ini dipergunakan untuk test kerja saya di Fast Print. Tech stack yang digunakan pada project ini:
1. Django
2. PostgreSQL
3. Docker

### Berikut adalah cara menjalankan project:
1. Pastikan sudah menginstal Docker dan Docker sudah berjalan
2. Clone project
3. Buka cmd/terminal, masuk ke lokasi root folder project
4. Masukkan command untuk migrasi ke database di postgresql dan jalankan secara berurutan
- docker compose run web python manage.py makemigrations
- docker compose run web python manage.py migrate
5. Lalu, untuk mengisi data di table dimana data didapatkan melalui API yang telah disediakan di soal, jalankan command berikut di cmd/terminal
```bash
docker compose run web python manage.py sync_api
```