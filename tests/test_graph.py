"""
test_graph.py — Unit Test untuk IoTGraph (graph.py)
Jalankan: pytest test_graph.py -v
"""

import pytest
from graph import IoTGraph


# ── Fixture: dummy Device sederhana ──────────────────────────────────────────
class DummyDevice:
    """Stub Device agar tidak perlu import modul device.py."""
    def __init__(self, device_id: str):
        self.device_id = device_id


# ── Helper ────────────────────────────────────────────────────────────────────
def make_graph(*device_ids):
    """Buat IoTGraph dan tambahkan device-device berdasarkan ID yang diberikan."""
    g = IoTGraph()
    for did in device_ids:
        g.add_device(DummyDevice(did))
    return g


# ══════════════════════════════════════════════════════════════════════════════
# 1. add_device
# ══════════════════════════════════════════════════════════════════════════════
class TestAddDevice:

    def test_device_terdaftar_di_adj(self):
        g = IoTGraph()
        d = DummyDevice("A")
        g.add_device(d)
        assert "A" in g.adj

    def test_device_terdaftar_di_devices(self):
        g = IoTGraph()
        d = DummyDevice("A")
        g.add_device(d)
        assert g.devices["A"] is d

    def test_adj_awal_none(self):
        g = make_graph("A")
        assert g.adj["A"] is None

    def test_add_device_duplikat_tidak_overwrite_edge(self):
        """Menambahkan device yang sudah ada tidak menghapus edge yang ada."""
        g = make_graph("A", "B")
        g.add_link("A", "B", 10)
        g.add_device(DummyDevice("A"))          # tambah ulang
        assert g.degree("A") == 1               # edge tetap ada

    def test_tambah_banyak_device(self):
        ids = [f"D{i}" for i in range(50)]
        g = make_graph(*ids)
        assert len(g.adj) == 50


# ══════════════════════════════════════════════════════════════════════════════
# 2. add_link
# ══════════════════════════════════════════════════════════════════════════════
class TestAddLink:

    def test_edge_ada_di_kedua_arah(self):
        g = make_graph("A", "B")
        g.add_link("A", "B", 20)
        nbr_a = dict(g.neighbors("A"))
        nbr_b = dict(g.neighbors("B"))
        assert "B" in nbr_a
        assert "A" in nbr_b

    def test_latensi_tersimpan_benar(self):
        g = make_graph("A", "B")
        g.add_link("A", "B", 35)
        nbr = dict(g.neighbors("A"))
        assert nbr["B"] == 35

    def test_add_link_buat_node_baru_jika_belum_ada(self):
        """add_link harus membuat node baru otomatis jika belum ada di adj."""
        g = IoTGraph()
        g.add_link("X", "Y", 5)
        assert "X" in g.adj
        assert "Y" in g.adj

    def test_multi_edge_dari_satu_node(self):
        g = make_graph("A", "B", "C")
        g.add_link("A", "B", 10)
        g.add_link("A", "C", 20)
        assert g.degree("A") == 2

    def test_self_loop(self):
        """Self-loop tidak crash dan terekam."""
        g = make_graph("A")
        g.add_link("A", "A", 0)
        # degree akan mencatat 2 entry (kedua arah ke diri sendiri)
        assert g.degree("A") >= 1


# ══════════════════════════════════════════════════════════════════════════════
# 3. remove_link
# ══════════════════════════════════════════════════════════════════════════════
class TestRemoveLink:

    def test_hapus_edge_berhasil(self):
        g = make_graph("A", "B")
        g.add_link("A", "B", 10)
        result = g.remove_link("A", "B")
        assert result is True

    def test_edge_hilang_di_kedua_arah(self):
        g = make_graph("A", "B")
        g.add_link("A", "B", 10)
        g.remove_link("A", "B")
        assert g.degree("A") == 0
        assert g.degree("B") == 0

    def test_hapus_edge_tidak_ada_return_false(self):
        g = make_graph("A", "B")
        result = g.remove_link("A", "B")
        assert result is False

    def test_hapus_satu_edge_tidak_hapus_edge_lain(self):
        g = make_graph("A", "B", "C")
        g.add_link("A", "B", 10)
        g.add_link("A", "C", 20)
        g.remove_link("A", "B")
        nbr = dict(g.neighbors("A"))
        assert "B" not in nbr
        assert "C" in nbr


