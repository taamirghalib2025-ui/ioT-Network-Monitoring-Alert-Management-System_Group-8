import numpy as np
import random
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple

# — Seed tetap ————————————————————————————
np.random.seed(23)
random.seed(23)

DEVICE_TYPES = ['SENSOR', 'GATEWAY', 'SERVER']
ALERT_TYPES  = {'CRITICAL': 1, 'WARNING': 2, 'INFO': 3}


# — Dataclass ————————————————————————————
@dataclass
class Device:
    device_id: str
    tipe: str               # SENSOR / GATEWAY / SERVER
    status: str  = 'ONLINE'
    last_reading: float = 0.0


@dataclass
class Alert:
    alert_id: int
    device_id: str
    tipe: int               # 1=CRITICAL, 2=WARNING, 3=INFO
    pesan: str


# — Node Linked List (general) ————————————————————
class Node:
    def __init__(self, data):
        self.data = data
        self.next: Optional['Node'] = None


# ═══════════════════════════════════════════════════════════
#  MODUL 5 — Routing Optimal & Audit
# ═══════════════════════════════════════════════════════════

class RoutingOptimal:
    """
    Dijkstra untuk mencari rute latensi minimum dari GATEWAY_0
    ke setiap perangkat.
    Big-O: O(V²) dengan adjacency list sederhana.
    """

    def __init__(self):
        # graph: {node_id: [(tetangga, bobot), ...]}
        self.graph: Dict[str, List[Tuple[str, float]]] = {}

    # ── Tambah edge ──────────────────────────────────────
    def add_edge(self, u: str, v: str, bobot: float) -> None:
        """Tambahkan edge dua-arah ke graph."""
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append((v, bobot))
        self.graph[v].append((u, bobot))

    # ── Dijkstra ─────────────────────────────────────────
    def dijkstra(self, sumber: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
        """
        Jalankan Dijkstra dari node sumber.
        Return (jarak, prev) agar path bisa direkonstruksi.
        """
        INF = float('inf')
        dist: Dict[str, float] = {n: INF for n in self.graph}
        prev: Dict[str, Optional[str]] = {n: None for n in self.graph}

        if sumber not in dist:
            print(f"[ROUTING] Node '{sumber}' tidak ditemukan di graph.")
            return dist, prev

        dist[sumber] = 0.0
        belum_diproses = set(self.graph.keys())

        while belum_diproses:
            # Pilih node dengan jarak terkecil (Selection Sort mini)
            u = min(belum_diproses, key=lambda n: dist[n])
            if dist[u] == INF:
                break
            belum_diproses.remove(u)

            for (v, bobot) in self.graph.get(u, []):
                alt = dist[u] + bobot
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

        return dist, prev

    # ── Rekonstruksi jalur ────────────────────────────────
    def get_path(self, prev: Dict[str, Optional[str]],
                 tujuan: str) -> List[str]:
        """Kembalikan daftar node dari sumber ke tujuan."""
        jalur: List[str] = []
        node: Optional[str] = tujuan
        while node is not None:
            jalur.append(node)
            node = prev.get(node)
        jalur.reverse()
        return jalur

    # ── Identifikasi bottleneck ───────────────────────────
    def bottleneck_link(self, sumber: str) -> Optional[Tuple[str, str, float]]:
        """
        Cari edge dengan latensi tertinggi pada shortest-path tree
        (edge yang paling sering menjadi 'bottleneck').
        """
        dist, prev = self.dijkstra(sumber)
        max_bobot: float = -1.0
        bottleneck: Optional[Tuple[str, str, float]] = None

        for node, induk in prev.items():
            if induk is None:
                continue
            # Cari bobot edge (induk → node)
            for (v, w) in self.graph.get(induk, []):
                if v == node and w > max_bobot:
                    max_bobot = w
                    bottleneck = (induk, node, w)
        return bottleneck

    # ── Audit latensi dengan Selection Sort ───────────────
    def audit_latensi(self, sumber: str = 'GATEWAY_0') -> List[Tuple[str, float]]:
        """
        Urutkan semua perangkat berdasarkan latensi ke sumber
        menggunakan Selection Sort.
        Big-O: O(V²) — sesuai spesifikasi.
        """
        dist, _ = self.dijkstra(sumber)

        # Buat list (device, latensi) lalu Selection Sort
        items: List[Tuple[str, float]] = [
            (d, v) for d, v in dist.items() if v < float('inf')
        ]

        n = len(items)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if items[j][1] < items[min_idx][1]:
                    min_idx = j
            items[i], items[min_idx] = items[min_idx], items[i]

        return items

    # ── ROUTING <device> ──────────────────────────────────
    def routing(self, tujuan: str,
                sumber: str = 'GATEWAY_0') -> None:
        """
        Tampilkan rute terpendek dari sumber ke tujuan
        beserta total latensi. Big-O: O(V+E).
        """
        dist, prev = self.dijkstra(sumber)

        if tujuan not in dist or dist[tujuan] == float('inf'):
            print(f"[ROUTING] Tidak ada rute dari {sumber} ke {tujuan}.")
            return

        jalur = self.get_path(prev, tujuan)
        print(f"\n[ROUTING] {sumber} → {tujuan}")
        print(f"  Jalur   : {' → '.join(jalur)}")
        print(f"  Latensi : {dist[tujuan]:.1f} ms")

    # ── AUDIT_LATENSI ─────────────────────────────────────
    def tampilkan_audit(self, sumber: str = 'GATEWAY_0') -> None:
        """
        Tampilkan daftar perangkat terurut dari latensi terendah
        ke tertinggi (Selection Sort).
        """
        hasil = self.audit_latensi(sumber)
        print(f"\n[AUDIT_LATENSI] Urutan perangkat dari {sumber}:")
        for rank, (device, latensi) in enumerate(hasil, 1):
            print(f"  {rank:2}. {device:<20} {latensi:6.1f} ms")

    # ── LAPORAN_JARINGAN ──────────────────────────────────
    def laporan_jaringan(self, sumber: str = 'GATEWAY_0') -> None:
        """
        Tampilkan laporan lengkap: rute terpendek semua node,
        bottleneck link, dan audit latensi.
        """
        dist, prev = self.dijkstra(sumber)
        print(f"\n{'='*50}")
        print(f"  LAPORAN JARINGAN — Sumber: {sumber}")
        print(f"{'='*50}")

        # Rute terpendek tiap perangkat
        print("\n[Rute Terpendek]")
        for tujuan in sorted(dist):
            if tujuan == sumber:
                continue
            if dist[tujuan] == float('inf'):
                print(f"  {tujuan:<20} TIDAK TERJANGKAU")
            else:
                jalur = self.get_path(prev, tujuan)
                print(f"  {tujuan:<20} {dist[tujuan]:6.1f} ms  |  {' → '.join(jalur)}")

        # Bottleneck
        bn = self.bottleneck_link(sumber)
        print("\n[Bottleneck Link]")
        if bn:
            print(f"  {bn[0]} ↔ {bn[1]}  ({bn[2]:.1f} ms)")
        else:
            print("  Tidak ada.")

        # Audit latensi
        self.tampilkan_audit(sumber)
        print(f"{'='*50}\n")


# ═══════════════════════════════════════════════════════════
#  Demo / smoke-test
# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    router = RoutingOptimal()

    # Bangun topologi contoh (40 node IoT sesuai spesifikasi)
    # Gateway sebagai pusat
    for i in range(5):
        router.add_edge('GATEWAY_0', f'GATEWAY_{i+1}', round(random.uniform(5, 20), 1))

    for g in range(1, 6):
        for s in range(1, 9):
            router.add_edge(f'GATEWAY_{g}', f'SENSOR_{g}_{s}',
                            round(random.uniform(10, 60), 1))

    router.add_edge('GATEWAY_0', 'SERVER_0', round(random.uniform(2, 8), 1))

    # Perintah CLI
    router.routing('SENSOR_3_5')
    router.routing('SERVER_0')
    router.routing('GATEWAY_4')
    router.laporan_jaringan()