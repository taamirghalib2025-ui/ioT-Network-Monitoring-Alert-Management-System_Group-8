"""
CLI Monitoring - IoT Network Monitoring Alert Management System
Mata Kuliah: ELT60213 Algoritma dan Struktur Data
Team Based Project TA 2025/2026
"""

import time
from datetime import datetime


# ─────────────────────────────────────────────
#  DATA STRUCTURES (import dari modul lain)
#  Diasumsikan sudah ada: Graph, LinkedList, Stack, Queue, BST
# ─────────────────────────────────────────────

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node
        self.size += 1

    def to_list(self):
        result, cur = [], self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result


class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):   self._data.append(item)
    def pop(self):          return self._data.pop() if self._data else None
    def peek(self):         return self._data[-1] if self._data else None
    def is_empty(self):     return len(self._data) == 0
    def size(self):         return len(self._data)
    def to_list(self):      return list(reversed(self._data))


class Queue:
    def __init__(self):
        self._data = []

    def enqueue(self, item): self._data.append(item)
    def dequeue(self):       return self._data.pop(0) if self._data else None
    def is_empty(self):      return len(self._data) == 0
    def size(self):          return len(self._data)
    def to_list(self):       return list(self._data)


class BSTNode:
    def __init__(self, key, value):
        self.key   = key
        self.value = value
        self.left  = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if not node:
            return BSTNode(key, value)
        if key < node.key:
            node.left  = self._insert(node.left,  key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
        return node

    def search(self, key):
        node = self._search(self.root, key)
        return node.value if node else None

    def _search(self, node, key):
        if not node or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left,  key)
        return self._search(node.right, key)

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left,  result)
            result.append((node.key, node.value))
            self._inorder(node.right, result)


class Graph:
    """Adjacency-list graph dengan bobot latensi."""
    def __init__(self):
        self.adj = {}        # {node_id: [(neighbor_id, latency), ...]}
        self.devices = {}    # {node_id: device_info_dict}

    def add_device(self, device_id, tipe):
        if device_id not in self.adj:
            self.adj[device_id] = []
        self.devices[device_id] = {"id": device_id, "tipe": tipe}
        # O(1)

    def add_link(self, u, v, latensi):
        if u not in self.adj or v not in self.adj:
            return False
        self.adj[u].append((v, latensi))
        self.adj[v].append((u, latensi))
        return True
        # O(1)

    def get_neighbors(self, node_id):
        return self.adj.get(node_id, [])

    def dijkstra(self, src, dst):
        """
        Routing terpendek (latensi minimum) dengan Dijkstra.
        Big-O: O((V + E) log V)
        """
        import heapq
        dist = {n: float('inf') for n in self.adj}
        prev = {n: None for n in self.adj}
        dist[src] = 0
        heap = [(0, src)]

        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, w in self.adj.get(u, []):
                alt = dist[u] + w
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(heap, (alt, v))

        # Rekonstruksi path
        path, cur = [], dst
        while cur:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        if path and path[0] == src:
            return path, dist[dst]
        return [], float('inf')

    def bfs_isolasi(self, start):
        """
        BFS untuk menemukan semua node yang dapat dijangkau dari start.
        Node yang TIDAK terjangkau = terisolasi.
        Big-O: O(V + E)
        """
        visited = set()
        queue   = Queue()
        queue.enqueue(start)
        visited.add(start)

        while not queue.is_empty():
            node = queue.dequeue()
            for neighbor, _ in self.adj.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.enqueue(neighbor)

        terisolasi = [n for n in self.adj if n not in visited]
        return visited, terisolasi

    def audit_latensi(self):
        """
        Kumpulkan semua edge beserta latensinya.
        Big-O: O(E)
        """
        edges = []
        seen  = set()
        for u in self.adj:
            for v, w in self.adj[u]:
                key = tuple(sorted([u, v]))
                if key not in seen:
                    seen.add(key)
                    edges.append((u, v, w))
        return sorted(edges, key=lambda x: x[2], reverse=True)


# ─────────────────────────────────────────────
#  ALERT SYSTEM
# ─────────────────────────────────────────────

