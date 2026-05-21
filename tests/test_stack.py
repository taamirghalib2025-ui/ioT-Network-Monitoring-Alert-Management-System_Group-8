# ============================================================
# test_stack.py
# Unit Test: AlertStack & Stack
# Topik 4: IoT Network Monitoring & Alert Management System
# ELT60213 Algoritma dan Struktur Data - TA 2025/2026
# ============================================================

import unittest
import time
from stack import Alert, AlertStack, Stack


def buat_alert(alert_id: int, tipe: int = 1, device_id: str = "SENSOR_0") -> Alert:
    """Helper: buat Alert dummy untuk keperluan test."""
    tipe_label = {1: "CRITICAL", 2: "WARNING", 3: "INFO"}
    return Alert(
        alert_id=alert_id,
        device_id=device_id,
        tipe=tipe,
        pesan=f"Pesan {tipe_label.get(tipe, 'UNKNOWN')} #{alert_id}",
        timestamp=time.time(),
    )


# ─────────────────────────────────────────────────────────────
# Test Suite 1: AlertStack — Operasi Dasar
# ─────────────────────────────────────────────────────────────
class TestAlertStackDasar(unittest.TestCase):
    """Menguji operasi push, pop, peek, is_empty, is_full, dan __len__."""

    def setUp(self):
        self.stk = AlertStack(kapasitas=5)

    # ── Push & ukuran ─────────────────────────────────────────
    def test_push_menambah_ukuran(self):
        """Setiap push harus menambah _size sebesar 1."""
        for i in range(1, 4):
            self.stk.push(buat_alert(i))
            self.assertEqual(len(self.stk), i)

    def test_push_top_adalah_alert_terakhir(self):
        """Alert yang terakhir di-push harus berada di puncak (LIFO)."""
        for i in range(1, 4):
            self.stk.push(buat_alert(i))
        self.assertEqual(self.stk.peek().alert_id, 3)

    # ── Pop ────────────────────────────────────────────────────
    def test_pop_mengembalikan_alert_teratas(self):
        """pop() harus mengembalikan alert teratas (LIFO)."""
        self.stk.push(buat_alert(10))
        self.stk.push(buat_alert(20))
        hasil = self.stk.pop()
        self.assertEqual(hasil.alert_id, 20)

    def test_pop_mengurangi_ukuran(self):
        """pop() harus mengurangi _size sebesar 1."""
        self.stk.push(buat_alert(1))
        self.stk.push(buat_alert(2))
        self.stk.pop()
        self.assertEqual(len(self.stk), 1)

    def test_pop_urutan_lifo(self):
        """Urutan pop harus kebalikan urutan push (LIFO)."""
        ids_push = [1, 2, 3, 4, 5]
        for i in ids_push:
            self.stk.push(buat_alert(i))
        ids_pop = [self.stk.pop().alert_id for _ in range(5)]
        self.assertEqual(ids_pop, list(reversed(ids_push)))

    def test_pop_stack_kosong_mengembalikan_none(self):
        """pop() pada stack kosong harus mengembalikan None."""
        self.assertIsNone(self.stk.pop())

    # ── Peek ───────────────────────────────────────────────────
    def test_peek_tidak_mengubah_ukuran(self):
        """peek() tidak boleh mengubah ukuran stack."""
        self.stk.push(buat_alert(1))
        self.stk.push(buat_alert(2))
        _ = self.stk.peek()
        self.assertEqual(len(self.stk), 2)

    def test_peek_mengembalikan_alert_teratas(self):
        """peek() harus mengembalikan alert paling atas tanpa menghapus."""
        self.stk.push(buat_alert(7))
        self.stk.push(buat_alert(9))
        self.assertEqual(self.stk.peek().alert_id, 9)
        self.assertEqual(len(self.stk), 2)  # ukuran tetap

    def test_peek_stack_kosong_mengembalikan_none(self):
        """peek() pada stack kosong harus mengembalikan None."""
        self.assertIsNone(self.stk.peek())

    # ── is_empty / is_full ────────────────────────────────────
    def test_is_empty_saat_baru_dibuat(self):
        self.assertTrue(self.stk.is_empty())

    def test_is_empty_setelah_push(self):
        self.stk.push(buat_alert(1))
        self.assertFalse(self.stk.is_empty())

    def test_is_empty_setelah_pop_habis(self):
        self.stk.push(buat_alert(1))
        self.stk.pop()
        self.assertTrue(self.stk.is_empty())

    def test_is_full_saat_kapasitas_tercapai(self):
        for i in range(1, 6):  # kapasitas = 5
            self.stk.push(buat_alert(i))
        self.assertTrue(self.stk.is_full())

    def test_is_full_false_sebelum_kapasitas(self):
        self.stk.push(buat_alert(1))
        self.assertFalse(self.stk.is_full())

    # ── __len__ ───────────────────────────────────────────────
    def test_len_kosong(self):
        self.assertEqual(len(self.stk), 0)

    def test_len_setelah_beberapa_push(self):
        for i in range(3):
            self.stk.push(buat_alert(i))
        self.assertEqual(len(self.stk), 3)


