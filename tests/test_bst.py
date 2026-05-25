"""
test_bst.py — Unit Test untuk Binary Search Tree (BST Registry)
Sistem Monitoring Jaringan IoT
"""

import pytest
from src.data_structures.bst import BSTRegistry

# =====================================================================
# Kelas Dummy untuk Testing
# Membuat kelas  pengujian BST mandiri 
# =====================================================================
class MockDevice:
    def __init__(self, device_id, tipe="SENSOR", status="ONLINE"):
        self.device_id = device_id
        self.tipe = tipe
        self.status = status

# =====================================================================
# Setup Fixture
# =====================================================================
@pytest.fixture
def registry():
    """Fixture ini akan dijalankan otomatis sebelum setiap fungsi test di bawah."""
    return BSTRegistry()

# =====================================================================
# Skenario Pengujian (Test Cases)
# =====================================================================

def test_insert_dan_search_berhasil(registry):
    # Persiapan data
    dev1 = MockDevice("SENSOR_2")
    dev2 = MockDevice("GATEWAY_1")
    
    # Eksekusi insert
    registry.insert(dev1)
    registry.insert(dev2)
    
    # Eksekusi search dan validasi (Assert)
    hasil_cari = registry.search("SENSOR_2")
    assert hasil_cari is not None, "Data seharusnya ditemukan"
    assert hasil_cari.device_id == "SENSOR_2", "ID Device harus cocok"
    
def test_search_data_tidak_ada(registry):
    # Persiapan data
    registry.insert(MockDevice("GATEWAY_0"))
    
    # Eksekusi mencari data fiktif
    hasil_gagal = registry.search("SERVER_RAHASIA")
    
    # Validasi
    assert hasil_gagal is None, "Data yang tidak ada harus mengembalikan None"

def test_update_status(registry):
    # Persiapan data
    dev1 = MockDevice("SENSOR_1", "SENSOR", "ONLINE")
    registry.insert(dev1)
    
    # Eksekusi update status
    registry.update_status("SENSOR_1", "OFFLINE")
    
    # Cek apakah status di dalam BST benar-benar berubah
    hasil = registry.search("SENSOR_1")
    assert hasil.status == "OFFLINE", "Status seharusnya berubah menjadi OFFLINE"

def test_inorder_traversal_sorting(registry):
    # Memasukkan data secara acak (tidak urut abjad)
    registry.insert(MockDevice("SENSOR_3"))
    registry.insert(MockDevice("GATEWAY_0"))
    registry.insert(MockDevice("SERVER_A"))
    registry.insert(MockDevice("SENSOR_1"))
    
    # Eksekusi Inorder
    hasil_inorder = registry.inorder()
    
    # Kita ambil hanya device_id-nya saja untuk dicek
    id_list = [dev.device_id for dev in hasil_inorder]
    
    # Validasi: Hasil harus terurut secara leksikografis (abjad)
    assert id_list == ["GATEWAY_0", "SENSOR_1", "SENSOR_3", "SERVER_A"], "Hasil inorder traversal harus terurut sesuai abjad"