class AlertSystem:
    """
    Manajemen alert menggunakan Stack (history) + Queue (antrian proses) + BST (index).
    """
    def __init__(self):
        self.alert_queue   = Queue()       # antrian alert masuk
        self.alert_history = Stack()       # history alert terproses
        self.alert_index   = BST()         # index berdasarkan timestamp
        self._counter      = 0

    def alert_in(self, device, tipe, pesan):
        """
        Masukkan alert ke dalam antrian.
        Big-O: O(1)
        """
        self._counter += 1
        alert = {
            "id"       : self._counter,
            "device"   : device,
            "tipe"     : tipe,
            "pesan"    : pesan,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status"   : "PENDING",
        }
        self.alert_queue.enqueue(alert)
        self.alert_index.insert(self._counter, alert)
        return alert
        # O(log n) untuk BST insert

    def process_alert(self):
        """
        Proses alert pertama dari antrian → pindah ke history stack.
        Big-O: O(log n)
        """
        if self.alert_queue.is_empty():
            return None
        alert = self.alert_queue.dequeue()
        alert["status"] = "PROCESSED"
        self.alert_history.push(alert)
        return alert

    def history(self, n=10):
        """
        Tampilkan n alert terakhir dari history stack.
        Big-O: O(n)
        """
        return self.alert_history.to_list()[:n]


# ─────────────────────────────────────────────
#  CLI MONITORING
# ─────────────────────────────────────────────