# ─────────────────────────────────────────────────────────────
# Test Suite 2: AlertStack — Auto-hapus Bottom (Overflow)
# ─────────────────────────────────────────────────────────────
class TestAlertStackOverflow(unittest.TestCase):
    """Menguji perilaku saat stack melebihi kapasitas (hapus bottom)."""

    def test_ukuran_tidak_melebihi_kapasitas(self):
        """Ukuran tidak boleh pernah melebihi kapasitas."""
        stk = AlertStack(kapasitas=3)
        for i in range(1, 10):
            stk.push(buat_alert(i))
            self.assertLessEqual(len(stk), 3)

    def test_alert_terlama_terhapus_saat_penuh(self):
        """Alert pertama (terlama) harus hilang setelah overflow."""
        stk = AlertStack(kapasitas=3)
        for i in range(1, 5):   # push 4 alert ke kapasitas 3
            stk.push(buat_alert(i))
        ids = [a.alert_id for a in stk.to_list()]
        self.assertNotIn(1, ids,
            "Alert#1 (terlama) seharusnya sudah terhapus")

    def test_alert_terbaru_tetap_ada_setelah_overflow(self):
        """Alert terbaru harus selalu ada di puncak setelah overflow."""
        stk = AlertStack(kapasitas=3)
        for i in range(1, 7):
            stk.push(buat_alert(i))
        self.assertEqual(stk.peek().alert_id, 6)

    def test_isi_stack_setelah_overflow_berurut(self):
        """Setelah overflow, isi stack harus berupa 3 alert terbaru."""
        stk = AlertStack(kapasitas=3)
        for i in range(1, 7):   # push alert 1–6
            stk.push(buat_alert(i))
        ids = [a.alert_id for a in stk.to_list()]
        # top→bottom: 6, 5, 4
        self.assertEqual(ids, [6, 5, 4])

    def test_overflow_kapasitas_satu(self):
        """Kapasitas 1: setiap push baru menggantikan alert sebelumnya."""
        stk = AlertStack(kapasitas=1)
        stk.push(buat_alert(100))
        stk.push(buat_alert(200))
        self.assertEqual(len(stk), 1)
        self.assertEqual(stk.peek().alert_id, 200)

    def test_overflow_banyak_push(self):
        """50 push ke kapasitas 5 → hanya 5 alert terbaru yang tersisa."""
        stk = AlertStack(kapasitas=5)
        for i in range(1, 51):
            stk.push(buat_alert(i))
        self.assertEqual(len(stk), 5)
        ids = [a.alert_id for a in stk.to_list()]
        self.assertEqual(ids, [50, 49, 48, 47, 46])


