
import time
import random
import string
import os             # <-- Tambahkan ini
import sys            

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dataclasses import dataclass

# Mengimpor struktur data kustom buatan Anda
from src.data_structures.bst import BSTDeviceRegistry
from src.data_structures.queue import AlertPriorityQueue
from src.data_structures.stack import Alert, AlertStack
from src.data_structures.graph import IoTGraph

# ── Dataclass Dummy untuk Pengujian Perangkat ─────────────────────────────────
@dataclass
class DummyDevice:
    device_id: str
    tipe: str
    status: str
    last_reading: float

def generate_random_id(length=8):
    """Menghasilkan ID acak alfanumerik yang unik untuk simulasi IoT."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def run_benchmark():
    print("=" * 65)
    print("🚀 BENCHMARK SYSTEM: IOT NETWORK MONITORING & ALERT MANAGEMENT")
    print("=" * 65)
    
    # Skala jumlah data uji besar untuk membuktikan Big-O
    N = 2000  
    
    # ==========================================================================
    # 1. BENCHMARK: BST Registry (Registrasi Perangkat)
    # Ekspektasi: insert O(log n) rata-rata, search O(log n) rata-rata
    # ==========================================================================
    print(f"\n[1] Menguji BSTRegistry (Skala Data: {N} Devices)")
    bst = BSTDeviceRegistry()
    
    # Membuat daftar objek device tiruan dengan ID unik secara acak
    devices_pool = [
        DummyDevice(f"DEV_{generate_random_id()}", "SENSOR_SUHU", "ONLINE", time.time())
        for _ in range(N)
    ]

    # Mengukur performa operasi penambahan (Insert) ke BST
    start_time = time.perf_counter()
    for dev in devices_pool:
        bst.insert(dev.device_id, dev.tipe, dev.status, dev.last_reading)
    waktu_insert_bst = time.perf_counter() - start_time
    
    # Mengukur performa pencarian acak (Search) pada pohon BST
    search_targets = random.sample(devices_pool, min(500, N))
    start_time = time.perf_counter()
    for target in search_targets:
        bst.search(target.device_id)
    waktu_search_bst = time.perf_counter() - start_time
    print(f"  └─ O(log n) Search 500 devices acak  : {waktu_search_bst:.6f} detik")


    # ==========================================================================
    # 2. BENCHMARK: Priority Queue (Manajemen Antrean Alert)
    # Ekspektasi: enqueue O(n) worst-case, dequeue O(1)
    # ==========================================================================
    print(f"\n[2] Menguji AlertPriorityQueue (Skala Data: {N} Alerts)")
    pq = AlertPriorityQueue()
    
    # Kondisi terburuk (Worst Case) bagi Linked List terurut menaik (ASC) adalah
    # ketika data baru selalu memiliki nilai tipe prioritas yang lebih besar 
    # atau sama dengan data yang sudah mengantre, memaksanya traverse ke ujung.
    alerts_worst_case = [
        Alert(alert_id=i, device_id=f"DEV_{i}", tipe=3, pesan="INFO LEVEL LOG", timestamp=time.time())
        for i in range(N)
    ]
    
    # Mengukur performa Enqueue terurut
    start_time = time.perf_counter()
    for alt in alerts_worst_case:
        pq.enqueue(alt)
    waktu_enqueue_pq = time.perf_counter() - start_time
    print(f"  └─ O(n) Enqueue {N} alerts (Worst Case) : {waktu_enqueue_pq:.6f} detik")
    
    # Mengukur performa Dequeue (Selalu mengambil elemen terdepan / head)
    start_time = time.perf_counter()
    while not pq.is_empty():
        pq.dequeue()
    waktu_dequeue_pq = time.perf_counter() - start_time
    print(f"  └─ O(1) Dequeue {N} alerts             : {waktu_dequeue_pq:.6f} detik")


    # ==========================================================================
    # 3. BENCHMARK: Alert Stack (Riwayat Log Per-Device)
    # Ekspektasi: push O(1) normal, O(n) saat penuh untuk hapus bottom
    # ==========================================================================
    print(f"\n[3] Menguji AlertStack (Kapasitas Batas Log: 50)")
    stack_max_capacity = 50
    alert_stack = AlertStack(kapasitas=stack_max_capacity)
    
    # Memasukkan total 1500 log ke dalam stack berkapasitas 50 untuk memicu
    # operasi internal `_hapus_bottom` sebanyak 1450 kali.
    total_logs = 1500
    log_alerts = [
        Alert(alert_id=i, device_id="DEV_STATIC_01", tipe=2, pesan="WARNING LIMIT", timestamp=time.time())
        for i in range(total_logs)
    ]
    
    start_time = time.perf_counter()
    for log in log_alerts:
        alert_stack.push(log)
    waktu_push_stack = time.perf_counter() - start_time
    print(f"  └─ Push {total_logs} logs ke Stack (Kapasitas={stack_max_capacity})")
    print(f"     -> Total Waktu Eksekusi           : {waktu_push_stack:.6f} detik")
    print(f"     -> Ukuran elemen akhir di Stack   : {len(alert_stack)} / {alert_stack.kapasitas}")


    # ==========================================================================
    # 4. BENCHMARK: IoT Graph (Topologi Infrastruktur Jaringan)
    # Ekspektasi: add_device O(1), add_link O(1), DFS O(V+E) menggunakan Stack Kustom
    # ==========================================================================
    V_nodes = 500  # Jumlah Titik Infrastruktur (Router/Gateway/Sensor)
    print(f"\n[4] Menguji IoTGraph Topology (Vertices: {V_nodes})")
    graph = IoTGraph()
    
    # Mengisi Node Jaringan ke dalam Graph
    for i in range(V_nodes):
        node_device = DummyDevice(f"NODE_{i}", "ROUTER_CORE", "ONLINE", time.time())
        graph.add_device(node_device)
        
    # Menghubungkan tautan (Edges) antar node secara acak untuk membentuk topologi
    edges_counter = 0
    for i in range(V_nodes):
        # Setiap node dihubungkan ke 2 hingga 4 tetangga acak
        jumlah_koneksi = random.randint(2, 4)
        for _ in range(jumlah_koneksi):
            target_node_idx = random.randint(0, V_nodes - 1)
            if target_node_idx != i:
                graph.add_link(f"NODE_{i}", f"NODE_{target_node_idx}", latensi=random.randint(5, 80))
                edges_counter += 1
                
    print(f"  └─ Infrastruktur Graph Berhasil Dibangun ({len(graph.adj)} Node terdaftar)")
    
    # 📝 PERBAIKAN LOGIKA DFS: Menimpa metode dfs_reachable bawaan agar murni 
    # menggunakan implementasi kelas kustom Stack() Anda (bukan list python bawaan).
    def custom_dfs_reachable(graph_instance, source_node: str) -> set:
        visited_nodes = set()
        dfs_stack = AlertStack()  # Menggunakan Stack buatan sendiri dari stack.py
        dfs_stack.push(source_node)
        
        while not dfs_stack.is_empty():
            current_node = dfs_stack.pop()
            if current_node in visited_nodes:
                continue
            visited_nodes.add(current_node)
            for neighbor_dest, _ in graph_instance.neighbors(current_node):
                if neighbor_dest not in visited_nodes:
                    dfs_stack.push(neighbor_dest)
        return visited_nodes

    # Melakukan pengujian kecepatan penelusuran jaringan (DFS Traversal)
    start_time = time.perf_counter()
    titik_terjangkau = custom_dfs_reachable(graph, "NODE_0")
    waktu_dfs_traversal = time.perf_counter() - start_time
    
    print(f"  └─ O(V+E) DFS Reachability dari 'NODE_0' : {waktu_dfs_traversal:.6f} detik")
    print(f"     -> Total node terjangkau dari pusat: {len(titik_terjangkau)} Node")
    print("=" * 65)
    print("✨ Selesai. Pengujian struktur data berhasil tanpa hambatan.")
    print("=" * 65)

if __name__ == "__main__":
    run_benchmark()