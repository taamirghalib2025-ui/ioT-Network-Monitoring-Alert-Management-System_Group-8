"""
stack.py — Modul 4: Alert Stack & DFS Stack
Struktur: Singly Linked List (LIFO)
"""

from typing import Optional, List
from data_structures.linked_list import LLNode  

# ── 1. Stack Khusus Riwayat Alert (Maksimal 20 elemen) ────────────────────────
class AlertStack:
    def __init__(self, kapasitas: int = 20):
        self.top: Optional[LLNode] = None
        self.size: int = 0
        self.kapasitas: int = kapasitas

    def push(self, alert) -> None:
        """Big-O: O(1) normal, O(n) saat penuh."""
        if self.size >= self.kapasitas:
            self._hapus_bottom()

        node = LLNode(alert)
        node.next = self.top
        self.top = node
        self.size += 1

    def pop(self):
        """Big-O: O(1)."""
        if self.size == 0: return None
        data = self.top.data
        self.top = self.top.next
        self.size -= 1
        return data

    def peek(self):
        return self.top.data if self.top else None

    def to_list(self) -> List:
        """Mengembalikan isi stack dari atas ke bawah."""
        result, current = [], self.top
        while current:
            result.append(current.data)
            current = current.next
        return result

    def _hapus_bottom(self) -> None:
        """Menghapus elemen paling bawah (oldest)."""
        if self.size <= 1:
            self.top = None
            self.size = 0
            return

        current = self.top
        while current.next and current.next.next:
            current = current.next
        current.next = None
        self.size -= 1

    def __len__(self) -> int:
        return self.size


# ── 2. Stack Umum (Untuk keperluan pencarian DFS di Graph) ────────────────────
class Stack:
    def __init__(self):
        self.top: Optional[LLNode] = None
        self.size: int = 0

    def push(self, data) -> None:
        node = LLNode(data)
        node.next = self.top
        self.top = node
        self.size += 1

    def pop(self):
        if self.size == 0: return None
        data = self.top.data
        self.top = self.top.next
        self.size -= 1
        return data

    def is_empty(self) -> bool:
        return self.size == 0

    def __len__(self) -> int:
        return self.size
