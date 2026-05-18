# ============================================================
# stack.py
# Modul: Stack berbasis Singly Linked List (LIFO)
# Topik 4: IoT Network Monitoring & Alert Management System
# ELT60213 Algoritma dan Struktur Data - TA 2025/2026
# ============================================================

from __future__ import annotations
from typing import Optional, List
from dataclasses import dataclass


# ── Dataclass Alert (dipakai sebagai data di Stack) ──────────
@dataclass
class Alert:
    """Representasi satu alert dari perangkat IoT."""
    alert_id: int
    device_id: str
    tipe: int          # 1=CRITICAL, 2=WARNING, 3=INFO
    pesan: str
    timestamp: float


# ── Node Singly Linked List ───────────────────────────────────
class LLNode:
    """
    Node tunggal untuk Singly Linked List.
    Menyimpan satu data dan pointer ke node berikutnya.
    """
    def __init__(self, data=None):
        self.data = data
        self.next: Optional[LLNode] = None


# ── Stack berbasis Singly Linked List ─────────────────────────
class AlertStack:
    """
    Stack LIFO berbasis Singly Linked List untuk riwayat alert per-device.

    Setiap device IoT memiliki satu AlertStack sendiri.
    Maksimal menyimpan `kapasitas` alert terakhir (default=20).
    Jika penuh, alert paling lama (paling bawah) otomatis dihapus
    agar alert terbaru selalu bisa masuk.

    Kompleksitas:
        push  : O(n) worst-case (hanya saat penuh, untuk hapus bottom)
                O(1) kondisi normal
        pop   : O(1)
        peek  : O(1)
        to_list: O(n)
    Ruang: O(n) di mana n = kapasitas
    """

    def __init__(self, kapasitas: int = 20):
        self.top: Optional[LLNode] = None
        self._size: int = 0
        self.kapasitas: int = kapasitas

    # ── Operasi utama ──────────────────────────────────────────

    def push(self, alert: Alert) -> None:
        """
        Masukkan alert baru ke puncak stack (LIFO).

        Jika stack sudah penuh (size == kapasitas), elemen paling
        bawah (alert paling lama) dihapus terlebih dahulu agar
        jumlah node tetap <= kapasitas.

        Big-O waktu : O(1) normal | O(n) saat penuh (hapus bottom)
        Big-O ruang : O(1) tambahan per operasi
        """
        if self._size >= self.kapasitas:
            self._hapus_bottom()  # hapus alert terlama → O(n)

        # Buat node baru dan taruh di puncak → O(1)
        node = LLNode(alert)
        node.next = self.top
        self.top = node
        self._size += 1

    def pop(self) -> Optional[Alert]:
        """
        Ambil dan hapus alert dari puncak stack (LIFO).

        Mengembalikan None jika stack kosong.

        Big-O waktu : O(1)
        Big-O ruang : O(1)
        """
        if self.is_empty():
            return None

        data = self.top.data
        self.top = self.top.next
        self._size -= 1
        return data

    def peek(self) -> Optional[Alert]:
        """
        Lihat alert paling atas tanpa menghapusnya.

        Big-O waktu : O(1)
        """
        if self.is_empty():
            return None
        return self.top.data

    # ── Operasi bantu ──────────────────────────────────────────

    def is_empty(self) -> bool:
        """Kembalikan True jika stack kosong. Big-O: O(1)."""
        return self._size == 0

    def is_full(self) -> bool:
        """Kembalikan True jika stack sudah penuh. Big-O: O(1)."""
        return self._size >= self.kapasitas

    def to_list(self) -> List[Alert]:
        """
        Kembalikan semua alert sebagai list dari top ke bottom
        (alert terbaru di indeks 0, terlama di indeks terakhir).

        Big-O waktu : O(n)
        Big-O ruang : O(n)
        """
        result: List[Alert] = []
        current = self.top
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def clear(self) -> None:
        """
        Kosongkan seluruh stack.
        Big-O waktu : O(1) — cukup reset pointer dan counter.
        """
        self.top = None
        self._size = 0

    def __len__(self) -> int:
        """Kembalikan jumlah elemen saat ini. Big-O: O(1)."""
        return self._size

    def __repr__(self) -> str:
        alerts = self.to_list()
        ids = [f"Alert#{a.alert_id}({['','CRITICAL','WARNING','INFO'][a.tipe]})"
               for a in alerts]
        return f"AlertStack(size={self._size}/{self.kapasitas}, top→[{', '.join(ids)}])"

    # ── Operasi internal ───────────────────────────────────────

    def _hapus_bottom(self) -> None:
        """
        Hapus node paling bawah (alert paling lama).
        Dipanggil secara internal saat stack penuh.

        Big-O waktu : O(n) — harus traverse ke node sebelum bottom.
        Big-O ruang : O(1)
        """
        if self._size == 0:
            return

        # Hanya 1 elemen
        if self._size == 1:
            self.top = None
            self._size = 0
            return

        # Traverse ke node sebelum yang terakhir
        current = self.top
        while current.next is not None and current.next.next is not None:
            current = current.next

        # current.next adalah node terakhir → putus linknya
        current.next = None
        self._size -= 1


