# ================================================================
# test_queue.py
# Unit Test: AlertPriorityQueue
# Topik 4: IoT Network Monitoring & Alert Management System
# ELT60213 Algoritma dan Struktur Data - TA 2025/2026
#
# Jalankan:
#   python test_queue.py
# ================================================================

import sys
import time
from queue import AlertPriorityQueue


# ── Stub Alert ───────────────────────────────────────────────────
# Meniru objek alert asli; hanya butuh atribut .tipe dan .pesan

class Alert:
    def __init__(self, tipe: int, pesan: str):
        self.tipe  = tipe   # 1=CRITICAL, 2=WARNING, 3=INFO
        self.pesan = pesan

    def __repr__(self):
        label = {1: "CRITICAL", 2: "WARNING", 3: "INFO"}.get(self.tipe, str(self.tipe))
        return f"Alert({label}, '{self.pesan}')"


# ── Helper test framework ────────────────────────────────────────

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
# TEST: AlertPriorityQueue
# ================================================================

def test_apq():
    print()
    print("=" * 60)
    print("  AlertPriorityQueue")
    print("=" * 60)

    # ── is_empty & __len__ ───────────────────────────────────────
    def t():
        q = AlertPriorityQueue()
        assert q.is_empty(),  "queue baru harus kosong"
        assert len(q) == 0,   f"size harus 0, dapat {len(q)}"
    _test("is_empty() & __len__() — queue baru", "O(1)", t)

    # ── enqueue satu elemen ──────────────────────────────────────
    def t():
        q = AlertPriorityQueue()
        q.enqueue(Alert(2, "disk penuh"))
        assert not q.is_empty(),        "seharusnya tidak kosong"
        assert len(q) == 1,             f"size harus 1, dapat {len(q)}"
        assert q.peek().tipe == 2,      "peek harus tipe 2"
    _test("enqueue() — satu elemen", "O(n)", t)

    # ── urutan prioritas: CRITICAL di depan ──────────────────────
    def t():
        q = AlertPriorityQueue()
        q.enqueue(Alert(3, "info"))
        q.enqueue(Alert(1, "critical"))
        q.enqueue(Alert(2, "warning"))
        urutan = [a.tipe for a in q.pending_alerts()]
        assert urutan == [1, 2, 3], \
            f"urutan harus [1,2,3], dapat {urutan}"
    _test("enqueue() — urutan prioritas ASC (CRITICAL=1 di depan)", "O(n)", t)

    # ── enqueue urutan terbalik ──────────────────────────────────
    def t():
        q = AlertPriorityQueue()
        for tipe in [3, 2, 1]:
            q.enqueue(Alert(tipe, f"alert-{tipe}"))
        urutan = [a.tipe for a in q.pending_alerts()]
        assert urutan == [1, 2, 3], \
            f"urutan salah setelah insert terbalik: {urutan}"
    _test("enqueue() — insert terbalik (3,2,1) → tetap [1,2,3]", "O(n)", t)

    # ── enqueue sudah terurut ────────────────────────────────────
    def t():
        q = AlertPriorityQueue()
        for tipe in [1, 2, 3]:
            q.enqueue(Alert(tipe, f"alert-{tipe}"))
        urutan = [a.tipe for a in q.pending_alerts()]
        assert urutan == [1, 2, 3], \
            f"urutan salah: {urutan}"
    _test("enqueue() — insert sudah terurut (1,2,3)", "O(n)", t)

    # ── enqueue prioritas sama: FIFO dalam tier ──────────────────
    def t():
        q = AlertPriorityQueue()
        q.enqueue(Alert(2, "W1"))
        q.enqueue(Alert(2, "W2"))
        q.enqueue(Alert(2, "W3"))
        pesan = [a.pesan for a in q.pending_alerts()]
        assert pesan == ["W1", "W2", "W3"], \
            f"FIFO dalam tier sama salah: {pesan}"
    _test("enqueue() — prioritas sama mempertahankan urutan FIFO", "O(n)", t)

    # ── enqueue prioritas sama di antara berbeda ─────────────────
    def t():
        q = AlertPriorityQueue()
        q.enqueue(Alert(1, "C1"))
        q.enqueue(Alert(3, "I1"))
        q.enqueue(Alert(1, "C2"))   # CRITICAL kedua, harus setelah C1
        q.enqueue(Alert(2, "W1"))
        urutan = [(a.tipe, a.pesan) for a in q.pending_alerts()]
        assert urutan[0] == (1, "C1"), f"posisi 0 salah: {urutan[0]}"
        assert urutan[1] == (1, "C2"), f"posisi 1 salah: {urutan[1]}"
        assert urutan[2] == (2, "W1"), f"posisi 2 salah: {urutan[2]}"
        assert urutan[3] == (3, "I1"), f"posisi 3 salah: {urutan[3]}"
    _test("enqueue() — tier campur, FIFO dalam tier sama", "O(n)", t)

    # ── dequeue mengembalikan CRITICAL duluan ────────────────────
    def t():
        q = AlertPriorityQueue()
        q.enqueue(Alert(3, "info"))
        q.enqueue(Alert(1, "critical"))
        q.enqueue(Alert(2, "warning"))
        first = q.dequeue()
        assert first.tipe == 1, \
            f"dequeue pertama harus CRITICAL (1), dapat {first.tipe}"
    _test("dequeue() — kembalikan CRITICAL (tipe=1) duluan", "O(1)", t)

    # ── dequeue mengurangi size ──────────────────────────────────
    def t():
        q = AlertPriorityQueue()
        for tipe in [1, 2, 3]:
            q.enqueue(Alert(tipe, "x"))
        q.dequeue()
        assert len(q) == 2, f"size harus 2, dapat {len(q)}"
        q.dequeue()
        assert len(q) == 1, f"size harus 1, dapat {len(q)}"
        q.dequeue()
        assert len(q) == 0, f"size harus 0, dapat {len(q)}"
        assert q.is_empty(), "seharusnya kosong"
    _test("dequeue() — size berkurang setiap dequeue", "O(1)", t)

    # ── dequeue urutan penuh ─────────────────────────────────────
    def t():
        q = AlertPriorityQueue()
        q.enqueue(Alert(2, "W"))
        q.enqueue(Alert(1, "C"))
        q.enqueue(Alert(3, "I"))
        urutan = []
        while not q.is_empty():
            urutan.append(q.dequeue().tipe)
        assert urutan == [1, 2, 3], \
            f"urutan dequeue salah: {urutan}"
    _test("dequeue() — urutan penuh [1,2,3]", "O(1)", t)

    # ── dequeue dari queue kosong ────────────────────────────────
    def t():
        q = AlertPriorityQueue()
        assert q.dequeue() is None, "dequeue kosong harus None"
    _test("dequeue() — queue kosong (edge case)", "O(1)", t)

    # ── dequeue sampai kosong, lalu enqueue lagi ─────────────────
    def t():
        q = AlertPriorityQueue()
        q.enqueue(Alert(1, "C"))
        q.dequeue()
        assert q.is_empty(), "harus kosong setelah dequeue semua"
        q.enqueue(Alert(2, "W"))
        assert len(q) == 1,       f"size harus 1, dapat {len(q)}"
        assert q.peek().tipe == 2, "peek harus tipe 2"
    _test("enqueue setelah kosong — queue reusable", "O(n)", t)

    # ── peek tidak menghapus ─────────────────────────────────────
    def t():
        q = AlertPriorityQueue()
        q.enqueue(Alert(1, "C"))
        q.enqueue(Alert(2, "W"))
        top = q.peek()
        assert top.tipe == 1, f"peek harus tipe 1, dapat {top.tipe}"
        assert len(q) == 2,   f"size tidak boleh berubah, dapat {len(q)}"
        assert q.peek().tipe == 1, "peek kedua harus sama"
    _test("peek() — tidak menghapus elemen", "O(1)", t)

    # ── peek queue kosong ────────────────────────────────────────
    def t():
        q = AlertPriorityQueue()
        assert q.peek() is None, "peek kosong harus None"
    _test("peek() — queue kosong (edge case)", "O(1)", t)

    # ── pending_alerts mengembalikan semua ───────────────────────
    def t():
        q = AlertPriorityQueue()
        alerts = [Alert(3,"I"), Alert(1,"C"), Alert(2,"W")]
        for a in alerts:
            q.enqueue(a)
        pending = q.pending_alerts()
        assert len(pending) == 3, \
            f"pending harus 3 elemen, dapat {len(pending)}"
        assert pending[0].tipe == 1, "elemen pertama harus CRITICAL"
        assert pending[2].tipe == 3, "elemen terakhir harus INFO"
    _test("pending_alerts() — kembalikan semua terurut", "O(n)", t)

    # ── pending_alerts tidak mengubah queue ──────────────────────
    def t():
        q = AlertPriorityQueue()
        q.enqueue(Alert(1,"C")); q.enqueue(Alert(2,"W"))
        _ = q.pending_alerts()
        assert len(q) == 2, \
            f"size tidak boleh berubah setelah pending_alerts, dapat {len(q)}"
    _test("pending_alerts() — tidak mengubah queue", "O(n)", t)

    # ── pending_alerts queue kosong ──────────────────────────────
    def t():
        q = AlertPriorityQueue()
        assert q.pending_alerts() == [], "harus list kosong"
    _test("pending_alerts() — queue kosong", "O(n)", t)

    # ── enqueue banyak elemen, validasi size ─────────────────────
    def t():
        q = AlertPriorityQueue()
        n = 50
        for i in range(n):
            q.enqueue(Alert((i % 3) + 1, f"alert-{i}"))
        assert len(q) == n, f"size harus {n}, dapat {len(q)}"
        dequeued = 0
        prev_tipe = 0
        while not q.is_empty():
            a = q.dequeue()
            assert a.tipe >= prev_tipe, \
                f"urutan rusak: tipe {a.tipe} setelah {prev_tipe}"
            prev_tipe = a.tipe
            dequeued += 1
        assert dequeued == n, f"harus dequeue {n} kali, dapat {dequeued}"
    _test("stress — 50 alert campur, urutan selalu ASC", "O(n)", t)

    # ── enqueue CRITICAL ke queue berisi WARNING/INFO ─────────────
    def t():
        q = AlertPriorityQueue()
        q.enqueue(Alert(2, "W1"))
        q.enqueue(Alert(3, "I1"))
        q.enqueue(Alert(1, "C_baru"))   # disisip di depan
        assert q.peek().tipe == 1,       "CRITICAL harus jadi head"
        assert q.peek().pesan == "C_baru"
        assert len(q) == 3
    _test("enqueue CRITICAL ke queue yg sudah isi WARNING/INFO", "O(n)", t)

    # ── konsistensi head setelah dequeue ─────────────────────────
    def t():
        q = AlertPriorityQueue()
        q.enqueue(Alert(1, "C"))
        q.enqueue(Alert(2, "W"))
        q.dequeue()                     # hapus CRITICAL
        assert q.head is not None,       "head tidak boleh None"
        assert q.head.data.tipe == 2,   \
            f"head baru harus WARNING (2), dapat {q.head.data.tipe}"
    _test("head pointer update setelah dequeue CRITICAL", "O(1)", t)


# ================================================================
# MAIN
# ================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Test Runner — AlertPriorityQueue")
    print("  ELT60213 Algoritma dan Struktur Data TA 2025/2026")
    print("=" * 60)

    t0 = time.perf_counter()
    test_apq()
    elapsed_ms = (time.perf_counter() - t0) * 1000

    _summary()
    print(f"  Waktu  : {elapsed_ms:.2f} ms")
    print()

    failed = sum(1 for _, _, ok, _ in _results if not ok)
    sys.exit(1 if failed > 0 else 0)