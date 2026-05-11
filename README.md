# Panduan Penggunaan dan Instalasi

Dokumen ini berisi panduan untuk menjalankan aplikasi "Rental PS 3 Genuk City" di lingkungan lokal (Localhost) maupun di lingkungan produksi (Railway).

## 1. Menjalankan di Komputer Lokal (Docker)

**Persyaratan:**
Pastikan Docker dan Docker Compose sudah terinstal dan berjalan di komputer Anda.

**Langkah-langkah:**
1. Buka terminal atau command prompt.
2. Arahkan direktori aktif ke folder utama proyek (tempat file `docker-compose.yml` berada).
3. Jalankan perintah berikut untuk membangun dan menjalankan semua kontainer:
   ```bash
   docker-compose up -d --build