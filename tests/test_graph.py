"""
test_graph.py — Unit Test untuk Graph (Topologi Jaringan IoT)
Sistem Monitoring Jaringan IoT
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath('src'))
from data_structures.graph import IoTGraph

# =====================================================================
# Kelas Dummy untuk Testing
# =====================================================================
class MockDevice:
    def __init__(self, device_id, tipe="SENSOR"):
        self.device_id = device_id
        self.tipe = tipe

# =====================================================================
# Setup Fixture
# =====================================================================
@pytest.fixture
def graph():
    """Membuat graf kosong baru sebelum setiap fungsi test."""
    return IoTGraph()

# =====================================================================
# Skenario Pengujian (Test Cases)
# =====================================================================

def test_add_device(graph):
    # Persiapan data
    dev = MockDevice("GATEWAY_0")
    
    # Eksekusi
    graph.add_device(dev)
    
    # Validasi: Device harus terdaftar di dictionary adj dan devices
    assert "GATEWAY_0" in graph.adj, "Device harus masuk ke adjacency list"
    assert "GATEWAY_0" in graph.devices, "Device harus masuk ke dictionary devices"

def test_add_link_dan_neighbors(graph):
    # Persiapan 2 alat
    graph.add_device(MockDevice("GATEWAY_0"))
    graph.add_device(MockDevice("SENSOR_1"))
    
    # Eksekusi: Sambungkan kabel dengan latensi 15ms
    graph.add_link("GATEWAY_0", "SENSOR_1", 15)
    
    # Eksekusi: Cek siapa saja tetangga GATEWAY_0
    tetangga_gw = graph.neighbors("GATEWAY_0")
    
    # Validasi
    assert len(tetangga_gw) == 1, "GATEWAY_0 seharusnya punya 1 tetangga"
    # Format return tetangga biasanya: [("SENSOR_1", 15)]
    assert tetangga_gw[0][0] == "SENSOR_1", "Tetangganya harus SENSOR_1"
    assert tetangga_gw[0][1] == 15, "Latensinya harus 15 ms"

def test_deteksi_node_terisolasi(graph):
    # Persiapan 3 alat
    graph.add_device(MockDevice("GATEWAY_0"))
    graph.add_device(MockDevice("SENSOR_A"))
    graph.add_device(MockDevice("SENSOR_TERISOLASI"))
    
    # Sambungkan GATEWAY_0 HANYA ke SENSOR_A
    graph.add_link("GATEWAY_0", "SENSOR_A", 10)
    
    # Eksekusi: Cari siapa yang terisolasi dari GATEWAY_0
    hasil_isolasi = graph.isolated_devices("GATEWAY_0")
    
    # Validasi
    assert "SENSOR_TERISOLASI" in hasil_isolasi, "SENSOR_TERISOLASI harus terdeteksi putus"
    assert "SENSOR_A" not in hasil_isolasi, "SENSOR_A aman, tidak boleh masuk daftar terisolasi"
    assert "GATEWAY_0" not in hasil_isolasi, "GATEWAY_0 adalah pusat, tidak terisolasi"