# ─────────────────────────────────────────────────────────────
# Test Suite 3: AlertStack — to_list & clear
# ─────────────────────────────────────────────────────────────
class TestAlertStackToListClear(unittest.TestCase):
    """Menguji to_list() dan clear()."""

    def setUp(self):
        self.stk = AlertStack(kapasitas=5)
        for i in range(1, 5):
            self.stk.push(buat_alert(i))

    def test_to_list_urutan_top_ke_bottom(self):
        """to_list() harus mengembalikan alert dari top ke bottom."""
        ids = [a.alert_id for a in self.stk.to_list()]
        self.assertEqual(ids, [4, 3, 2, 1])

    def test_to_list_panjang_sama_dengan_size(self):
        """Panjang list hasil to_list() harus sama dengan len(stk)."""
        self.assertEqual(len(self.stk.to_list()), len(self.stk))

    def test_to_list_stack_kosong(self):
        """to_list() pada stack kosong harus mengembalikan list kosong."""
        empty = AlertStack()
        self.assertEqual(empty.to_list(), [])

    def test_to_list_tidak_mengubah_stack(self):
        """to_list() tidak boleh mengubah isi atau ukuran stack."""
        size_before = len(self.stk)
        top_before = self.stk.peek().alert_id
        self.stk.to_list()
        self.assertEqual(len(self.stk), size_before)
        self.assertEqual(self.stk.peek().alert_id, top_before)

    def test_clear_mengosongkan_stack(self):
        """clear() harus membuat stack kosong dan size = 0."""
        self.stk.clear()
        self.assertTrue(self.stk.is_empty())
        self.assertEqual(len(self.stk), 0)

    def test_clear_lalu_push_bisa_berjalan(self):
        """Setelah clear(), stack harus bisa menerima push baru."""
        self.stk.clear()
        self.stk.push(buat_alert(99))
        self.assertEqual(len(self.stk), 1)
        self.assertEqual(self.stk.peek().alert_id, 99)


# ─────────────────────────────────────────────────────────────
# Test Suite 4: AlertStack — Tipe Alert & Data Integrity
# ─────────────────────────────────────────────────────────────
class TestAlertStackDataIntegrity(unittest.TestCase):
    """Memastikan data Alert tersimpan dan terbaca dengan benar."""

    def test_data_alert_tidak_berubah_setelah_push_pop(self):
        """Semua atribut Alert harus identik setelah push → pop."""
        stk = AlertStack()
        original = Alert(
            alert_id=42,
            device_id="GATEWAY_7",
            tipe=2,
            pesan="Tegangan tidak stabil",
            timestamp=1_700_000_000.0,
        )
        stk.push(original)
        hasil = stk.pop()
        self.assertEqual(hasil.alert_id, 42)
        self.assertEqual(hasil.device_id, "GATEWAY_7")
        self.assertEqual(hasil.tipe, 2)
        self.assertEqual(hasil.pesan, "Tegangan tidak stabil")
        self.assertAlmostEqual(hasil.timestamp, 1_700_000_000.0)

    def test_push_tipe_critical(self):
        stk = AlertStack()
        stk.push(buat_alert(1, tipe=1))
        self.assertEqual(stk.peek().tipe, 1)

    def test_push_tipe_warning(self):
        stk = AlertStack()
        stk.push(buat_alert(2, tipe=2))
        self.assertEqual(stk.peek().tipe, 2)

    def test_push_tipe_info(self):
        stk = AlertStack()
        stk.push(buat_alert(3, tipe=3))
        self.assertEqual(stk.peek().tipe, 3)

    def test_beberapa_device_independen(self):
        """Stack berbeda untuk device berbeda tidak saling mempengaruhi."""
        stk_a = AlertStack(kapasitas=5)
        stk_b = AlertStack(kapasitas=5)
        stk_a.push(buat_alert(1, device_id="DEV_A"))
        stk_b.push(buat_alert(2, device_id="DEV_B"))
        self.assertEqual(stk_a.peek().device_id, "DEV_A")
        self.assertEqual(stk_b.peek().device_id, "DEV_B")
        self.assertEqual(len(stk_a), 1)
        self.assertEqual(len(stk_b), 1)


