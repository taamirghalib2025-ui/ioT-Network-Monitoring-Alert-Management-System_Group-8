
import numpy as np
import random
from dataclasses import dataclass, field
from typing import Optional, List

#Seed
np.random.seed(23)
random.seed(23)

DEVICE_TYPES = ['SENSOR', 'GATEWAY', 'SERVER']
ALERT_TYPES  = {'CRITICAL': 1, 'WARNING': 2, 'INFO': 3}


#Data Model
@dataclass
class Device:
    device_id:    str
    tipe:         str          # SENSOR / GATEWAY / SERVER
    status:       str = 'ONLINE'
    last_reading: float = 0.0

#  BST Node
class BSTNode:
   
    def __init__(self, device: Device):
        self.device: Device          = device
        self.left:   Optional['BSTNode'] = None
        self.right:  Optional['BSTNode'] = None

#  BST Device Registry
class BSTRegistry:
    
    def __init__(self):
        self.root: Optional[BSTNode] = None
        self._size: int = 0

    # ------------------------------------------------------------------
    # INSERT
    # ------------------------------------------------------------------
    def insert(self, device: Device) -> None:
        
        self.root = self._insert_recursive(self.root, device)

    def _insert_recursive(self, node: Optional[BSTNode], device: Device) -> BSTNode:
        # Basis: posisi kosong â†’ buat node baru
        if node is None:
            self._size += 1
            return BSTNode(device)

        if device.device_id < node.device.device_id:
            # Kunci lebih kecil â†’ masuk ke subtree kiri
            node.left = self._insert_recursive(node.left, device)

        elif device.device_id > node.device.device_id:
            # Kunci lebih besar â†’ masuk ke subtree kanan
            node.right = self._insert_recursive(node.right, device)

        else:
            # Kunci sama â†’ update (upsert), jangan tambah size
            node.device = device

        return node

    # ------------------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------------------
    def search(self, device_id: str) -> Optional[Device]:
        
        node = self._search_recursive(self.root, device_id)
        return node.device if node else None

    def _search_recursive(self, node: Optional[BSTNode], device_id: str) -> Optional[BSTNode]:
        # Basis: node kosong atau ditemukan
        if node is None:
            return None
        if device_id == node.device.device_id:
            return node

        if device_id < node.device.device_id:
            return self._search_recursive(node.left, device_id)
        else:
            return self._search_recursive(node.right, device_id)

    # ------------------------------------------------------------------
    # UPDATE STATUS
    # ------------------------------------------------------------------
    def update_status(self, device_id: str, status: str) -> bool:
        
        if status not in ('ONLINE', 'OFFLINE'):
            raise ValueError(f"Status tidak valid: '{status}'. Harus 'ONLINE' atau 'OFFLINE'.")

        node = self._search_recursive(self.root, device_id)
        if node is None:
            return False

        node.device.status = status
        return True

    # ------------------------------------------------------------------
    # INORDER TRAVERSAL  (Left â†’ Root â†’ Right)
    # ------------------------------------------------------------------
    def inorder(self) -> List[Device]:
        
        result: List[Device] = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node: Optional[BSTNode], result: List[Device]) -> None:
        if node is None:
            return
        self._inorder_recursive(node.left, result)
        result.append(node.device)
        self._inorder_recursive(node.right, result)

    # ------------------------------------------------------------------
    # Helper: ukuran BST
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return self._size

    # ------------------------------------------------------------------
    # Helper: pretty-print tree (untuk debugging)
    # ------------------------------------------------------------------
    def print_tree(self, node: Optional[BSTNode] = None,
                   prefix: str = "", is_left: bool = True,
                   _first_call: bool = True) -> None:
        """Cetak struktur BST ke konsol (visual, untuk debug)."""
        if _first_call:
            node = self.root
        if node is None:
            if _first_call:
                print("(BST kosong)")
            return
        print(prefix + ("â”œâ”€â”€ " if not is_left else "â””â”€â”€ ") + node.device.device_id
              + f" [{node.device.tipe}|{node.device.status}]")
        new_prefix = prefix + ("â”‚   " if not is_left else "    ")
        if node.left or node.right:
            if node.right:
                self.print_tree(node.right, new_prefix, False, _first_call=False)
            if node.left:
                self.print_tree(node.left, new_prefix, True, _first_call=False)

