"""
modul_5.py — Modul 5: Routing Optimal & Audit Latensi
Menggunakan Dijkstra untuk mencari rute minimum, mencari bottleneck pada SPT,
dan mengaudit perangkat dengan Selection Sort berbasis Linked List.
"""

import heapq
from data_structures.graph import IoTGraph
from data_structures.linked_list import LLNode  # Menggunakan LLNode buatan sendiri

def run_routing_optimal(graph: IoTGraph, start_node: str = 'GATEWAY_0'):
    """
    Mencari rute latensi minimum dari start_node ke semua perangkat (Dijkstra)
    dan mengidentifikasi 'bottleneck link' pada Shortest Path Tree (SPT).
    Spesifikasi: Big-O: O((V+E) log V)
    """
    print("=" * 60)
    print(f"ROUTING OPTIMAL (DIJKSTRA) DARI: {start_node}")
    print("=" * 60)

    if start_node not in graph.adj:
        print(f"[ERROR] Node awal '{start_node}' tidak ditemukan di topologi.")
        return None

    distances = {node: float('infinity') for node in graph.adj}
    distances[start_node] = 0
    previous = {node: None for node in graph.adj}
    
    # Mencatat bobot edge yang membawa ke node tersebut dalam SPT
    spt_edge_weights = {} 
    
    # Priority Queue: (jarak_kumulatif, current_node)
    pq = [(0, start_node)]
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        if current_dist > distances[current_node]:
            continue
            
        for neighbor, latensi in graph.neighbors(current_node):
            jarak_baru = current_dist + latensi
            
            if jarak_baru < distances[neighbor]:
                distances[neighbor] = jarak_baru
                previous[neighbor] = current_node
                spt_edge_weights[neighbor] = latensi  # Catat bobot edge SPT
                heapq.heappush(pq, (jarak_baru, neighbor))

    # 1. Cetak Rute Terpendek
    for node in sorted(graph.adj.keys()):
        if node == start_node:
            continue
        if distances[node] == float('infinity'):
            print(f"  -> {node}: [TIDAK TERJANGKAU]")
        else:
            path = []
            curr = node
            while curr:
                path.append(curr)
                curr = previous[curr]
            path.reverse()
            print(f"  -> {node}: {distances[node]} ms | Rute: {' -> '.join(path)}")

    # 2. Identifikasi 'Bottleneck Link' pada Shortest Path Tree (SPT)
    print("-" * 60)
    max_weight = -1
    bottleneck_edge = None
    
    for node, weight in spt_edge_weights.items():
        if distances[node] != float('infinity') and weight > max_weight:
            max_weight = weight
            bottleneck_edge = (previous[node], node)

    if bottleneck_edge:
        print(f"[BOTTLENECK LINK SPT] Edge dengan bobot tertinggi pada Shortest Path Tree:")
        print(f"  {bottleneck_edge[0]} <---> {bottleneck_edge[1]} dengan bobot: {max_weight} ms")
    else:
        print("[BOTTLENECK LINK SPT] Tidak ditemukan jalur aktif.")

    print("=" * 60)
    print("-> Kompleksitas Waktu: Big-O: O((V+E) log V)\n")
    
    # Mengembalikan data jarak untuk digunakan oleh fungsi audit
    return distances


def run_audit_latensi(graph: IoTGraph, distances: dict) -> None:
    """
    Melakukan audit dengan mengurutkan perangkat berdasarkan latensi ke GATEWAY
    menggunakan algoritma Selection Sort pada Linked List (LLNode).
    Spesifikasi: Big-O: O(V^2) di mana V adalah jumlah perangkat
    """
    print("=" * 60)
    print("AUDIT LATENSI PERANGKAT (SELECTION SORT ON LINKED LIST)")
    print("=" * 60)

    if not distances:
        print("[INFO] Tidak ada data jarak untuk diaudit.")
        return

    # 1. Masukkan data perangkat ke struktur Linked List (LLNode)
    head = None
    tail = None
    
    for node_id, dist in distances.items():
        # Masukkan selain GATEWAY itu sendiri dan pastikan node terjangkau
        if node_id != 'GATEWAY_0' and dist != float('infinity'):
            # Menyimpan dictionary data di dalam field LLNode.data
            new_node = LLNode({'id': node_id, 'latensi': dist})
            if head is None:
                head = new_node
                tail = new_node
            else:
                tail.next = new_node
                tail = new_node

    if head is None:
        print("[INFO] Tidak ada perangkat terhubung yang bisa diaudit.")
        return

    # 2. Algoritma Selection Sort pada Linked List (Ascending / Terkecil ke Terbesar)
    i = head
    while i:
        min_node = i
        j = i.next
        while j:
            if j.data['latensi'] < min_node.data['latensi']:
                min_node = j
            j = j.next
        
        # Tukar posisi data (Swap) jika ditemukan node dengan latensi lebih kecil
        if min_node != i:
            i.data, min_node.data = min_node.data, i.data
        i = i.next

    # 3. Cetak Hasil Audit Langsung dari Penelusuran Linked List
    print("Daftar Perangkat Terurut Berdasarkan Latensi Kumulatif ke GATEWAY:")
    curr = head
    idx = 1
    while curr:
        print(f"  {idx}. {curr.data['id']} -> Total Latensi: {curr.data['latensi']} ms")
        curr = curr.next
        idx += 1

    print("=" * 60)
    print("-> Kompleksitas Waktu: Big-O: O(V^2) - Selection Sort pada Linked List\n")