import numpy as np
import random
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from graph import IoTGraph
from queue import AlertPriorityQueue
from bst   import BSTDeviceRegistry
from stack import AlertStack, Alert

np.random.seed(23)
random.seed(23)

ALERT_TYPES  = {'CRITICAL': 1, 'WARNING': 2, 'INFO': 3}
ALERT_LABELS = {1: 'CRITICAL', 2: 'WARNING', 3: 'INFO'}
GATEWAY      = 'GATEWAY_0'


@dataclass
class Device:
    device_id: str
    tipe: str
    status: str = 'ONLINE'
    last_reading: float = 0.0


# ── Dijkstra ─────────────────────────────────────────────────
def dijkstra(graph, source):
    """Big-O: O(V^2 + E)"""
    INF = float('inf')
    dist   = {v: INF  for v in graph.adj}
    parent = {v: None for v in graph.adj}
    visited = set()
    dist[source] = 0

    for _ in range(len(graph.adj)):
        u = min((v for v in graph.adj if v not in visited), key=lambda v: dist[v], default=None)
        if u is None or dist[u] == INF:
            break
        visited.add(u)
        for nbr, lat in graph.neighbors(u):
            if dist[u] + lat < dist[nbr]:
                dist[nbr]   = dist[u] + lat
                parent[nbr] = u

    return dist, parent


def get_path(parent, target):
    path, cur = [], target
    while cur:
        path.append(cur)
        cur = parent.get(cur)
    return list(reversed(path))


# ── Selection Sort Linked List (untuk AUDIT_LATENSI) ─────────
class LatNode:
    def __init__(self, device_id, latensi):
        self.device_id = device_id
        self.latensi   = latensi
        self.next      = None


def selection_sort_ll(head):
    """Big-O: O(n^2)"""
    cur = head
    while cur:
        mn = cur
        s  = cur.next
        while s:
            if s.latensi < mn.latensi:
                mn = s
            s = s.next
        cur.device_id, mn.device_id = mn.device_id, cur.device_id
        cur.latensi,   mn.latensi   = mn.latensi,   cur.latensi
        cur = cur.next
    return head


# ── Generator jaringan awal ───────────────────────────────────
def generate_iot_network(n=40, extra=20, seed=23):
    rng = np.random.default_rng(seed)
    devs = [Device('GATEWAY_0', 'GATEWAY')]
    for i in range(1, 5):
        devs.append(Device(f'SERVER_{i}', 'SERVER'))
    for i in range(5, n):
        devs.append(Device(f'SENSOR_{i}', 'SENSOR', last_reading=float(rng.uniform(0, 100))))

    perm  = rng.permutation(n)
    edges = []
    for i in range(1, n):
        edges.append((devs[perm[i-1]].device_id, devs[perm[i]].device_id, int(rng.integers(5, 200))))
    for _ in range(extra):
        i, j = rng.choice(n, 2, replace=False)
        edges.append((devs[i].device_id, devs[j].device_id, int(rng.integers(5, 200))))

    return devs, edges


