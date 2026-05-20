import numpy as np
import random
import time
from dataclasses import dataclass, field
from typing import Optional, List, Tuple

# ── Seed ──────────────────────────────────────────────────────
np.random.seed(23)
random.seed(23)

DEVICE_TYPES = ['SENSOR', 'GATEWAY', 'SERVER']
ALERT_TYPES  = {'CRITICAL': 1, 'WARNING': 2, 'INFO': 3}


# ── Dataclass Device ──────────────────────────────────────────────────────────
@dataclass
class Device:
    device_id: str
    tipe: str                  # SENSOR / GATEWAY / SERVER
    status: str = 'ONLINE'
    last_reading: float = 0.0


# ── BST Node ──────────────────────────────────────────────────────────────────
class BSTNode:
    def __init__(self, device: Device):
        self.device: Device = device
        self.left:  Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None


# ═════════════════════════════════════════════════════════════════════════════
#  BST Registry  —  Modul 3
# ═════════════════════════════════════════════════════════════════════════════
class BSTRegistry:

    def __init__(self):
        self.root: Optional[BSTNode] = None
        self._size: int = 0

    # ── Helper: perbandingan kunci ───────────────────────────────────────────
    @staticmethod
    def _cmp(a: str, b: str) -> int:
        
        if a < b:
            return -1
        if a > b:
            return 1
        return 0

    # ── INSERT ───────────────────────────────────────────────────────────────
    def insert(self, device: Device) -> None:
     
        new_node = BSTNode(device)

        if self.root is None:
            self.root = new_node
            self._size += 1
            return

        current = self.root
        while True:
            cmp = self._cmp(device.device_id, current.device.device_id)

            if cmp == 0:
                # device_id sudah ada → update data (bukan duplikasi)
                current.device = device
                return

            elif cmp < 0:
                if current.left is None:
                    current.left = new_node
                    self._size += 1
                    return
                current = current.left

            else:  # cmp > 0
                if current.right is None:
                    current.right = new_node
                    self._size += 1
                    return
                current = current.right

    # ── SEARCH ───────────────────────────────────────────────────────────────
    def search(self, device_id: str) -> Optional[Device]:
      
        current = self.root
        while current is not None:
            cmp = self._cmp(device_id, current.device.device_id)
            if cmp == 0:
                return current.device
            elif cmp < 0:
                current = current.left
            else:
                current = current.right
        return None

    # ── UPDATE STATUS ─────────────────────────────────────────────────────────
    def update_status(self, device_id: str, status: str) -> bool:
       
        if status not in ('ONLINE', 'OFFLINE'):
            raise ValueError(f"Status tidak valid: '{status}'. Gunakan 'ONLINE' atau 'OFFLINE'.")

        current = self.root
        while current is not None:
            cmp = self._cmp(device_id, current.device.device_id)
            if cmp == 0:
                current.device.status = status
                return True
            elif cmp < 0:
                current = current.left
            else:
                current = current.right
        return False  # device_id tidak ditemukan

    # ── INORDER ───────────────────────────────────────────────────────────────
    def inorder(self) -> List[Device]:
      
        result: List[Device] = []
        # Iteratif menggunakan stack eksplisit (tidak rekursif)
        stack: List[BSTNode] = []
        current = self.root

        while current is not None or stack:
            # Jangkau node paling kiri
            while current is not None:
                stack.append(current)
                current = current.left

            # Kunjungi node
            current = stack.pop()
            result.append(current.device)

            # Pindah ke sub-pohon kanan
            current = current.right

        return result

    # ── DELETE (bonus: tidak wajib tapi berguna) ─────────────────────────────
    def delete(self, device_id: str) -> bool:
      
        self.root, deleted = self._delete_recursive(self.root, device_id)
        if deleted:
            self._size -= 1
        return deleted

    def _delete_recursive(
        self, node: Optional[BSTNode], device_id: str
    ) -> Tuple[Optional[BSTNode], bool]:
        if node is None:
            return None, False

        cmp = self._cmp(device_id, node.device.device_id)

        if cmp < 0:
            node.left, deleted = self._delete_recursive(node.left, device_id)
        elif cmp > 0:
            node.right, deleted = self._delete_recursive(node.right, device_id)
        else:
            # Node ditemukan
            deleted = True
            if node.left is None:
                return node.right, deleted
            if node.right is None:
                return node.left, deleted

            # Node punya dua anak → ganti dengan in-order successor (terkecil di kanan)
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.device = successor.device
            node.right, _ = self._delete_recursive(node.right, successor.device.device_id)

        return node, deleted

    # ── Utilitas ──────────────────────────────────────────────────────────────
    def __len__(self) -> int:
        return self._size

    def height(self) -> int:
        """Hitung tinggi BST. O(n)."""
        def _height(node: Optional[BSTNode]) -> int:
            if node is None:
                return 0
            return 1 + max(_height(node.left), _height(node.right))
        return _height(self.root)

    def display_tree(self, node: Optional[BSTNode] = None,
                     prefix: str = "", is_left: bool = True) -> None:
        """Tampilkan BST sebagai diagram ASCII di terminal."""
        if node is None:
            if self.root is None:
                print("(BST kosong)")
            return

        connector = "├── " if is_left else "└── "
        print(prefix + connector + f"{node.device.device_id} [{node.device.tipe}|{node.device.status}]")

        extension = "│   " if is_left else "    "
        if node.left or node.right:
            if node.left:
                self.display_tree(node.left,  prefix + extension, True)
            if node.right:
                self.display_tree(node.right, prefix + extension, False)


