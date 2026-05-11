# Rental PS 3 Genuk City

Aplikasi berbasis web untuk manajemen penyewaan PlayStation dengan arsitektur Microservices. Aplikasi ini melacak data penyewa, durasi sewa, nomor PS, dan menghitung total harga secara otomatis (Tarif: Rp5.000/jam).

## Teknologi yang Digunakan
- **Frontend:** HTML, CSS, Vanilla JavaScript (Nginx)
- **Backend:** Python, Flask, Flask-CORS
- **Database:** MySQL
- **Cache:** Redis
- **Infrastruktur:** Docker & Docker Compose

## Struktur Proyek
- `/frontend`: Berisi UI aplikasi dan logika untuk mengambil/mengirim data ke API.
- `/backend`: Berisi REST API yang menghubungkan frontend dengan database dan cache.
- `docker-compose.yml`: File konfigurasi untuk menjalankan seluruh layanan secara lokal dengan Docker.
- `MANUAL.md`: Panduan instalasi dan penggunaan aplikasi.