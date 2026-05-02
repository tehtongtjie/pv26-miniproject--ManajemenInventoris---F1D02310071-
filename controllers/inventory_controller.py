from database import db_manager

def inisialisasi():
    db_manager.init_db()


# ── CREATE ────────────────────────────────────────────────────────────────────

def tambah_barang(kode_barang, nama_barang, kategori, jumlah,
                  satuan, harga, lokasi, keterangan, tanggal_masuk):
    # Validasi field wajib dan logika dasar
    if not all([kode_barang.strip(), nama_barang.strip(), kategori.strip(), satuan.strip()]):
        return False, "Semua field bertanda * wajib diisi."
        
    if jumlah < 0:
        return False, "Jumlah stok tidak boleh kurang dari 0."
    
    if harga < 0:
        return False, "Harga tidak boleh kurang dari 0."

    data = {
        "kode_barang": kode_barang.strip().upper(),
        "nama_barang": nama_barang.strip(),
        "kategori": kategori.strip(),
        "jumlah": int(jumlah),
        "satuan": satuan.strip(),
        "harga": float(harga),
        "lokasi": lokasi.strip(),
        "keterangan": keterangan.strip(),
        "tanggal_masuk": tanggal_masuk,
    }

    berhasil = db_manager.tambah_barang(data)
    if berhasil:
        return True, f"Barang '{nama_barang}' berhasil ditambahkan ke sistem."
    else:
        # Biasanya gagal karena constraint UNIQUE pada kode_barang
        return False, f"Gagal! Kode barang '{kode_barang}' sudah ada dalam database."


# ── READ ──────────────────────────────────────────────────────────────────────

def get_semua_barang():
    """Mengambil list semua barang dari database."""
    return db_manager.ambil_semua_barang()


def cari_barang(keyword: str):
    """Mencari barang berdasarkan nama atau kode."""
    return db_manager.cari_barang(keyword.strip())


def get_barang_by_id(id_barang: int):
    """Mengambil data detail satu barang berdasarkan ID primary key."""
    return db_manager.ambil_barang_by_id(id_barang)


# ── UPDATE ────────────────────────────────────────────────────────────────────

def edit_barang(id_barang, kode_barang, nama_barang, kategori, jumlah,
                satuan, harga, lokasi, keterangan, tanggal_masuk):
    """Memperbarui data barang yang sudah ada."""
    
    if not all([kode_barang.strip(), nama_barang.strip(), kategori.strip()]):
        return False, "Data wajib (Kode, Nama, Kategori) tidak boleh kosong."

    if jumlah < 0 or harga < 0:
        return False, "Jumlah atau Harga tidak boleh bernilai negatif."

    data = {
        "kode_barang": kode_barang.strip().upper(),
        "nama_barang": nama_barang.strip(),
        "kategori": kategori.strip(),
        "jumlah": int(jumlah),
        "satuan": satuan.strip(),
        "harga": float(harga),
        "lokasi": lokasi.strip(),
        "keterangan": keterangan.strip(),
        "tanggal_masuk": tanggal_masuk,
    }

    berhasil = db_manager.update_barang(id_barang, data)
    if berhasil:
        return True, f"Data barang '{nama_barang}' berhasil diperbarui."
    else:
        return False, "Gagal memperbarui database. Pastikan kode barang tidak duplikat."


# ── DELETE ────────────────────────────────────────────────────────────────────

def hapus_barang(id_barang: int):
    """Menghapus barang dari database berdasarkan ID."""
    if not id_barang:
        return False, "ID Barang tidak valid."
        
    berhasil = db_manager.hapus_barang(id_barang)
    if berhasil:
        return True, "Data barang telah dihapus permanen."
    else:
        return False, "Gagal menghapus data. Barang mungkin sudah tidak ada."


# ── STATISTIK & UTILITY ───────────────────────────────────────────────────────

def get_statistik():
    return db_manager.statistik()


def format_rupiah(nilai: float) -> str:
    try:
        formatted = "{:,.0f}".format(nilai).replace(",", ".")
        return f"Rp {formatted}"
    except (ValueError, TypeError):
        return "Rp 0"