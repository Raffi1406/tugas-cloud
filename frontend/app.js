const API_URL = 'https://tugas-cloud-production-b4bf.up.railway.app'
let activePS = []

function formatRupiah(angka) {

    return new Intl.NumberFormat(
        'id-ID',
        {
            style: 'currency',
            currency: 'IDR'
        }
    ).format(angka)
}

async function fetchRentals() {

    try {

        const res = await fetch(`${API_URL}/rentals`)
        const data = await res.json()

        const list = document.getElementById('rental-list')

        list.innerHTML = ''

        if (!Array.isArray(data)) return

        activePS = data
            .filter(item => item.status === 'Aktif')
            .map(item => parseInt(item.ps))

        data.forEach(item => {

            const li = document.createElement('li')

            li.innerHTML = `
                <div style="display:flex; flex-direction:column;">
                    <span style="font-weight:bold;">
                        ${item.nama} - PS ${item.ps}
                    </span>

                    <span>
                        ${item.durasi} Jam
                    </span>
                </div>

                <div style="display:flex; flex-direction:column; align-items:end;">
                    <span style="font-weight:bold; color:blue;">
                        ${formatRupiah(item.total_harga)}
                    </span>

                    <span>
                        ${item.status}
                    </span>
                </div>
            `

            list.appendChild(li)
        })

    } catch (e) {

        console.log(e)
    }
}

async function addRental() {

    const nama = document.getElementById('nama-input').value
    const ps = parseInt(document.getElementById('ps-input').value)
    const durasi = parseInt(document.getElementById('durasi-input').value)

    if (!nama || !ps || !durasi) {

        alert('Semua field wajib diisi')
        return
    }

    if (ps < 1 || ps > 10) {

        alert('Nomor PS harus 1-10')
        return
    }

    if (activePS.includes(ps)) {

        alert(`PS ${ps} sedang dipakai`)
        return
    }

    try {

        const res = await fetch(`${API_URL}/rentals`, {

            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify({
                nama,
                ps,
                durasi
            })
        })

        const result = await res.json()

        console.log(result)

        if (res.ok) {

            alert('Berhasil tambah rental')

            document.getElementById('nama-input').value = ''
            document.getElementById('ps-input').value = ''
            document.getElementById('durasi-input').value = ''

            fetchRentals()
            updateStats()

        } else {

            alert(result.error || 'Gagal tambah data')
        }

    } catch (e) {

        console.log(e)

        alert('Koneksi server gagal')
    }
}

async function updateStats() {

    try {

        const res = await fetch(`${API_URL}/stats`)

        const result = await res.json()

        const totalRental = result.data.total_rental || 0
        const totalPendapatan = result.data.total_pendapatan || 0

        document.getElementById('stats-container').innerHTML = `
            <div style="display:flex; justify-content:space-between;">

                <div>
                    Total Rental
                    <br>
                    <b>${totalRental}</b>
                </div>

                <div style="text-align:right;">
                    Pendapatan
                    <br>
                    <b>${formatRupiah(totalPendapatan)}</b>
                </div>

            </div>
        `

    } catch (e) {

        console.log(e)
    }
}

fetchRentals()
updateStats()