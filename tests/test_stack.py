"""
test_stack.py — Unit Test untuk Alert Stack & DFS Stack
Sistem Monitoring Jaringan IoT
"""

import pytest
import sys
import os

# Penunjuk jalan ke folder src
sys.path.insert(0, os.path.abspath('src'))

# Mengimpor kedua jenis Stack dari kodemu
from data_structures.stack import AlertStack, Stack

# =====================================================================
# Kelas Dummy untuk Alert
# =====================================================================
class MockAlert:
    def __init__(self, alert_id):
        self.alert_id = alert_id

# =====================================================================
# Skenario Pengujian: AlertStack (Dengan Batas Kapasitas)
# =====================================================================

def test_alert_stack_push_pop_peek():
    astack = AlertStack()
    astack.push(MockAlert("A1"))
    astack.push(MockAlert("A2"))

    # Prinsip LIFO (Last In, First Out): Yang terakhir masuk (A2) harus di atas
    assert astack.peek().alert_id == "A2", "Peek harus mengembalikan elemen terakhir masuk"
    assert len(astack) == 2, "Ukuran stack harus 2"

    # Pop harus mengeluarkan A2 duluan
    popped = astack.pop()
    assert popped.alert_id == "A2", "Pop harus mengeluarkan elemen paling atas"
    assert len(astack) == 1, "Ukuran setelah pop harus 1"

def test_alert_stack_capacity_limit():
    # Kita set kapasitasnya sengaja kecil (cuma 3) agar mudah diuji batasnya
    astack = AlertStack(kapasitas=3)
    
    astack.push(MockAlert("Alert_Lama_1"))
    astack.push(MockAlert("Alert_Lama_2"))
    astack.push(MockAlert("Alert_Lama_3"))
    
    # Kondisi stack sekarang penuh: [Top] Alert_3 -> Alert_2 -> Alert_1 [Bottom]
    assert len(astack) == 3
    
    # Eksekusi: Masukkan elemen ke-4. Seharusnya membuang "Alert_Lama_1" (paling bawah/lama)
    astack.push(MockAlert("Alert_Baru_4"))
    
    # Validasi Kapasitas
    assert len(astack) == 3, "Ukuran maksimal stack tidak boleh melebihi kapasitas (3)"
    
    # Validasi urutan setelah dibuang (menggunakan fungsi to_list buatanmu)
    isi_list = astack.to_list()
    assert isi_list[0].alert_id == "Alert_Baru_4", "Paling atas harus yang terbaru"
    assert isi_list[1].alert_id == "Alert_Lama_3"
    assert isi_list[2].alert_id == "Alert_Lama_2", "Paling bawah harus Alert_Lama_2. Alert_Lama_1 harusnya sudah lenyap"

# =====================================================================
# Skenario Pengujian: Stack Umum (DFS)
# =====================================================================

def test_general_stack_operations():
    s = Stack()
    
    # Validasi awal
    assert s.is_empty() is True, "Awalnya stack harus kosong"
    
    # Eksekusi push
    s.push("Node_A")
    s.push("Node_B")
    
    # Validasi isi
    assert s.is_empty() is False
    assert len(s) == 2
    
    # Validasi LIFO
    assert s.pop() == "Node_B", "Node_B harus keluar duluan"
    assert s.pop() == "Node_A", "Node_A keluar belakangan"
    assert s.pop() is None, "Pop pada stack kosong harus mengembalikan None"