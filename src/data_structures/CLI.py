"""
CLI.py — IoT Network Monitoring & Alert Management System
Lokasi  : src/data_structures/CLI.py
Mata Kuliah : ELT60213 Algoritma dan Struktur Data
Team Based Project TA 2025/2026 — Group 8
"""

from datetime import datetime

# Import dari modul data struktur yang sudah ada di repo
from bst     import BST
from graph   import Graph
from queue   import Queue
from stack   import Stack
from routing import routing   # fungsi Dijkstra / shortest-path


# ══════════════════════════════════════════════
#  ALERT SYSTEM
#  Queue  → antrian alert masuk       O(1) enqueue/dequeue
#  Stack  → history alert terproses   O(1) push/pop
#  BST    → index/search by alert-id  O(log n)
# ══════════════════════════════════════════════

class AlertSystem:
    def __init__(self):
        self.pending  = Queue()   # alert masuk, belum diproses
        self.history  = Stack()   # alert sudah diproses
        self.index    = BST()     # BST: key=alert_id, value=alert_dict
        self._counter = 0

    # ── ALERT_IN ─────────────────────────────
    def alert_in(self, device, tipe, pesan):
        """
        Masukkan alert baru ke antrian.
        Big-O : O(log n)  — BST insert untuk indexing
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
        self.pending.enqueue(alert)
        self.index.insert(self._counter, alert)
        return alert

    # ── PROCESS_ALERT ────────────────────────
    def process_alert(self):
        """
        Ambil alert pertama dari antrian → simpan ke history stack.
        Big-O : O(1)
        """
        if self.pending.is_empty():
            return None
        alert          = self.pending.dequeue()
        alert["status"] = "PROCESSED"
        self.history.push(alert)
        return alert

    # ── HISTORY ──────────────────────────────
    def get_history(self, n=10):
        """
        Kembalikan n alert terakhir dari history stack.
        Big-O : O(n)
        """
        return self.history.to_list()[:n]


# ══════════════════════════════════════════════
#  CLI MONITORING
# ══════════════════════════════════════════════

class CLIMonitoring:
    def __init__(self):
        self.graph  = Graph()
        self.alerts = AlertSystem()

    # ── banner helpers ────────────────────────

    @staticmethod
    def _header(title):
        w = 58
        print("\n" + "═" * w)
        print(f"  {title}")
        print("═" * w)

    @staticmethod
    def _big_o(label):
        print(f"  📊 Big-O: {label}")

    # ══════════════════════════════════════════
    #  ADD_DEVICE <id> <tipe>
    #  Big-O : O(1)
    # ══════════════════════════════════════════
    def add_device(self, device_id: str, tipe: str):
        self._header(f"ADD_DEVICE  {device_id}  [{tipe}]")

        if self.graph.has_node(device_id):
            print(f"  ⚠  Device '{device_id}' sudah terdaftar.")
        else:
            self.graph.add_node(device_id, tipe)
            print(f"  ✔  Device '{device_id}' (tipe: {tipe}) ditambahkan.")

        self._big_o("O(1)")

    # ══════════════════════════════════════════
    #  ADD_LINK <u> <v> <latensi>
    #  Big-O : O(1)
    # ══════════════════════════════════════════
    def add_link(self, u: str, v: str, latensi: int):
        self._header(f"ADD_LINK  {u} ↔ {v}  (latensi: {latensi} ms)")

        ok = self.graph.add_edge(u, v, latensi)
        if ok:
            print(f"  ✔  Link {u} ↔ {v} berhasil ditambahkan.")
        else:
            print(f"  ✖  Gagal: device '{u}' atau '{v}' tidak ditemukan.")

        self._big_o("O(1)")

    # ══════════════════════════════════════════
    #  ALERT_IN <device> <type> <pesan>
    #  Big-O : O(log n)
    # ══════════════════════════════════════════
    def alert_in(self, device: str, tipe: str, pesan: str):
        self._header(f"ALERT_IN  {device}  [{tipe}]")

        alert = self.alerts.alert_in(device, tipe, pesan)
        print(f"  ✔  Alert #{alert['id']} masuk ke antrian.")
        print(f"     Device  : {alert['device']}")
        print(f"     Tipe    : {alert['tipe']}")
        print(f"     Pesan   : {alert['pesan']}")
        print(f"     Waktu   : {alert['timestamp']}")

        self._big_o("O(log n)  — BST insert untuk indexing")

    # ══════════════════════════════════════════
    #  PROCESS_ALERT
    #  Big-O : O(1)
    # ══════════════════════════════════════════
    def process_alert(self):
        self._header("PROCESS_ALERT")

        alert = self.alerts.process_alert()
        if alert:
            print(f"  ✔  Alert #{alert['id']} berhasil diproses.")
            print(f"     Device : {alert['device']}")
            print(f"     Pesan  : {alert['pesan']}")
            print(f"     Status : {alert['status']}")
        else:
            print("  ℹ  Tidak ada alert dalam antrian.")

        self._big_o("O(1)")

    # ══════════════════════════════════════════
    #  HISTORY [n]
    #  Big-O : O(n)
    # ══════════════════════════════════════════
    def show_history(self, n: int = 5):
        self._header("HISTORY ALERT")

        records = self.alerts.get_history(n)
        if not records:
            print("  ℹ  Belum ada alert yang diproses.")
        else:
            print(f"  {'#':>4}  {'WAKTU':19}  {'DEVICE':<12}  {'TIPE':<14}  PESAN")
            print("  " + "─" * 70)
            for r in records:
                icon = "✔" if r["status"] == "PROCESSED" else "⏳"
                print(f"  {icon}{r['id']:>3}  {r['timestamp']}  "
                      f"{r['device']:<12}  {r['tipe']:<14}  {r['pesan']}")

        self._big_o("O(n)")

    # ══════════════════════════════════════════
    #  ISOLASI <device>
    #  Big-O : O(V + E)  — BFS
    # ══════════════════════════════════════════
    def isolasi(self, device_id: str):
        self._header(f"ISOLASI  [{device_id}]")

        if not self.graph.has_node(device_id):
            print(f"  ✖  Device '{device_id}' tidak ditemukan.")
            self._big_o("O(V + E)")
            return

        reachable   = self.graph.bfs(device_id)          # set of node ids
        all_nodes   = set(self.graph.get_all_nodes())
        isolated    = sorted(all_nodes - reachable)
        reachable_s = sorted(reachable)

        print(f"  ✔  Terjangkau  ({len(reachable_s):>3}) : {', '.join(reachable_s)}")
        if isolated:
            print(f"  ⚠  Terisolasi  ({len(isolated):>3}) : {', '.join(isolated)}")
        else:
            print("  ✔  Semua device terhubung — tidak ada yang terisolasi.")

        self._big_o("O(V + E)  — BFS")

    # ══════════════════════════════════════════
    #  ROUTING <device>
    #  Big-O : O((V + E) log V)  — Dijkstra
    # ══════════════════════════════════════════
    def routing_device(self, device_id: str):
        self._header(f"ROUTING  [{device_id}]")

        if not self.graph.has_node(device_id):
            print(f"  ✖  Device '{device_id}' tidak ditemukan.")
            self._big_o("O((V + E) log V)")
            return

        targets = [n for n in self.graph.get_all_nodes() if n != device_id]
        if not targets:
            print("  ℹ  Tidak ada device lain dalam jaringan.")
            self._big_o("O((V + E) log V)")
            return

        print(f"  {'TUJUAN':<14}  {'PATH':<40}  TOTAL LATENSI")
        print("  " + "─" * 65)
        for dst in sorted(targets):
            path, cost = routing(self.graph, device_id, dst)
            if path:
                path_str = " → ".join(path)
                print(f"  {dst:<14}  {path_str:<40}  {cost} ms")
            else:
                print(f"  {dst:<14}  ✖ Tidak terjangkau")

        self._big_o("O((V + E) log V)  — Dijkstra")

    # ══════════════════════════════════════════
    #  AUDIT_LATENSI
    #  Big-O : O(E log E)
    # ══════════════════════════════════════════
    def audit_latensi(self):
        self._header("AUDIT LATENSI")

        edges = self.graph.get_all_edges()   # list of (u, v, weight)
        if not edges:
            print("  ℹ  Belum ada link yang terdaftar.")
            self._big_o("O(E log E)")
            return

        edges_sorted = sorted(edges, key=lambda x: x[2], reverse=True)

        max_w = edges_sorted[0][2] if edges_sorted else 1
        print(f"  {'FROM':<14}  {'TO':<14}  {'LATENSI':>10}  BAR")
        print("  " + "─" * 55)
        for u, v, w in edges_sorted:
            bar = "█" * max(1, int(w / max_w * 20))
            print(f"  {u:<14}  {v:<14}  {w:>8} ms  {bar}")

        self._big_o("O(E log E)  — sorting edges")

    # ══════════════════════════════════════════
    #  LAPORAN_JARINGAN
    #  Big-O : O(V + E)
    # ══════════════════════════════════════════
    def laporan_jaringan(self):
        self._header("LAPORAN JARINGAN")

        nodes = self.graph.get_all_nodes()
        edges = self.graph.get_all_edges()

        print(f"  Total Device  : {len(nodes)}")
        print(f"  Total Link    : {len(edges)}")
        print(f"  Total Alert   : {self.alerts._counter}")
        print(f"  Alert Pending : {self.alerts.pending.size()}")
        print(f"  Alert Selesai : {len(self.alerts.history.to_list())}")
        print()
        print(f"  {'DEVICE ID':<14}  {'TIPE':<12}  KONEKSI (neighbor · latensi)")
        print("  " + "─" * 58)
        for node_id in sorted(nodes):
            tipe  = self.graph.get_node_type(node_id)
            nbrs  = self.graph.get_neighbors(node_id)
            nbr_s = ", ".join(f"{n}·{w}ms" for n, w in nbrs) or "—"
            print(f"  {node_id:<14}  {tipe:<12}  {nbr_s}")

        self._big_o("O(V + E)")


# ══════════════════════════════════════════════
#  REPL  —  interactive command loop
# ══════════════════════════════════════════════

HELP_TEXT = """
  Perintah yang tersedia:
  ─────────────────────────────────────────────────────
  ADD_DEVICE      <id> <tipe>
  ADD_LINK        <u> <v> <latensi>
  ALERT_IN        <device> <tipe> <pesan>
  PROCESS_ALERT
  HISTORY         [n]
  ISOLASI         <device>
  ROUTING         <device>
  AUDIT_LATENSI
  LAPORAN_JARINGAN
  HELP
  EXIT
