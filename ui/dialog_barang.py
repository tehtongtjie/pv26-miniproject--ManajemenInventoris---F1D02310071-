from PySide6.QtWidgets import (
    QDialog, QFormLayout, QVBoxLayout, QHBoxLayout,
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox,
    QTextEdit, QDialogButtonBox, QLabel, QDateEdit,
    QMessageBox, QFrame
)
from PySide6.QtCore import Qt, QDate, QLocale

# Daftar Kategori Default
KATEGORI_LIST = [
    "Elektronik", "Perabot", "Alat Tulis", "Bahan Makanan",
    "Peralatan Kebersihan", "Peralatan Kantor", "Pakaian",
    "Peralatan Teknik", "Medis", "Lainnya"
]

# Daftar Satuan Default
SATUAN_LIST = ["pcs", "unit", "box", "lusin", "kg", "gram", "liter", "meter", "roll", "set"]

class DialogBarang(QDialog):
    def __init__(self, parent=None, data_barang: dict = None):
        super().__init__(parent)
        self.data_barang = data_barang
        self.mode_edit = data_barang is not None
        
        # Set Locale ke Indonesia agar format angka menggunakan titik (ribuan) dan koma (desimal)
        self.setLocale(QLocale(QLocale.Indonesian, QLocale.Indonesia))
        
        self._setup_ui()
        
        if self.mode_edit:
            self._isi_form(data_barang)
            # Kode barang biasanya bersifat unik (ID), jadi dikunci saat mode edit
            self.input_kode.setEnabled(False) 
            self.input_kode.setToolTip("Kode barang tidak dapat diubah.")

    def _setup_ui(self):
        judul_teks = "Edit Data Barang" if self.mode_edit else "Tambah Barang Baru"
        self.setWindowTitle(judul_teks)
        self.setMinimumWidth(500)
        
        layout_utama = QVBoxLayout(self)
        layout_utama.setContentsMargins(0, 0, 0, 0)
        layout_utama.setSpacing(0)

        # ── Header Section ──────────────────────────────────────────────────
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame") # ID untuk QSS
        header_frame.setFixedHeight(60)
        header_layout = QVBoxLayout(header_frame)
        
        lbl_judul = QLabel(judul_teks)
        lbl_judul.setObjectName("dialogTitle") # ID untuk QSS
        lbl_judul.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(lbl_judul)
        layout_utama.addWidget(header_frame)

        # ── Form Section ────────────────────────────────────────────────────
        container_form = QVBoxLayout()
        container_form.setContentsMargins(25, 20, 25, 10)
        container_form.setSpacing(15)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignLeft)
        form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        # Field: Kode Barang
        self.input_kode = QLineEdit()
        self.input_kode.setPlaceholderText("Contoh: BRG001")
        form.addRow("Kode Barang *", self.input_kode)

        # Field: Nama Barang
        self.input_nama = QLineEdit()
        self.input_nama.setPlaceholderText("Masukkan nama lengkap barang...")
        form.addRow("Nama Barang *", self.input_nama)

        # Field: Kategori
        self.combo_kategori = QComboBox()
        self.combo_kategori.addItems(KATEGORI_LIST)
        self.combo_kategori.setEditable(True)
        form.addRow("Kategori *", self.combo_kategori)

        # Field: Stok & Satuan (HBox)
        layout_stok = QHBoxLayout()
        self.spin_jumlah = QSpinBox()
        self.spin_jumlah.setRange(0, 999999)
        self.spin_jumlah.setMinimumHeight(32)
        
        self.combo_satuan = QComboBox()
        self.combo_satuan.addItems(SATUAN_LIST)
        self.combo_satuan.setEditable(True)
        self.combo_satuan.setFixedWidth(120)
        
        layout_stok.addWidget(self.spin_jumlah, 1)
        layout_stok.addWidget(self.combo_satuan)
        form.addRow("Stok & Satuan *", layout_stok)

        # Field: Harga Satuan
        self.spin_harga = QDoubleSpinBox()
        self.spin_harga.setRange(0, 999999999)
        self.spin_harga.setDecimals(0)
        self.spin_harga.setPrefix("Rp ")
        # PERBAIKAN: Menggunakan setGroupSeparatorShown sesuai saran error
        self.spin_harga.setGroupSeparatorShown(True) 
        self.spin_harga.setMinimumHeight(32)
        form.addRow("Harga Satuan *", self.spin_harga)

        # Field: Lokasi
        self.input_lokasi = QLineEdit()
        self.input_lokasi.setPlaceholderText("Contoh: Gudang A / Rak 1")
        form.addRow("Lokasi Simpan", self.input_lokasi)

        # Field: Tanggal
        self.date_masuk = QDateEdit()
        self.date_masuk.setDate(QDate.currentDate())
        self.date_masuk.setCalendarPopup(True)
        self.date_masuk.setDisplayFormat("dd MMMM yyyy")
        form.addRow("Tanggal Masuk", self.date_masuk)

        # Field: Keterangan
        self.input_keterangan = QTextEdit()
        self.input_keterangan.setPlaceholderText("Catatan tambahan...")
        self.input_keterangan.setMaximumHeight(70)
        form.addRow("Keterangan", self.input_keterangan)

        container_form.addLayout(form)

        # Label info
        lbl_wajib = QLabel("* Wajib diisi")
        lbl_wajib.setObjectName("labelWajib")
        container_form.addWidget(lbl_wajib)
        
        layout_utama.addLayout(container_form)

        # ── Button Section ──────────────────────────────────────────────────
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.button(QDialogButtonBox.Ok).setText("Simpan Barang")
        self.buttons.button(QDialogButtonBox.Cancel).setText("Batal")
        self.buttons.setContentsMargins(25, 10, 25, 25)
        
        self.buttons.accepted.connect(self._validasi_dan_terima)
        self.buttons.rejected.connect(self.reject)
        layout_utama.addWidget(self.buttons)

    def _isi_form(self, data: dict):
        """Mengisi kolom input dengan data yang ada (saat Edit)."""
        self.input_kode.setText(str(data.get("kode_barang", "")))
        self.input_nama.setText(str(data.get("nama_barang", "")))
        
        kat = data.get("kategori", "Lainnya")
        idx_kat = self.combo_kategori.findText(kat)
        if idx_kat >= 0: self.combo_kategori.setCurrentIndex(idx_kat)
        else: self.combo_kategori.setEditText(kat)

        self.spin_jumlah.setValue(int(data.get("jumlah", 0)))
        
        sat = data.get("satuan", "pcs")
        idx_sat = self.combo_satuan.findText(sat)
        if idx_sat >= 0: self.combo_satuan.setCurrentIndex(idx_sat)
        else: self.combo_satuan.setEditText(sat)

        self.spin_harga.setValue(float(data.get("harga", 0)))
        self.input_lokasi.setText(str(data.get("lokasi", "")))
        self.input_keterangan.setPlainText(str(data.get("keterangan", "")))

        tgl_str = data.get("tanggal_masuk", "")
        tgl = QDate.fromString(tgl_str, "yyyy-MM-dd")
        if tgl.isValid():
            self.date_masuk.setDate(tgl)

    def _validasi_dan_terima(self):
        """Validasi input sebelum dialog ditutup."""
        if not self.input_kode.text().strip():
            QMessageBox.warning(self, "Validasi Gagal", "Kode Barang harus diisi!")
            self.input_kode.setFocus()
            return
        if not self.input_nama.text().strip():
            QMessageBox.warning(self, "Validasi Gagal", "Nama Barang harus diisi!")
            self.input_nama.setFocus()
            return
        self.accept()

    def get_data(self) -> dict:
        """Mengembalikan data dari inputan user sebagai dictionary."""
        return {
            "kode_barang": self.input_kode.text().strip().upper(),
            "nama_barang": self.input_nama.text().strip(),
            "kategori": self.combo_kategori.currentText().strip(),
            "jumlah": self.spin_jumlah.value(),
            "satuan": self.combo_satuan.currentText().strip(),
            "harga": self.spin_harga.value(),
            "lokasi": self.input_lokasi.text().strip(),
            "keterangan": self.input_keterangan.toPlainText().strip(),
            "tanggal_masuk": self.date_masuk.date().toString("yyyy-MM-dd"),
        }