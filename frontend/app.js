const API_URL = 'https://tugas-cloud-production.up.railway.app';
// const API_URL = 'http://127.0.0.1:8080';

// Variabel global untuk menyimpan daftar PS yang sedang dipakai
let activePS = []; 

function formatRupiah(angka) {
    return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR' }).format(angka);
}


async function fetchRentals() {
    try {
        const res = await fetch(`${API_URL}/rentals`);
        const data = await res.json();
        const list = document.getElementById('rental-list');
        list.innerHTML = '';

        if (!Array.isArray(data)) return;

        // Reset dan update daftar PS yang statusnya 'Aktif'
        activePS = data
            .filter(item => item.status === 'Aktif')
            .map(item => parseInt(item.ps)); 

        data.forEach(item => {
            const li = document.createElement('li');
            li.innerHTML = `
                <div style="display: flex; flex-direction: column;">
                    <span style="font-weight: bold; font-size: 16px; color: #333;">${item.nama} - PS No ${item.ps}</span>
                    <span style="font-size: 13px; color: #555;">${item.durasi} Jam</span>
                </div>
                <div style="display: flex; flex-direction: column; align-items: flex-end;">
                    <span style="font-weight: bold; color: #1a73e8;">${formatRupiah(item.total_harga)}</span>
                    <span style="font-size: 12px; color: #666; background: #e0e0e0; padding: 2px 6px; border-radius: 10px; margin-top: 4px;">${item.status}</span>
                </div>
            `;
            list.appendChild(li);
        });
    } catch (e) {}
}

async function addRental() {
    const nama = document.getElementById('nama-input').value;
    const ps = parseInt(document.getElementById('ps-input').value); // Ubah jadi integer
    const durasi = document.getElementById('durasi-input').value;

    if (!nama || !ps || !durasi) return;

    // VALIDASI 1: Cek apakah nomor PS antara 1 sampai 10
    if (ps < 1 || ps > 10) {
        alert("Nomor PS tidak valid! Silakan masukkan nomor 1 sampai 10.");
        return; // Hentikan proses
    }

    // VALIDASI 2: Cek apakah PS sedang disewa (Aktif)
    if (activePS.includes(ps)) {
        alert(`Maaf, PS Nomor ${ps} sedang disewa! Silakan pilih nomor PS yang lain.`);
        return; // Hentikan proses
    }

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
            fetchRentals(); // Ini otomatis akan memperbarui daftar activePS juga
            updateStats();
        } else {
            alert("Gagal menambahkan data.");
        }
    } catch (e) {
        alert("Koneksi ke server gagal.");
    }
}

async function updateStats() {
    try {
        const res = await fetch(`${API_URL}/stats`);
        const result = await res.json();
        
        const totalRental = result.data.total_rental || 0;
        const totalPendapatan = result.data.total_pendapatan || 0;

        document.getElementById('stats-container').innerHTML = 
            `<div style="display: flex; justify-content: space-between; font-size: 14px;">
                <div>Total Transaksi:<br><b style="font-size: 18px;">${totalRental}</b></div>
                <div style="text-align: right;">Pendapatan:<br><b style="font-size: 18px; color: #1a73e8;">${formatRupiah(totalPendapatan)}</b></div>
            </div>`;
    } catch (e) {}
}

fetchRentals();
updateStats();