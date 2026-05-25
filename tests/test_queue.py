"""
test_queue.py — Unit Test untuk Priority Alert Queue
Sistem Monitoring Jaringan IoT
"""

import pytest
import sys
import os

# Penunjuk jalan ke folder src agar data_structures bisa di-import
sys.path.insert(0, os.path.abspath('src'))

from data_structures.queue import AlertPriorityQueue

# =====================================================================
# Kelas Dummy untuk Alert
# Kita buat tiruan objek Alert agar pengujian ini mandiri dan terisolasi
# =====================================================================
class MockAlert:
    def __init__(self, alert_id, tipe, deskripsi=""):
        self.alert_id = alert_id
        self.tipe = tipe  # 1=CRITICAL, 2=WARNING, 3=INFO
        self.deskripsi = deskripsi

# =====================================================================
# Setup Fixture
# =====================================================================
@pytest.fixture
def pq():
    """Membuat objek AlertPriorityQueue kosong sebelum setiap fungsi test."""
    return AlertPriorityQueue()

# =====================================================================
# Skenario Pengujian (Test Cases)
# =====================================================================

def test_enqueue_sorting_priority(pq):
    # Memasukkan data dengan urutan prioritas acak (tidak berurutan)
    pq.enqueue(MockAlert("ALERT_INFO", 3, "Suhu normal"))
    pq.enqueue(MockAlert("ALERT_CRITICAL", 1, "Kebakaran terdeteksi!"))
    pq.enqueue(MockAlert("ALERT_WARNING", 2, "Suhu agak hangat"))
    
    # Validasi: Karena urutan ASC (1 terkecil/tertinggi), ALERT_CRITICAL harus di depan!
    assert pq.is_empty() is False, "Queue tidak boleh kosong"
    assert pq.peek().alert_id == "ALERT_CRITICAL", "Alert dengan tipe=1 harus berada di paling depan (head)"
    
    # Eksekusi dequeue pertama (mengambil yang paling depan)
    first_out = pq.dequeue()
    assert first_out.alert_id == "ALERT_CRITICAL"
    
    # Validasi setelah yang pertama diambil: tipe=2 (WARNING) harus naik ke depan
    assert pq.peek().alert_id == "ALERT_WARNING", "Setelah CRITICAL diambil, WARNING harus maju ke depan"

def test_dequeue_on_empty_queue(pq):
    # Validasi: Mengambil data dari queue yang kosong tidak boleh error/crash, harus return None
    assert pq.dequeue() is None, "Queue kosong jika di-dequeue harus mengembalikan None"

def test_pending_alerts_list_order(pq):
    # Memasukkan dua alert
    pq.enqueue(MockAlert("ALERT_B", 2))
    pq.enqueue(MockAlert("ALERT_A", 1))
    
    # Eksekusi mengambil seluruh list alert yang mengantre
    daftar_antrean = pq.pending_alerts()
    
    # Validasi
    assert len(daftar_antrean) == 2, "Harus ada 2 alert di dalam list antrean"
    assert daftar_antrean[0].alert_id == "ALERT_A", "Di dalam list antrean, ALERT_A harus di indeks 0 karena tipe=1"

def test_queue_size_and_is_empty(pq):
    assert pq.is_empty() is True, "Awalnya queue harus kosong"
    assert len(pq) == 0, "Ukuran awal harus 0"
    
    pq.enqueue(MockAlert("ALERT_TEST", 1))
    
    assert pq.is_empty() is False, "Harus mendeteksi tidak kosong setelah di-enqueue"
    assert len(pq) == 1, "Ukuran harus bertambah menjadi 1"