"""
main.py
Entry point aplikasi InventoRIS - Sistem Manajemen Inventaris
Memuat stylesheet QSS eksternal dan menjalankan aplikasi
"""

import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

# Pastikan direktori project ada di path agar import modular berjalan
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow


def muat_stylesheet(app: QApplication) -> None:
    """Memuat file QSS eksternal dan menerapkannya ke seluruh aplikasi."""
    qss_path = os.path.join(os.path.dirname(__file__), "styles", "app.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"[PERINGATAN] File stylesheet tidak ditemukan: {qss_path}")


def main():
    # Aktifkan High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("InventoRIS")
    app.setOrganizationName("PV26 - Pemrograman Visual")

    # Muat stylesheet dari file eksternal (bukan inline)
    muat_stylesheet(app)

    # Tampilkan jendela utama
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