class CLIMonitoring:
    def __init__(self):
        self.graph  = Graph()
        self.alerts = AlertSystem()
        self.log    = LinkedList()   # log semua aktivitas CLI

    # ── helpers ──────────────────────────────

    def _log(self, msg):
        entry = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
        self.log.append(entry)

    def _print_header(self, title):
        width = 56
        print("\n" + "═" * width)
        print(f"  {title}")
        print("═" * width)

    def _big_o(self, label):
        print(f"  📊 Big-O: {label}")

    # ── perintah utama ────────────────────────

    def add_device(self, device_id, tipe):
        """ADD_DEVICE <id> <tipe>  →  O(1)"""
        self._print_header(f"ADD_DEVICE: {device_id} [{tipe}]")
        if device_id in self.graph.adj:
            print(f"  ⚠  Device '{device_id}' sudah ada.")
        else:
            self.graph.add_device(device_id, tipe)
            print(f"  ✔  Device '{device_id}' (tipe: {tipe}) berhasil ditambahkan.")
            self._log(f"ADD_DEVICE {device_id} {tipe}")
        self._big_o("O(1)")

    def add_link(self, u, v, latensi):
        """ADD_LINK <u> <v> <latensi>  →  O(1)"""
        self._print_header(f"ADD_LINK: {u} ↔ {v}  (latensi: {latensi} ms)")
        ok = self.graph.add_link(u, v, latensi)
        if ok:
            print(f"  ✔  Link {u} ↔ {v} dengan latensi {latensi} ms ditambahkan.")
            self._log(f"ADD_LINK {u} {v} {latensi}")
        else:
            print(f"  ✖  Gagal: salah satu device tidak ditemukan.")
        self._big_o("O(1)")

    def alert_in(self, device, tipe, pesan):
        """ALERT_IN <device> <type> <pesan>  →  O(log n)"""
        self._print_header(f"ALERT_IN: {device} [{tipe}]")
        alert = self.alerts.alert_in(device, tipe, pesan)
        print(f"  ✔  Alert #{alert['id']} masuk ke antrian.")
        print(f"     Device  : {device}")
        print(f"     Tipe    : {tipe}")
        print(f"     Pesan   : {pesan}")
        print(f"     Waktu   : {alert['timestamp']}")
        self._log(f"ALERT_IN {device} {tipe}")
        self._big_o("O(log n) — BST insert untuk index")

    def process_alert(self):
        """PROCESS_ALERT  →  O(log n)"""
        self._print_header("PROCESS_ALERT")
        alert = self.alerts.process_alert()
        if alert:
            print(f"  ✔  Alert #{alert['id']} diproses.")
            print(f"     Device : {alert['device']}")
            print(f"     Pesan  : {alert['pesan']}")
            print(f"     Status : {alert['status']}")
            self._log(f"PROCESS_ALERT #{alert['id']}")
        else:
            print("  ℹ  Tidak ada alert dalam antrian.")
        self._big_o("O(log n)")

    def history(self, n=5):
        """HISTORY  →  O(n)"""
        self._print_header("HISTORY ALERT")
        recs = self.alerts.history(n)
        if not recs:
            print("  ℹ  Belum ada alert yang diproses.")
        for r in recs:
            status_icon = "✔" if r["status"] == "PROCESSED" else "⏳"
            print(f"  {status_icon} #{r['id']:>3}  {r['timestamp']}  {r['device']:<12}  {r['tipe']:<10}  {r['pesan']}")
        self._big_o("O(n)")

    def isolasi(self, device_id):
        """ISOLASI <device>  →  O(V + E)"""
        self._print_header(f"ISOLASI: mulai dari {device_id}")
        if device_id not in self.graph.adj:
            print(f"  ✖  Device '{device_id}' tidak ditemukan.")
            return
        terjangkau, terisolasi = self.graph.bfs_isolasi(device_id)
        print(f"  ✔  Terjangkau ({len(terjangkau)}) : {', '.join(sorted(terjangkau))}")
        if terisolasi:
            print(f"  ⚠  Terisolasi  ({len(terisolasi)}) : {', '.join(sorted(terisolasi))}")
        else:
            print("  ✔  Semua device terhubung, tidak ada yang terisolasi.")
        self._log(f"ISOLASI {device_id} → {len(terisolasi)} terisolasi")
        self._big_o("O(V + E) — BFS")

    def routing(self, device_id):
        """ROUTING <device>  →  O((V+E) log V)"""
        self._print_header(f"ROUTING: jalur terpendek dari {device_id}")
        if device_id not in self.graph.adj:
            print(f"  ✖  Device '{device_id}' tidak ditemukan.")
            return
        targets = [n for n in self.graph.adj if n != device_id]
        if not targets:
            print("  ℹ  Tidak ada device lain.")
            return
        for dst in targets:
            path, cost = self.graph.dijkstra(device_id, dst)
            if path:
                print(f"  → {dst:<12}  path: {' → '.join(path):<40}  total: {cost} ms")
            else:
                print(f"  → {dst:<12}  ✖ Tidak terjangkau")
        self._log(f"ROUTING {device_id}")
        self._big_o("O((V + E) log V) — Dijkstra")

    def audit_latensi(self):
        """AUDIT_LATENSI  →  O(E log E)"""
        self._print_header("AUDIT LATENSI")
        edges = self.graph.audit_latensi()
        if not edges:
            print("  ℹ  Belum ada link yang terdaftar.")
            return
        print(f"  {'FROM':<12} {'TO':<12} {'LATENSI':>10}")
        print("  " + "-" * 36)
        for u, v, w in edges:
            bar = "█" * min(int(w / 5), 20)
            print(f"  {u:<12} {v:<12} {w:>8} ms  {bar}")
        self._log("AUDIT_LATENSI")
        self._big_o("O(E log E) — sorting edges")

    def laporan_jaringan(self):
        """LAPORAN_JARINGAN  →  O(V + E)"""
        self._print_header("LAPORAN JARINGAN")
        devices = self.graph.devices
        print(f"  Total Device : {len(devices)}")
        print(f"  Total Alert  : {self.alerts._counter}")
        print(f"  Alert Pending: {self.alerts.alert_queue.size()}")
        print(f"  Alert Selesai: {len(self.alerts.alert_history.to_list())}")
        print()
        print(f"  {'ID':<14} {'TIPE':<12} {'TETANGGA'}")
        print("  " + "-" * 50)
        for dev_id, info in devices.items():
            neighbors = ", ".join(
                f"{n}({w}ms)" for n, w in self.graph.get_neighbors(dev_id)
            )
            print(f"  {dev_id:<14} {info['tipe']:<12} {neighbors or '-'}")
        self._log("LAPORAN_JARINGAN")
        self._big_o("O(V + E)")

    # ── REPL ─────────────────────────────────

    def run(self):
        banner = """
╔══════════════════════════════════════════════════════╗
║   IoT Network Monitoring & Alert Management System   ║
║   ELT60213 Algoritma dan Struktur Data — Group 8     ║
╚══════════════════════════════════════════════════════╝
Ketik HELP untuk daftar perintah, EXIT untuk keluar.
"""
        print(banner)

        commands = {
            "ADD_DEVICE"      : "ADD_DEVICE <id> <tipe>",
            "ADD_LINK"        : "ADD_LINK <u> <v> <latensi>",
            "ALERT_IN"        : "ALERT_IN <device> <tipe> <pesan>",
            "PROCESS_ALERT"   : "PROCESS_ALERT",
            "HISTORY"         : "HISTORY [n]",
            "ISOLASI"         : "ISOLASI <device>",
            "ROUTING"         : "ROUTING <device>",
            "AUDIT_LATENSI"   : "AUDIT_LATENSI",
            "LAPORAN_JARINGAN": "LAPORAN_JARINGAN",
            "HELP"            : "HELP",
            "EXIT"            : "EXIT",
        }

        while True:
            try:
                raw = input("\n> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nKeluar dari CLI.")
                break

            if not raw:
                continue

            parts = raw.split(maxsplit=3)
            cmd   = parts[0].upper()

            if cmd == "EXIT":
                print("Sampai jumpa!")
                break

            elif cmd == "HELP":
                self._print_header("DAFTAR PERINTAH")
                for c, usage in commands.items():
                    print(f"  {usage}")

            elif cmd == "ADD_DEVICE":
                if len(parts) < 3:
                    print("  Penggunaan: ADD_DEVICE <id> <tipe>")
                else:
                    self.add_device(parts[1], parts[2])

            elif cmd == "ADD_LINK":
                if len(parts) < 4:
                    print("  Penggunaan: ADD_LINK <u> <v> <latensi>")
                else:
                    try:
                        self.add_link(parts[1], parts[2], int(parts[3]))
                    except ValueError:
                        print("  ✖  Latensi harus berupa angka.")

            elif cmd == "ALERT_IN":
                if len(parts) < 4:
                    print("  Penggunaan: ALERT_IN <device> <tipe> <pesan>")
                else:
                    self.alert_in(parts[1], parts[2], parts[3])

            elif cmd == "PROCESS_ALERT":
                self.process_alert()

            elif cmd == "HISTORY":
                n = int(parts[1]) if len(parts) > 1 else 5
                self.history(n)

            elif cmd == "ISOLASI":
                if len(parts) < 2:
                    print("  Penggunaan: ISOLASI <device>")
                else:
                    self.isolasi(parts[1])

            elif cmd == "ROUTING":
                if len(parts) < 2:
                    print("  Penggunaan: ROUTING <device>")
                else:
                    self.routing(parts[1])

            elif cmd == "AUDIT_LATENSI":
                self.audit_latensi()

            elif cmd == "LAPORAN_JARINGAN":
                self.laporan_jaringan()

            else:
                print(f"  ✖  Perintah '{cmd}' tidak dikenal. Ketik HELP.")


# ─────────────────────────────────────────────
#  DEMO OTOMATIS (opsional, untuk testing)
# ─────────────────────────────────────────────

def demo():
    cli = CLIMonitoring()

    print("=== DEMO OTOMATIS ===")

    cli.add_device("R1", "Router")
    cli.add_device("R2", "Router")
    cli.add_device("SW1", "Switch")
    cli.add_device("PC1", "EndDevice")
    cli.add_device("PC2", "EndDevice")

    cli.add_link("R1",  "R2",  10)
    cli.add_link("R1",  "SW1", 5)
    cli.add_link("SW1", "PC1", 2)
    cli.add_link("SW1", "PC2", 3)

    cli.alert_in("PC1",  "HIGH_LATENCY",   "Latensi melebihi 100ms")
    cli.alert_in("R2",   "PACKET_LOSS",    "Packet loss 15%")
    cli.alert_in("SW1",  "DOWN",           "Interface Gi0/1 down")

    cli.process_alert()
    cli.process_alert()

    cli.history()
    cli.isolasi("R1")
    cli.routing("R1")
    cli.audit_latensi()
    cli.laporan_jaringan()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        CLIMonitoring().run()