"""
db_manager.py
Database Manager - Lapisan database untuk aplikasi Manajemen Inventaris
Menangani semua operasi SQLite (CRUD)
"""

import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventaris.db")


def get_connection():
    """Membuat dan mengembalikan koneksi ke database SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Inisialisasi database: buat tabel jika belum ada."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS barang (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            kode_barang TEXT    NOT NULL UNIQUE,
            nama_barang TEXT    NOT NULL,
            kategori    TEXT    NOT NULL,
            jumlah      INTEGER NOT NULL DEFAULT 0,
            satuan      TEXT    NOT NULL,
            harga       REAL    NOT NULL DEFAULT 0,
            lokasi      TEXT,
            keterangan  TEXT,
            tanggal_masuk TEXT  NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# ── CREATE ──────────────────────────────────────────────────────────────────

def tambah_barang(data: dict) -> bool:
    """
    Menambah data barang baru ke database.
    data: dict dengan key kode_barang, nama_barang, kategori, jumlah,
          satuan, harga, lokasi, keterangan, tanggal_masuk
    Mengembalikan True jika berhasil, False jika gagal.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO barang
                (kode_barang, nama_barang, kategori, jumlah, satuan,
                 harga, lokasi, keterangan, tanggal_masuk)
            VALUES
                (:kode_barang, :nama_barang, :kategori, :jumlah, :satuan,
                 :harga, :lokasi, :keterangan, :tanggal_masuk)
        """, data)
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


# ── READ ─────────────────────────────────────────────────────────────────────

def ambil_semua_barang() -> list:
    """Mengambil seluruh data barang dari database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM barang ORDER BY id DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def cari_barang(keyword: str) -> list:
    """Mencari barang berdasarkan nama atau kode barang."""
    conn = get_connection()
    cursor = conn.cursor()
    like = f"%{keyword}%"
    cursor.execute("""
        SELECT * FROM barang
        WHERE nama_barang LIKE ? OR kode_barang LIKE ? OR kategori LIKE ?
        ORDER BY id DESC
    """, (like, like, like))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def ambil_barang_by_id(id_barang: int) -> dict | None:
    """Mengambil satu data barang berdasarkan ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM barang WHERE id = ?", (id_barang,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


# ── UPDATE ───────────────────────────────────────────────────────────────────

def update_barang(id_barang: int, data: dict) -> bool:
    """
    Memperbarui data barang yang sudah ada.
    Mengembalikan True jika berhasil.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        data["id"] = id_barang
        cursor.execute("""
            UPDATE barang SET
                kode_barang   = :kode_barang,
                nama_barang   = :nama_barang,
                kategori      = :kategori,
                jumlah        = :jumlah,
                satuan        = :satuan,
                harga         = :harga,
                lokasi        = :lokasi,
                keterangan    = :keterangan,
                tanggal_masuk = :tanggal_masuk
            WHERE id = :id
        """, data)
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


# ── DELETE ───────────────────────────────────────────────────────────────────

def hapus_barang(id_barang: int) -> bool:
    """Menghapus data barang berdasarkan ID."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM barang WHERE id = ?", (id_barang,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


# ── STATISTIK ─────────────────────────────────────────────────────────────────

def statistik() -> dict:
    """Mengambil ringkasan statistik inventaris."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total_item FROM barang")
    total_item = cursor.fetchone()["total_item"]
    cursor.execute("SELECT COALESCE(SUM(jumlah), 0) as total_stok FROM barang")
    total_stok = cursor.fetchone()["total_stok"]
    cursor.execute("SELECT COALESCE(SUM(jumlah * harga), 0) as total_nilai FROM barang")
    total_nilai = cursor.fetchone()["total_nilai"]
    cursor.execute("SELECT COUNT(DISTINCT kategori) as total_kategori FROM barang")
    total_kategori = cursor.fetchone()["total_kategori"]
    conn.close()
    return {
        "total_item": total_item,
        "total_stok": total_stok,
        "total_nilai": total_nilai,
        "total_kategori": total_kategori,
    }
