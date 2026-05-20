# ================================================================
# linked_list.py
# Modul: Implementasi Singly Linked List & Doubly Linked List
# Topik 4: IoT Network Monitoring & Alert Management System
# ELT60213 Algoritma dan Struktur Data - TA 2025/2026
# ================================================================

from __future__ import annotations
from typing import Optional, Any


# ── Node untuk Singly Linked List ────────────────────────────────

class SLLNode:
    """
    Node untuk Singly Linked List.
    Menyimpan data dan pointer ke node berikutnya.
    Big-O ruang: O(1) per node.
    """
    def __init__(self, data: Any = None):
        self.data = data
        self.next: Optional[SLLNode] = None

    def __repr__(self) -> str:
        return f"SLLNode({self.data})"


# ── Node untuk Doubly Linked List ────────────────────────────────

class DLLNode:
    """
    Node untuk Doubly Linked List.
    Menyimpan data, pointer ke node berikutnya, dan pointer ke node sebelumnya.
    Big-O ruang: O(1) per node.
    """
    def __init__(self, data: Any = None):
        self.data = data
        self.next: Optional[DLLNode] = None
        self.prev: Optional[DLLNode] = None

    def __repr__(self) -> str:
        return f"DLLNode({self.data})"


# ── Singly Linked List ────────────────────────────────────────────

class SinglyLinkedList:
    """
    Implementasi Singly Linked List dari nol.
    Digunakan sebagai fondasi Stack, Queue, Priority Queue, dan adjacency list Graph.

    Operasi utama:
    - add_front  : O(1)
    - add_back   : O(1)  <- menggunakan pointer tail
    - remove_front: O(1)
    - remove_back : O(n)  <- harus traverse hingga node sebelum tail
    - find       : O(n)
    - delete_by_value: O(n)
    - size / is_empty: O(1)

    Big-O ruang: O(n) untuk n elemen.
    """

    def __init__(self):
        self.head: Optional[SLLNode] = None
        self.tail: Optional[SLLNode] = None
        self._size: int = 0

    # ── Properti ─────────────────────────────────────────────────

    def is_empty(self) -> bool:
        """Cek apakah list kosong. Big-O: O(1)."""
        return self._size == 0

    def __len__(self) -> int:
        """Kembalikan jumlah elemen. Big-O: O(1)."""
        return self._size

    # ── Operasi Penyisipan ────────────────────────────────────────

    def add_front(self, data: Any) -> None:
        """
        Sisipkan node baru di depan (head).
        Big-O waktu: O(1).

        Contoh:
            list: [B -> C]
            add_front(A)
            list: [A -> B -> C]
        """
        node = SLLNode(data)
        node.next = self.head
        self.head = node
        if self.tail is None:       # list sebelumnya kosong
            self.tail = node
        self._size += 1

    def add_back(self, data: Any) -> None:
        """
        Sisipkan node baru di belakang (tail).
        Big-O waktu: O(1) karena ada pointer tail.

        Contoh:
            list: [A -> B]
            add_back(C)
            list: [A -> B -> C]
        """
        node = SLLNode(data)
        if self.tail is None:       # list kosong
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def insert_after(self, target_data: Any, new_data: Any) -> bool:
        """
        Sisipkan node baru setelah node dengan nilai target_data.
        Big-O waktu: O(n) karena harus cari node target lebih dulu.
        Kembalikan True jika berhasil, False jika target tidak ditemukan.
        """
        current = self.head
        while current is not None:
            if current.data == target_data:
                node = SLLNode(new_data)
                node.next = current.next
                current.next = node
                if current == self.tail:    # target adalah tail
                    self.tail = node
                self._size += 1
                return True
            current = current.next
        return False

    # ── Operasi Penghapusan ───────────────────────────────────────

    def remove_front(self) -> Optional[Any]:
        """
        Hapus dan kembalikan data dari node terdepan (head).
        Big-O waktu: O(1).
        Kembalikan None jika list kosong.

        Contoh:
            list: [A -> B -> C]
            remove_front() -> A
            list: [B -> C]
        """
        if self.head is None:
            return None
        data = self.head.data
        self.head = self.head.next
        if self.head is None:       # list menjadi kosong
            self.tail = None
        self._size -= 1
        return data

    def remove_back(self) -> Optional[Any]:
        """
        Hapus dan kembalikan data dari node terakhir (tail).
        Big-O waktu: O(n) karena harus traverse untuk temukan node sebelum tail.
        Kembalikan None jika list kosong.

        Analisis: Singly Linked List tidak punya pointer prev,
        sehingga harus iterasi dari head untuk menemukan node sebelum tail.
        Gunakan Doubly Linked List jika operasi ini sering dipanggil.
        """
        if self.head is None:
            return None
        data = self.tail.data
        if self.head == self.tail:  # hanya satu elemen
            self.head = None
            self.tail = None
        else:
            current = self.head
            while current.next != self.tail:
                current = current.next
            current.next = None
            self.tail = current
        self._size -= 1
        return data

    def delete_by_value(self, data: Any) -> bool:
        """
        Hapus node pertama yang datanya sama dengan nilai yang dicari.
        Big-O waktu: O(n).
        Kembalikan True jika berhasil dihapus, False jika tidak ditemukan.

        Contoh:
            list: [A -> B -> C -> B]
            delete_by_value(B)  -> True
            list: [A -> C -> B]  (hanya yang pertama dihapus)
        """
        if self.head is None:
            return False

        # Kasus khusus: node yang dihapus adalah head
        if self.head.data == data:
            self.remove_front()
            return True

        current = self.head
        while current.next is not None:
            if current.next.data == data:
                if current.next == self.tail:   # menghapus tail
                    self.tail = current
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    # ── Operasi Pencarian ─────────────────────────────────────────

    def find(self, data: Any) -> Optional[SLLNode]:
        """
        Cari dan kembalikan node pertama dengan data yang cocok.
        Big-O waktu: O(n).
        Kembalikan None jika tidak ditemukan.
        """
        current = self.head
        while current is not None:
            if current.data == data:
                return current
            current = current.next
        return None

    def contains(self, data: Any) -> bool:
        """
        Cek apakah nilai data ada dalam list.
        Big-O waktu: O(n).
        """
        return self.find(data) is not None

    def get_at(self, index: int) -> Optional[Any]:
        """
        Kembalikan data pada posisi index (0-based).
        Big-O waktu: O(n).
        Kembalikan None jika index di luar batas.
        """
        if index < 0 or index >= self._size:
            return None
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    # ── Operasi Utilitas ──────────────────────────────────────────

    def to_list(self) -> list:
        """
        Konversi Linked List ke Python list untuk keperluan debug/tampilan.
        Big-O waktu: O(n).
        """
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def clear(self) -> None:
        """
        Kosongkan seluruh list.
        Big-O waktu: O(1) — hanya reset pointer.
        """
        self.head = None
        self.tail = None
        self._size = 0

    def reverse(self) -> None:
        """
        Balikkan urutan list secara in-place.
        Big-O waktu: O(n), Big-O ruang: O(1).

        Contoh:
            list: [A -> B -> C]
            reverse()
            list: [C -> B -> A]
        """
        prev = None
        current = self.head
        self.tail = self.head   # head lama menjadi tail baru
        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def __repr__(self) -> str:
        items = self.to_list()
        return " -> ".join(str(x) for x in items) + " -> NULL"

    def __iter__(self):
        """Memungkinkan iterasi dengan for loop. Big-O: O(n)."""
        current = self.head
        while current is not None:
            yield current.data
            current = current.next


