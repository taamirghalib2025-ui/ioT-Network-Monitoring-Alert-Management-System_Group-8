<<<<<<< HEAD
=======
from typing import Optional, Any

# ── 1. Node untuk Queue dan Stack ─────────────────────────────────────────────
class LLNode:
    """
    Node generik untuk Singly Linked List.
    Digunakan untuk menyimpan objek Alert di Priority Queue dan Stack.
    """
    def __init__(self, data: Any = None):
        self.data = data
        self.next: Optional['LLNode'] = None

    def __repr__(self):
        return f"LLNode(data={self.data})"


# ── 2. Node untuk Graph ───────────────────────────────────────────────────────
class EdgeNode:
    """
    Node khusus untuk Adjacency List pada IoT Graph.
    Menyimpan id perangkat tujuan (dest) beserta bobot koneksinya (latensi).
    """
    def __init__(self, dest: str, latensi: int):
        self.dest = dest
        self.latensi = latensi
        self.next: Optional['EdgeNode'] = None

    def __repr__(self):
        return f"EdgeNode(dest='{self.dest}', latensi={self.latensi}ms)"
>>>>>>> b639c124380ee13dd4b4ed5bdac21aa762b7bab2
