const API_URL = 'https://tugas-cloud-production.up.railway.app'; // Ganti jika URL backend beda

async function fetchRentals() {
    try {
        const res = await fetch(`${API_URL}/rentals`);
        const data = await res.json();
        const list = document.getElementById('rental-list');
        list.innerHTML = '';

        if (!Array.isArray(data)) return;

        data.forEach(item => {
            const li = document.createElement('li');
            li.style = "padding: 10px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; background: white; margin-bottom: 5px; border-radius: 5px;";
            li.innerHTML = `
                <span><b>${item.nama}</b> - PS ${item.ps}</span>
                <span>${item.durasi} Jam (${item.status})</span>
            `;
            list.appendChild(li);
        });
    } catch (e) {
        console.error(e);
    }
}

async function addRental() {
    const nama = document.getElementById('nama-input').value;
    const ps = document.getElementById('ps-input').value;
    const durasi = document.getElementById('durasi-input').value;

    if (!nama || !ps || !durasi) return;

    try {
        const res = await fetch(`${API_URL}/rentals`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nama, ps, durasi })
        });

        if (res.ok) {
            document.getElementById('nama-input').value = '';
            document.getElementById('ps-input').value = '';
            document.getElementById('durasi-input').value = '';
            fetchRentals();
            updateStats();
        }
    } catch (e) {
        alert("Gagal koneksi ke server");
    }
}

async function updateStats() {
    try {
        const res = await fetch(`${API_URL}/stats`);
        const result = await res.json();
        document.getElementById('stats-container').innerHTML = 
            `<p>Total Transaksi: <b>${result.data.total_rental}</b></p>`;
    } catch (e) { console.log(e); }
}

fetchRentals();
updateStats();