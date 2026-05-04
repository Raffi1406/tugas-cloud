const API_URL = 'https://tugas-cloud-production.up.railway.app';

async function fetchTodos() {
    try {
        const res = await fetch(`${API_URL}/todos`);
        const data = await res.json();
        const list = document.getElementById('todo-list');
        list.innerHTML = '';

        if (!Array.isArray(data)) throw new Error("Format data salah");

        data.forEach(todo => {
            const li = document.createElement('li');
            li.style = "padding: 10px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between;";
            li.innerHTML = `<span>${todo.task}</span> <span>${todo.completed ? '✅' : '⏳'}</span>`;
            list.appendChild(li);
        });
    } catch (e) {
        document.getElementById('todo-list').innerHTML = `<li style="color:red">Error: ${e.message}</li>`;
    }
}

async function addTask() {
    const input = document.getElementById('task-input');
    if (!input.value) return;

    try {
        const res = await fetch(`${API_URL}/todos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task: input.value })
        });

        if (res.ok) {
            input.value = '';
            await fetchTodos(); // Langsung update daftar
            updateStats();
        }
    } catch (e) {
        alert("Gagal menambah tugas");
    }
}

async function updateStats() {
    try {
        const res = await fetch(`${API_URL}/stats`);
        const result = await res.json();
        const s = result.data;
        document.getElementById('stats-container').innerHTML = 
            `<small>Total: ${s.total} | Selesai: ${s.completed} | Pending: ${s.pending}</small>`;
    } catch (e) { console.log("Stats error"); }
}

// Jalankan saat load awal
fetchTodos();
updateStats();