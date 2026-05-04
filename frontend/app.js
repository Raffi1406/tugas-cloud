// URL Backend kamu
const API_URL = '[https://tugas-cloud-production.up.railway.app](https://tugas-cloud-production.up.railway.app)';

async function fetchTodos() {
    try {
        const res = await fetch(`${API_URL}/todos`);
        const data = await res.json();
        
        const list = document.getElementById('todo-list');
        list.innerHTML = '';

        // Validasi apakah data adalah array
        if (!Array.isArray(data)) {
            throw new Error("Data bukan array");
        }

        if (data.length === 0) {
            list.innerHTML = '<li style="text-align:center; color:#888;">Belum ada tugas hari ini.</li>';
            return;
        }

        data.forEach(todo => {
            const li = document.createElement('li');
            li.className = 'todo-item'; // Tambahkan class untuk CSS
            li.style = "background:white; padding:12px; margin-bottom:8px; border-radius:8px; display:flex; justify-content:space-between; box-shadow: 0 2px 4px rgba(0,0,0,0.05);";
            li.innerHTML = `<span>${todo.task}</span> <span>${todo.completed ? '✅' : '⏳'}</span>`;
            list.appendChild(li);
        });
    } catch (e) {
        console.error(e);
        document.getElementById('todo-list').innerHTML = `<li style="color:red; background:#ffebeb; padding:10px; border-radius:8px;">Error: ${e.message}. Cek koneksi database di Railway.</li>`;
    }
}

async function addTask() {
    const input = document.getElementById('task-input');
    const taskValue = input.value.trim();
    
    if (!taskValue) return;

    try {
        const res = await fetch(`${API_URL}/todos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task: taskValue })
        });

        if (res.ok) {
            input.value = '';
            await fetchTodos();
            updateStats();
        } else {
            alert("Gagal menyimpan ke server.");
        }
    } catch (e) {
        alert("Server tidak merespons.");
    }
}

async function updateStats() {
    try {
        const res = await fetch(`${API_URL}/stats`);
        const result = await res.json();
        const s = result.data;
        document.getElementById('stats-container').innerHTML = 
            `<div style="font-size: 0.8rem; color: #666; margin-bottom: 10px;">
                Total: <b>${s.total}</b> | Selesai: <b>${s.completed}</b> | Pending: <b>${s.pending}</b>
            </div>`;
    } catch (e) { console.log("Gagal update stats"); }
}

// Load data saat pertama kali buka
fetchTodos();
updateStats();