# ══════════════════════════════════════════════════════════════════════════════
# 4. remove_device
# ══════════════════════════════════════════════════════════════════════════════
class TestRemoveDevice:

    def test_hapus_device_berhasil(self):
        g = make_graph("A")
        assert g.remove_device("A") is True
        assert "A" not in g.adj

    def test_hapus_device_tidak_ada_return_false(self):
        g = IoTGraph()
        assert g.remove_device("Z") is False

    def test_edge_ke_device_terhapus_ikut_hilang(self):
        g = make_graph("A", "B", "C")
        g.add_link("A", "B", 5)
        g.add_link("A", "C", 5)
        g.remove_device("A")
        assert "A" not in dict(g.neighbors("B"))
        assert "A" not in dict(g.neighbors("C"))

    def test_device_juga_dihapus_dari_devices_dict(self):
        g = make_graph("A")
        g.remove_device("A")
        assert "A" not in g.devices


# ══════════════════════════════════════════════════════════════════════════════
# 5. neighbors
# ══════════════════════════════════════════════════════════════════════════════
class TestNeighbors:

    def test_neighbors_kosong_jika_tidak_ada_edge(self):
        g = make_graph("A")
        assert g.neighbors("A") == []

    def test_neighbors_node_tidak_ada_return_kosong(self):
        g = IoTGraph()
        assert g.neighbors("Z") == []

    def test_neighbors_benar(self):
        g = make_graph("A", "B", "C")
        g.add_link("A", "B", 10)
        g.add_link("A", "C", 30)
        result = dict(g.neighbors("A"))
        assert result == {"B": 10, "C": 30}

    def test_neighbors_tidak_mengandung_node_lain(self):
        g = make_graph("A", "B", "C")
        g.add_link("A", "B", 10)
        result = dict(g.neighbors("A"))
        assert "C" not in result


# ══════════════════════════════════════════════════════════════════════════════
# 6. degree
# ══════════════════════════════════════════════════════════════════════════════
class TestDegree:

    def test_degree_nol_tanpa_edge(self):
        g = make_graph("A")
        assert g.degree("A") == 0

    def test_degree_bertambah_setiap_link(self):
        g = make_graph("A", "B", "C", "D")
        g.add_link("A", "B", 1)
        g.add_link("A", "C", 2)
        g.add_link("A", "D", 3)
        assert g.degree("A") == 3

    def test_degree_node_tidak_ada_return_nol(self):
        g = IoTGraph()
        assert g.degree("PHANTOM") == 0


# ══════════════════════════════════════════════════════════════════════════════
# 7. dfs_reachable
# ══════════════════════════════════════════════════════════════════════════════
class TestDfsReachable:

    def test_hanya_source_jika_tidak_ada_edge(self):
        g = make_graph("A", "B", "C")
        assert g.dfs_reachable("A") == {"A"}

    def test_semua_terjangkau_pada_graph_terhubung(self):
        g = make_graph("A", "B", "C")
        g.add_link("A", "B", 5)
        g.add_link("B", "C", 5)
        assert g.dfs_reachable("A") == {"A", "B", "C"}

    def test_komponen_terpisah_tidak_terjangkau(self):
        g = make_graph("A", "B", "C", "D")
        g.add_link("A", "B", 5)
        g.add_link("C", "D", 5)
        reachable = g.dfs_reachable("A")
        assert "C" not in reachable
        assert "D" not in reachable

    def test_source_selalu_ada_di_hasil(self):
        g = make_graph("X")
        assert "X" in g.dfs_reachable("X")

    def test_graph_linear(self):
        """A - B - C - D - E semua terjangkau dari A."""
        ids = ["A", "B", "C", "D", "E"]
        g = make_graph(*ids)
        for i in range(len(ids) - 1):
            g.add_link(ids[i], ids[i + 1], 1)
        assert g.dfs_reachable("A") == set(ids)


