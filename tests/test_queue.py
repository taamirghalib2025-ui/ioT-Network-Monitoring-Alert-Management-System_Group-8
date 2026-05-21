"""
test_queue.py — Unit Test untuk AlertPriorityQueue
Lokasi  : tests/test_queue.py
Mata Kuliah : ELT60213 Algoritma dan Struktur Data
Team Based Project TA 2025/2026 — Group 8

Cara menjalankan:
    python -m pytest tests/test_queue.py -v
    atau
    python tests/test_queue.py
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'data_structures'))

from queue import AlertPriorityQueue


# ══════════════════════════════════════════════
#  HELPER: Mock Alert Object
#  Simulasi objek alert dengan atribut .tipe
#  CRITICAL=1, WARNING=2, INFO=3
# ══════════════════════════════════════════════

class Alert:
    CRITICAL = 1
    WARNING  = 2
    INFO     = 3

    def __init__(self, tipe: int, pesan: str, device: str = "DEV"):
        self.tipe   = tipe
        self.pesan  = pesan
        self.device = device

    def __repr__(self):
        label = {1: "CRITICAL", 2: "WARNING", 3: "INFO"}.get(self.tipe, "?")
        return f"Alert({label}, '{self.pesan}')"


def make_alert(tipe, pesan="test", device="DEV"):
    return Alert(tipe, pesan, device)


# ══════════════════════════════════════════════
#  TEST INISIALISASI
# ══════════════════════════════════════════════

class TestInisialisasi(unittest.TestCase):

    def test_queue_kosong_saat_dibuat(self):
        q = AlertPriorityQueue()
        self.assertTrue(q.is_empty())

    def test_size_nol_saat_dibuat(self):
        q = AlertPriorityQueue()
        self.assertEqual(len(q), 0)

    def test_head_none_saat_dibuat(self):
        q = AlertPriorityQueue()
        self.assertIsNone(q.head)

    def test_peek_kosong_return_none(self):
        q = AlertPriorityQueue()
        self.assertIsNone(q.peek())

    def test_dequeue_kosong_return_none(self):
        q = AlertPriorityQueue()
        self.assertIsNone(q.dequeue())

    def test_pending_alerts_kosong_return_list_kosong(self):
        q = AlertPriorityQueue()
        self.assertEqual(q.pending_alerts(), [])


# ══════════════════════════════════════════════
#  TEST ENQUEUE
# ══════════════════════════════════════════════

class TestEnqueue(unittest.TestCase):

    def setUp(self):
        self.q = AlertPriorityQueue()

    def test_enqueue_satu_elemen_tidak_kosong(self):
        self.q.enqueue(make_alert(Alert.INFO, "Test"))
        self.assertFalse(self.q.is_empty())

    def test_enqueue_size_bertambah(self):
        self.q.enqueue(make_alert(Alert.INFO))
        self.q.enqueue(make_alert(Alert.WARNING))
        self.assertEqual(len(self.q), 2)

    def test_enqueue_critical_ke_depan_jika_masuk_terakhir(self):
        """CRITICAL yang masuk belakangan harus tetap di depan."""
        self.q.enqueue(make_alert(Alert.INFO,     "info"))
        self.q.enqueue(make_alert(Alert.WARNING,  "warning"))
        self.q.enqueue(make_alert(Alert.CRITICAL, "critical"))
        self.assertEqual(self.q.head.data.tipe, Alert.CRITICAL)

    def test_enqueue_urutan_prioritas_ascending(self):
        """
        Setelah enqueue campur, antrian harus terurut ASC by tipe:
        CRITICAL(1) → WARNING(2) → INFO(3)
        """
        self.q.enqueue(make_alert(Alert.INFO,     "A"))
        self.q.enqueue(make_alert(Alert.CRITICAL, "B"))
        self.q.enqueue(make_alert(Alert.WARNING,  "C"))
        tipe_list = [a.tipe for a in self.q.pending_alerts()]
        self.assertEqual(tipe_list, [1, 2, 3])

    def test_enqueue_dua_critical_keduanya_masuk(self):
        """Dua alert CRITICAL boleh masuk, keduanya tersimpan."""
        self.q.enqueue(make_alert(Alert.CRITICAL, "C1"))
        self.q.enqueue(make_alert(Alert.CRITICAL, "C2"))
        self.assertEqual(len(self.q), 2)

    def test_enqueue_urutan_stabil_tipe_sama(self):
        """
        Alert dengan tipe sama: yang pertama masuk ada di depan
        (enqueue memakai <=, jadi yang baru masuk setelah yang lama).
        """
        self.q.enqueue(make_alert(Alert.WARNING, "pertama"))
        self.q.enqueue(make_alert(Alert.WARNING, "kedua"))
        self.assertEqual(self.q.head.data.pesan, "pertama")

    def test_enqueue_info_di_belakang_critical(self):
        self.q.enqueue(make_alert(Alert.CRITICAL, "C"))
        self.q.enqueue(make_alert(Alert.INFO,     "I"))
        alerts = self.q.pending_alerts()
        self.assertEqual(alerts[0].tipe, Alert.CRITICAL)
        self.assertEqual(alerts[1].tipe, Alert.INFO)

    def test_enqueue_banyak_alert_terurut(self):
        """10 alert campur harus terurut ASC setelah semua masuk."""
        import random
        tipes = [1, 3, 2, 1, 3, 2, 1, 2, 3, 1]
        for t in tipes:
            self.q.enqueue(make_alert(t, f"p{t}"))
        result = [a.tipe for a in self.q.pending_alerts()]
        self.assertEqual(result, sorted(tipes))


# ══════════════════════════════════════════════
#  TEST DEQUEUE
# ══════════════════════════════════════════════

class TestDequeue(unittest.TestCase):

    def setUp(self):
        self.q = AlertPriorityQueue()
        self.q.enqueue(make_alert(Alert.INFO,     "info"))
        self.q.enqueue(make_alert(Alert.CRITICAL, "critical"))
        self.q.enqueue(make_alert(Alert.WARNING,  "warning"))

    def test_dequeue_kembalikan_prioritas_tertinggi(self):
        """Dequeue pertama harus CRITICAL (tipe=1)."""
        alert = self.q.dequeue()
        self.assertEqual(alert.tipe, Alert.CRITICAL)

    def test_dequeue_urutan_benar(self):
        """Urutan dequeue harus: CRITICAL → WARNING → INFO."""
        order = [self.q.dequeue().tipe for _ in range(3)]
        self.assertEqual(order, [Alert.CRITICAL, Alert.WARNING, Alert.INFO])

    def test_dequeue_size_berkurang(self):
        self.q.dequeue()
        self.assertEqual(len(self.q), 2)

    def test_dequeue_sampai_kosong(self):
        self.q.dequeue()
        self.q.dequeue()
        self.q.dequeue()
        self.assertTrue(self.q.is_empty())

    def test_dequeue_pada_queue_kosong_return_none(self):
        q_kosong = AlertPriorityQueue()
        self.assertIsNone(q_kosong.dequeue())

    def test_dequeue_satu_elemen_reset_head(self):
        q = AlertPriorityQueue()
        q.enqueue(make_alert(Alert.CRITICAL, "satu"))
        q.dequeue()
        self.assertIsNone(q.head)
        self.assertTrue(q.is_empty())

    def test_dequeue_tidak_ubah_sisa_antrian(self):
        """Setelah dequeue CRITICAL, WARNING harus jadi head baru."""
        self.q.dequeue()
        self.assertEqual(self.q.head.data.tipe, Alert.WARNING)

    def test_dequeue_kembalikan_objek_alert_benar(self):
        alert = self.q.dequeue()
        self.assertEqual(alert.pesan, "critical")


# ══════════════════════════════════════════════
#  TEST PEEK
# ══════════════════════════════════════════════

class TestPeek(unittest.TestCase):

    def setUp(self):
        self.q = AlertPriorityQueue()

    def test_peek_tidak_menghapus_elemen(self):
        self.q.enqueue(make_alert(Alert.CRITICAL, "C"))
        self.q.peek()
        self.assertEqual(len(self.q), 1)

    def test_peek_kembalikan_prioritas_tertinggi(self):
        self.q.enqueue(make_alert(Alert.WARNING,  "W"))
        self.q.enqueue(make_alert(Alert.CRITICAL, "C"))
        self.assertEqual(self.q.peek().tipe, Alert.CRITICAL)

    def test_peek_sama_dengan_dequeue_pertama(self):
        self.q.enqueue(make_alert(Alert.INFO,     "I"))
        self.q.enqueue(make_alert(Alert.CRITICAL, "C"))
        peeked   = self.q.peek()
        dequeued = self.q.dequeue()
        self.assertEqual(peeked.pesan, dequeued.pesan)

    def test_peek_queue_kosong_return_none(self):
        self.assertIsNone(self.q.peek())

    def test_peek_konsisten_setelah_enqueue_baru(self):
        """Setelah enqueue CRITICAL baru, peek harus update ke CRITICAL."""
        self.q.enqueue(make_alert(Alert.INFO, "I"))
        self.assertEqual(self.q.peek().tipe, Alert.INFO)
        self.q.enqueue(make_alert(Alert.CRITICAL, "C"))
        self.assertEqual(self.q.peek().tipe, Alert.CRITICAL)


# ══════════════════════════════════════════════
#  TEST PENDING_ALERTS
# ══════════════════════════════════════════════

class TestPendingAlerts(unittest.TestCase):

    def setUp(self):
        self.q = AlertPriorityQueue()

    def test_pending_alerts_return_list(self):
        self.q.enqueue(make_alert(Alert.INFO, "I"))
        self.assertIsInstance(self.q.pending_alerts(), list)

    def test_pending_alerts_panjang_benar(self):
        self.q.enqueue(make_alert(Alert.INFO,    "I"))
        self.q.enqueue(make_alert(Alert.WARNING, "W"))
        self.assertEqual(len(self.q.pending_alerts()), 2)

    def test_pending_alerts_tidak_menghapus_elemen(self):
        self.q.enqueue(make_alert(Alert.CRITICAL, "C"))
        self.q.pending_alerts()
        self.assertEqual(len(self.q), 1)

    def test_pending_alerts_urutan_prioritas(self):
        self.q.enqueue(make_alert(Alert.INFO,     "I"))
        self.q.enqueue(make_alert(Alert.CRITICAL, "C"))
        self.q.enqueue(make_alert(Alert.WARNING,  "W"))
        tipes = [a.tipe for a in self.q.pending_alerts()]
        self.assertEqual(tipes, [1, 2, 3])

    def test_pending_alerts_kosong_return_list_kosong(self):
        self.assertEqual(self.q.pending_alerts(), [])

    def test_pending_alerts_berisi_objek_asli(self):
        alert = make_alert(Alert.CRITICAL, "unik")
        self.q.enqueue(alert)
        self.assertIs(self.q.pending_alerts()[0], alert)


# ══════════════════════════════════════════════
#  TEST IS_EMPTY & LEN
# ══════════════════════════════════════════════

class TestIsEmptyDanLen(unittest.TestCase):

    def test_is_empty_true_saat_kosong(self):
        self.assertTrue(AlertPriorityQueue().is_empty())

    def test_is_empty_false_setelah_enqueue(self):
        q = AlertPriorityQueue()
        q.enqueue(make_alert(Alert.INFO))
        self.assertFalse(q.is_empty())

    def test_is_empty_true_setelah_semua_dequeue(self):
        q = AlertPriorityQueue()
        q.enqueue(make_alert(Alert.INFO))
        q.dequeue()
        self.assertTrue(q.is_empty())

    def test_len_sesuai_jumlah_enqueue(self):
        q = AlertPriorityQueue()
        for i in range(5):
            q.enqueue(make_alert(Alert.INFO, f"p{i}"))
        self.assertEqual(len(q), 5)

    def test_len_berkurang_setelah_dequeue(self):
        q = AlertPriorityQueue()
        q.enqueue(make_alert(Alert.CRITICAL))
        q.enqueue(make_alert(Alert.WARNING))
        q.dequeue()
        self.assertEqual(len(q), 1)


# ══════════════════════════════════════════════
#  TEST INTEGRASI — Skenario IoT
# ══════════════════════════════════════════════

class TestIntegrasi(unittest.TestCase):

    def test_skenario_monitoring_jaringan(self):
        """
        Skenario: 5 alert masuk campur → semua diproses
        sesuai urutan prioritas CRITICAL→WARNING→INFO.
        """
        q = AlertPriorityQueue()
        q.enqueue(make_alert(Alert.INFO,     "Suhu normal",       "SENSOR_01"))
        q.enqueue(make_alert(Alert.CRITICAL, "Link putus",        "ROUTER_01"))
        q.enqueue(make_alert(Alert.WARNING,  "Latensi tinggi",    "SWITCH_01"))
        q.enqueue(make_alert(Alert.CRITICAL, "Power failure",     "SERVER_01"))
        q.enqueue(make_alert(Alert.WARNING,  "Packet loss 10%",   "ROUTER_02"))

        urutan = []
        while not q.is_empty():
            urutan.append(q.dequeue().tipe)

        # Harus terurut ASC: semua CRITICAL duluan, lalu WARNING, lalu INFO
        self.assertEqual(urutan, sorted(urutan))
        self.assertEqual(urutan.count(Alert.CRITICAL), 2)
        self.assertEqual(urutan.count(Alert.WARNING),  2)
        self.assertEqual(urutan.count(Alert.INFO),     1)

    def test_skenario_enqueue_dequeue_bergantian(self):
        """
        Enqueue dan dequeue bergantian harus tetap mempertahankan
        properti priority queue.
        """
        q = AlertPriorityQueue()
        q.enqueue(make_alert(Alert.WARNING,  "W1"))
        q.enqueue(make_alert(Alert.INFO,     "I1"))

        # Dequeue pertama: WARNING (tipe=2 < INFO tipe=3)
        a1 = q.dequeue()
        self.assertEqual(a1.tipe, Alert.WARNING)

        # Masukkan CRITICAL
        q.enqueue(make_alert(Alert.CRITICAL, "C1"))

        # Dequeue berikut: CRITICAL (lebih tinggi dari INFO)
        a2 = q.dequeue()
        self.assertEqual(a2.tipe, Alert.CRITICAL)

        # Sisa: INFO
        a3 = q.dequeue()
        self.assertEqual(a3.tipe, Alert.INFO)
        self.assertTrue(q.is_empty())

    def test_skenario_semua_critical(self):
        """Semua alert CRITICAL → urutan masuk = urutan keluar (FIFO dalam tipe sama)."""
        q = AlertPriorityQueue()
        pesans = ["C1", "C2", "C3"]
        for p in pesans:
            q.enqueue(make_alert(Alert.CRITICAL, p))

        hasil = [q.dequeue().pesan for _ in range(3)]
        self.assertEqual(hasil, pesans)

    def test_skenario_queue_besar(self):
        """50 alert campur → semua keluar terurut ASC."""
        q = AlertPriorityQueue()
        tipes_input = [2, 1, 3, 1, 2, 3, 1, 2, 3, 2] * 5  # 50 alert
        for t in tipes_input:
            q.enqueue(make_alert(t))

        hasil = []
        while not q.is_empty():
            hasil.append(q.dequeue().tipe)

        self.assertEqual(hasil, sorted(tipes_input))
        self.assertEqual(len(hasil), 50)


# ══════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  TEST QUEUE — IoT Network Monitoring System  Group 8")
    print("=" * 60)
    unittest.main(verbosity=2) 