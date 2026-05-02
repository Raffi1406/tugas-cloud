// Pastikan URL menggunakan HTTPS dan sesuai dengan URL backend kamu
const API_URL = 'https://tugas-cloud-production.up.railway.app';

// Fungsi untuk mengambil dan menampilkan statistik
async function fetchStats() {
    try {
        const response = await fetch(`${API_URL}/stats`);
        const result = await response.json();
        const stats = result.data;
        
        document.getElementById('stats-container').innerHTML = `
            <div style="background: #eef2f7; padding: 10px; border-radius: 8px; margin-bottom: 15px;">
                <strong>Statistik:</strong><br>
                Total: ${stats.total} | Selesai: ${stats.completed} | Pending: ${stats.pending} <br>
                <small>Sumber data: ${result.source}</small>
            </div>
        `;
    } catch (error) {
        console.error("Gagal mengambil statistik:", error);
    }
}

// Fungsi untuk mengambil dan menampilkan daftar tugas
async function fetchTodos() {
    try {
        const response = await fetch(`${API_URL}/todos`);
        const todos = await response.json();
        const list = document.getElementById('todo-list');
        
        list.innerHTML = ''; // Kosongkan daftar lama
        
        if (todos.length === 0) {
            list.innerHTML = '<li>Belum ada tugas.</li>';
            return;
        }

        todos.forEach(todo => {
            list.innerHTML += `
                <li style="display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #ddd;">
                    <span>${todo.task}</span>
                    <span>${todo.completed ? '✅' : '⏳'}</span>
                </li>
            `;
        });
    } catch (error) {
        console.error("Gagal mengambil daftar tugas:", error);
        document.getElementById('todo-list').innerHTML = '<li>Gagal terhubung ke server.</li>';
    }
}

// Fungsi untuk menambah tugas baru
async function addTask() {
    const input = document.getElementById('task-input');
    const task = input.value;
    
    if (!task) {
        alert("Isi tugasnya dulu, Raffi!");
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/todos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task })
        });

        if (response.ok) {
            input.value = ''; // Kosongkan input setelah berhasil
            
            // KUNCI UTAMA: Panggil ulang fungsi fetch agar tampilan update otomatis
            await fetchTodos(); 
            await fetchStats();
        } else {
            alert("Gagal menambah tugas ke server.");
        }
    } catch (error) {
        console.error("Error saat menambah tugas:", error);
        alert("Tidak bisa terhubung ke backend.");
    }
}

// Jalankan fungsi saat halaman pertama kali dibuka
fetchTodos();
fetchStats();