#  Generator data awal (sama dengan starter code)
def generate_iot_network(n_devices: int = 40, n_extra_edges: int = 20, seed: int = 23):
    rng = np.random.default_rng(seed)
    devices = []
    devices.append(Device('GATEWAY_0', 'GATEWAY'))
    for i in range(1, 5):
        devices.append(Device(f'SERVER_{i}', 'SERVER'))
    for i in range(5, n_devices):
        devices.append(Device(f'SENSOR_{i}', 'SENSOR',
                               last_reading=float(rng.uniform(0, 100))))
    perm  = rng.permutation(n_devices)
    edges = []
    for i in range(1, n_devices):
        u   = devices[perm[i - 1]].device_id
        v   = devices[perm[i]].device_id
        lat = int(rng.integers(5, 200))
        edges.append((u, v, lat))
    for _ in range(n_extra_edges):
        i, j = rng.choice(n_devices, 2, replace=False)
        lat  = int(rng.integers(5, 200))
        edges.append((devices[i].device_id, devices[j].device_id, lat))
    return devices, edges

#  Demo / Unit-test sederhana
def demo():
    print("=" * 60)
    print("  MODUL 3 â€“ BST Device Registry (Demo)")
    print("=" * 60)

    # 1. Bangun BST dari data generate
    bst = BSTRegistry()
    devices, _ = generate_iot_network(40, 20, seed=23)

    for d in devices:
        bst.insert(d)

    print(f"\n[INFO] Total perangkat di-insert : {len(bst)}")

    # 2. Inorder daftar terurut berdasarkan device_id
    print("\n Daftar perangkat terurut (inorder)")
    sorted_devices = bst.inorder()
    print(f"{'device_id':<15} {'tipe':<10} {'status':<10} {'last_reading':>12}")
    print("-" * 50)
    for d in sorted_devices:
        print(f"{d.device_id:<15} {d.tipe:<10} {d.status:<10} {d.last_reading:>12.2f}")

    # 3. Search
    print("\nTest SEARCH")
    test_ids = ['GATEWAY_0', 'SERVER_2', 'SENSOR_15', 'SENSOR_99']
    for did in test_ids:
        result = bst.search(did)
        if result:
            print(f"  FOUND  '{did}': tipe={result.tipe}, status={result.status}")
        else:
            print(f"  NOT FOUND '{did}'")

    # 4. Update status
    print("\nTest UPDATE_STATUS")
    updates = [('SENSOR_5', 'OFFLINE'), ('SERVER_3', 'OFFLINE'), ('SENSOR_99', 'OFFLINE')]
    for did, new_status in updates:
        ok = bst.update_status(did, new_status)
        if ok:
            d = bst.search(did)
            print(f"  UPDATE OK  '{did}' â†’ status={d.status}")
        else:
            print(f"  UPDATE FAIL '{did}' (tidak ditemukan)")

    # 5. Verifikasi update lewat inorder (tampilkan yang OFFLINE)
    print("\nPerangkat OFFLINE setelah update")
    offline = [d for d in bst.inorder() if d.status == 'OFFLINE']
    for d in offline:
        print(f"  {d.device_id} [{d.tipe}]")

    # 6. Insert device baru
    print("\nTest INSERT device baru")
    new_dev = Device('SENSOR_99', 'SENSOR', status='ONLINE', last_reading=42.5)
    bst.insert(new_dev)
    found = bst.search('SENSOR_99')
    print(f"  Setelah insert 'SENSOR_99': status={found.status if found else 'N/A'}")

    print("\n[Big-O Summary]")
    print("  insert        : O(log n) rata-rata")
    print("  search        : O(log n) rata-rata")
    print("  update_status : O(log n) rata-rata  (search + O(1) update)")
    print("  inorder       : O(n)")
    print("=" * 60)


if __name__ == '__main__':
    demo()