# 📦 InventoRIS — Sistem Manajemen Inventaris

> Mini Project Pemrograman Visual (PV26)  
> Aplikasi desktop manajemen inventaris barang menggunakan PySide6 dan SQLite

---

## 👤 Informasi Mahasiswa

| Field           | Nilai               |
| --------------- | ------------------- |
| **Nama**        | Lalu Rifqi Ramadhan |
| **NIM**         | F1D02310071         |
| **Kelas**       | PV26                |
| **Mata Kuliah** | Pemrograman Visual  |

---

## 📋 Deskripsi Aplikasi

**InventoRizZ** adalah aplikasi manajemen inventaris barang berbasis desktop yang dibangun menggunakan framework PySide6. Aplikasi ini memungkinkan pengguna untuk mengelola data barang di gudang atau toko secara efisien melalui antarmuka grafis yang intuitif.

### Fitur Utama:

- ✅ **Tambah Barang** — Form input lengkap dengan 8 field data barang
- ✅ **Edit Barang** — Update data barang yang sudah ada
- ✅ **Hapus Barang** — Hapus dengan konfirmasi dialog
- ✅ **Pencarian Real-time** — Cari berdasarkan nama, kode, atau kategori
- ✅ **Dashboard Statistik** — Ringkasan total item, stok, nilai, dan kategori
- ✅ **Indikator Stok Rendah** — Baris berwarna kuning jika stok < 5
- ✅ **Persistensi Data** — Data tersimpan di SQLite, tidak hilang setelah aplikasi ditutup

---

## 🗂️ Struktur Project (Separation of Concerns)

```
inventory_app/
│
├── main.py                          # Entry point aplikasi
│
├── ui/                              # Layer UI (tampilan)
│   ├── __init__.py
│   ├── main_window.py               # Jendela utama
│   └── dialog_barang.py             # Dialog tambah/edit barang
│
├── controllers/                     # Layer Controller (logika bisnis)
│   ├── __init__.py
│   └── inventory_controller.py      # Validasi dan orchestrasi
│
├── database/                        # Layer Database
│   ├── __init__.py
│   ├── db_manager.py                # Operasi SQLite CRUD
│   └── inventaris.db                # File database (dibuat otomatis)
│
├── styles/
│   └── app.qss                      # Stylesheet QSS eksternal
│
└── README.md
```

### Prinsip SoC yang Diterapkan:

| Layer          | File                                       | Tanggung Jawab            |
| -------------- | ------------------------------------------ | ------------------------- |
| **View**       | `ui/main_window.py`, `ui/dialog_barang.py` | Tampilan & interaksi user |
| **Controller** | `controllers/inventory_controller.py`      | Validasi & logika bisnis  |
| **Database**   | `database/db_manager.py`                   | Operasi SQL langsung      |
| **Style**      | `styles/app.qss`                           | Styling visual aplikasi   |

---

## 🗃️ Desain Database

**Tabel:** `barang`

| Kolom           | Tipe    | Keterangan                   |
| --------------- | ------- | ---------------------------- |
| `id`            | INTEGER | Primary Key, Auto Increment  |
| `kode_barang`   | TEXT    | Kode unik barang (UNIQUE)    |
| `nama_barang`   | TEXT    | Nama lengkap barang          |
| `kategori`      | TEXT    | Kategori barang              |
| `jumlah`        | INTEGER | Stok saat ini                |
| `satuan`        | TEXT    | Satuan barang (pcs, kg, dll) |
| `harga`         | REAL    | Harga satuan                 |
| `lokasi`        | TEXT    | Lokasi penyimpanan           |
| `keterangan`    | TEXT    | Catatan tambahan             |
| `tanggal_masuk` | TEXT    | Tanggal barang masuk         |

---

## ⚙️ Cara Menjalankan

### Prasyarat

- Python 3.10 atau lebih baru
- PySide6

### Instalasi

```bash
# 1. Clone repository
git clone https://github.com/username/pv26-miniproject-inventaris-F1Dxxxxxxx.git
cd pv26-miniproject-inventaris-F1Dxxxxxxx

# 2. Install dependensi
pip install PySide6

# 3. Jalankan aplikasi
python main.py
```

> Database (`inventaris.db`) akan dibuat **otomatis** di folder `database/` saat pertama kali dijalankan.

---

## 🧪 Teknologi yang Digunakan

| Teknologi   | Versi    | Kegunaan                      |
| ----------- | -------- | ----------------------------- |
| **Python**  | 3.10+    | Bahasa pemrograman utama      |
| **PySide6** | 6.x      | Framework GUI (Qt for Python) |
| **SQLite**  | built-in | Database penyimpanan lokal    |
| **QSS**     | —        | Styling antarmuka             |

---

## 🎥 Video Demo

[Link YouTube — akan diisi setelah upload]

---

## 📌 Catatan

- Baris berwarna **kuning** menandakan stok barang di bawah 5 unit
- Double-click pada baris tabel untuk langsung membuka dialog edit
- Shortcut keyboard: `Ctrl+N` (Tambah), `Ctrl+E` (Edit), `Delete` (Hapus), `F5` (Refresh)