# ═════════════════════════════════════════════════════════════════════════════
#  Generator data awal (diambil dari starter code)
# ═════════════════════════════════════════════════════════════════════════════
def generate_iot_network(n_devices: int = 40, n_extra_edges: int = 20, seed: int = 23):
    rng = np.random.default_rng(seed)
    devices = []

    devices.append(Device('GATEWAY_0', 'GATEWAY'))
    for i in range(1, 5):
        devices.append(Device(f'SERVER_{i}', 'SERVER'))
    for i in range(5, n_devices):
        devices.append(Device(f'SENSOR_{i}', 'SENSOR',
                               last_reading=float(rng.uniform(0, 100))))

    # Edge (hanya digunakan oleh modul lain, di sini kita kembalikan saja)
    perm  = rng.permutation(n_devices)
    edges = []
    for i in range(1, n_devices):
        u   = devices[perm[i-1]].device_id
        v   = devices[perm[i]].device_id
        lat = int(rng.integers(5, 200))
        edges.append((u, v, lat))
    for _ in range(n_extra_edges):
        i, j = rng.choice(n_devices, 2, replace=False)
        lat  = int(rng.integers(5, 200))
        edges.append((devices[i].device_id, devices[j].device_id, lat))

    return devices, edges


# ═════════════════════════════════════════════════════════════════════════════
#  Demo & Pengujian Modul 3
# ═════════════════════════════════════════════════════════════════════════════
def demo_modul3():
    print("=" * 65)
    print("  MODUL 3 — BST Device Registry")
    print("  IoT Network Monitoring & Alert Management System")
    print("=" * 65)

    # 1) Buat BST dan isi dengan 40 perangkat
    bst = BSTRegistry()
    devices, _ = generate_iot_network(40, 20, seed=23)

    print(f"\n[1] INSERT — Memasukkan {len(devices)} perangkat ke BST ...")
    t0 = time.perf_counter()
    for d in devices:
        bst.insert(d)
    t1 = time.perf_counter()
    print(f"    Jumlah node  : {len(bst)}")
    print(f"    Tinggi BST   : {bst.height()}")
    print(f"    Waktu insert : {(t1-t0)*1000:.3f} ms")

    # 2) INORDER — daftar terurut
    print("\n[2] INORDER — Daftar perangkat terurut (device_id):")
    sorted_devices = bst.inorder()
    for i, dev in enumerate(sorted_devices):
        marker = "●" if dev.status == 'ONLINE' else "○"
        print(f"    {marker} {dev.device_id:<15} [{dev.tipe:<7}] last={dev.last_reading:.1f}")
        if i >= 9:
            print(f"    ... (total {len(sorted_devices)} perangkat)")
            break

    # 3) SEARCH — cari beberapa device
    print("\n[3] SEARCH — Mencari perangkat:")
    queries = ['GATEWAY_0', 'SENSOR_15', 'SERVER_3', 'SENSOR_99']
    for qid in queries:
        t0 = time.perf_counter()
        found = bst.search(qid)
        t1 = time.perf_counter()
        if found:
            print(f"    ✔ {qid:<15} → tipe={found.tipe}, status={found.status}, "
                  f"last_reading={found.last_reading:.1f}  [{(t1-t0)*1e6:.2f} µs]")
        else:
            print(f"    ✘ {qid:<15} → TIDAK DITEMUKAN  [{(t1-t0)*1e6:.2f} µs]")

    # 4) UPDATE STATUS
    print("\n[4] UPDATE_STATUS — Mengubah status perangkat:")
    updates = [('SENSOR_10', 'OFFLINE'), ('SERVER_2', 'OFFLINE'),
               ('SENSOR_10', 'ONLINE'),  ('SENSOR_99', 'OFFLINE')]
    for dev_id, new_status in updates:
        ok = bst.update_status(dev_id, new_status)
        if ok:
            dev = bst.search(dev_id)
            print(f"    ✔ {dev_id:<15} → status sekarang: {dev.status}")
        else:
            print(f"    ✘ {dev_id:<15} → device tidak ditemukan, gagal update")

    # 5) DELETE (bonus)
    print("\n[5] DELETE — Menghapus perangkat (bonus):")
    targets = ['SENSOR_7', 'SERVER_4', 'SENSOR_999']
    for dev_id in targets:
        ok = bst.delete(dev_id)
        status = "berhasil dihapus" if ok else "tidak ditemukan"
        print(f"    {'✔' if ok else '✘'} {dev_id:<15} → {status}")
    print(f"    Jumlah node setelah delete: {len(bst)}")

    # 6) Tampilkan sub-pohon kecil (visual)
    print("\n[6] Visualisasi sub-pohon (10 node pertama setelah insert ulang kecil):")
    mini_bst = BSTRegistry()
    sample_ids = ['GATEWAY_0', 'SERVER_2', 'SERVER_1', 'SENSOR_5',
                  'SENSOR_20', 'SERVER_3', 'SENSOR_8', 'SENSOR_6']
    for sid in sample_ids:
        mini_bst.insert(Device(sid, 'SENSOR'))
    print(f"    {'':4}(root)")
    mini_bst.display_tree(mini_bst.root, prefix="    ", is_left=False)

    # 7) Analisis Big-O
    print("\n[7] Analisis Kompleksitas Waktu:")
    print("    Operasi         | Best/Avg  | Worst (skewed BST)")
    print("    ----------------+-----------+-------------------")
    print("    insert          | O(log n)  | O(n)")
    print("    search          | O(log n)  | O(n)")
    print("    update_status   | O(log n)  | O(n)")
    print("    delete          | O(log n)  | O(n)")
    print("    inorder         | O(n)      | O(n)")
    print()
    print("    *rata-rata O(log n) tercapai jika BST relatif seimbang")
    print("     (data dimasukkan dalam urutan acak, bukan terurut)")

    # 8) Benchmark: ukuran data bervariasi
    print("\n[8] Benchmark Runtime (3 ukuran data):")
    print(f"    {'n_devices':>10} | {'insert (ms)':>12} | {'search (ms)':>12} | {'inorder (ms)':>13}")
    print(f"    {'-'*10}-+-{'-'*12}-+-{'-'*12}-+-{'-'*13}")
    for n in [40, 200, 1000]:
        devs, _ = generate_iot_network(n, n//2, seed=23)

        b = BSTRegistry()
        t0 = time.perf_counter()
        for d in devs:
            b.insert(d)
        t_ins = (time.perf_counter() - t0) * 1000

        mid_id = devs[n // 2].device_id
        t0 = time.perf_counter()
        for _ in range(100):
            b.search(mid_id)
        t_srch = (time.perf_counter() - t0) * 10  # rata-rata 100x → ms

        t0 = time.perf_counter()
        b.inorder()
        t_inord = (time.perf_counter() - t0) * 1000

        print(f"    {n:>10} | {t_ins:>12.3f} | {t_srch:>12.4f} | {t_inord:>13.4f}")

    print("\n[✓] Demo Modul 3 selesai.")


if __name__ == '__main__':
    demo_modul3()