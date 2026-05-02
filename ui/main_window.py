"""
main_window.py
Jendela Utama - Tampilan utama aplikasi Manajemen Inventaris
Fokus: menampilkan data, pencarian, dan tombol aksi
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel,
    QLineEdit, QMessageBox, QMenuBar, QMenu, QFrame,
    QHeaderView, QStatusBar, QAbstractItemView
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QFont, QColor, QIcon

from controllers.inventory_controller import (
    get_semua_barang, cari_barang, hapus_barang,
    get_statistik, format_rupiah, inisialisasi
)
from ui.dialog_barang import DialogBarang
from controllers import inventory_controller as ctrl

# Informasi Mahasiswa
NAMA_MAHASISWA = "Nama Mahasiswa"
NIM_MAHASISWA  = "F1Dxxxxxxx"


class MainWindow(QMainWindow):
    """
    Jendela utama aplikasi Manajemen Inventaris.
    Bertugas menampilkan data dan menghubungkan aksi user ke controller.
    """

    def __init__(self):
        super().__init__()
        inisialisasi()
        self.setWindowTitle("InventoRIS - Sistem Manajemen Inventaris")
        self.setMinimumSize(1100, 680)
        self._setup_menu()
        self._setup_ui()
        self._setup_statusbar()
        self.muat_data()

    # ── Menu Bar ──────────────────────────────────────────────────────────────

    def _setup_menu(self):
        menubar = self.menuBar()

        # Menu File
        menu_file = menubar.addMenu("&File")
        act_refresh = QAction("🔄  Muat Ulang Data", self)
        act_refresh.setShortcut("F5")
        act_refresh.triggered.connect(self.muat_data)
        menu_file.addAction(act_refresh)
        menu_file.addSeparator()
        act_keluar = QAction("❌  Keluar", self)
        act_keluar.setShortcut("Ctrl+Q")
        act_keluar.triggered.connect(self.close)
        menu_file.addAction(act_keluar)

        # Menu Barang
        menu_barang = menubar.addMenu("&Barang")
        act_tambah = QAction("➕  Tambah Barang Baru", self)
        act_tambah.setShortcut("Ctrl+N")
        act_tambah.triggered.connect(self.aksi_tambah)
        menu_barang.addAction(act_tambah)
        act_edit = QAction("✏️  Edit Barang Terpilih", self)
        act_edit.setShortcut("Ctrl+E")
        act_edit.triggered.connect(self.aksi_edit)
        menu_barang.addAction(act_edit)
        act_hapus = QAction("🗑️  Hapus Barang Terpilih", self)
        act_hapus.setShortcut("Delete")
        act_hapus.triggered.connect(self.aksi_hapus)
        menu_barang.addAction(act_hapus)

        # Menu Bantuan
        menu_bantuan = menubar.addMenu("&Bantuan")
        act_tentang = QAction("ℹ️  Tentang Aplikasi", self)
        act_tentang.triggered.connect(self._tampilkan_tentang)
        menu_bantuan.addAction(act_tentang)

    # ── Setup UI Utama ────────────────────────────────────────────────────────

    def _setup_ui(self):
        widget_pusat = QWidget()
        self.setCentralWidget(widget_pusat)
        layout_utama = QVBoxLayout(widget_pusat)
        layout_utama.setSpacing(0)
        layout_utama.setContentsMargins(0, 0, 0, 0)

        # Header
        layout_utama.addWidget(self._buat_header())

        # Statistik
        self.panel_statistik = self._buat_panel_statistik()
        layout_utama.addWidget(self.panel_statistik)

        # Toolbar (pencarian + tombol aksi)
        layout_utama.addWidget(self._buat_toolbar())

        # Tabel data
        layout_utama.addWidget(self._buat_tabel(), stretch=1)

    def _buat_header(self) -> QWidget:
        """Membuat header aplikasi dengan nama app dan info mahasiswa."""
        frame = QFrame()
        frame.setObjectName("headerFrame")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(20, 16, 20, 16)

        # Nama aplikasi
        lbl_app = QLabel("📦  InventoRIS")
        lbl_app.setObjectName("appTitle")
        layout.addWidget(lbl_app)

        layout.addStretch()

        # Info mahasiswa (tidak bisa diedit)
        frame_info = QFrame()
        frame_info.setObjectName("infoMahasiswa")
        layout_info = QVBoxLayout(frame_info)
        layout_info.setContentsMargins(12, 6, 12, 6)
        layout_info.setSpacing(2)
        lbl_nama = QLabel(f"👤 {NAMA_MAHASISWA}")
        lbl_nama.setObjectName("labelNama")
        lbl_nim = QLabel(f"🎓 NIM: {NIM_MAHASISWA}")
        lbl_nim.setObjectName("labelNIM")
        layout_info.addWidget(lbl_nama)
        layout_info.addWidget(lbl_nim)
        layout.addWidget(frame_info)

        return frame

    def _buat_panel_statistik(self) -> QWidget:
        """Panel kartu statistik ringkasan inventaris."""
        frame = QFrame()
        frame.setObjectName("statistikFrame")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(12)

        self.kartu_item     = self._buat_kartu("0", "Total Jenis Barang", "kartuBiru")
        self.kartu_stok     = self._buat_kartu("0", "Total Stok", "kartuHijau")
        self.kartu_nilai    = self._buat_kartu("Rp 0", "Total Nilai Inventaris", "kartuOranye")
        self.kartu_kategori = self._buat_kartu("0", "Total Kategori", "kartuUngu")

        layout.addWidget(self.kartu_item)
        layout.addWidget(self.kartu_stok)
        layout.addWidget(self.kartu_nilai)
        layout.addWidget(self.kartu_kategori)
        return frame

    def _buat_kartu(self, nilai: str, label: str, obj_name: str) -> QFrame:
        """Membuat satu kartu statistik."""
        frame = QFrame()
        frame.setObjectName(obj_name)
        frame.setFixedHeight(80)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(2)
        lbl_nilai = QLabel(nilai)
        lbl_nilai.setObjectName("kartuNilai")
        lbl_label = QLabel(label)
        lbl_label.setObjectName("kartuLabel")
        layout.addWidget(lbl_nilai)
        layout.addWidget(lbl_label)
        # Simpan referensi ke label nilai agar bisa diupdate
        frame.lbl_nilai = lbl_nilai
        return frame

    def _buat_toolbar(self) -> QWidget:
        """Toolbar pencarian dan tombol CRUD."""
        frame = QFrame()
        frame.setObjectName("toolbarFrame")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(10)

        # Input pencarian
        self.input_cari = QLineEdit()
        self.input_cari.setPlaceholderText("🔍  Cari berdasarkan nama, kode, atau kategori...")
        self.input_cari.setObjectName("inputCari")
        self.input_cari.textChanged.connect(self._on_cari)
        layout.addWidget(self.input_cari, stretch=1)

        # Tombol Tambah
        self.btn_tambah = QPushButton("➕  Tambah")
        self.btn_tambah.setObjectName("btnTambah")
        self.btn_tambah.clicked.connect(self.aksi_tambah)
        layout.addWidget(self.btn_tambah)

        # Tombol Edit
        self.btn_edit = QPushButton("✏️  Edit")
        self.btn_edit.setObjectName("btnEdit")
        self.btn_edit.clicked.connect(self.aksi_edit)
        layout.addWidget(self.btn_edit)

        # Tombol Hapus
        self.btn_hapus = QPushButton("🗑️  Hapus")
        self.btn_hapus.setObjectName("btnHapus")
        self.btn_hapus.clicked.connect(self.aksi_hapus)
        layout.addWidget(self.btn_hapus)

        return frame

    def _buat_tabel(self) -> QTableWidget:
        """Membuat QTableWidget untuk menampilkan data barang."""
        self.tabel = QTableWidget()
        self.tabel.setObjectName("tabelBarang")
        self.tabel.setColumnCount(9)
        self.tabel.setHorizontalHeaderLabels([
            "ID", "Kode Barang", "Nama Barang", "Kategori",
            "Jumlah", "Satuan", "Harga Satuan", "Lokasi", "Tgl Masuk"
        ])

        # Pengaturan tampilan tabel
        header = self.tabel.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Kode
        header.setSectionResizeMode(2, QHeaderView.Stretch)            # Nama
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Kategori
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Jumlah
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Satuan
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Harga
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # Lokasi
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)  # Tanggal

        self.tabel.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabel.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabel.setAlternatingRowColors(True)
        self.tabel.verticalHeader().setVisible(False)
        self.tabel.setShowGrid(True)
        self.tabel.doubleClicked.connect(self.aksi_edit)

        return self.tabel

    def _setup_statusbar(self):
        """Setup status bar di bagian bawah."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.lbl_status = QLabel("Siap")
        self.status_bar.addWidget(self.lbl_status)

    # ── Memuat & Menampilkan Data ─────────────────────────────────────────────

    def muat_data(self, data_list: list = None):
        """Memuat ulang data ke tabel dari database atau list yang diberikan."""
        if data_list is None:
            data_list = get_semua_barang()

        self.tabel.setRowCount(0)
        for baris_ke, barang in enumerate(data_list):
            self.tabel.insertRow(baris_ke)
            self._isi_baris(baris_ke, barang)

        self._update_statistik()
        jumlah = len(data_list)
        self.lbl_status.setText(f"Menampilkan {jumlah} barang")

    def _isi_baris(self, baris: int, barang: dict):
        """Mengisi satu baris tabel dengan data barang."""
        def item(teks, align=Qt.AlignLeft | Qt.AlignVCenter):
            it = QTableWidgetItem(str(teks))
            it.setTextAlignment(align)
            return it

        center = Qt.AlignCenter

        self.tabel.setItem(baris, 0, item(barang["id"], center))
        self.tabel.setItem(baris, 1, item(barang["kode_barang"], center))
        self.tabel.setItem(baris, 2, item(barang["nama_barang"]))
        self.tabel.setItem(baris, 3, item(barang["kategori"], center))
        self.tabel.setItem(baris, 4, item(barang["jumlah"], center))
        self.tabel.setItem(baris, 5, item(barang["satuan"], center))
        self.tabel.setItem(baris, 6, item(format_rupiah(barang["harga"]), Qt.AlignRight | Qt.AlignVCenter))
        self.tabel.setItem(baris, 7, item(barang.get("lokasi", "-")))
        self.tabel.setItem(baris, 8, item(barang.get("tanggal_masuk", "-"), center))

        # Warna baris jika stok rendah (< 5)
        if barang["jumlah"] < 5:
            for col in range(9):
                cell = self.tabel.item(baris, col)
                if cell:
                    cell.setBackground(QColor("#fff3cd"))

    def _update_statistik(self):
        """Memperbarui kartu statistik di header."""
        stat = get_statistik()
        self.kartu_item.lbl_nilai.setText(str(stat["total_item"]))
        self.kartu_stok.lbl_nilai.setText(str(stat["total_stok"]))
        self.kartu_nilai.lbl_nilai.setText(format_rupiah(stat["total_nilai"]))
        self.kartu_kategori.lbl_nilai.setText(str(stat["total_kategori"]))

    # ── Pencarian ─────────────────────────────────────────────────────────────

    def _on_cari(self, keyword: str):
        """Slot: dipanggil saat teks pencarian berubah."""
        if keyword.strip():
            hasil = cari_barang(keyword.strip())
        else:
            hasil = get_semua_barang()
        self.muat_data(hasil)

    # ── Aksi CRUD ─────────────────────────────────────────────────────────────

    def aksi_tambah(self):
        """Membuka dialog tambah barang baru."""
        dialog = DialogBarang(self)
        if dialog.exec():
            data = dialog.get_data()
            ok, pesan = ctrl.tambah_barang(**data)
            if ok:
                QMessageBox.information(self, "Berhasil", pesan)
                self.muat_data()
                self.lbl_status.setText(f"✅ {pesan}")
            else:
                QMessageBox.warning(self, "Gagal", pesan)

    def aksi_edit(self):
        """Membuka dialog edit untuk barang yang dipilih."""
        id_barang = self._get_id_terpilih()
        if id_barang is None:
            QMessageBox.information(self, "Info", "Pilih satu barang yang ingin diedit.")
            return

        barang = ctrl.get_barang_by_id(id_barang)
        if not barang:
            QMessageBox.warning(self, "Error", "Data barang tidak ditemukan.")
            return

        dialog = DialogBarang(self, data_barang=barang)
        if dialog.exec():
            data = dialog.get_data()
            ok, pesan = ctrl.edit_barang(id_barang, **data)
            if ok:
                QMessageBox.information(self, "Berhasil", pesan)
                self.muat_data()
                self.lbl_status.setText(f"✅ {pesan}")
            else:
                QMessageBox.warning(self, "Gagal", pesan)

    def aksi_hapus(self):
        """Menghapus barang yang dipilih setelah konfirmasi."""
        id_barang = self._get_id_terpilih()
        if id_barang is None:
            QMessageBox.information(self, "Info", "Pilih satu barang yang ingin dihapus.")
            return

        # Dialog konfirmasi sebelum menghapus
        konfirmasi = QMessageBox.question(
            self,
            "Konfirmasi Hapus",
            f"Yakin ingin menghapus barang dengan ID {id_barang}?\n"
            "Tindakan ini tidak bisa dibatalkan.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if konfirmasi == QMessageBox.Yes:
            ok, pesan = hapus_barang(id_barang)
            if ok:
                QMessageBox.information(self, "Berhasil", pesan)
                self.muat_data()
                self.lbl_status.setText(f"🗑️ {pesan}")
            else:
                QMessageBox.warning(self, "Gagal", pesan)

    def _get_id_terpilih(self) -> int | None:
        """Mengambil ID barang dari baris yang dipilih di tabel."""
        baris = self.tabel.currentRow()
        if baris < 0:
            return None
        item = self.tabel.item(baris, 0)
        if item:
            return int(item.text())
        return None

    # ── Dialog Tentang Aplikasi ───────────────────────────────────────────────

    def _tampilkan_tentang(self):
        """Menampilkan informasi tentang aplikasi."""
        QMessageBox.about(
            self,
            "Tentang Aplikasi",
            f"""<b>📦 InventoRIS</b><br>
            <b>Sistem Manajemen Inventaris</b><br><br>
            Aplikasi desktop untuk mengelola data inventaris barang<br>
            dengan fitur tambah, edit, hapus, dan pencarian data.<br><br>
            <b>Teknologi:</b> Python, PySide6, SQLite<br><br>
            <hr>
            <b>Nama Mahasiswa:</b> {NAMA_MAHASISWA}<br>
            <b>NIM:</b> {NIM_MAHASISWA}<br>
            <b>Mata Kuliah:</b> Pemrograman Visual<br>
            <b>Mini Project – Manajemen Inventaris</b>
            """
        )
