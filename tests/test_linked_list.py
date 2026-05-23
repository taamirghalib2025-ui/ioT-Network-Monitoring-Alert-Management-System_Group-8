# ================================================================
# test_linked_list.py
# Unit Test: Singly Linked List & Doubly Linked List
# Topik 4: IoT Network Monitoring & Alert Management System
# ELT60213 Algoritma dan Struktur Data - TA 2025/2026
#
# Jalankan:
#   python test_linked_list.py
# ================================================================

import sys
import time
from linked_list import SinglyLinkedList, DoublyLinkedList


# ── Helper test framework sederhana ──────────────────────────────

_results = []

def _test(name: str, complexity: str, fn):
    try:
        fn()
        _results.append((name, complexity, True, None))
        print(f"  [LULUS] {name}  {complexity}")
    except AssertionError as e:
        _results.append((name, complexity, False, str(e)))
        print(f"  [GAGAL] {name}  {complexity}")
        print(f"          ↳ {e}")


def _summary():
    total  = len(_results)
    passed = sum(1 for _, _, ok, _ in _results if ok)
    failed = total - passed
    print()
    print("=" * 60)
    print(f"  Total  : {total}")
    print(f"  Lulus  : {passed}")
    print(f"  Gagal  : {failed}")
    if failed == 0:
        print("  Status : ✓ Semua test lulus")
    else:
        print("  Status : ✗ Ada test yang gagal")
        for name, _, ok, msg in _results:
            if not ok:
                print(f"    - {name}: {msg}")
    print("=" * 60)


# ================================================================
# TEST: SinglyLinkedList
# ================================================================

