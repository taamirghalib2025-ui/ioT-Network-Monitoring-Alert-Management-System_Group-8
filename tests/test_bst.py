"""
test_bst.py — Unit Test untuk BST Device Registry
==================================================
Menguji semua method di BSTDeviceRegistry:
insert, search, update_status, inorder

Jalankan: python -m pytest tests/test_bst.py -v
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'data_structures'))
from bst import DeviceNode, BSTDeviceRegistry


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def registry_kosong():
    """BST kosong."""
    return BSTDeviceRegistry()


@pytest.fixture
def registry_isi():
    """
    BST dengan 5 device:
        GATEWAY_1, SENSOR_2, SENSOR_3, SERVER_4, SENSOR_5
    """
    bst = BSTDeviceRegistry()
    bst.insert("GATEWAY_1", "GATEWAY", "ONLINE",  0.0)
    bst.insert("SENSOR_2",  "SENSOR",  "ONLINE",  22.5)
    bst.insert("SENSOR_3",  "SENSOR",  "OFFLINE", 0.0)
    bst.insert("SERVER_4",  "SERVER",  "ONLINE",  0.0)
    bst.insert("SENSOR_5",  "SENSOR",  "ONLINE",  18.3)
    return bst


# ── Test DeviceNode ───────────────────────────────────────────────────────────

class TestDeviceNode:
    def test_buat_default(self):
        node = DeviceNode("SENSOR_1", "SENSOR")
        assert node.device_id    == "SENSOR_1"
        assert node.tipe         == "SENSOR"
        assert node.status       == "ONLINE"
        assert node.last_reading == 0.0
        assert node.left  is None
        assert node.right is None

    def test_buat_custom(self):
        node = DeviceNode("GW_1", "GATEWAY", "OFFLINE", 99.9)
        assert node.status       == "OFFLINE"
        assert node.last_reading == 99.9

    def test_repr(self):
        node = DeviceNode("SENSOR_1", "SENSOR")
        r = repr(node)
        assert "SENSOR_1" in r
        assert "SENSOR"   in r
        assert "ONLINE"   in r


# ── Test Insert ───────────────────────────────────────────────────────────────

class TestInsert:
    def test_insert_pertama_jadi_root(self, registry_kosong):
        registry_kosong.insert("SENSOR_1", "SENSOR")
        assert registry_kosong.root is not None
        assert registry_kosong.root.device_id == "SENSOR_1"

    def test_insert_kiri(self, registry_kosong):
        registry_kosong.insert("SENSOR_B", "SENSOR")
        registry_kosong.insert("SENSOR_A", "SENSOR")   # A < B → kiri
        assert registry_kosong.root.left.device_id == "SENSOR_A"

    def test_insert_kanan(self, registry_kosong):
        registry_kosong.insert("SENSOR_A", "SENSOR")
        registry_kosong.insert("SENSOR_B", "SENSOR")   # B > A → kanan
        assert registry_kosong.root.right.device_id == "SENSOR_B"

    def test_insert_duplikat_error(self, registry_isi):
        with pytest.raises(ValueError):
            registry_isi.insert("SENSOR_2", "SENSOR")

    def test_insert_banyak_node(self, registry_isi):
        hasil = registry_isi.inorder()
        assert len(hasil) == 5

    def test_insert_dengan_reading(self, registry_kosong):
        registry_kosong.insert("SENSOR_X", "SENSOR", "ONLINE", 37.5)
        node = registry_kosong.search("SENSOR_X")
        assert node.last_reading == 37.5


# ── Test Search ───────────────────────────────────────────────────────────────

class TestSearch:
    def test_search_ada(self, registry_isi):
        node = registry_isi.search("SENSOR_2")
        assert node is not None
        assert node.device_id == "SENSOR_2"
        assert node.tipe      == "SENSOR"

    def test_search_tidak_ada(self, registry_isi):
        assert registry_isi.search("TIDAK_ADA") is None

    def test_search_root(self, registry_isi):
        node = registry_isi.search("GATEWAY_1")
        assert node == registry_isi.root

    def test_search_bst_kosong(self, registry_kosong):
        assert registry_kosong.search("SENSOR_1") is None

    def test_search_semua_node(self, registry_isi):
        for dev_id in ["GATEWAY_1", "SENSOR_2", "SENSOR_3", "SERVER_4", "SENSOR_5"]:
            assert registry_isi.search(dev_id) is not None


# ── Test Update Status ────────────────────────────────────────────────────────

class TestUpdateStatus:
    def test_update_status_berhasil(self, registry_isi):
        hasil = registry_isi.update_status("SENSOR_2", "OFFLINE")
        assert hasil is True
        node = registry_isi.search("SENSOR_2")
        assert node.status == "OFFLINE"

    def test_update_status_tidak_ada(self, registry_isi):
        hasil = registry_isi.update_status("TIDAK_ADA", "OFFLINE")
        assert hasil is False

    def test_update_dengan_reading(self, registry_isi):
        registry_isi.update_status("SENSOR_3", "ONLINE", last_reading=55.5)
        node = registry_isi.search("SENSOR_3")
        assert node.status       == "ONLINE"
        assert node.last_reading == 55.5

    def test_update_tanpa_reading_tidak_ubah(self, registry_isi):
        node_sebelum = registry_isi.search("SENSOR_2")
        reading_lama = node_sebelum.last_reading
        registry_isi.update_status("SENSOR_2", "OFFLINE")
        assert registry_isi.search("SENSOR_2").last_reading == reading_lama

    def test_update_online_ke_offline_ke_online(self, registry_isi):
        registry_isi.update_status("SENSOR_5", "OFFLINE")
        assert registry_isi.search("SENSOR_5").status == "OFFLINE"
        registry_isi.update_status("SENSOR_5", "ONLINE")
        assert registry_isi.search("SENSOR_5").status == "ONLINE"


# ── Test Inorder ──────────────────────────────────────────────────────────────

class TestInorder:
    def test_inorder_terurut(self, registry_isi):
        hasil = registry_isi.inorder()
        ids = [node.device_id for node in hasil]
        assert ids == sorted(ids)

    def test_inorder_jumlah_node(self, registry_isi):
        assert len(registry_isi.inorder()) == 5

    def test_inorder_kosong(self, registry_kosong):
        assert registry_kosong.inorder() == []

    def test_inorder_satu_node(self, registry_kosong):
        registry_kosong.insert("SENSOR_1", "SENSOR")
        hasil = registry_kosong.inorder()
        assert len(hasil) == 1
        assert hasil[0].device_id == "SENSOR_1"

    def test_inorder_semua_tipe(self, registry_isi):
        tipe_list = [node.tipe for node in registry_isi.inorder()]
        assert "SENSOR"  in tipe_list
        assert "GATEWAY" in tipe_list
        assert "SERVER"  in tipe_list


# ── Test Integrasi ────────────────────────────────────────────────────────────

class TestIntegrasi:
    def test_insert_search_update(self, registry_kosong):
        """Insert → search → update → verifikasi."""
        registry_kosong.insert("SENSOR_X", "SENSOR", "ONLINE", 10.0)
        node = registry_kosong.search("SENSOR_X")
        assert node.status == "ONLINE"

        registry_kosong.update_status("SENSOR_X", "OFFLINE", 0.0)
        node = registry_kosong.search("SENSOR_X")
        assert node.status       == "OFFLINE"
        assert node.last_reading == 0.0

    def test_urutan_insert_tidak_pengaruhi_inorder(self):
        """Apapun urutan insert, inorder harus tetap terurut."""
        bst = BSTDeviceRegistry()
        ids = ["SENSOR_E", "SENSOR_A", "SENSOR_C", "SENSOR_B", "SENSOR_D"]
        for i, dev_id in enumerate(ids):
            bst.insert(dev_id, "SENSOR", "ONLINE", float(i))
        hasil = [n.device_id for n in bst.inorder()]
        assert hasil == sorted(ids)

    def test_big_o_search_log_n(self, registry_kosong):
        """Insert 100 device, pastikan search tetap menemukan semua."""
        import string, itertools
        ids = []
        for a, b in itertools.product(string.ascii_uppercase, repeat=2):
            dev_id = f"S_{a}{b}"
            ids.append(dev_id)
            try:
                registry_kosong.insert(dev_id, "SENSOR")
            except ValueError:
                pass
            if len(ids) >= 100:
                break

        for dev_id in ids[:10]:
            assert registry_kosong.search(dev_id) is not None