# ══════════════════════════════════════════════════════════════════════════════
# 8. isolated_devices
# ══════════════════════════════════════════════════════════════════════════════
class TestIsolatedDevices:

    def test_semua_terhubung_tidak_ada_isolated(self):
        g = make_graph("GATEWAY_0", "A", "B")
        g.add_link("GATEWAY_0", "A", 5)
        g.add_link("A", "B", 5)
        assert g.isolated_devices() == []

    def test_device_tanpa_koneksi_ke_gateway_adalah_isolated(self):
        g = make_graph("GATEWAY_0", "A", "B")
        g.add_link("GATEWAY_0", "A", 5)
        # B tidak terhubung ke mana-mana
        isolated = g.isolated_devices()
        assert "B" in isolated

    def test_custom_gateway(self):
        g = make_graph("GW", "X", "Y")
        g.add_link("GW", "X", 5)
        isolated = g.isolated_devices(gateway="GW")
        assert "Y" in isolated
        assert "X" not in isolated

    def test_semua_isolated_jika_gateway_tidak_ada_edge(self):
        g = make_graph("GATEWAY_0", "A", "B")
        isolated = g.isolated_devices()
        assert set(isolated) == {"A", "B"}


# ══════════════════════════════════════════════════════════════════════════════
# 9. __repr__
# ══════════════════════════════════════════════════════════════════════════════
class TestRepr:

    def test_repr_node_dan_edge(self):
        g = make_graph("A", "B", "C")
        g.add_link("A", "B", 10)
        g.add_link("B", "C", 20)
        r = repr(g)
        assert "nodes=3" in r
        assert "edges=2" in r

    def test_repr_graph_kosong(self):
        g = IoTGraph()
        assert "nodes=0" in repr(g)
        assert "edges=0" in repr(g)


# ══════════════════════════════════════════════════════════════════════════════
# 10. Skenario integrasi
# ══════════════════════════════════════════════════════════════════════════════
class TestIntegrasi:

    def test_add_remove_link_cycle(self):
        """Tambah lalu hapus semua edge — graph harus kembali ke degree 0."""
        g = make_graph("A", "B", "C")
        g.add_link("A", "B", 10)
        g.add_link("B", "C", 15)
        g.remove_link("A", "B")
        g.remove_link("B", "C")
        for node in ["A", "B", "C"]:
            assert g.degree(node) == 0

    def test_isolasi_setelah_hapus_device(self):
        """Setelah GATEWAY dihapus, semua node jadi isolated terhadap gateway baru."""
        g = make_graph("GATEWAY_0", "A", "B")
        g.add_link("GATEWAY_0", "A", 5)
        g.add_link("A", "B", 5)
        g.remove_device("GATEWAY_0")

        # Tambah gateway baru yang tidak terhubung
        g.add_device(DummyDevice("GATEWAY_0"))
        isolated = g.isolated_devices()
        assert "A" in isolated
        assert "B" in isolated

    def test_graph_besar(self):
        """Stress test: 100 node, semua terhubung ke gateway secara bintang."""
        g = make_graph("GATEWAY_0")
        for i in range(100):
            did = f"SENSOR_{i}"
            g.add_device(DummyDevice(did))
            g.add_link("GATEWAY_0", did, i + 1)

        assert g.degree("GATEWAY_0") == 100
        assert len(g.dfs_reachable("GATEWAY_0")) == 101  # gateway + 100 sensor
        assert g.isolated_devices() == []