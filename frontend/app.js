const API_URL = 'https://tugas-cloud-production.up.railway.app';

async function fetchStats() {
    const response = await fetch(`${API_URL}/stats`);
    const result = await response.json();
    const stats = result.data;
    document.getElementById('stats-container').innerHTML = `
        <strong>Statistik:</strong><br>
        Total: ${stats.total} | Selesai: ${stats.completed} | Pending: ${stats.pending} <br>
        <small>Sumber data: ${result.source}</small>
    `;
}

async function fetchTodos() {
    const response = await fetch(`${API_URL}/todos`);
    const todos = await response.json();
    const list = document.getElementById('todo-list');
    list.innerHTML = '';
    todos.forEach(todo => {
        list.innerHTML += `
            <li>
                <span>${todo.task}</span>
                <span>${todo.completed ? '✅' : '⏳'}</span>
            </li>
        `;
    });
}

async function addTask() {
    const input = document.getElementById('task-input');
    const task = input.value;
    if (!task) return;
    
    await fetch(`${API_URL}/todos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task })
    });
    
    input.value = '';
    fetchTodos();
    fetchStats();
}

fetchTodos();
fetchStats();