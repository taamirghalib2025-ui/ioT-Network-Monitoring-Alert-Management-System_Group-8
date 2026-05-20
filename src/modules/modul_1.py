import numpy as np
import random
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple

# ── Seed tetap ──────────────────────────────────────────────
np.random.seed(23)
random.seed(23)

DEVICE_TYPES = ['SENSOR', 'GATEWAY', 'SERVER']
ALERT_TYPES  = {'CRITICAL': 1, 'WARNING': 2, 'INFO': 3}


# ── Dataclass ────────────────────────────────────────────────
@dataclass
class Device:
    device_id: str
    tipe: str           # SENSOR / GATEWAY / SERVER
    status: str = 'ONLINE'
    last_reading: float = 0.0


# ── Node Linked List (general) ───────────────────────────────
class LLNode:
    """Node serbaguna untuk Stack dan struktur lain."""
    def __init__(self, data=None):
        self.data = data
        self.next: Optional['LLNode'] = None


# ── Edge Node untuk adjacency list ──────────────────────────
class EdgeNode:
  
    def __init__(self, dest: str, latensi: int):
        self.dest    = dest
        self.latensi = latensi
        self.next: Optional['EdgeNode'] = None


# ════════════════════════════════════════════════════════════
#   MODUL 1 – IoTGraph
# ════════════════════════════════════════════════════════════
class IoTGraph:

    def __init__(self):
        self.adj: Dict[str, Optional[EdgeNode]] = {}
        self.devices: Dict[str, Device] = {}

    # ── Tambah perangkat ──────────────────────────────────────
    def add_device(self, device: Device) -> None:
       
        if device.device_id not in self.adj:
            self.adj[device.device_id]    = None   # belum ada edge
            self.devices[device.device_id] = device

    # ── Tambah koneksi ────────────────────────────────────────
    def add_link(self, u: str, v: str, latensi: int) -> None:
       
        if u not in self.adj or v not in self.adj:
            return  # salah satu node belum terdaftar

        # u → v
        edge_uv       = EdgeNode(v, latensi)
        edge_uv.next  = self.adj[u]
        self.adj[u]   = edge_uv

        # v → u  (undirected)
        edge_vu       = EdgeNode(u, latensi)
        edge_vu.next  = self.adj[v]
        self.adj[v]   = edge_vu

    # ── Hapus koneksi ─────────────────────────────────────────
    def remove_link(self, u: str, v: str) -> None:
    
        if u in self.adj:
            self.adj[u] = self._remove_from_list(self.adj[u], v)
        if v in self.adj:
            self.adj[v] = self._remove_from_list(self.adj[v], u)

    def _remove_from_list(self,
                          head: Optional[EdgeNode],
                          dest: str) -> Optional[EdgeNode]:
       
        dummy      = EdgeNode('__dummy__', 0)
        dummy.next = head
        prev, curr = dummy, head
        while curr is not None:
            if curr.dest == dest:
                prev.next = curr.next
                break
            prev, curr = curr, curr.next
        return dummy.next

    # ── Hapus perangkat ───────────────────────────────────────
    def remove_device(self, device_id: str) -> None:
       
        if device_id not in self.adj:
            return
        # Hapus semua edge dari node lain ke device_id
        for uid in list(self.adj.keys()):
            if uid != device_id:
                self.adj[uid] = self._remove_from_list(self.adj[uid], device_id)
        # Hapus entri device_id sendiri
        del self.adj[device_id]
        del self.devices[device_id]

    # ── Tetangga ──────────────────────────────────────────────
    def neighbors(self, u: str) -> List[Tuple[str, int]]:
       
        result: List[Tuple[str, int]] = []
        curr = self.adj.get(u)
        while curr is not None:
            result.append((curr.dest, curr.latensi))
            curr = curr.next
        return result

    # ── Derajat node ──────────────────────────────────────────
    def degree(self, u: str) -> int:
      
        count = 0
        curr  = self.adj.get(u)
        while curr is not None:
            count += 1
            curr   = curr.next
        return count

    # ── DFS berbasis Stack Linked List ────────────────────────
    def dfs_reachable(self, source: str) -> set:
      
        if source not in self.adj:
            return set()

        visited: set  = set()
        # Inisialisasi stack: LLNode sebagai top-of-stack
        stack_top      = LLNode(source)

        while stack_top is not None:
            # Pop
            current    = stack_top.data
            stack_top  = stack_top.next

            if current in visited:
                continue
            visited.add(current)

            # Push semua tetangga yang belum dikunjungi
            edge = self.adj.get(current)
            while edge is not None:
                if edge.dest not in visited:
                    new_node      = LLNode(edge.dest)
                    new_node.next = stack_top
                    stack_top     = new_node
                edge = edge.next

        return visited

    # ── Deteksi perangkat terisolasi ──────────────────────────
    def isolated_devices(self, gateway: str = 'GATEWAY_0') -> List[str]:
      
        reachable = self.dfs_reachable(gateway)
        return [d for d in self.adj if d not in reachable]

    # ── Ringkasan laporan ─────────────────────────────────────
    def laporan_jaringan(self) -> None:
        """Cetak ringkasan statistik topologi jaringan."""
        total_edges = sum(self.degree(u) for u in self.adj) // 2
        isolated    = self.isolated_devices()

        print("\n" + "=" * 50)
        print("  LAPORAN TOPOLOGI JARINGAN IoT")
        print("=" * 50)
        print(f"  Total perangkat  : {len(self.devices)}")
        print(f"  Total koneksi    : {total_edges}")
        print(f"  Terisolasi       : {len(isolated)} perangkat")
        if isolated:
            print(f"  Detail terisolasi: {isolated}")
        print()
        print("  Adjacency List (5 node pertama):")
        for i, node_id in enumerate(self.adj):
            if i >= 5:
                print("    ...")
                break
            nbrs = self.neighbors(node_id)
            preview = nbrs[:3]
            suffix  = f" +{len(nbrs)-3} lainnya" if len(nbrs) > 3 else ""
            print(f"    {node_id:15s} deg={self.degree(node_id):3d}  → {preview}{suffix}")
        print()
        print("  Kompleksitas:")
        print("    add_device    : O(1)")
        print("    add_link      : O(1)")
        print("    remove_link   : O(deg(u) + deg(v))")
        print("    remove_device : O(V + E)")
        print("    neighbors     : O(deg(u))")
        print("    degree        : O(deg(u))")
        print("    dfs_reachable : O(V + E)")
        print("=" * 50)


