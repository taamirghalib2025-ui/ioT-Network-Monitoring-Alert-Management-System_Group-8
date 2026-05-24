"""
queue.py — Modul 2: Priority Alert Queue
Struktur: Linked List terurut ASC berdasarkan prioritas (CRITICAL=1 di depan)
Big-O  : enqueue O(n), dequeue O(1)
"""

from typing import Optional, List


# ── Node Linked List ──────────────────────────────────────────────────────────
class LLNode:
    def __init__(self, data=None):
        self.data = data
        self.next: Optional['LLNode'] = None


# ── Priority Alert Queue ──────────────────────────────────────────────────────
class AlertPriorityQueue:
    """
    Priority Queue berbasis Linked List terurut.
    CRITICAL (tipe=1) selalu diproses duluan.
    Mendukung: enqueue, dequeue, pending_alerts.
    Big-O: enqueue O(n) worst-case, dequeue O(1).
    """

    def __init__(self):
        self.head: Optional[LLNode] = None
        self._size: int = 0

    # ── Masukkan alert sesuai prioritas ───────────────────────────────────────
    def enqueue(self, alert) -> None:
        """
        Insertion terurut: alert dengan tipe lebih kecil (prioritas lebih tinggi)
        diletakkan lebih depan.
        Big-O: O(n) worst-case.
        """
        new_node = LLNode(alert)

        # Kosong atau prioritas lebih tinggi dari head
        if self.head is None or alert.tipe < self.head.data.tipe:
            new_node.next = self.head
            self.head     = new_node
        else:
            current = self.head
            while current.next and current.next.data.tipe <= alert.tipe:
                current = current.next
            new_node.next  = current.next
            current.next   = new_node

        self._size += 1

    # ── Ambil alert prioritas tertinggi ───────────────────────────────────────
    def dequeue(self):
        """
        Ambil & hapus alert di depan (prioritas tertinggi).
        Big-O: O(1).
        Kembalikan None jika queue kosong.
        """
        if self.head is None:
            return None
        alert      = self.head.data
        self.head  = self.head.next
        self._size -= 1
        return alert

    # ── Lihat alert tanpa menghapus ───────────────────────────────────────────
    def peek(self):
        """Kembalikan alert prioritas tertinggi tanpa menghapus. O(1)."""
        return self.head.data if self.head else None

    # ── Daftar semua alert yang menunggu ──────────────────────────────────────
    def pending_alerts(self) -> List:
        """Kembalikan list semua alert dari depan ke belakang. O(n)."""
        result, cur = [], self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    # ── Cek apakah queue kosong ───────────────────────────────────────────────
    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f'AlertPriorityQueue(size={self._size})'