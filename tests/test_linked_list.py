"""
test_linked_list.py — Unit Test untuk Node Linked List & Edge Graph
Sistem Monitoring Jaringan IoT
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath('src'))
from data_structures.linked_list import LLNode, EdgeNode

# =====================================================================
# Skenario Pengujian (Test Cases)
# =====================================================================

def test_llnode_creation_and_linking():
    # Eksekusi: Membuat dua node terpisah
    node1 = LLNode("Alert_Panas")
    node2 = LLNode("Alert_Asap")
    
    # Eksekusi: Menyambungkan node1 ke node2 (konsep dasar Linked List)
    node1.next = node2
    
    # Validasi Node 1
    assert node1.data == "Alert_Panas", "Data node1 harus sesuai"
    assert node1.next is not None, "node1 harusnya sudah tersambung ke node lain"
    
    # Validasi Node 2 (lewat sambungan node 1)
    assert node1.next.data == "Alert_Asap", "Data yang disambung harus Alert_Asap"
    assert node2.next is None, "Ekor dari Linked List harusnya None"

def test_edgenode_creation():
    # Eksekusi: Membuat node khusus untuk sisi Graph
    edge1 = EdgeNode("GATEWAY_Utama", 25)
    
    # Validasi
    assert edge1.dest == "GATEWAY_Utama", "Tujuan node harus sesuai"
    assert edge1.latensi == 25, "Latensi harus bernilai 25"
    assert edge1.next is None, "Edge baru belum disambung ke mana-mana, harusnya None"