# ════════════════════════════════════════════════════════════
#   Generator data jaringan (dari starter code, JANGAN ubah seed)
# ════════════════════════════════════════════════════════════
def generate_iot_network(n_devices: int = 40,
                         n_extra_edges: int = 20,
                         seed: int = 23):
    rng     = np.random.default_rng(seed)
    devices = []

    # 1 gateway, beberapa server, sisanya sensor
    devices.append(Device('GATEWAY_0', 'GATEWAY'))
    for i in range(1, 5):
        devices.append(Device(f'SERVER_{i}', 'SERVER'))
    for i in range(5, n_devices):
        devices.append(Device(f'SENSOR_{i}', 'SENSOR',
                               last_reading=float(rng.uniform(0, 100))))

    # Spanning tree: pastikan semua terhubung
    perm  = rng.permutation(n_devices)
    edges = []
    for i in range(1, n_devices):
        u   = devices[perm[i - 1]].device_id
        v   = devices[perm[i]].device_id
        lat = int(rng.integers(5, 200))   # 5–200 ms
        edges.append((u, v, lat))

    # Edge tambahan (acak)
    for _ in range(n_extra_edges):
        i, j = rng.choice(n_devices, 2, replace=False)
        lat  = int(rng.integers(5, 200))
        edges.append((devices[i].device_id, devices[j].device_id, lat))

    return devices, edges


# ════════════════════════════════════════════════════════════
#   Demo / Uji Modul 1
# ════════════════════════════════════════════════════════════
def demo_modul1():
    print("=" * 50)
    print("  MODUL 1 – Graph Topologi Jaringan")
    print("  IoT Network Monitoring System")
    print("=" * 50)

    # ── 1. Bangun graph dari data generator ──────────────────
    graph             = IoTGraph()
    devices, edges    = generate_iot_network(40, 20, seed=23)

    for d in devices:
        graph.add_device(d)
    for u, v, lat in edges:
        graph.add_link(u, v, lat)

    print("\n[1] Graph berhasil dibangun.")
    print(f"    Jumlah node terdaftar : {len(graph.devices)}")

    # ── 2. Neighbors & Degree ────────────────────────────────
    print("\n[2] Tetangga dan derajat GATEWAY_0:")
    nbrs = graph.neighbors('GATEWAY_0')
    print(f"    degree = {graph.degree('GATEWAY_0')}")
    for dest, lat in nbrs:
        print(f"      → {dest}  (latensi {lat} ms)")

    # ── 3. DFS & Isolated Devices ────────────────────────────
    reachable = graph.dfs_reachable('GATEWAY_0')
    isolated  = graph.isolated_devices('GATEWAY_0')
    print(f"\n[3] DFS dari GATEWAY_0:")
    print(f"    Node terjangkau : {len(reachable)}")
    print(f"    Node terisolasi : {len(isolated)}")
    if isolated:
        print(f"    Detail          : {isolated}")
    else:
        print("    Semua perangkat terjangkau dari GATEWAY_0 ✓")

    # ── 4. Uji remove_link ───────────────────────────────────
    print("\n[4] Uji remove_link SERVER_1 ↔ GATEWAY_0:")
    # Cek dulu apakah edge ada
    before = [d for d, _ in graph.neighbors('SERVER_1')]
    graph.remove_link('SERVER_1', 'GATEWAY_0')
    after  = [d for d, _ in graph.neighbors('SERVER_1')]
    print(f"    Sebelum hapus (tetangga SERVER_1): {before}")
    print(f"    Setelah hapus (tetangga SERVER_1): {after}")

    # ── 5. Uji remove_device ─────────────────────────────────
    print("\n[5] Uji remove_device SENSOR_10:")
    graph.remove_device('SENSOR_10')
    ada = 'SENSOR_10' in graph.devices
    print(f"    SENSOR_10 masih di graph : {ada}")
    # Cek sisa edge ke SENSOR_10
    found = False
    for uid in graph.adj:
        curr = graph.adj[uid]
        while curr:
            if curr.dest == 'SENSOR_10':
                found = True
            curr = curr.next
    print(f"    Sisa edge ke SENSOR_10  : {found}")

    # ── 6. Laporan jaringan ───────────────────────────────────
    graph.laporan_jaringan()


# ════════════════════════════════════════════════════════════
if __name__ == '__main__':
    demo_modul1()