def test_sll():
    print()
    print("=" * 60)
    print("  Singly Linked List")
    print("=" * 60)

    # ── is_empty ─────────────────────────────────────────────────
    def t():
        s = SinglyLinkedList()
        assert s.is_empty(), "seharusnya kosong"
        assert len(s) == 0,  "size harus 0"
    _test("is_empty() — list baru", "O(1)", t)

    # ── add_front ────────────────────────────────────────────────
    def t():
        s = SinglyLinkedList()
        s.add_front("B")
        s.add_front("A")
        assert s.get_at(0) == "A", f"index 0 harus A, dapat {s.get_at(0)}"
        assert s.get_at(1) == "B", f"index 1 harus B, dapat {s.get_at(1)}"
        assert len(s) == 2,        f"size harus 2, dapat {len(s)}"
    _test("add_front() — tambah di depan", "O(1)", t)

    # ── add_back ─────────────────────────────────────────────────
    def t():
        s = SinglyLinkedList()
        s.add_back("X"); s.add_back("Y"); s.add_back("Z")
        assert s.to_list() == ["X", "Y", "Z"], \
            f"urutan salah: {s.to_list()}"
    _test("add_back() — tambah di belakang", "O(1)", t)

    # ── add_front + add_back gabungan ────────────────────────────
    def t():
        s = SinglyLinkedList()
        s.add_back("B"); s.add_front("A"); s.add_back("C")
        assert s.to_list() == ["A", "B", "C"], \
            f"urutan salah: {s.to_list()}"
    _test("add_front + add_back — gabungan", "O(1)", t)

    # ── get_at ───────────────────────────────────────────────────
    def t():
        s = SinglyLinkedList()
        for x in ["G", "H", "I"]:
            s.add_back(x)
        assert s.get_at(0) == "G",  f"index 0 salah: {s.get_at(0)}"
        assert s.get_at(2) == "I",  f"index 2 salah: {s.get_at(2)}"
        assert s.get_at(-1) is None, "index negatif harus None"
        assert s.get_at(5)  is None, "index out of bounds harus None"
    _test("get_at() — akses berdasarkan index", "O(n)", t)

    # ── find & contains ──────────────────────────────────────────
    def t():
        s = SinglyLinkedList()
        for x in ["SENSOR_1", "GATEWAY_0", "SERVER_1"]:
            s.add_back(x)
        assert s.find("GATEWAY_0") is not None, "GATEWAY_0 harus ditemukan"
        assert s.find("TIDAK_ADA") is None,     "nilai tidak ada harus None"
        assert s.contains("SERVER_1") is True,  "SERVER_1 harus ada"
        assert s.contains("CLOUD")   is False,  "CLOUD tidak boleh ada"
    _test("find() & contains()", "O(n)", t)

    # ── remove_front ─────────────────────────────────────────────
    def t():
        s = SinglyLinkedList()
        s.add_back("A"); s.add_back("B")
        d = s.remove_front()
        assert d == "A",           f"harus A, dapat {d}"
        assert len(s) == 1,        f"size harus 1, dapat {len(s)}"
        assert s.get_at(0) == "B", f"head baru harus B"
    _test("remove_front() — hapus dari depan", "O(1)", t)

    # ── remove_back ──────────────────────────────────────────────
    def t():
        s = SinglyLinkedList()
        s.add_back("X"); s.add_back("Y"); s.add_back("Z")
        d = s.remove_back()
        assert d == "Z",    f"harus Z, dapat {d}"
        assert len(s) == 2, f"size harus 2, dapat {len(s)}"
    _test("remove_back() — hapus dari belakang", "O(n)", t)

    # ── edge case: remove dari list kosong ───────────────────────
    def t():
        s = SinglyLinkedList()
        assert s.remove_front() is None, "remove_front() kosong harus None"
        assert s.remove_back()  is None, "remove_back() kosong harus None"
    _test("remove_front/back() — list kosong (edge case)", "O(1)", t)

    # ── edge case: remove satu elemen ────────────────────────────
    def t():
        s = SinglyLinkedList()
        s.add_back("solo")
        d = s.remove_front()
        assert d == "solo",      f"harus solo, dapat {d}"
        assert s.is_empty(),     "harus kosong setelah hapus"
        assert s.head is None,   "head harus None"
        assert s.tail is None,   "tail harus None"
    _test("remove_front() — list satu elemen (head=tail update)", "O(1)", t)

    # ── delete_by_value: elemen pertama ──────────────────────────
    def t():
        s = SinglyLinkedList()
        for x in ["A", "B", "C", "B"]:
            s.add_back(x)
        ok = s.delete_by_value("B")
        assert ok is True,                        "harus True"
        assert s.to_list() == ["A", "C", "B"],    \
            f"hanya pertama dihapus: {s.to_list()}"
    _test("delete_by_value() — hapus elemen pertama", "O(n)", t)

    # ── delete_by_value: nilai tidak ada ─────────────────────────
    def t():
        s = SinglyLinkedList()
        s.add_back("A")
        assert s.delete_by_value("Z") is False, "harus False"
    _test("delete_by_value() — nilai tidak ada", "O(n)", t)

    # ── delete_by_value: hapus tail ──────────────────────────────
    def t():
        s = SinglyLinkedList()
        for x in ["P", "Q", "R"]:
            s.add_back(x)
        s.delete_by_value("R")
        assert s.tail.data == "Q", f"tail baru harus Q, dapat {s.tail.data}"
        assert len(s) == 2,        f"size harus 2, dapat {len(s)}"
    _test("delete_by_value() — hapus tail", "O(n)", t)

    # ── insert_after ─────────────────────────────────────────────
    def t():
        s = SinglyLinkedList()
        s.add_back("A"); s.add_back("C")
        ok = s.insert_after("A", "B")
        assert ok is True,                    "harus True"
        assert s.to_list() == ["A", "B", "C"], \
            f"urutan salah: {s.to_list()}"
    _test("insert_after() — sisip setelah target", "O(n)", t)

    # ── insert_after: target tidak ada ───────────────────────────
    def t():
        s = SinglyLinkedList()
        s.add_back("A")
        assert s.insert_after("Z", "B") is False, "harus False"
    _test("insert_after() — target tidak ada", "O(n)", t)

    # ── reverse ──────────────────────────────────────────────────
    def t():
        s = SinglyLinkedList()
        for x in [1, 2, 3, 4, 5]:
            s.add_back(x)
        s.reverse()
        assert s.to_list() == [5, 4, 3, 2, 1], \
            f"urutan salah: {s.to_list()}"
        assert s.head.data == 5, f"head harus 5, dapat {s.head.data}"
        assert s.tail.data == 1, f"tail harus 1, dapat {s.tail.data}"
    _test("reverse() — balik urutan in-place", "O(n)", t)

    # ── clear ────────────────────────────────────────────────────
    def t():
        s = SinglyLinkedList()
        for x in [1, 2, 3]:
            s.add_back(x)
        s.clear()
        assert s.is_empty(), "harus kosong setelah clear"
        assert len(s) == 0,  f"size harus 0, dapat {len(s)}"
    _test("clear() — kosongkan list", "O(1)", t)

    # ── iterasi ──────────────────────────────────────────────────
    def t():
        s = SinglyLinkedList()
        for x in [10, 20, 30]:
            s.add_back(x)
        collected = list(s)
        assert collected == [10, 20, 30], \
            f"iterasi salah: {collected}"
    _test("iterasi — for loop (__iter__)", "O(n)", t)

    # ── konsistensi size ─────────────────────────────────────────
    def t():
        s = SinglyLinkedList()
        for i in range(10):
            s.add_back(i)
        s.remove_front()
        s.remove_back()
        s.delete_by_value(5)
        assert len(s) == 7, f"size harus 7, dapat {len(s)}"
    _test("size konsisten setelah banyak operasi", "O(1)", t)