# ─────────────────────────────────────────────────────────────
# Test Suite 5: Stack Umum (untuk DFS)
# ─────────────────────────────────────────────────────────────
class TestStackUmum(unittest.TestCase):
    """Menguji Stack serbaguna yang dipakai untuk DFS traversal."""

    def setUp(self):
        self.s = Stack()

    def test_push_dan_len(self):
        self.s.push("A")
        self.s.push("B")
        self.assertEqual(len(self.s), 2)

    def test_pop_urutan_lifo(self):
        nodes = ["GATEWAY_0", "SERVER_1", "SENSOR_5", "SENSOR_12"]
        for n in nodes:
            self.s.push(n)
        popped = [self.s.pop() for _ in range(4)]
        self.assertEqual(popped, list(reversed(nodes)))

    def test_pop_kosong_mengembalikan_none(self):
        self.assertIsNone(self.s.pop())

    def test_peek_tidak_menghapus(self):
        self.s.push("X")
        self.s.push("Y")
        self.assertEqual(self.s.peek(), "Y")
        self.assertEqual(len(self.s), 2)

    def test_peek_kosong_mengembalikan_none(self):
        self.assertIsNone(self.s.peek())

    def test_is_empty_awal(self):
        self.assertTrue(self.s.is_empty())

    def test_is_empty_setelah_push(self):
        self.s.push(1)
        self.assertFalse(self.s.is_empty())

    def test_push_berbagai_tipe_data(self):
        """Stack umum harus bisa menyimpan berbagai tipe data."""
        self.s.push(42)
        self.s.push("string")
        self.s.push([1, 2, 3])
        self.s.push({"key": "val"})
        self.assertEqual(len(self.s), 4)
        self.assertEqual(self.s.pop(), {"key": "val"})

    def test_simulasi_dfs_traversal(self):
        """Simulasi DFS: push tetangga, pop untuk kunjungi node."""
        visited = []
        self.s.push("A")
        # A → B, C | B → D
        graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": [],
            "D": [],
        }
        visited_set = set()
        while not self.s.is_empty():
            node = self.s.pop()
            if node in visited_set:
                continue
            visited_set.add(node)
            visited.append(node)
            for neighbor in reversed(graph.get(node, [])):
                self.s.push(neighbor)

        # Semua node harus dikunjungi
        self.assertCountEqual(visited, ["A", "B", "C", "D"])
        # Tidak ada duplikasi
        self.assertEqual(len(visited), len(set(visited)))


# ─────────────────────────────────────────────────────────────
# Test Suite 6: Edge Case & Batas
# ─────────────────────────────────────────────────────────────
class TestEdgeCase(unittest.TestCase):
    """Kasus batas dan skenario tidak biasa."""

    def test_alert_stack_kapasitas_default_20(self):
        stk = AlertStack()
        self.assertEqual(stk.kapasitas, 20)

    def test_push_tepat_kapasitas_tidak_hapus(self):
        """Push sejumlah kapasitas (bukan lebih) → tidak ada yang terhapus."""
        stk = AlertStack(kapasitas=4)
        for i in range(1, 5):
            stk.push(buat_alert(i))
        ids = [a.alert_id for a in stk.to_list()]
        self.assertEqual(sorted(ids), [1, 2, 3, 4])

    def test_push_tepat_satu_lebih_kapasitas(self):
        """Push kapasitas + 1 → alert pertama hilang."""
        stk = AlertStack(kapasitas=4)
        for i in range(1, 6):
            stk.push(buat_alert(i))
        ids = [a.alert_id for a in stk.to_list()]
        self.assertNotIn(1, ids)
        self.assertEqual(len(stk), 4)

    def test_pop_semua_lalu_push_lagi(self):
        """Pop habis lalu push lagi harus berjalan normal."""
        stk = AlertStack(kapasitas=3)
        for i in range(1, 4):
            stk.push(buat_alert(i))
        for _ in range(3):
            stk.pop()
        self.assertTrue(stk.is_empty())
        stk.push(buat_alert(99))
        self.assertEqual(stk.peek().alert_id, 99)
        self.assertEqual(len(stk), 1)

    def test_hapus_bottom_satu_elemen(self):
        """_hapus_bottom pada stack dengan 1 node → stack kosong."""
        stk = AlertStack(kapasitas=1)
        stk.push(buat_alert(1))   # penuh
        stk.push(buat_alert(2))   # trigger _hapus_bottom → hapus #1
        self.assertEqual(len(stk), 1)
        self.assertEqual(stk.peek().alert_id, 2)

    def test_repr_alert_stack(self):
        """__repr__ harus mengembalikan string yang mengandung info size."""
        stk = AlertStack(kapasitas=5)
        stk.push(buat_alert(1, tipe=1))
        r = repr(stk)
        self.assertIn("AlertStack", r)
        self.assertIn("1/5", r)
        self.assertIn("CRITICAL", r)

    def test_repr_stack_umum(self):
        """__repr__ Stack harus mengembalikan string deskriptif."""
        s = Stack()
        s.push("NODE_X")
        r = repr(s)
        self.assertIn("Stack", r)
        self.assertIn("NODE_X", r)


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    unittest.main(verbosity=2)