# ── Doubly Linked List ────────────────────────────────────────────

class DoublyLinkedList:
    """
    Implementasi Doubly Linked List dari nol.
    Lebih fleksibel dari SLL: mendukung traversal dua arah dan
    remove_back O(1) karena ada pointer prev di setiap node.

    Operasi utama:
    - add_front   : O(1)
    - add_back    : O(1)
    - remove_front: O(1)
    - remove_back : O(1)  <- keunggulan DLL vs SLL
    - find        : O(n)
    - delete_node : O(1)  <- jika sudah punya referensi node-nya
    - size / is_empty: O(1)

    Big-O ruang: O(n) untuk n elemen.
    Overhead memori DLL vs SLL: tiap node DLL butuh 1 pointer extra (prev).
    Untuk n=40 device x 20 alert = 800 node → overhead masih sangat kecil.
    """

    def __init__(self):
        self.head: Optional[DLLNode] = None
        self.tail: Optional[DLLNode] = None
        self._size: int = 0

    # ── Properti ─────────────────────────────────────────────────

    def is_empty(self) -> bool:
        """Big-O: O(1)."""
        return self._size == 0

    def __len__(self) -> int:
        """Big-O: O(1)."""
        return self._size

    # ── Operasi Penyisipan ────────────────────────────────────────

    def add_front(self, data: Any) -> None:
        """
        Sisipkan node baru di depan.
        Big-O waktu: O(1).
        """
        node = DLLNode(data)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self._size += 1

    def add_back(self, data: Any) -> None:
        """
        Sisipkan node baru di belakang.
        Big-O waktu: O(1) — keunggulan vs SLL karena ada pointer tail.
        """
        node = DLLNode(data)
        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1

    # ── Operasi Penghapusan ───────────────────────────────────────

    def remove_front(self) -> Optional[Any]:
        """
        Hapus dan kembalikan data dari depan.
        Big-O waktu: O(1).
        """
        if self.head is None:
            return None
        data = self.head.data
        if self.head == self.tail:  # satu elemen
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self._size -= 1
        return data

    def remove_back(self) -> Optional[Any]:
        """
        Hapus dan kembalikan data dari belakang.
        Big-O waktu: O(1) — inilah keunggulan utama DLL vs SLL.
        Pada SLL, operasi ini O(n) karena harus traverse dari head.
        """
        if self.tail is None:
            return None
        data = self.tail.data
        if self.head == self.tail:  # satu elemen
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self._size -= 1
        return data

    def delete_node(self, node: DLLNode) -> None:
        """
        Hapus node tertentu dari list (jika sudah punya referensi node-nya).
        Big-O waktu: O(1) — tidak perlu traverse karena ada pointer prev & next.
        """
        if node == self.head:
            self.remove_front()
            return
        if node == self.tail:
            self.remove_back()
            return
        # Node di tengah: bypass node
        node.prev.next = node.next
        node.next.prev = node.prev
        self._size -= 1

    def delete_by_value(self, data: Any) -> bool:
        """
        Hapus node pertama dengan nilai data yang cocok.
        Big-O waktu: O(n) untuk pencarian + O(1) untuk penghapusan.
        """
        current = self.head
        while current is not None:
            if current.data == data:
                self.delete_node(current)
                return True
            current = current.next
        return False

    # ── Operasi Pencarian ─────────────────────────────────────────

    def find(self, data: Any) -> Optional[DLLNode]:
        """
        Cari node dengan data yang cocok (pencarian maju dari head).
        Big-O waktu: O(n).
        """
        current = self.head
        while current is not None:
            if current.data == data:
                return current
            current = current.next
        return None

    def contains(self, data: Any) -> bool:
        """Cek apakah nilai ada dalam list. Big-O: O(n)."""
        return self.find(data) is not None

    def find_backward(self, data: Any) -> Optional[DLLNode]:
        """
        Cari node dengan pencarian mundur dari tail.
        Berguna jika data yang dicari biasanya ada di dekat tail.
        Big-O waktu: O(n).
        """
        current = self.tail
        while current is not None:
            if current.data == data:
                return current
            current = current.prev
        return None

    # ── Operasi Utilitas ──────────────────────────────────────────

    def to_list(self) -> list:
        """Konversi ke Python list (traversal maju). Big-O: O(n)."""
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def to_list_reversed(self) -> list:
        """Konversi ke Python list (traversal mundur dari tail). Big-O: O(n)."""
        result = []
        current = self.tail
        while current is not None:
            result.append(current.data)
            current = current.prev
        return result

    def clear(self) -> None:
        """Kosongkan seluruh list. Big-O: O(1)."""
        self.head = None
        self.tail = None
        self._size = 0

    def __repr__(self) -> str:
        items = self.to_list()
        return "NULL <-> " + " <-> ".join(str(x) for x in items) + " <-> NULL"

    def __iter__(self):
        """Iterasi maju. Big-O: O(n)."""
        current = self.head
        while current is not None:
            yield current.data
            current = current.next


