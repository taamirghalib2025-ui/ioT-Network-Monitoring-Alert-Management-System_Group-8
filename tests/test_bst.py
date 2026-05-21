"""
test_bst.py — Unit Test untuk BSTDeviceRegistry
Lokasi  : tests/test_bst.py
Mata Kuliah : ELT60213 Algoritma dan Struktur Data
Team Based Project TA 2025/2026 — Group 8

Cara menjalankan:
    python -m pytest tests/test_bst.py -v
    atau
    python tests/test_bst.py
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'data_structures'))

from bst import BSTDeviceRegistry, DeviceNode


# ══════════════════════════════════════════════
#  TEST INSERT
# ══════════════════════════════════════════════

class TestInsert(unittest.TestCase):

    def setUp(self):
        self.bst = BSTDeviceRegistry()

    def test_insert_root(self):
        """Insert pertama harus menjadi root."""
        self.bst.insert("D001", "SENSOR")
        self.assertIsNotNone(self.bst.root)
        self.assertEqual(self.bst.root.device_id, "D001")

    def test_insert_left_child(self):
        """Device dengan id lebih kecil harus masuk ke kiri."""
        self.bst.insert("D005", "GATEWAY")
        self.bst.insert("D002", "SENSOR")
        self.assertEqual(self.bst.root.left.device_id, "D002")

    def test_insert_right_child(self):
        """Device dengan id lebih besar harus masuk ke kanan."""
        self.bst.insert("D005", "GATEWAY")
        self.bst.insert("D008", "SERVER")
        self.assertEqual(self.bst.root.right.device_id, "D008")

    def test_insert_default_status_online(self):
        """Default status harus ONLINE."""
        self.bst.insert("D001", "SENSOR")
        self.assertEqual(self.bst.root.status, "ONLINE")

    def test_insert_default_last_reading_nol(self):
        """Default last_reading harus 0.0."""
        self.bst.insert("D001", "SENSOR")
        self.assertEqual(self.bst.root.last_reading, 0.0)

    def test_insert_custom_status_dan_reading(self):
        """Insert dengan status dan last_reading custom harus tersimpan benar."""
        self.bst.insert("D001", "SENSOR", status="OFFLINE", last_reading=3.14)
        node = self.bst.root
        self.assertEqual(node.status, "OFFLINE")
        self.assertAlmostEqual(node.last_reading, 3.14)

    def test_insert_tipe_sensor(self):
        """Tipe SENSOR harus tersimpan benar."""
        self.bst.insert("D001", "SENSOR")
        self.assertEqual(self.bst.root.tipe, "SENSOR")

    def test_insert_tipe_gateway(self):
        """Tipe GATEWAY harus tersimpan benar."""
        self.bst.insert("D001", "GATEWAY")
        self.assertEqual(self.bst.root.tipe, "GATEWAY")

    def test_insert_tipe_server(self):
        """Tipe SERVER harus tersimpan benar."""
        self.bst.insert("D001", "SERVER")
        self.assertEqual(self.bst.root.tipe, "SERVER")

    def test_insert_duplikat_raise_error(self):
        """Insert device_id yang sama harus raise ValueError."""
        self.bst.insert("D001", "SENSOR")
        with self.assertRaises(ValueError):
            self.bst.insert("D001", "GATEWAY")

    def test_insert_banyak_node(self):
        """Insert banyak node harus membentuk BST yang valid."""
        ids = ["D005", "D002", "D008", "D001", "D003", "D007", "D009"]
        for did in ids:
            self.bst.insert(did, "SENSOR")
        # Verifikasi via inorder — harus terurut
        inorder_ids = [n.device_id for n in self.bst.inorder()]
        self.assertEqual(inorder_ids, sorted(ids))


# ══════════════════════════════════════════════
#  TEST SEARCH
# ══════════════════════════════════════════════

class TestSearch(unittest.TestCase):

    def setUp(self):
        self.bst = BSTDeviceRegistry()
        for did, tipe in [("D005", "GATEWAY"), ("D002", "SENSOR"),
                          ("D008", "SERVER"),  ("D001", "SENSOR"),
                          ("D007", "SENSOR")]:
            self.bst.insert(did, tipe)

    def test_search_root(self):
        """Search root harus berhasil."""
        node = self.bst.search("D005")
        self.assertIsNotNone(node)
        self.assertEqual(node.device_id, "D005")

    def test_search_kiri(self):
        """Search node di subtree kiri harus berhasil."""
        node = self.bst.search("D002")
        self.assertIsNotNone(node)

    def test_search_kanan(self):
        """Search node di subtree kanan harus berhasil."""
        node = self.bst.search("D008")
        self.assertIsNotNone(node)

    def test_search_leaf(self):
        """Search node daun (leaf) harus berhasil."""
        node = self.bst.search("D001")
        self.assertIsNotNone(node)
        self.assertEqual(node.device_id, "D001")

    def test_search_tidak_ada(self):
        """Search device yang tidak ada harus return None."""
        node = self.bst.search("D999")
        self.assertIsNone(node)

    def test_search_bst_kosong(self):
        """Search pada BST kosong harus return None."""
        bst_kosong = BSTDeviceRegistry()
        self.assertIsNone(bst_kosong.search("D001"))

    def test_search_kembalikan_devivenode(self):
        """Search harus mengembalikan objek DeviceNode."""
        node = self.bst.search("D007")
        self.assertIsInstance(node, DeviceNode)

    def test_search_data_benar(self):
        """Node hasil search harus memiliki data yang tepat."""
        node = self.bst.search("D002")
        self.assertEqual(node.tipe, "SENSOR")


# ══════════════════════════════════════════════
#  TEST UPDATE STATUS
# ══════════════════════════════════════════════

class TestUpdateStatus(unittest.TestCase):

    def setUp(self):
        self.bst = BSTDeviceRegistry()
        self.bst.insert("D001", "SENSOR",  status="ONLINE",  last_reading=1.0)
        self.bst.insert("D002", "GATEWAY", status="ONLINE",  last_reading=2.0)
        self.bst.insert("D003", "SERVER",  status="OFFLINE", last_reading=0.0)

    def test_update_status_online_ke_offline(self):
        """Status ONLINE harus bisa diubah ke OFFLINE."""
        result = self.bst.update_status("D001", "OFFLINE")
        self.assertTrue(result)
        self.assertEqual(self.bst.search("D001").status, "OFFLINE")

    def test_update_status_offline_ke_online(self):
        """Status OFFLINE harus bisa diubah ke ONLINE."""
        result = self.bst.update_status("D003", "ONLINE")
        self.assertTrue(result)
        self.assertEqual(self.bst.search("D003").status, "ONLINE")

    def test_update_status_dengan_reading_baru(self):
        """last_reading harus terupdate jika parameter diberikan."""
        self.bst.update_status("D001", "ONLINE", last_reading=99.9)
        node = self.bst.search("D001")
        self.assertAlmostEqual(node.last_reading, 99.9)

    def test_update_status_tanpa_reading(self):
        """last_reading tidak berubah jika parameter tidak diberikan."""
        self.bst.update_status("D001", "OFFLINE")
        node = self.bst.search("D001")
        self.assertAlmostEqual(node.last_reading, 1.0)  # tetap 1.0

    def test_update_status_device_tidak_ada(self):
        """update_status pada device yang tidak ada harus return False."""
        result = self.bst.update_status("D999", "OFFLINE")
        self.assertFalse(result)

    def test_update_status_tidak_mengubah_device_lain(self):
        """Update satu device tidak boleh mempengaruhi device lain."""
        self.bst.update_status("D001", "OFFLINE", last_reading=50.0)
        node_d2 = self.bst.search("D002")
        self.assertEqual(node_d2.status, "ONLINE")
        self.assertAlmostEqual(node_d2.last_reading, 2.0)

    def test_update_reading_nol(self):
        """last_reading boleh diupdate ke 0.0."""
        self.bst.update_status("D001", "ONLINE", last_reading=0.0)
        node = self.bst.search("D001")
        self.assertAlmostEqual(node.last_reading, 0.0)


# ══════════════════════════════════════════════
#  TEST INORDER
# ══════════════════════════════════════════════

class TestInorder(unittest.TestCase):

    def setUp(self):
        self.bst = BSTDeviceRegistry()

    def test_inorder_kosong(self):
        """Inorder pada BST kosong harus return list kosong."""
        self.assertEqual(self.bst.inorder(), [])

    def test_inorder_satu_node(self):
        """Inorder dengan satu node harus return list satu elemen."""
        self.bst.insert("D001", "SENSOR")
        result = self.bst.inorder()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].device_id, "D001")

    def test_inorder_urutan_ascending(self):
        """Inorder harus mengembalikan node terurut ascending by device_id."""
        ids = ["D005", "D002", "D008", "D001", "D003"]
        for did in ids:
            self.bst.insert(did, "SENSOR")
        result_ids = [n.device_id for n in self.bst.inorder()]
        self.assertEqual(result_ids, sorted(ids))

    def test_inorder_semua_node_ada(self):
        """Inorder harus mengembalikan semua node yang diinsert."""
        ids = ["D005", "D002", "D008", "D001", "D003", "D007", "D009"]
        for did in ids:
            self.bst.insert(did, "SENSOR")
        result_ids = [n.device_id for n in self.bst.inorder()]
        self.assertEqual(sorted(result_ids), sorted(ids))

    def test_inorder_kembalikan_devivenode(self):
        """Setiap elemen hasil inorder harus bertipe DeviceNode."""
        self.bst.insert("D001", "SENSOR")
        self.bst.insert("D002", "GATEWAY")
        for node in self.bst.inorder():
            self.assertIsInstance(node, DeviceNode)

    def test_inorder_insert_berurutan(self):
        """Inorder pada insert berurutan (worst case linear) tetap terurut."""
        for i in range(1, 6):
            self.bst.insert(f"D00{i}", "SENSOR")
        result_ids = [n.device_id for n in self.bst.inorder()]
        self.assertEqual(result_ids, sorted(result_ids))


# ══════════════════════════════════════════════
#  TEST INTEGRASI
# ══════════════════════════════════════════════

class TestIntegrasi(unittest.TestCase):

    def test_skenario_lengkap(self):
        """
        Skenario: register device → search → update status → cek inorder.
        """
        bst = BSTDeviceRegistry()

        # Register
        bst.insert("GW01", "GATEWAY", "ONLINE",  0.0)
        bst.insert("SN01", "SENSOR",  "ONLINE",  23.5)
        bst.insert("SN02", "SENSOR",  "ONLINE",  18.2)
        bst.insert("SV01", "SERVER",  "ONLINE",  0.0)
        bst.insert("SN03", "SENSOR",  "OFFLINE", 0.0)

        # Search berhasil
        self.assertIsNotNone(bst.search("GW01"))
        self.assertIsNotNone(bst.search("SN02"))

        # Search tidak ada
        self.assertIsNone(bst.search("XX99"))

        # Update status
        bst.update_status("SN03", "ONLINE", last_reading=30.1)
        node = bst.search("SN03")
        self.assertEqual(node.status, "ONLINE")
        self.assertAlmostEqual(node.last_reading, 30.1)

        # Inorder — semua 5 node, terurut
        inorder = bst.inorder()
        self.assertEqual(len(inorder), 5)
        ids = [n.device_id for n in inorder]
        self.assertEqual(ids, sorted(ids))

    def test_skenario_device_offline_massal(self):
        """Semua device bisa diubah ke OFFLINE sekaligus."""
        bst = BSTDeviceRegistry()
        device_ids = ["D001", "D002", "D003", "D004", "D005"]
        for did in device_ids:
            bst.insert(did, "SENSOR", "ONLINE", 10.0)

        for did in device_ids:
            bst.update_status(did, "OFFLINE")

        for node in bst.inorder():
            self.assertEqual(node.status, "OFFLINE")

    def test_duplikat_tidak_merusak_bst(self):
        """Setelah ValueError duplikat, BST tetap konsisten."""
        bst = BSTDeviceRegistry()
        bst.insert("D001", "SENSOR")
        bst.insert("D002", "GATEWAY")

        with self.assertRaises(ValueError):
            bst.insert("D001", "SERVER")

        # BST masih benar
        self.assertEqual(len(bst.inorder()), 2)
        self.assertEqual(bst.search("D001").tipe, "SENSOR")  # tidak berubah


# ══════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  TEST BST — IoT Network Monitoring System  Group 8")
    print("=" * 60)
    unittest.main(verbosity=2)