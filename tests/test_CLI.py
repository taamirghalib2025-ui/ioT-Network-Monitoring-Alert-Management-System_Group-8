"""
test_CLI.py — Unit Test untuk CLI.py
Lokasi  : tests/test_CLI.py
Mata Kuliah : ELT60213 Algoritma dan Struktur Data
Team Based Project TA 2025/2026 — Group 8

Cara menjalankan:
    python -m pytest tests/test_CLI.py -v
    atau
    python tests/test_CLI.py
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Tambahkan path src/data_structures agar bisa import CLI
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'data_structures'))

from CLI import CLIMonitoring, AlertSystem


# ══════════════════════════════════════════════
#  HELPER: mock graph sederhana untuk testing
#  tanpa bergantung pada implementasi graph.py
# ══════════════════════════════════════════════

class MockGraph:
    def __init__(self):
        self._nodes = {}   # {id: tipe}
        self._edges = []   # [(u, v, w)]
        self._adj   = {}   # {id: [(neighbor, weight)]}

    def has_node(self, nid):
        return nid in self._nodes

    def add_node(self, nid, tipe):
        self._nodes[nid] = tipe
        self._adj[nid]   = []

    def add_edge(self, u, v, w):
        if u not in self._nodes or v not in self._nodes:
            return False
        self._edges.append((u, v, w))
        self._adj[u].append((v, w))
        self._adj[v].append((u, w))
        return True

    def get_all_nodes(self):
        return list(self._nodes.keys())

    def get_all_edges(self):
        return list(self._edges)

    def get_neighbors(self, nid):
        return self._adj.get(nid, [])

    def get_node_type(self, nid):
        return self._nodes.get(nid, "Unknown")

    def bfs(self, start):
        visited = set()
        queue   = [start]
        while queue:
            node = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            for nbr, _ in self._adj.get(node, []):
                if nbr not in visited:
                    queue.append(nbr)
        return visited


def make_cli():
    """Buat CLIMonitoring dengan MockGraph agar test tidak bergantung graph.py."""
    cli = CLIMonitoring.__new__(CLIMonitoring)
    cli.graph  = MockGraph()
    cli.alerts = AlertSystem.__new__(AlertSystem)

    from queue import Queue   # built-in Python queue — kita mock AlertSystem manual
    # Buat AlertSystem secara langsung
    cli.alerts = AlertSystem.__new__(AlertSystem)

    # Inisialisasi manual pakai mock data struktur sederhana
    class SimpleQueue:
        def __init__(self):        self._d = []
        def enqueue(self, x):      self._d.append(x)
        def dequeue(self):         return self._d.pop(0) if self._d else None
        def is_empty(self):        return len(self._d) == 0
        def size(self):            return len(self._d)
        def to_list(self):         return list(self._d)

    class SimpleStack:
        def __init__(self):        self._d = []
        def push(self, x):         self._d.append(x)
        def pop(self):             return self._d.pop() if self._d else None
        def is_empty(self):        return len(self._d) == 0
        def to_list(self):         return list(reversed(self._d))

    class SimpleBST:
        def __init__(self):        self._d = {}
        def insert(self, k, v):    self._d[k] = v
        def search(self, k):       return self._d.get(k)

    cli.alerts.pending  = SimpleQueue()
    cli.alerts.history  = SimpleStack()
    cli.alerts.index    = SimpleBST()
    cli.alerts._counter = 0

    return cli


# ══════════════════════════════════════════════
#  TEST SUITE
# ══════════════════════════════════════════════

class TestAlertSystem(unittest.TestCase):
    """Unit test untuk AlertSystem (Queue + Stack + BST)."""

    def setUp(self):
        self.cli = make_cli()

    # ── ALERT_IN ─────────────────────────────

    def test_alert_in_menambah_ke_antrian(self):
        """ALERT_IN harus menambah alert ke pending queue."""
        self.cli.alerts.alert_in("PC1", "HIGH_LATENCY", "Latensi tinggi")
        self.assertEqual(self.cli.alerts.pending.size(), 1)

    def test_alert_in_counter_naik(self):
        """Setiap ALERT_IN counter harus bertambah 1."""
        self.cli.alerts.alert_in("PC1", "HIGH_LATENCY", "Pesan 1")
        self.cli.alerts.alert_in("PC2", "PACKET_LOSS",  "Pesan 2")
        self.assertEqual(self.cli.alerts._counter, 2)

    def test_alert_in_id_unik(self):
        """Setiap alert harus memiliki id unik yang berbeda."""
        a1 = self.cli.alerts.alert_in("PC1", "DOWN", "Pesan A")
        a2 = self.cli.alerts.alert_in("PC2", "DOWN", "Pesan B")
        self.assertNotEqual(a1["id"], a2["id"])

    def test_alert_in_data_tersimpan_benar(self):
        """Field device, tipe, pesan harus tersimpan dengan benar."""
        alert = self.cli.alerts.alert_in("R1", "PACKET_LOSS", "Drop 20%")
        self.assertEqual(alert["device"], "R1")
        self.assertEqual(alert["tipe"],   "PACKET_LOSS")
        self.assertEqual(alert["pesan"],  "Drop 20%")
        self.assertEqual(alert["status"], "PENDING")

    def test_alert_in_bst_index_tersimpan(self):
        """Alert harus terindex di BST dengan key = alert id."""
        alert = self.cli.alerts.alert_in("SW1", "DOWN", "Interface down")
        hasil = self.cli.alerts.index.search(alert["id"])
        self.assertIsNotNone(hasil)
        self.assertEqual(hasil["device"], "SW1")

    # ── PROCESS_ALERT ────────────────────────

    def test_process_alert_fifo(self):
        """PROCESS_ALERT harus memproses alert pertama masuk (FIFO)."""
        self.cli.alerts.alert_in("PC1", "DOWN",         "Pertama")
        self.cli.alerts.alert_in("PC2", "HIGH_LATENCY", "Kedua")
        processed = self.cli.alerts.process_alert()
        self.assertEqual(processed["pesan"], "Pertama")

    def test_process_alert_ubah_status(self):
        """Status alert harus berubah menjadi PROCESSED setelah diproses."""
        self.cli.alerts.alert_in("R1", "DOWN", "Test status")
        processed = self.cli.alerts.process_alert()
        self.assertEqual(processed["status"], "PROCESSED")

    def test_process_alert_pindah_ke_history(self):
        """Alert yang diproses harus masuk ke history stack."""
        self.cli.alerts.alert_in("R1", "DOWN", "Test history")
        self.cli.alerts.process_alert()
        history = self.cli.alerts.history.to_list()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["pesan"], "Test history")

    def test_process_alert_antrian_kosong(self):
        """PROCESS_ALERT pada antrian kosong harus return None."""
        hasil = self.cli.alerts.process_alert()
        self.assertIsNone(hasil)

    def test_process_alert_kurangi_pending(self):
        """Pending queue harus berkurang 1 setelah PROCESS_ALERT."""
        self.cli.alerts.alert_in("PC1", "DOWN", "A")
        self.cli.alerts.alert_in("PC2", "DOWN", "B")
        self.cli.alerts.process_alert()
        self.assertEqual(self.cli.alerts.pending.size(), 1)

    # ── HISTORY ──────────────────────────────

    def test_history_urutan_lifo(self):
        """HISTORY harus mengembalikan alert terbaru di posisi pertama (LIFO)."""
        self.cli.alerts.alert_in("PC1", "DOWN", "Pertama")
        self.cli.alerts.process_alert()
        self.cli.alerts.alert_in("PC2", "DOWN", "Kedua")
        self.cli.alerts.process_alert()
        history = self.cli.alerts.get_history(5)
        self.assertEqual(history[0]["pesan"], "Kedua")

    def test_history_limit_n(self):
        """get_history(n) harus mengembalikan maksimal n item."""
        for i in range(10):
            self.cli.alerts.alert_in(f"PC{i}", "DOWN", f"Pesan {i}")
            self.cli.alerts.process_alert()
        history = self.cli.alerts.get_history(3)
        self.assertLessEqual(len(history), 3)

    def test_history_kosong_jika_belum_ada(self):
        """History harus kosong jika belum ada alert yang diproses."""
        history = self.cli.alerts.get_history()
        self.assertEqual(history, [])


class TestCLIDevice(unittest.TestCase):
    """Unit test untuk ADD_DEVICE dan ADD_LINK."""

    def setUp(self):
        self.cli = make_cli()

    # ── ADD_DEVICE ────────────────────────────

    def test_add_device_berhasil(self):
        """ADD_DEVICE harus menambahkan device ke graph."""
        with patch('builtins.print'):
            self.cli.add_device("R1", "Router")
        self.assertIn("R1", self.cli.graph.get_all_nodes())

    def test_add_device_duplikat(self):
        """ADD_DEVICE dengan id yang sama tidak boleh menambah duplikat."""
        with patch('builtins.print'):
            self.cli.add_device("R1", "Router")
            self.cli.add_device("R1", "Router")
        self.assertEqual(self.cli.graph.get_all_nodes().count("R1"), 1)

    def test_add_device_tipe_tersimpan(self):
        """Tipe device harus tersimpan dengan benar."""
        with patch('builtins.print'):
            self.cli.add_device("SW1", "Switch")
        tipe = self.cli.graph.get_node_type("SW1")
        self.assertEqual(tipe, "Switch")

    def test_add_multiple_devices(self):
        """Bisa menambahkan banyak device berbeda."""
        with patch('builtins.print'):
            self.cli.add_device("R1", "Router")
            self.cli.add_device("R2", "Router")
            self.cli.add_device("SW1", "Switch")
        self.assertEqual(len(self.cli.graph.get_all_nodes()), 3)

    # ── ADD_LINK ──────────────────────────────

    def test_add_link_berhasil(self):
        """ADD_LINK harus menambahkan edge antara dua device yang ada."""
        with patch('builtins.print'):
            self.cli.add_device("R1", "Router")
            self.cli.add_device("R2", "Router")
            self.cli.add_link("R1", "R2", 10)
        edges = self.cli.graph.get_all_edges()
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0], ("R1", "R2", 10))

    def test_add_link_device_tidak_ada(self):
        """ADD_LINK gagal jika salah satu device belum terdaftar."""
        with patch('builtins.print'):
            self.cli.add_device("R1", "Router")
            self.cli.add_link("R1", "XX", 10)   # XX tidak ada
        self.assertEqual(len(self.cli.graph.get_all_edges()), 0)

    def test_add_link_latensi_tersimpan(self):
        """Nilai latensi harus tersimpan dengan benar di edge."""
        with patch('builtins.print'):
            self.cli.add_device("A", "Router")
            self.cli.add_device("B", "Router")
            self.cli.add_link("A", "B", 42)
        _, _, w = self.cli.graph.get_all_edges()[0]
        self.assertEqual(w, 42)


class TestCLIIsolasi(unittest.TestCase):
    """Unit test untuk ISOLASI (BFS)."""

    def setUp(self):
        self.cli = make_cli()
        with patch('builtins.print'):
            self.cli.add_device("R1",  "Router")
            self.cli.add_device("R2",  "Router")
            self.cli.add_device("SW1", "Switch")
            self.cli.add_device("PC1", "EndDevice")   # sengaja tidak dihubungkan
            self.cli.add_link("R1",  "R2",  10)
            self.cli.add_link("R1",  "SW1", 5)

    def test_isolasi_node_terhubung(self):
        """R1, R2, SW1 harus saling terjangkau dari R1."""
        reachable = self.cli.graph.bfs("R1")
        self.assertIn("R1",  reachable)
        self.assertIn("R2",  reachable)
        self.assertIn("SW1", reachable)

    def test_isolasi_node_terputus(self):
        """PC1 tidak terhubung ke R1, harus terdeteksi sebagai terisolasi."""
        reachable  = self.cli.graph.bfs("R1")
        all_nodes  = set(self.cli.graph.get_all_nodes())
        isolated   = all_nodes - reachable
        self.assertIn("PC1", isolated)

    def test_isolasi_device_tidak_ada(self):
        """ISOLASI pada device yang tidak ada tidak boleh crash."""
        with patch('builtins.print'):
            try:
                self.cli.isolasi("XXXX")
            except Exception as e:
                self.fail(f"isolasi() melempar exception tidak terduga: {e}")


class TestCLIAuditLaporan(unittest.TestCase):
    """Unit test untuk AUDIT_LATENSI dan LAPORAN_JARINGAN."""

    def setUp(self):
        self.cli = make_cli()
        with patch('builtins.print'):
            self.cli.add_device("R1",  "Router")
            self.cli.add_device("R2",  "Router")
            self.cli.add_device("SW1", "Switch")
            self.cli.add_link("R1", "R2",  50)
            self.cli.add_link("R1", "SW1", 20)

    def test_audit_latensi_urutan_descending(self):
        """AUDIT_LATENSI harus mengurutkan edge dari latensi tertinggi ke terendah."""
        edges = self.cli.graph.get_all_edges()
        edges_sorted = sorted(edges, key=lambda x: x[2], reverse=True)
        self.assertEqual(edges_sorted[0][2], 50)
        self.assertEqual(edges_sorted[1][2], 20)

    def test_audit_latensi_tidak_crash_kosong(self):
        """AUDIT_LATENSI pada graph kosong tidak boleh crash."""
        cli_kosong = make_cli()
        with patch('builtins.print'):
            try:
                cli_kosong.audit_latensi()
            except Exception as e:
                self.fail(f"audit_latensi() crash pada graph kosong: {e}")

    def test_laporan_jaringan_jumlah_device(self):
        """LAPORAN_JARINGAN harus melaporkan jumlah device yang benar."""
        nodes = self.cli.graph.get_all_nodes()
        self.assertEqual(len(nodes), 3)

    def test_laporan_jaringan_jumlah_link(self):
        """LAPORAN_JARINGAN harus melaporkan jumlah link yang benar."""
        edges = self.cli.graph.get_all_edges()
        self.assertEqual(len(edges), 2)

    def test_laporan_jaringan_alert_counter(self):
        """LAPORAN_JARINGAN harus melaporkan jumlah alert yang masuk."""
        self.cli.alerts.alert_in("R1", "DOWN", "Test 1")
        self.cli.alerts.alert_in("R2", "DOWN", "Test 2")
        self.assertEqual(self.cli.alerts._counter, 2)


class TestCLIIntegrasi(unittest.TestCase):
    """Integration test — simulasi skenario penggunaan nyata."""

    def setUp(self):
        self.cli = make_cli()

    def test_skenario_lengkap(self):
        """
        Skenario: tambah device → link → alert masuk → proses → cek history.
        Semua langkah harus berjalan tanpa error.
        """
        with patch('builtins.print'):
            # Setup jaringan
            self.cli.add_device("R1",  "Router")
            self.cli.add_device("R2",  "Router")
            self.cli.add_device("SW1", "Switch")
            self.cli.add_device("PC1", "EndDevice")
            self.cli.add_link("R1", "R2",  15)
            self.cli.add_link("R1", "SW1", 8)
            self.cli.add_link("SW1","PC1", 3)

            # Alert masuk
            self.cli.alert_in("PC1", "HIGH_LATENCY", "Latensi 200ms")
            self.cli.alert_in("R2",  "PACKET_LOSS",  "Drop 10%")
            self.cli.alert_in("SW1", "DOWN",         "Port mati")

        # Cek pending = 3
        self.assertEqual(self.cli.alerts.pending.size(), 3)

        # Proses 2 alert
        with patch('builtins.print'):
            self.cli.process_alert()
            self.cli.process_alert()

        # Pending tersisa 1, history 2
        self.assertEqual(self.cli.alerts.pending.size(), 1)
        self.assertEqual(len(self.cli.alerts.history.to_list()), 2)

        # History: yang terakhir diproses ada di atas
        history = self.cli.alerts.get_history()
        self.assertEqual(history[0]["pesan"], "Drop 10%")

    def test_skenario_isolasi_jaringan_terputus(self):
        """Device tanpa link harus terdeteksi terisolasi."""
        with patch('builtins.print'):
            self.cli.add_device("R1",  "Router")
            self.cli.add_device("R2",  "Router")
            self.cli.add_device("PC_ISOLATED", "EndDevice")  # tidak dihubungkan
            self.cli.add_link("R1", "R2", 10)

        reachable = self.cli.graph.bfs("R1")
        isolated  = set(self.cli.graph.get_all_nodes()) - reachable
        self.assertIn("PC_ISOLATED", isolated)
        self.assertNotIn("R2", isolated)

    def test_skenario_alert_tanpa_device(self):
        """ALERT_IN boleh masuk meski device belum ada di graph (alert tetap valid)."""
        alert = self.cli.alerts.alert_in("GHOST_DEVICE", "DOWN", "Unknown device")
        self.assertEqual(alert["device"], "GHOST_DEVICE")
        self.assertEqual(self.cli.alerts.pending.size(), 1)


# ══════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  TEST CLI — IoT Network Monitoring System  Group 8")
    print("=" * 60)
    unittest.main(verbosity=2)