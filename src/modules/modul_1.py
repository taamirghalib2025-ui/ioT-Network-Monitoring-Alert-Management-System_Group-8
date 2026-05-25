"""
modul_1.py — Modul 1: Graph Topologi Jaringan IoT
Bertindak sebagai service layer untuk memproses perintah terkait topologi jaringan
dan menampilkan kompleksitas waktu (Big-O)k.
"""

from data_structures.graph import IoTGraph
# Jika kelas Device dideklarasikan di file lain, pastikan untuk mengimpornya jika diperlukan
# from data_structures.priority_queue import Device 

def run_add_device(graph: IoTGraph, device) -> None:
    """
    Menjalankan fungsi tambah perangkat ke dalam topologi jaringan.
    Spesifikasi: Big-O: O(1)
    """
    graph.add_device(device)
    print(f"[SUCCESS] Perangkat '{device.device_id}' ({device.tipe}) berhasil ditambahkan ke topologi.")
    print("-> Kompleksitas Waktu: Big-O: O(1)\n")


def run_add_link(graph: IoTGraph, u: str, v: str, latensi: int) -> None:
    """
    Menjalankan fungsi tambah koneksi (edge) antar perangkat.
    Spesifikasi: Big-O: O(1)
    """
    if u not in graph.adj or v not in graph.adj:
        print(f"[ERROR] Gagal menambahkan link. Perangkat '{u}' atau '{v}' tidak ditemukan.")
        return
        
    graph.add_link(u, v, latensi)
    print(f"[SUCCESS] Link terbentuk antara '{u}' <---> '{v}' dengan latensi {latensi} ms.")
    print("-> Kompleksitas Waktu: Big-O: O(1)\n")


def run_remove_link(graph: IoTGraph, u: str, v: str) -> None:
    """
    Menjalankan fungsi hapus koneksi antar perangkat.
    Spesifikasi: Big-O: O(deg(u) + deg(v))
    """
    status = graph.remove_link(u, v)
    if status:
        print(f"[SUCCESS] Link antara '{u}' <---> '{v}' berhasil diputus.")
    else:
        print(f"[WARNING] Tidak ada link aktif antara '{u}' dan '{v}'.")
    print("-> Kompleksitas Waktu: Big-O: O(deg(u) + deg(v))\n")


def run_deteksi_isolasi(graph: IoTGraph, gateway: str = 'GATEWAY_0') -> None:
    """
    Mendeteksi komponen/perangkat yang terisolasi (tidak terjangkau dari gateway pusat).
    Menggunakan algoritma DFS berbasis Stack.
    Spesifikasi: Big-O: O(V+E)
    """
    print(f"[AUDIT] Menjalankan DFS untuk deteksi komponen terisolasi dari '{gateway}'...")
    perangkat_terisolasi = graph.isolated_devices(gateway)
    
    if perangkat_terisolasi:
        print(f"[ALERT] Ditemukan {len(perangkat_terisolasi)} perangkat terisolasi:")
        for idx, device_id in enumerate(perangkat_terisolasi, 1):
            device = graph.devices.get(device_id)
            status_str = device.status if device else "UNKNOWN"
            print(f"   {idx}. {device_id} [Status: {status_str}]")
    else:
        print("[SAFE] Semua perangkat terhubung dengan baik ke jaringan utama.")
    print("-> Kompleksitas Waktu: Big-O: O(V+E)\n")


def run_laporan_jaringan(graph: IoTGraph) -> None:
    """
    Menampilkan visualisasi teks ringkas mengenai seluruh topologi jaringan,
    jumlah tetangga (degree), dan nilai latensinya.
    Spesifikasi: Big-O: O(V+E)
    """
    print("=" * 60)
    print("LAPORAN TOPOLOGI JARINGAN IoT KAMPUS UNY")
    print("=" * 60)
    print(f"Total Perangkat (Node) : {len(graph.adj)}")
    
    # Hitung total edge (karena undirected, jumlah degree dibagi 2)
    total_edges = sum(graph.degree(u) for u in graph.adj) // 2
    print(f"Total Koneksi (Edge)   : {total_edges}")
    print("-" * 60)
    
    for device_id in sorted(graph.adj.keys()):
        deg = graph.degree(device_id)
        tetangga = graph.neighbors(device_id)
        tetangga_str = ", ".join([f"{dest}({lat}ms)" for dest, lat in tetangga])
        print(f"[{device_id}] -> Degree: {deg} | Tetangga: [{tetangga_str if tetangga_str else 'Tidak ada'}]")
        
    print("=" * 60)
    print("-> Kompleksitas Waktu: Big-O: O(V+E)\n")