# ── CLI ───────────────────────────────────────────────────────
def main():
    graph   = IoTGraph()
    bst     = BSTDeviceRegistry()
    queue   = AlertPriorityQueue()
    stacks: Dict[str, AlertStack] = {}
    counter = [0]

    devs, edges = generate_iot_network()
    for d in devs:
        graph.add_device(d)
        bst.insert(d.device_id, d.tipe, d.status, d.last_reading)
        stacks[d.device_id] = AlertStack(kapasitas=20)
    for u, v, lat in edges:
        graph.add_link(u, v, lat)

    print("IoT Monitoring System | Ketik BANTUAN untuk daftar perintah")

    while True:
        try:
            raw = input("IoT> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("Keluar."); break

        if not raw:
            continue

        tokens = raw.split()
        cmd    = tokens[0].upper()
        args   = tokens[1:]

        # ── BANTUAN ──────────────────────────────────────────
        if cmd == 'BANTUAN':
            print("""
Perintah yang tersedia:
  ADD_DEVICE <id> <tipe>              Big-O: O(1)
  ADD_LINK <u> <v> <latensi>          Big-O: O(1)
  REMOVE_LINK <u> <v>                 Big-O: O(deg(u)+deg(v))
  ALERT_IN <device> <type> <pesan>    Big-O: enqueue O(n), push O(1)
  PROCESS_ALERT                       Big-O: O(1)
  PENDING_ALERTS                      Big-O: O(n)
  HISTORY <device_id>                 Big-O: O(n)
  ROLLBACK_STATUS <device_id>         Big-O: O(n)
  ISOLASI                             Big-O: O(V+E)
  ROUTING <device>                    Big-O: O(V^2+E)
  AUDIT_LATENSI                       Big-O: O(V^2+E) + O(n^2)
  LAPORAN_JARINGAN
  STATUS <device_id>                  Big-O: O(log n)
  KELUAR""")

        # ── ADD_DEVICE ───────────────────────────────────────
        elif cmd == 'ADD_DEVICE':
            if len(args) < 2:
                print("Gunakan: ADD_DEVICE <id> <tipe>"); continue
            did, tipe = args[0].upper(), args[1].upper()
            if tipe not in ('SENSOR', 'GATEWAY', 'SERVER'):
                print("Tipe harus: SENSOR / GATEWAY / SERVER"); continue
            d = Device(did, tipe)
            graph.add_device(d)
            bst.insert(did, tipe)
            stacks[did] = AlertStack(kapasitas=20)
            print(f"[Big-O: O(1) graph + O(log n) BST] Perangkat '{did}' ({tipe}) ditambahkan.")

        # ── ADD_LINK ─────────────────────────────────────────
        elif cmd == 'ADD_LINK':
            if len(args) < 3:
                print("Gunakan: ADD_LINK <u> <v> <latensi>"); continue
            u, v = args[0].upper(), args[1].upper()
            try: lat = int(args[2])
            except: print("Latensi harus integer."); continue
            if u not in graph.adj or v not in graph.adj:
                print("Perangkat tidak ditemukan."); continue
            graph.add_link(u, v, lat)
            print(f"[Big-O: O(1)] Koneksi {u} <-> {v} ({lat} ms) ditambahkan.")

        # ── REMOVE_LINK ──────────────────────────────────────
        elif cmd == 'REMOVE_LINK':
            if len(args) < 2:
                print("Gunakan: REMOVE_LINK <u> <v>"); continue
            u, v = args[0].upper(), args[1].upper()
            ok = graph.remove_link(u, v)
            print(f"[Big-O: O(deg(u)+deg(v))] {'Koneksi dihapus.' if ok else 'Koneksi tidak ditemukan.'}")

        # ── ALERT_IN ─────────────────────────────────────────
        elif cmd == 'ALERT_IN':
            if len(args) < 3:
                print("Gunakan: ALERT_IN <device> <type> <pesan>"); continue
            did, tipe_str, pesan = args[0].upper(), args[1].upper(), ' '.join(args[2:])
            if did not in graph.adj:
                print(f"Perangkat '{did}' tidak ditemukan."); continue
            if tipe_str not in ALERT_TYPES:
                print("Tipe alert: CRITICAL / WARNING / INFO"); continue
            counter[0] += 1
            a = Alert(counter[0], did, ALERT_TYPES[tipe_str], pesan, time.time())
            queue.enqueue(a)
            stacks[did].push(a)
            print(f"[Big-O: enqueue O(n), push O(1)] Alert #{a.alert_id} ({tipe_str}) dari {did} masuk queue. Total pending: {len(queue)}")

        # ── PROCESS_ALERT ────────────────────────────────────
        elif cmd == 'PROCESS_ALERT':
            a = queue.dequeue()
            if a is None:
                print("[Big-O: O(1)] Queue kosong."); continue
            print(f"[Big-O: O(1)] Proses Alert #{a.alert_id} | {ALERT_LABELS[a.tipe]} | {a.device_id} | {a.pesan}")
            if a.tipe == 1:
                bst.update_status(a.device_id, 'OFFLINE')
                print(f"  -> Status '{a.device_id}' diubah ke OFFLINE (CRITICAL alert)")
            print(f"  Sisa queue: {len(queue)}")

        # ── PENDING_ALERTS ───────────────────────────────────
        elif cmd == 'PENDING_ALERTS':
            items = queue.pending_alerts()
            print(f"[Big-O: O(n)] {len(items)} alert menunggu:")
            for a in items:
                print(f"  #{a.alert_id} | {ALERT_LABELS[a.tipe]:<8} | {a.device_id:<15} | {a.pesan}")

        # ── HISTORY ──────────────────────────────────────────
        elif cmd == 'HISTORY':
            if not args:
                print("Gunakan: HISTORY <device_id>"); continue
            did = args[0].upper()
            if did not in stacks:
                print(f"Perangkat '{did}' tidak ditemukan."); continue
            hist = stacks[did].to_list()
            print(f"[Big-O: O(n)] Riwayat alert '{did}' ({len(hist)} tersimpan):")
            for i, a in enumerate(hist, 1):
                print(f"  {i}. #{a.alert_id} | {ALERT_LABELS[a.tipe]:<8} | {a.pesan}")

        # ── ROLLBACK_STATUS ──────────────────────────────────
        elif cmd == 'ROLLBACK_STATUS':
            if not args:
                print("Gunakan: ROLLBACK_STATUS <device_id>"); continue
            did = args[0].upper()
            if did not in stacks:
                print(f"Perangkat '{did}' tidak ditemukan."); continue
            stacks[did].pop()
            hist   = stacks[did].to_list()
            status = 'OFFLINE' if hist and hist[0].tipe == 1 else 'ONLINE'
            bst.update_status(did, status)
            print(f"[Big-O: O(n) stack + O(log n) BST] Status '{did}' di-rollback -> {status}")

        # ── STATUS ───────────────────────────────────────────
        elif cmd == 'STATUS':
            if not args:
                print("Gunakan: STATUS <device_id>"); continue
            did  = args[0].upper()
            node = bst.search(did)
            if node is None:
                print(f"[Big-O: O(log n)] Perangkat '{did}' tidak ditemukan di BST."); continue
            print(f"[Big-O: O(log n)] {node.device_id} | {node.tipe} | {node.status} | reading={node.last_reading:.2f}")

        # ── ISOLASI ──────────────────────────────────────────
        elif cmd == 'ISOLASI':
            isolated = graph.isolated_devices(GATEWAY)
            print(f"[Big-O: O(V+E)] Perangkat terisolasi dari {GATEWAY}: {len(isolated)}")
            for d in isolated:
                print(f"  - {d}")

        # ── ROUTING ──────────────────────────────────────────
        elif cmd == 'ROUTING':
            if not args:
                print("Gunakan: ROUTING <device_id>"); continue
            target = args[0].upper()
            if target not in graph.adj:
                print(f"Perangkat '{target}' tidak ditemukan."); continue
            dist, parent = dijkstra(graph, GATEWAY)
            if dist[target] == float('inf'):
                print(f"[Big-O: O(V^2+E)] '{target}' tidak terjangkau."); continue
            path = get_path(parent, target)
            print(f"[Big-O: O(V^2+E)] Rute ke {target}: {' -> '.join(path)}")
            print(f"  Total latensi: {dist[target]} ms")
            # bottleneck
            hops = []
            for i in range(len(path)-1):
                u, v = path[i], path[i+1]
                lat  = next((l for d, l in graph.neighbors(u) if d == v), 0)
                hops.append((u, v, lat))
                print(f"  Hop {i+1}: {u} -> {v} ({lat} ms)")
            if hops:
                b = max(hops, key=lambda x: x[2])
                print(f"  Bottleneck: {b[0]} <-> {b[1]} ({b[2]} ms)")

        # ── AUDIT_LATENSI ────────────────────────────────────
        elif cmd == 'AUDIT_LATENSI':
            dist, _ = dijkstra(graph, GATEWAY)
            head = None
            for did, lat in dist.items():
                n      = LatNode(did, lat if lat < float('inf') else 9_999_999)
                n.next = head
                head   = n
            head = selection_sort_ll(head)
            print(f"[Big-O: Dijkstra O(V^2+E) + Selection Sort O(n^2)] Audit latensi dari {GATEWAY}:")
            cur, rank = head, 1
            while cur:
                lat_str = f"{cur.latensi} ms" if cur.latensi < 9_999_999 else "terisolasi"
                dev     = graph.devices.get(cur.device_id)
                tipe    = dev.tipe if dev else '?'
                print(f"  {rank:>3}. {cur.device_id:<20} {lat_str:<15} {tipe}")
                cur = cur.next; rank += 1

        # ── LAPORAN_JARINGAN ─────────────────────────────────
        elif cmd == 'LAPORAN_JARINGAN':
            all_dev  = bst.inorder()
            n_edges  = sum(graph.degree(u) for u in graph.adj) // 2
            isolated = graph.isolated_devices(GATEWAY)
            pending  = queue.pending_alerts()
            dist, _  = dijkstra(graph, GATEWAY)

            print("=== LAPORAN JARINGAN ===")
            print(f"Perangkat : {len(all_dev)} total | {sum(1 for d in all_dev if d.status=='ONLINE')} online | {sum(1 for d in all_dev if d.status=='OFFLINE')} offline")
            print(f"Jaringan  : {len(graph.adj)} node | {n_edges} edge | {len(isolated)} terisolasi")
            print(f"Queue     : {len(pending)} pending | CRITICAL:{sum(1 for a in pending if a.tipe==1)} WARNING:{sum(1 for a in pending if a.tipe==2)} INFO:{sum(1 for a in pending if a.tipe==3)}")
            print(f"Stack     : {sum(len(s) for s in stacks.values())} alert tersimpan")

            print("Top 5 latensi tertinggi:")
            top5 = sorted([(k,v) for k,v in dist.items() if v < float('inf')], key=lambda x: x[1], reverse=True)[:5]
            for i, (d, l) in enumerate(top5, 1):
                print(f"  {i}. {d:<20} {l} ms")

            offline = [d for d in all_dev if d.status == 'OFFLINE']
            if offline:
                print(f"Perangkat OFFLINE: {', '.join(d.device_id for d in offline)}")

        # ── KELUAR ───────────────────────────────────────────
        elif cmd in ('KELUAR', 'EXIT'):
            print("Keluar."); break

        else:
            print(f"Perintah '{cmd}' tidak dikenal. Ketik BANTUAN.")

if __name__ == '__main__':
    main()