"""

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║   IoT Network Monitoring & Alert Management System       ║
║   ELT60213 Algoritma dan Struktur Data  —  Group 8       ║
╚══════════════════════════════════════════════════════════╝
  Ketik HELP untuk daftar perintah, EXIT untuk keluar.
""")

    cli = CLIMonitoring()

    while True:
        try:
            raw = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nKeluar.")
            break

        if not raw:
            continue

        parts = raw.split(maxsplit=3)
        cmd   = parts[0].upper()

        try:
            if cmd == "EXIT":
                print("Sampai jumpa!")
                break

            elif cmd == "HELP":
                print(HELP_TEXT)

            elif cmd == "ADD_DEVICE":
                if len(parts) < 3:
                    print("  Penggunaan: ADD_DEVICE <id> <tipe>")
                else:
                    cli.add_device(parts[1], parts[2])

            elif cmd == "ADD_LINK":
                if len(parts) < 4:
                    print("  Penggunaan: ADD_LINK <u> <v> <latensi>")
                else:
                    cli.add_link(parts[1], parts[2], int(parts[3]))

            elif cmd == "ALERT_IN":
                if len(parts) < 4:
                    print("  Penggunaan: ALERT_IN <device> <tipe> <pesan>")
                else:
                    cli.alert_in(parts[1], parts[2], parts[3])

            elif cmd == "PROCESS_ALERT":
                cli.process_alert()

            elif cmd == "HISTORY":
                n = int(parts[1]) if len(parts) > 1 else 5
                cli.show_history(n)

            elif cmd == "ISOLASI":
                if len(parts) < 2:
                    print("  Penggunaan: ISOLASI <device>")
                else:
                    cli.isolasi(parts[1])

            elif cmd == "ROUTING":
                if len(parts) < 2:
                    print("  Penggunaan: ROUTING <device>")
                else:
                    cli.routing_device(parts[1])

            elif cmd == "AUDIT_LATENSI":
                cli.audit_latensi()

            elif cmd == "LAPORAN_JARINGAN":
                cli.laporan_jaringan()

            else:
                print(f"  ✖  Perintah tidak dikenal: '{cmd}'. Ketik HELP.")

        except ValueError as e:
            print(f"  ✖  Input tidak valid: {e}")
        except Exception as e:
            print(f"  ✖  Error: {e}")


if __name__ == "__main__":
    main()