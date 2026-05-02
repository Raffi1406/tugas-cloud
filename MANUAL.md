# Manual Penggunaan Aplikasi Todo List

## Identitas
*   **Nama:** Raffi Ahmad
*   **NIM:** 32602300048 

## Link Kode Aplikasi
*   **GitHub Repository:** [Masukkan Link GitHub Anda di sini]

## Cara Menjalankan (Deployment)
1.  Pastikan Docker dan Docker Compose sudah terinstall.
2.  Buka terminal pada direktori root proyek.
3.  Jalankan perintah `docker-compose up -d --build`.
4.  Tunggu hingga seluruh container (db, redis, backend, frontend) berstatus running.

## Cara Mengakses melalui Cloud Emulator (Redfinger)
1.  Jalankan tunnel menggunakan Ngrok ke port frontend dengan perintah `ngrok http 80`.
2.  Salin URL publik yang diberikan oleh Ngrok (misal: `https://abcd-123.ngrok-free.app`).
3.  Buka aplikasi Redfinger, masuk ke browser di dalam emulator, dan paste URL tersebut.
4.  Aplikasi Todo List siap digunakan.

## Cara Penggunaan Fitur
*   **Menambah Tugas:** Ketikkan nama tugas pada kolom input lalu klik tombol "Tambah".
*   **Statistik Cache:** Aplikasi otomatis menyimpan statistik tugas (Total, Selesai, Pending) menggunakan layanan Redis (Cache) selama 30 detik untuk mengoptimalkan database PostgreSQL.