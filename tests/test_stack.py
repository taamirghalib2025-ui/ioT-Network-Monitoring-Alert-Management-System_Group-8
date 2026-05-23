# ================================================================
# test_stack.py
# Unit Test: AlertStack & Stack
# Topik 4: IoT Network Monitoring & Alert Management System
# ELT60213 Algoritma dan Struktur Data - TA 2025/2026
#
# Jalankan:
#   python test_stack.py
# ================================================================

import sys
import time
from stack import Alert, AlertStack, Stack


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


# ── Stub factory ─────────────────────────────────────────────────

def make_alert(alert_id: int, tipe: int = 1, device: str = "SENSOR_0") -> Alert:
    return Alert(
        alert_id=alert_id,
        device_id=device,
        tipe=tipe,
        pesan=f"Pesan alert {alert_id}",
        timestamp=time.time(),
    )


# ================================================================
# TEST: AlertStack
# ================================================================

def test_alert_stack():
    print()
    print("=" * 60)
    print("  AlertStack")
    print("=" * 60)

    # ── is_empty & __len__ ───────────────────────────────────────
    def t():
        s = AlertStack()
        assert s.is_empty(),  "stack baru harus kosong"
        assert len(s) == 0,   f"size harus 0, dapat {len(s)}"
    _test("is_empty() & __len__() — stack baru", "O(1)", t)

    # ── is_full ──────────────────────────────────────────────────
    def t():
        s = AlertStack(kapasitas=3)
        assert not s.is_full(), "belum penuh"
        for i in range(1, 4):
            s.push(make_alert(i))
        assert s.is_full(),    "seharusnya penuh setelah 3 push"
        assert len(s) == 3,    f"size harus 3, dapat {len(s)}"
    _test("is_full() — setelah push sampai kapasitas", "O(1)", t)

    # ── push dasar ───────────────────────────────────────────────
    def t():
        s = AlertStack(kapasitas=5)
        s.push(make_alert(1))
        assert not s.is_empty(),         "seharusnya tidak kosong"
        assert len(s) == 1,              f"size harus 1, dapat {len(s)}"
        assert s.top.data.alert_id == 1, "top harus Alert#1"
    _test("push() — satu elemen", "O(1)", t)

    # ── push LIFO: top selalu yang terbaru ───────────────────────
    def t():
        s = AlertStack(kapasitas=5)
        for i in [1, 2, 3]:
            s.push(make_alert(i))
        assert s.top.data.alert_id == 3, \
            f"top harus Alert#3 (terbaru), dapat {s.top.data.alert_id}"
    _test("push() — top selalu alert terbaru (LIFO)", "O(1)", t)

    # ── pop dasar ────────────────────────────────────────────────
    def t():
        s = AlertStack(kapasitas=5)
        s.push(make_alert(1))
        s.push(make_alert(2))
        a = s.pop()
        assert a.alert_id == 2, f"pop harus Alert#2, dapat {a.alert_id}"
        assert len(s) == 1,     f"size harus 1, dapat {len(s)}"
    _test("pop() — kembalikan top (LIFO)", "O(1)", t)

    # ── pop urutan LIFO penuh ────────────────────────────────────
    def t():
        s = AlertStack(kapasitas=5)
        for i in [1, 2, 3, 4, 5]:
            s.push(make_alert(i))
        urutan = []
        while not s.is_empty():
            urutan.append(s.pop().alert_id)
        assert urutan == [5, 4, 3, 2, 1], \
            f"urutan LIFO salah: {urutan}"
    _test("pop() — urutan LIFO [5,4,3,2,1]", "O(1)", t)

    # ── pop stack kosong ─────────────────────────────────────────
    def t():
        s = AlertStack()
        assert s.pop() is None, "pop kosong harus None"
    _test("pop() — stack kosong (edge case)", "O(1)", t)

    # ── peek tidak menghapus ─────────────────────────────────────
    def t():
        s = AlertStack(kapasitas=5)
        s.push(make_alert(1))
        s.push(make_alert(2))
        top = s.peek()
        assert top.alert_id == 2, f"peek harus Alert#2, dapat {top.alert_id}"
        assert len(s) == 2,       f"size tidak boleh berubah, dapat {len(s)}"
        assert s.peek().alert_id == 2, "peek kedua harus sama"
    _test("peek() — tidak menghapus elemen", "O(1)", t)

    # ── peek stack kosong ────────────────────────────────────────
    def t():
        s = AlertStack()
        assert s.peek() is None, "peek kosong harus None"
    _test("peek() — stack kosong (edge case)", "O(1)", t)

    # ── to_list: urutan top ke bottom ────────────────────────────
    def t():
        s = AlertStack(kapasitas=5)
        for i in [1, 2, 3]:
            s.push(make_alert(i))
        lst = [a.alert_id for a in s.to_list()]
        assert lst == [3, 2, 1], \
            f"to_list harus [3,2,1] (top→bottom), dapat {lst}"
    _test("to_list() — urutan top ke bottom", "O(n)", t)

    # ── to_list tidak mengubah stack ─────────────────────────────
    def t():
        s = AlertStack(kapasitas=5)
        for i in [1, 2, 3]:
            s.push(make_alert(i))
        _ = s.to_list()
        assert len(s) == 3, \
            f"size tidak boleh berubah setelah to_list, dapat {len(s)}"
        assert s.peek().alert_id == 3, "top tidak boleh berubah"
    _test("to_list() — tidak mengubah stack", "O(n)", t)

    # ── to_list stack kosong ─────────────────────────────────────
    def t():
        s = AlertStack()
        assert s.to_list() == [], "to_list kosong harus []"
    _test("to_list() — stack kosong", "O(n)", t)

    # ── clear ────────────────────────────────────────────────────
    def t():
        s = AlertStack(kapasitas=5)
        for i in range(1, 4):
            s.push(make_alert(i))
        s.clear()
        assert s.is_empty(),   "harus kosong setelah clear"
        assert len(s) == 0,    f"size harus 0, dapat {len(s)}"
        assert s.top is None,  "top harus None setelah clear"
    _test("clear() — kosongkan stack", "O(1)", t)

    # ── _hapus_bottom: overflow +1 ───────────────────────────────
    def t():
        s = AlertStack(kapasitas=3)
        for i in [1, 2, 3]:
            s.push(make_alert(i))
        s.push(make_alert(4))   # overflow → Alert#1 dihapus
        assert len(s) == 3,     f"size harus tetap 3, dapat {len(s)}"
        ids = [a.alert_id for a in s.to_list()]
        assert 1 not in ids,    f"Alert#1 (terlama) harus sudah dihapus: {ids}"
        assert ids[0] == 4,     f"top harus Alert#4 (terbaru): {ids}"
    _test("_hapus_bottom() — overflow +1, alert terlama dibuang", "O(n)", t)

    # ── _hapus_bottom: overflow berulang ─────────────────────────
    def t():
        s = AlertStack(kapasitas=3)
        for i in range(1, 7):   # push 6 alert ke kapasitas=3
            s.push(make_alert(i))
        assert len(s) == 3,     f"size harus 3, dapat {len(s)}"
        ids = [a.alert_id for a in s.to_list()]
        assert ids == [6, 5, 4], \
            f"harus menyimpan 3 terbaru [6,5,4], dapat {ids}"
    _test("_hapus_bottom() — overflow berulang, hanya 3 terbaru", "O(n)", t)

    # ── kapasitas=1: selalu hanya 1 elemen ───────────────────────
    def t():
        s = AlertStack(kapasitas=1)
        s.push(make_alert(1))
        s.push(make_alert(2))   # Alert#1 dibuang
        assert len(s) == 1,     f"size harus 1, dapat {len(s)}"
        assert s.peek().alert_id == 2, \
            f"top harus Alert#2, dapat {s.peek().alert_id}"
    _test("kapasitas=1 — selalu hanya simpan 1 elemen terbaru", "O(n)", t)

    # ── reusable setelah clear ───────────────────────────────────
    def t():
        s = AlertStack(kapasitas=5)
        for i in [1, 2, 3]:
            s.push(make_alert(i))
        s.clear()
        s.push(make_alert(99))
        assert len(s) == 1,               f"size harus 1, dapat {len(s)}"
        assert s.peek().alert_id == 99,   "top harus Alert#99"
    _test("stack reusable setelah clear()", "O(1)", t)

    # ── data tipe tersimpan dengan benar ─────────────────────────
    def t():
        s = AlertStack(kapasitas=5)
        a = Alert(42, "GATEWAY_0", 1, "CRITICAL kebakaran", 1234567890.0)
        s.push(a)
        top = s.peek()
        assert top.alert_id  == 42,              "alert_id salah"
        assert top.device_id == "GATEWAY_0",     "device_id salah"
        assert top.tipe      == 1,               "tipe salah"
        assert top.pesan     == "CRITICAL kebakaran", "pesan salah"
        assert top.timestamp == 1234567890.0,    "timestamp salah"
    _test("data Alert tersimpan lengkap dan benar", "O(1)", t)

    # ── konsistensi size setelah operasi campuran ─────────────────
    def t():
        s = AlertStack(kapasitas=10)
        for i in range(1, 8):
            s.push(make_alert(i))
        s.pop(); s.pop()
        s.push(make_alert(99))
        assert len(s) == 6, f"size harus 6, dapat {len(s)}"
    _test("konsistensi size setelah push/pop campuran", "O(1)", t)

    # ── stress: overflow panjang ─────────────────────────────────
    def t():
        cap = 5
        s = AlertStack(kapasitas=cap)
        for i in range(1, 51):    # push 50 alert ke kapasitas=5
            s.push(make_alert(i))
        assert len(s) == cap,     f"size harus {cap}, dapat {len(s)}"
        ids = [a.alert_id for a in s.to_list()]
        assert ids == [50, 49, 48, 47, 46], \
            f"harus 5 terbaru [50..46], dapat {ids}"
        prev = float('inf')
        for a in s.to_list():
            assert a.alert_id <= prev, "urutan top→bottom harus turun"
            prev = a.alert_id
    _test("stress — push 50 ke kapasitas=5, hanya 5 terbaru", "O(n)", t)