# ── Stack Umum untuk keperluan DFS (Graph Traversal) ─────────
class Stack:
    """
    Stack LIFO serbaguna berbasis Singly Linked List.
    Digunakan untuk: DFS traversal graph, log siklus, dll.

    Kompleksitas:
        push / pop / peek : O(1)
        Ruang             : O(n)
    """

    def __init__(self):
        self.top: Optional[LLNode] = None
        self._size: int = 0

    def push(self, data) -> None:
        """
        Masukkan data ke puncak stack.
        Big-O waktu: O(1)
        """
        node = LLNode(data)
        node.next = self.top
        self.top = node
        self._size += 1

    def pop(self):
        """
        Ambil dan hapus data dari puncak stack.
        Kembalikan None jika kosong.
        Big-O waktu: O(1)
        """
        if self.is_empty():
            return None
        data = self.top.data
        self.top = self.top.next
        self._size -= 1
        return data

    def peek(self):
        """
        Lihat data puncak tanpa menghapus.
        Big-O waktu: O(1)
        """
        return self.top.data if self.top else None

    def is_empty(self) -> bool:
        """Big-O: O(1)."""
        return self._size == 0

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"Stack(size={self._size}, top={self.peek()})"


# ── Unit Test Mandiri ──────────────────────────────────────────
if __name__ == "__main__":
    import time

    print("=" * 55)
    print("  Unit Test: AlertStack & Stack")
    print("  Topik 4 - IoT Network Monitoring")
    print("=" * 55)

    # ── Test 1: AlertStack dasar ───────────────────────────────
    print("\n[TEST 1] Push & Pop AlertStack (kapasitas=5)")
    stk = AlertStack(kapasitas=5)

    alerts_dummy = [
        Alert(i, f"SENSOR_{i}", (i % 3) + 1, f"Pesan alert {i}", time.time())
        for i in range(1, 6)
    ]

    for a in alerts_dummy:
        stk.push(a)
        print(f"  push Alert#{a.alert_id} ({['','CRITICAL','WARNING','INFO'][a.tipe]}) "
              f"→ size={len(stk)}")

    print(f"\n  Stack saat ini: {stk}")
    print(f"  peek() → Alert#{stk.peek().alert_id}")

    popped = stk.pop()
    print(f"  pop()  → Alert#{popped.alert_id} | size sekarang={len(stk)}")

    # ── Test 2: Auto-hapus bottom saat penuh ──────────────────
    print("\n[TEST 2] Auto-hapus bottom saat melebihi kapasitas")
    stk2 = AlertStack(kapasitas=3)
    for i in range(1, 7):
        a = Alert(i, "GATEWAY_0", 1, f"Overflow test {i}", time.time())
        stk2.push(a)
        ids = [x.alert_id for x in stk2.to_list()]
        print(f"  push Alert#{i} → isi stack (top→bottom): {ids}")

    print(f"\n  Stack akhir: {stk2}")

    # ── Test 3: to_list() ──────────────────────────────────────
    print("\n[TEST 3] to_list() — urutan top ke bottom")
    items = stk2.to_list()
    for idx, a in enumerate(items):
        print(f"  [{idx}] Alert#{a.alert_id} - {['','CRITICAL','WARNING','INFO'][a.tipe]}"
              f" - {a.pesan}")

    # ── Test 4: Stack umum untuk DFS ──────────────────────────
    print("\n[TEST 4] Stack umum (untuk DFS traversal)")
    s = Stack()
    for node_id in ["GATEWAY_0", "SERVER_1", "SENSOR_5", "SENSOR_12"]:
        s.push(node_id)
        print(f"  push '{node_id}' → size={len(s)}")

    print()
    while not s.is_empty():
        print(f"  pop → '{s.pop()}'")

    # ── Test 5: Stack kosong ───────────────────────────────────
    print("\n[TEST 5] Operasi pada stack kosong")
    empty = AlertStack()
    print(f"  is_empty()={empty.is_empty()}")
    print(f"  pop()     ={empty.pop()}")
    print(f"  peek()    ={empty.peek()}")

    print("\n✅ Semua test selesai tanpa error.")
    print("=" * 55)
