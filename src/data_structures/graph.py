"""
graph.py — Modul 1: Graph Topologi Jaringan IoT
Struktur: Adjacency List berbasis Linked List (EdgeNode)
Big-O  : add_device O(1), add_link O(1), neighbors O(deg(u)), DFS O(V+E)
"""

from typing import Optional, List, Tuple, Dict


# ── Edge Node untuk Adjacency List ───────────────────────────────────────────
class EdgeNode:
    def __init__(self, dest: str, latensi: int):
        self.dest    = dest
        self.latensi = latensi
        self.next: Optional['EdgeNode'] = None


# ── Graph Berbobot Undirected ─────────────────────────────────────────────────
class IoTGraph:
    """
    Graph berbobot (latensi ms) menggunakan adjacency list berbasis Linked List.
    Mendukung: add_device, add_link, remove_link, neighbors, degree, dfs_reachable.
    """

    def __init__(self):
        self.adj: Dict[str, Optional[EdgeNode]] = {}   # device_id -> EdgeNode head
        self.devices: Dict[str, object] = {}           # device_id -> Device object

    # ── Tambah perangkat ──────────────────────────────────────────────────────
    def add_device(self, device) -> None:
        """Big-O: O(1)."""
        if device.device_id not in self.adj:
            self.adj[device.device_id] = None
        self.devices[device.device_id] = device

    # ── Hapus perangkat ───────────────────────────────────────────────────────
    def remove_device(self, device_id: str) -> bool:
        """
        Hapus node beserta semua edge yang terhubung.
        Big-O: O(V+E) — harus scan semua adjacency list.
        """
        if device_id not in self.adj:
            return False

        # Hapus semua edge yang menuju device_id dari node lain
        for node in self.adj:
            if node == device_id:
                continue
            prev, cur = None, self.adj[node]
            while cur:
                if cur.dest == device_id:
                    if prev:
                        prev.next = cur.next
                    else:
                        self.adj[node] = cur.next
                    break
                prev, cur = cur, cur.next

        del self.adj[device_id]
        self.devices.pop(device_id, None)
        return True

    # ── Tambah koneksi (edge) ─────────────────────────────────────────────────
    def add_link(self, u: str, v: str, latensi: int) -> None:
        """Undirected — tambah di kedua arah. Big-O: O(1)."""
        for src, dst in [(u, v), (v, u)]:
            if src not in self.adj:
                self.adj[src] = None
            new_edge       = EdgeNode(dst, latensi)
            new_edge.next  = self.adj[src]
            self.adj[src]  = new_edge

    # ── Hapus koneksi (edge) ──────────────────────────────────────────────────
    def remove_link(self, u: str, v: str) -> bool:
        """Big-O: O(deg(u) + deg(v))."""
        removed = False
        for src, dst in [(u, v), (v, u)]:
            prev, cur = None, self.adj.get(src)
            while cur:
                if cur.dest == dst:
                    if prev:
                        prev.next = cur.next
                    else:
                        self.adj[src] = cur.next
                    removed = True
                    break
                prev, cur = cur, cur.next
        return removed

    # ── Tetangga sebuah node ──────────────────────────────────────────────────
    def neighbors(self, u: str) -> List[Tuple[str, int]]:
        """Kembalikan list (dest, latensi). Big-O: O(deg(u))."""
        result, cur = [], self.adj.get(u)
        while cur:
            result.append((cur.dest, cur.latensi))
            cur = cur.next
        return result

    # ── Degree sebuah node ────────────────────────────────────────────────────
    def degree(self, u: str) -> int:
        """Big-O: O(deg(u))."""
        count, cur = 0, self.adj.get(u)
        while cur:
            count += 1
            cur = cur.next
        return count

    # ── DFS — deteksi node yang terjangkau ────────────────────────────────────
    def dfs_reachable(self, source: str) -> set:
        """
        DFS iteratif menggunakan Python list sebagai stack.
        Big-O: O(V+E).
        """
        visited  = set()
        stack    = [source]
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            for dest, _ in self.neighbors(node):
                if dest not in visited:
                    stack.append(dest)
        return visited

    # ── Perangkat terisolasi dari gateway ─────────────────────────────────────
    def isolated_devices(self, gateway: str = 'GATEWAY_0') -> List[str]:
        """
        Kembalikan device yang tidak terjangkau dari gateway.
        Big-O: O(V+E).
        """
        reachable = self.dfs_reachable(gateway)
        return [d for d in self.adj if d not in reachable]

    # ── Info ──────────────────────────────────────────────────────────────────
    def __repr__(self) -> str:
        return (f'IoTGraph(nodes={len(self.adj)}, '
                f'edges={sum(self.degree(u) for u in self.adj) // 2})')
