# 📝 Todo List - Aplikasi Microservices

Aplikasi To-Do List sederhana dengan arsitektur microservices menggunakan Docker, PostgreSQL, Redis, dan Flask API.

## 🏗️ Arsitektur Aplikasi

Aplikasi ini terdiri dari **4 Service** yang di-containerize dengan Docker:

1. **Frontend Service** (Nginx)
   - Web interface untuk user
   - Port: 3000

2. **Backend API Service** (Python Flask)
   - REST API untuk operasi CRUD
   - Port: 5000

3. **Database Service** (PostgreSQL)
   - Persistent storage untuk data todo
   - Port: 5432

4. **Cache Service** (Redis)
   - Caching untuk meningkatkan performa
   - Cloud emulation service
   - Port: 6379

## 🚀 Cara Menjalankan Aplikasi

### Prerequisites
- Docker & Docker Compose terinstall
- Port 3000, 5000, 5432, 6379 tersedia

### Langkah-langkah

1. **Clone atau download folder aplikasi**
   ```bash
   cd todo-app
   ```

2. **Build dan jalankan semua service**
   ```bash
   docker-compose up --build
   ```

3. **Akses aplikasi**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

4. **Stop aplikasi**
   ```bash
   docker-compose down
   ```

5. **Stop dan hapus semua data**
   ```bash
   docker-compose down -v
   ```

## 📡 API Endpoints

### Get All Todos
```
GET /api/todos
Response: { data: [...], source: "cache" | "database" }
```

### Create Todo
```
POST /api/todos
Body: { title: string, description?: string }
Response: { id: number, message: string }
```

### Update Todo
```
PUT /api/todos/:id
Body: { completed?: boolean, title?: string, description?: string }
Response: { message: string }
```

### Delete Todo
```
DELETE /api/todos/:id
Response: { message: string }
```

### Get Statistics
```
GET /api/stats
Response: { data: { total, completed, pending }, source: "cache" | "database" }
```

## 🔧 Teknologi yang Digunakan

- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Backend**: Python Flask
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Container**: Docker & Docker Compose
- **Web Server**: Nginx

## 📊 Fitur Aplikasi

✅ Tambah task baru dengan judul dan deskripsi
✅ Tandai task sebagai selesai/belum selesai
✅ Hapus task
✅ Lihat statistik (total, selesai, pending)
✅ Data persistence dengan PostgreSQL
✅ Caching dengan Redis untuk performa optimal
✅ Responsive design

## 🧪 Testing API

Anda bisa test API menggunakan curl:

```bash
# Health check
curl http://localhost:5000/health

# Get all todos
curl http://localhost:5000/api/todos

# Create new todo
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"This is a test"}'

# Get stats
curl http://localhost:5000/api/stats
```

## 📁 Struktur Folder

```
todo-app/
├── docker-compose.yml       # Orchestrasi semua service
├── frontend/
│   ├── Dockerfile          # Container config untuk frontend
│   ├── index.html          # UI utama
│   ├── style.css           # Styling
│   └── app.js              # Logic frontend
├── backend/
│   ├── Dockerfile          # Container config untuk backend
│   ├── requirements.txt    # Dependencies Python
│   └── app.py              # Flask API application
└── README.md               # Dokumentasi ini
```

## 🎓 Konsep yang Diimplementasikan

1. **Microservices Architecture**: Aplikasi dibagi menjadi service-service independen
2. **Containerization**: Setiap service berjalan di Docker container
3. **Service Orchestration**: Docker Compose mengelola semua service
4. **Data Persistence**: PostgreSQL untuk storage yang persistent
5. **Caching Layer**: Redis untuk meningkatkan performa (emulasi cloud service)
6. **RESTful API**: Backend menyediakan API standar REST
7. **Separation of Concerns**: Frontend, Backend, Database terpisah

## 📝 Catatan

- Redis digunakan sebagai caching layer dan sebagai emulasi cloud service
- Cache di-invalidate otomatis ketika data berubah
- Database akan dibuat otomatis saat pertama kali dijalankan
- Data akan persist meskipun container di-restart (kecuali jika `docker-compose down -v`)

## 👨‍💻 Author

[Nama: Raffi Ahmad]
[NIM: 32602300048]


## 📄 License

Educational purposes only.