# ================================================================
# TEST: Stack (umum / DFS)
# ================================================================

def test_stack():
    print()
    print("=" * 60)
    print("  Stack (umum)")
    print("=" * 60)

    # ── is_empty & __len__ ───────────────────────────────────────
    def t():
        s = Stack()
        assert s.is_empty(), "stack baru harus kosong"
        assert len(s) == 0,  f"size harus 0, dapat {len(s)}"
    _test("is_empty() & __len__() — stack baru", "O(1)", t)

    # ── push & LIFO ──────────────────────────────────────────────
    def t():
        s = Stack()
        for v in ["GATEWAY_0", "SERVER_1", "SENSOR_5"]:
            s.push(v)
        assert s.peek() == "SENSOR_5", \
            f"top harus SENSOR_5, dapat {s.peek()}"
        assert len(s) == 3, f"size harus 3, dapat {len(s)}"
    _test("push() — top selalu nilai terbaru (LIFO)", "O(1)", t)

    # ── pop urutan LIFO ──────────────────────────────────────────
    def t():
        s = Stack()
        nodes = ["A", "B", "C", "D"]
        for v in nodes:
            s.push(v)
        urutan = []
        while not s.is_empty():
            urutan.append(s.pop())
        assert urutan == ["D", "C", "B", "A"], \
            f"urutan LIFO salah: {urutan}"
    _test("pop() — urutan LIFO [D,C,B,A]", "O(1)", t)

    # ── pop stack kosong ─────────────────────────────────────────
    def t():
        s = Stack()
        assert s.pop() is None, "pop kosong harus None"
    _test("pop() — stack kosong (edge case)", "O(1)", t)

    # ── peek tidak menghapus ─────────────────────────────────────
    def t():
        s = Stack()
        s.push("X"); s.push("Y")
        assert s.peek() == "Y",  f"peek harus Y, dapat {s.peek()}"
        assert len(s) == 2,      f"size tidak boleh berubah, dapat {len(s)}"
    _test("peek() — tidak menghapus elemen", "O(1)", t)

    # ── peek stack kosong ────────────────────────────────────────
    def t():
        s = Stack()
        assert s.peek() is None, "peek kosong harus None"
    _test("peek() — stack kosong (edge case)", "O(1)", t)

    # ── simulasi DFS traversal ───────────────────────────────────
    def t():
        # Graph sederhana: A→B, A→C, B→D
        graph = {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
        s = Stack()
        s.push("A")
        visited = []
        while not s.is_empty():
            node = s.pop()
            if node not in visited:
                visited.append(node)
                for neighbor in reversed(graph.get(node, [])):
                    s.push(neighbor)
        assert "A" in visited, "A harus dikunjungi"
        assert "D" in visited, "D harus dikunjungi"
        assert len(visited) == 4, f"harus 4 node, dapat {len(visited)}"
    _test("simulasi DFS traversal graph 4 node", "O(1)", t)

    # ── konsistensi size ─────────────────────────────────────────
    def t():
        s = Stack()
        for i in range(10):
            s.push(i)
        for _ in range(4):
            s.pop()
        assert len(s) == 6, f"size harus 6, dapat {len(s)}"
    _test("konsistensi size setelah push/pop", "O(1)", t)

    # ── tipe data beragam ────────────────────────────────────────
    def t():
        s = Stack()
        s.push(42)
        s.push("string")
        s.push([1, 2, 3])
        assert s.peek() == [1, 2, 3], "top harus list"
        s.pop()
        assert s.peek() == "string",  "top harus string"
    _test("push() — tipe data beragam (int, str, list)", "O(1)", t)


# ================================================================
# MAIN
# ================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Test Runner — AlertStack & Stack")
    print("  ELT60213 Algoritma dan Struktur Data TA 2025/2026")
    print("=" * 60)

    t0 = time.perf_counter()
    test_alert_stack()
    test_stack()
    elapsed_ms = (time.perf_counter() - t0) * 1000

    _summary()
    print(f"  Waktu  : {elapsed_ms:.2f} ms")
    print()

    failed = sum(1 for _, _, ok, _ in _results if not ok)
    sys.exit(1 if failed > 0 else 0)