# ================================================================
# UNIT TEST — jalankan file ini langsung untuk verifikasi
# python linked_list.py
# ================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Unit Test: SinglyLinkedList")
    print("=" * 60)

    sll = SinglyLinkedList()
    assert sll.is_empty(), "GAGAL: seharusnya kosong"

    # Test add_front & add_back
    sll.add_front("SENSOR_1")
    sll.add_front("GATEWAY_0")
    sll.add_back("SERVER_1")
    sll.add_back("SENSOR_2")
    print(f"  Isi SLL      : {sll}")
    assert len(sll) == 4, "GAGAL: size harus 4"
    assert sll.get_at(0) == "GATEWAY_0", "GAGAL: index 0"
    assert sll.get_at(3) == "SENSOR_2", "GAGAL: index 3"
    print(f"  [OK] add_front, add_back, get_at")

    # Test find & contains
    node = sll.find("SERVER_1")
    assert node is not None, "GAGAL: SERVER_1 harus ditemukan"
    assert sll.contains("SENSOR_2"), "GAGAL: SENSOR_2 harus ada"
    assert not sll.contains("SENSOR_99"), "GAGAL: SENSOR_99 tidak boleh ada"
    print(f"  [OK] find, contains")

    # Test remove_front & remove_back
    removed = sll.remove_front()
    assert removed == "GATEWAY_0", f"GAGAL: remove_front harus GATEWAY_0, dapat {removed}"
    removed = sll.remove_back()
    assert removed == "SENSOR_2", f"GAGAL: remove_back harus SENSOR_2, dapat {removed}"
    print(f"  Setelah remove: {sll}")
    print(f"  [OK] remove_front, remove_back")

    # Test delete_by_value
    sll.add_back("SENSOR_3")
    sll.add_back("SENSOR_4")
    result = sll.delete_by_value("SERVER_1")
    assert result is True, "GAGAL: delete SERVER_1 harus True"
    assert not sll.contains("SERVER_1"), "GAGAL: SERVER_1 masih ada"
    result = sll.delete_by_value("TIDAK_ADA")
    assert result is False, "GAGAL: delete nilai tidak ada harus False"
    print(f"  [OK] delete_by_value")

    # Test reverse
    sll2 = SinglyLinkedList()
    for x in [1, 2, 3, 4, 5]:
        sll2.add_back(x)
    sll2.reverse()
    assert sll2.to_list() == [5, 4, 3, 2, 1], f"GAGAL: reverse, dapat {sll2.to_list()}"
    print(f"  [OK] reverse")

    # Test iterasi
    total = sum(x for x in sll2)
    assert total == 15, f"GAGAL: sum harus 15, dapat {total}"
    print(f"  [OK] iterasi (__iter__)")

    print()
    print("=" * 60)
    print("Unit Test: DoublyLinkedList")
    print("=" * 60)

    dll = DoublyLinkedList()
    assert dll.is_empty(), "GAGAL: seharusnya kosong"

    # Test add_front & add_back
    dll.add_front("ALERT_2")
    dll.add_front("ALERT_1")
    dll.add_back("ALERT_3")
    dll.add_back("ALERT_4")
    print(f"  Isi DLL      : {dll}")
    assert len(dll) == 4, "GAGAL: size harus 4"
    print(f"  [OK] add_front, add_back")

    # Test remove_back O(1) — keunggulan DLL
    removed = dll.remove_back()
    assert removed == "ALERT_4", f"GAGAL: remove_back harus ALERT_4, dapat {removed}"
    removed = dll.remove_front()
    assert removed == "ALERT_1", f"GAGAL: remove_front harus ALERT_1, dapat {removed}"
    print(f"  Setelah remove: {dll}")
    print(f"  [OK] remove_front, remove_back (O(1) keduanya)")

    # Test traversal mundur
    dll2 = DoublyLinkedList()
    for x in ["A", "B", "C", "D"]:
        dll2.add_back(x)
    reversed_list = dll2.to_list_reversed()
    assert reversed_list == ["D", "C", "B", "A"], f"GAGAL: reversed, dapat {reversed_list}"
    print(f"  [OK] to_list_reversed (traversal mundur)")

    # Test delete_node O(1) dengan referensi langsung
    node_c = dll2.find("C")
    assert node_c is not None, "GAGAL: node C harus ada"
    dll2.delete_node(node_c)
    assert not dll2.contains("C"), "GAGAL: C masih ada setelah delete_node"
    print(f"  [OK] delete_node (O(1) dengan referensi node)")

    # Test find_backward
    dll2.add_back("E")
    node_e = dll2.find_backward("E")
    assert node_e is not None, "GAGAL: E tidak ditemukan dari backward"
    print(f"  [OK] find_backward")

    print()
    print("=" * 60)
    print("Perbandingan SLL vs DLL — Relevansi untuk Topik 4 IoT")
    print("=" * 60)
    print("""
  Operasi          | SLL (SinglyLinkedList) | DLL (DoublyLinkedList)
  -----------------|------------------------|------------------------
  add_front        | O(1)                   | O(1)
  add_back         | O(1)*                  | O(1)
  remove_front     | O(1)                   | O(1)
  remove_back      | O(n) ← harus traverse  | O(1) ← keunggulan DLL
  delete (by ref)  | O(n)                   | O(1) ← keunggulan DLL
  find             | O(n)                   | O(n)
  Memori per node  | data + 1 pointer       | data + 2 pointer

  Penggunaan dalam proyek ini:
  - SLL → Stack (AlertStack), Queue (AlertPriorityQueue), adjacency list IoTGraph
  - DLL → Tidak wajib di Topik 4, tetapi bisa dipakai jika perlu undo O(1) di tengah list
  * O(1) dengan pointer tail
    """)
    print("Semua unit test LULUS ✓")