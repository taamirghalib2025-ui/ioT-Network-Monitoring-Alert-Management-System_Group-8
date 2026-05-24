<<<<<<< HEAD
"""
main.py — Entry Point Aplikasi Monitoring Jaringan IoT
Sistem Monitoring Jaringan IoT
"""

import numpy as np
import time
import random
from typing import Dict

# Mengimpor struktur data
from data_structures.graph import IoTGraph
from data_structures.bst import BSTRegistry
from data_structures.queue import AlertPriorityQueue
from data_structures.stack import AlertStack

# Mengimpor modul CLI
from modules import modul_6

# Kunci utama agar hasil eksperimen dapat direproduksi
np.random.seed(23)
random.seed(23)

class Device:
    def __init__(self, device_id, tipe, status="ONLINE", last_reading=0.0):
        self.device_id = device_id
        self.tipe = tipe
        self.status = status
        self.last_reading = last_reading

def generate_iot_network(n_devices=40, n_extra_edges=20, seed=23):
    """
    Menghasilkan data jaringan simulasi sesuai panduan PDF.
    """
    rng = np.random.default_rng(seed)
    devices = []
    
    # 1 Gateway
    devices.append(Device('GATEWAY_0', 'GATEWAY'))
    
    # Beberapa Server
    for i in range(1, 5):
        devices.append(Device(f'SERVER_{i}', 'SERVER'))
        
    # Sisanya Sensor
    for i in range(5, n_devices):
        devices.append(Device(f'SENSOR_{i}', 'SENSOR', last_reading=float(rng.uniform(0, 100))))
        
    # Membangun Spanning tree agar pasti terhubung
    perm = rng.permutation(n_devices)
    edges = []
    for i in range(1, n_devices):
        u = devices[perm[i-1]].device_id
        v = devices[perm[i]].device_id
        lat = int(rng.integers(5, 200)) # latensi 5-200 ms
        edges.append((u, v, lat))
        
    # Tambah koneksi ekstra
    for _ in range(n_extra_edges):
        i, j = rng.choice(n_devices, 2, replace=False)
        lat = int(rng.integers(5, 200))
        edges.append((devices[i].device_id, devices[j].device_id, lat))
        
    return devices, edges

def main():
    print("=" * 65)
    print("INITIALIZING IOT NETWORK MONITORING SYSTEM...")
    print("=" * 65)
    
    # Inisialisasi semua struktur data
    graph = IoTGraph()
    bst_reg = BSTRegistry()
    alert_queue = AlertPriorityQueue()
    device_stacks: Dict[str, AlertStack] = {}
    
    # 1. Bangun jaringan menggunakan numpy
    print("[SYSTEM] Membangun topologi jaringan otomatis (Seed=23)...")
    devices, edges = generate_iot_network(40, 20, seed=23)
    
    for d in devices:
        graph.add_device(d)
        bst_reg.insert(d)
        device_stacks[d.device_id] = AlertStack(kapasitas=20)
        
    for u, v, lat in edges:
        graph.add_link(u, v, lat)
        
    print(f"[SYSTEM] Inisialisasi Selesai! Terbentuk {len(devices)} Perangkat dan {len(edges)} Koneksi.\n")
    
    # 2. Jalankan CLI dengan mengoperkan struktur data yang sudah terisi
    modul_6.run_cli(graph, alert_queue, bst_reg, device_stacks)

if __name__ == '__main__':
    main()
=======

>>>>>>> ed29a9374c50f7216482ce01749f415b160d626c