# ================================================================
# TEST: DoublyLinkedList
# ================================================================

def test_dll():
    print()
    print("=" * 60)
    print("  Doubly Linked List")
    print("=" * 60)

    # ── is_empty ─────────────────────────────────────────────────
    def t():
        d = DoublyLinkedList()
        assert d.is_empty(), "seharusnya kosong"
        assert len(d) == 0,  "size harus 0"
    _test("is_empty() — list baru", "O(1)", t)

    # ── add_front: pointer prev ──────────────────────────────────
    def t():
        d = DoublyLinkedList()
        d.add_front("ALERT_2"); d.add_front("ALERT_1")
        assert d.head.data == "ALERT_1",          \
            f"head harus ALERT_1, dapat {d.head.data}"
        assert d.head.next.data == "ALERT_2",     "next harus ALERT_2"
        assert d.head.next.prev is d.head,        "prev harus menunjuk head"
    _test("add_front() — pointer prev", "O(1)", t)

    # ── add_back: pointer prev ───────────────────────────────────
    def t():
        d = DoublyLinkedList()
        for x in ["A", "B", "C"]:
            d.add_back(x)
        assert d.to_list() == ["A", "B", "C"],  \
            f"urutan salah: {d.to_list()}"
        assert d.tail.data == "C",              f"tail harus C"
        assert d.tail.prev.data == "B",         "prev tail harus B"
    _test("add_back() — pointer prev", "O(1)", t)

    # ── remove_front O(1) ────────────────────────────────────────
    def t():
        d = DoublyLinkedList()
        for x in ["ALERT_1", "ALERT_2", "ALERT_3"]:
            d.add_back(x)
        v = d.remove_front()
        assert v == "ALERT_1",         f"harus ALERT_1, dapat {v}"
        assert d.head.prev is None,    "prev head baru harus None"
        assert len(d) == 2,            f"size harus 2, dapat {len(d)}"
    _test("remove_front() — O(1)", "O(1)", t)

    # ── remove_back O(1) ─────────────────────────────────────────
    def t():
        d = DoublyLinkedList()
        for x in ["X", "Y", "Z"]:
            d.add_back(x)
        v = d.remove_back()
        assert v == "Z",               f"harus Z, dapat {v}"
        assert d.tail.next is None,    "next tail baru harus None"
        assert len(d) == 2,            f"size harus 2, dapat {len(d)}"
    _test("remove_back() — O(1) keunggulan DLL", "O(1)", t)

    # ── edge case: remove satu elemen ────────────────────────────
    def t():
        d = DoublyLinkedList()
        d.add_back("solo")
        d.remove_front()
        assert d.is_empty(),   "harus kosong"
        assert d.head is None, "head harus None"
        assert d.tail is None, "tail harus None"
    _test("remove_front/back() — satu elemen (head=tail)", "O(1)", t)

    # ── delete_node: tengah ──────────────────────────────────────
    def t():
        d = DoublyLinkedList()
        for x in ["A", "B", "C", "D"]:
            d.add_back(x)
        node_b = d.find("B")
        d.delete_node(node_b)
        assert d.to_list() == ["A", "C", "D"],  \
            f"urutan salah: {d.to_list()}"
        assert len(d) == 3, f"size harus 3, dapat {len(d)}"
    _test("delete_node() — hapus node tengah O(1)", "O(1)", t)

    # ── delete_node: head ────────────────────────────────────────
    def t():
        d = DoublyLinkedList()
        for x in ["H", "I", "J"]:
            d.add_back(x)
        d.delete_node(d.head)
        assert d.head.data == "I",   f"head baru harus I, dapat {d.head.data}"
        assert d.head.prev is None,  "prev head baru harus None"
    _test("delete_node() — hapus head", "O(1)", t)

    # ── delete_node: tail ────────────────────────────────────────
    def t():
        d = DoublyLinkedList()
        for x in ["P", "Q", "R"]:
            d.add_back(x)
        d.delete_node(d.tail)
        assert d.tail.data == "Q",   f"tail baru harus Q, dapat {d.tail.data}"
        assert d.tail.next is None,  "next tail baru harus None"
    _test("delete_node() — hapus tail", "O(1)", t)

    # ── delete_by_value ──────────────────────────────────────────
    def t():
        d = DoublyLinkedList()
        for x in ["M", "N", "O"]:
            d.add_back(x)
        assert d.delete_by_value("N") is True,  "harus True"
        assert not d.contains("N"),             "N tidak boleh ada lagi"
        assert d.delete_by_value("Z") is False, "nilai tidak ada harus False"
    _test("delete_by_value()", "O(n)", t)

    # ── find & find_backward ─────────────────────────────────────
    def t():
        d = DoublyLinkedList()
        for x in ["A", "B", "C", "D"]:
            d.add_back(x)
        assert d.find("C")          is not None, "find C harus ada"
        assert d.find_backward("B") is not None, "find_backward B harus ada"
        assert d.find("Z")          is None,     "Z tidak ada"
        assert d.find_backward("Z") is None,     "Z tidak ada dari belakang"
    _test("find() & find_backward() — dua arah", "O(n)", t)

    # ── to_list_reversed ─────────────────────────────────────────
    def t():
        d = DoublyLinkedList()
        for x in ["A", "B", "C", "D"]:
            d.add_back(x)
        r = d.to_list_reversed()
        assert r == ["D", "C", "B", "A"], f"urutan terbalik salah: {r}"
    _test("to_list_reversed() — traversal mundur", "O(n)", t)

    # ── integritas pointer prev setelah add_back ─────────────────
    def t():
        d = DoublyLinkedList()
        for x in [1, 2, 3]:
            d.add_back(x)
        vals = []
        c = d.tail
        while c:
            vals.append(c.data)
            c = c.prev
        assert vals == [3, 2, 1], f"traversal mundur via prev salah: {vals}"
    _test("integritas pointer prev — setelah add_back", "O(1)", t)

    # ── integritas pointer setelah delete banyak node ────────────
    def t():
        d = DoublyLinkedList()
        for x in [1, 2, 3, 4, 5]:
            d.add_back(x)
        d.delete_by_value(2)
        d.delete_by_value(4)
        fwd = d.to_list()
        bwd = d.to_list_reversed()
        assert fwd == [1, 3, 5], f"maju salah: {fwd}"
        assert bwd == [5, 3, 1], f"mundur salah: {bwd}"
    _test("integritas pointer — setelah banyak penghapusan", "O(n)", t)

    # ── clear ────────────────────────────────────────────────────
    def t():
        d = DoublyLinkedList()
        for x in [1, 2, 3]:
            d.add_back(x)
        d.clear()
        assert d.is_empty(), "harus kosong setelah clear"
        assert d.head is None and d.tail is None, "head dan tail harus None"
    _test("clear() — kosongkan list", "O(1)", t)

    # ── konsistensi size ─────────────────────────────────────────
    def t():
        d = DoublyLinkedList()
        for i in range(8):
            d.add_back(i)
        d.remove_front()
        d.remove_back()
        d.delete_by_value(3)
        d.delete_by_value(6)
        assert len(d) == 4, f"size harus 4, dapat {len(d)}"
    _test("size konsisten setelah banyak operasi", "O(1)", t)


# ================================================================
# MAIN
# ================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Test Runner — Linked List")
    print("  ELT60213 Algoritma dan Struktur Data TA 2025/2026")
    print("=" * 60)

    t0 = time.perf_counter()
    test_sll()
    test_dll()
    elapsed_ms = (time.perf_counter() - t0) * 1000

    _summary()
    print(f"  Waktu  : {elapsed_ms:.2f} ms")
    print()

    failed = sum(1 for _, _, ok, _ in _results if not ok)
    sys.exit(1 if failed > 0 else 0)