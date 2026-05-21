"""
test_linked_list.py — Unit Test untuk SinglyLinkedList & DoublyLinkedList
Lokasi  : tests/test_linked_list.py
Mata Kuliah : ELT60213 Algoritma dan Struktur Data
Team Based Project TA 2025/2026 — Group 8

Cara menjalankan:
    python -m pytest tests/test_linked_list.py -v
    atau
    python tests/test_linked_list.py
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'data_structures'))

from linked_list import SinglyLinkedList, DoublyLinkedList, SLLNode, DLLNode


# ══════════════════════════════════════════════════════════════
#  SINGLY LINKED LIST — TEST SUITE
# ══════════════════════════════════════════════════════════════

class TestSLLInisialisasi(unittest.TestCase):
    """Test kondisi awal SinglyLinkedList."""

    def test_list_kosong_saat_dibuat(self):
        sll = SinglyLinkedList()
        self.assertTrue(sll.is_empty())

    def test_size_nol_saat_dibuat(self):
        sll = SinglyLinkedList()
        self.assertEqual(len(sll), 0)

    def test_head_none_saat_dibuat(self):
        sll = SinglyLinkedList()
        self.assertIsNone(sll.head)

    def test_tail_none_saat_dibuat(self):
        sll = SinglyLinkedList()
        self.assertIsNone(sll.tail)


class TestSLLAddFront(unittest.TestCase):
    """Test operasi add_front — O(1)."""

    def setUp(self):
        self.sll = SinglyLinkedList()

    def test_add_front_satu_elemen(self):
        self.sll.add_front("SENSOR_1")
        self.assertEqual(self.sll.head.data, "SENSOR_1")

    def test_add_front_update_head(self):
        self.sll.add_front("SENSOR_1")
        self.sll.add_front("GATEWAY_0")
        self.assertEqual(self.sll.head.data, "GATEWAY_0")

    def test_add_front_urutan_benar(self):
        for x in ["C", "B", "A"]:
            self.sll.add_front(x)
        self.assertEqual(self.sll.to_list(), ["A", "B", "C"])

    def test_add_front_size_bertambah(self):
        self.sll.add_front("X")
        self.sll.add_front("Y")
        self.assertEqual(len(self.sll), 2)

    def test_add_front_tail_diset_pada_elemen_pertama(self):
        self.sll.add_front("SENSOR_1")
        self.assertEqual(self.sll.tail.data, "SENSOR_1")

    def test_add_front_tidak_ubah_tail_saat_sudah_ada(self):
        self.sll.add_front("A")
        self.sll.add_front("B")
        self.assertEqual(self.sll.tail.data, "A")


class TestSLLAddBack(unittest.TestCase):
    """Test operasi add_back — O(1)."""

    def setUp(self):
        self.sll = SinglyLinkedList()

    def test_add_back_satu_elemen(self):
        self.sll.add_back("SERVER_1")
        self.assertEqual(self.sll.tail.data, "SERVER_1")

    def test_add_back_update_tail(self):
        self.sll.add_back("A")
        self.sll.add_back("B")
        self.assertEqual(self.sll.tail.data, "B")

    def test_add_back_urutan_benar(self):
        for x in ["A", "B", "C"]:
            self.sll.add_back(x)
        self.assertEqual(self.sll.to_list(), ["A", "B", "C"])

    def test_add_back_size_bertambah(self):
        self.sll.add_back("X")
        self.sll.add_back("Y")
        self.assertEqual(len(self.sll), 2)

    def test_add_back_head_diset_pada_elemen_pertama(self):
        self.sll.add_back("SENSOR_1")
        self.assertEqual(self.sll.head.data, "SENSOR_1")

    def test_add_back_tidak_ubah_head_saat_sudah_ada(self):
        self.sll.add_back("A")
        self.sll.add_back("B")
        self.assertEqual(self.sll.head.data, "A")


class TestSLLInsertAfter(unittest.TestCase):
    """Test operasi insert_after — O(n)."""

    def setUp(self):
        self.sll = SinglyLinkedList()
        for x in ["A", "B", "D"]:
            self.sll.add_back(x)

    def test_insert_after_tengah(self):
        self.sll.insert_after("B", "C")
        self.assertEqual(self.sll.to_list(), ["A", "B", "C", "D"])

    def test_insert_after_tail(self):
        self.sll.insert_after("D", "E")
        self.assertEqual(self.sll.tail.data, "E")

    def test_insert_after_target_tidak_ada(self):
        result = self.sll.insert_after("Z", "X")
        self.assertFalse(result)

    def test_insert_after_berhasil_return_true(self):
        result = self.sll.insert_after("A", "AA")
        self.assertTrue(result)

    def test_insert_after_size_bertambah(self):
        self.sll.insert_after("A", "AA")
        self.assertEqual(len(self.sll), 4)


class TestSLLRemoveFront(unittest.TestCase):
    """Test operasi remove_front — O(1)."""

    def setUp(self):
        self.sll = SinglyLinkedList()
        for x in ["GATEWAY_0", "SENSOR_1", "SERVER_1"]:
            self.sll.add_back(x)

    def test_remove_front_kembalikan_data_benar(self):
        data = self.sll.remove_front()
        self.assertEqual(data, "GATEWAY_0")

    def test_remove_front_update_head(self):
        self.sll.remove_front()
        self.assertEqual(self.sll.head.data, "SENSOR_1")

    def test_remove_front_size_berkurang(self):
        self.sll.remove_front()
        self.assertEqual(len(self.sll), 2)

    def test_remove_front_list_kosong_return_none(self):
        sll_kosong = SinglyLinkedList()
        self.assertIsNone(sll_kosong.remove_front())

    def test_remove_front_elemen_terakhir_reset_head_tail(self):
        sll = SinglyLinkedList()
        sll.add_back("X")
        sll.remove_front()
        self.assertIsNone(sll.head)
        self.assertIsNone(sll.tail)


class TestSLLRemoveBack(unittest.TestCase):
    """Test operasi remove_back — O(n)."""

    def setUp(self):
        self.sll = SinglyLinkedList()
        for x in ["A", "B", "C"]:
            self.sll.add_back(x)

    def test_remove_back_kembalikan_data_benar(self):
        data = self.sll.remove_back()
        self.assertEqual(data, "C")

    def test_remove_back_update_tail(self):
        self.sll.remove_back()
        self.assertEqual(self.sll.tail.data, "B")

    def test_remove_back_size_berkurang(self):
        self.sll.remove_back()
        self.assertEqual(len(self.sll), 2)

    def test_remove_back_list_kosong_return_none(self):
        sll_kosong = SinglyLinkedList()
        self.assertIsNone(sll_kosong.remove_back())

    def test_remove_back_elemen_terakhir_reset_head_tail(self):
        sll = SinglyLinkedList()
        sll.add_back("X")
        sll.remove_back()
        self.assertIsNone(sll.head)
        self.assertIsNone(sll.tail)

    def test_remove_back_dua_elemen(self):
        sll = SinglyLinkedList()
        sll.add_back("P")
        sll.add_back("Q")
        sll.remove_back()
        self.assertEqual(sll.head.data, "P")
        self.assertEqual(sll.tail.data, "P")


class TestSLLDeleteByValue(unittest.TestCase):
    """Test operasi delete_by_value — O(n)."""

    def setUp(self):
        self.sll = SinglyLinkedList()
        for x in ["A", "B", "C", "B", "D"]:
            self.sll.add_back(x)

    def test_delete_nilai_ada_return_true(self):
        self.assertTrue(self.sll.delete_by_value("C"))

    def test_delete_nilai_tidak_ada_return_false(self):
        self.assertFalse(self.sll.delete_by_value("Z"))

    def test_delete_hanya_kemunculan_pertama(self):
        self.sll.delete_by_value("B")
        # "B" kedua masih ada
        self.assertTrue(self.sll.contains("B"))

    def test_delete_head(self):
        self.sll.delete_by_value("A")
        self.assertEqual(self.sll.head.data, "B")

    def test_delete_tail(self):
        self.sll.delete_by_value("D")
        self.assertEqual(self.sll.tail.data, "B")

    def test_delete_size_berkurang(self):
        self.sll.delete_by_value("C")
        self.assertEqual(len(self.sll), 4)

    def test_delete_pada_list_kosong(self):
        sll_kosong = SinglyLinkedList()
        self.assertFalse(sll_kosong.delete_by_value("X"))


class TestSLLFind(unittest.TestCase):
    """Test operasi find & contains — O(n)."""

    def setUp(self):
        self.sll = SinglyLinkedList()
        for x in ["SENSOR_1", "GATEWAY_0", "SERVER_1"]:
            self.sll.add_back(x)

    def test_find_ada_return_node(self):
        node = self.sll.find("GATEWAY_0")
        self.assertIsInstance(node, SLLNode)
        self.assertEqual(node.data, "GATEWAY_0")

    def test_find_tidak_ada_return_none(self):
        self.assertIsNone(self.sll.find("SENSOR_99"))

    def test_contains_ada_return_true(self):
        self.assertTrue(self.sll.contains("SERVER_1"))

    def test_contains_tidak_ada_return_false(self):
        self.assertFalse(self.sll.contains("UNKNOWN"))

    def test_get_at_index_valid(self):
        self.assertEqual(self.sll.get_at(0), "SENSOR_1")
        self.assertEqual(self.sll.get_at(1), "GATEWAY_0")
        self.assertEqual(self.sll.get_at(2), "SERVER_1")

    def test_get_at_index_negatif_return_none(self):
        self.assertIsNone(self.sll.get_at(-1))

    def test_get_at_index_melebihi_size_return_none(self):
        self.assertIsNone(self.sll.get_at(99))


class TestSLLReverse(unittest.TestCase):
    """Test operasi reverse — O(n)."""

    def test_reverse_list_biasa(self):
        sll = SinglyLinkedList()
        for x in [1, 2, 3, 4, 5]:
            sll.add_back(x)
        sll.reverse()
        self.assertEqual(sll.to_list(), [5, 4, 3, 2, 1])

    def test_reverse_head_dan_tail_tertukar(self):
        sll = SinglyLinkedList()
        for x in ["A", "B", "C"]:
            sll.add_back(x)
        sll.reverse()
        self.assertEqual(sll.head.data, "C")
        self.assertEqual(sll.tail.data, "A")

    def test_reverse_satu_elemen(self):
        sll = SinglyLinkedList()
        sll.add_back("X")
        sll.reverse()
        self.assertEqual(sll.to_list(), ["X"])

    def test_reverse_dua_kali_kembali_ke_semula(self):
        sll = SinglyLinkedList()
        for x in [1, 2, 3]:
            sll.add_back(x)
        sll.reverse()
        sll.reverse()
        self.assertEqual(sll.to_list(), [1, 2, 3])

    def test_reverse_list_kosong_tidak_crash(self):
        sll = SinglyLinkedList()
        try:
            sll.reverse()
        except Exception as e:
            self.fail(f"reverse() pada list kosong crash: {e}")


class TestSLLUtilitas(unittest.TestCase):
    """Test to_list, clear, iterasi — O(n) / O(1)."""

    def test_to_list_benar(self):
        sll = SinglyLinkedList()
        for x in ["A", "B", "C"]:
            sll.add_back(x)
        self.assertEqual(sll.to_list(), ["A", "B", "C"])

    def test_to_list_kosong(self):
        self.assertEqual(SinglyLinkedList().to_list(), [])

    def test_clear_reset_semua(self):
        sll = SinglyLinkedList()
        for x in [1, 2, 3]:
            sll.add_back(x)
        sll.clear()
        self.assertTrue(sll.is_empty())
        self.assertIsNone(sll.head)
        self.assertIsNone(sll.tail)
        self.assertEqual(len(sll), 0)

    def test_iterasi_for_loop(self):
        sll = SinglyLinkedList()
        for x in [10, 20, 30]:
            sll.add_back(x)
        result = [x for x in sll]
        self.assertEqual(result, [10, 20, 30])

    def test_iterasi_sum(self):
        sll = SinglyLinkedList()
        for x in [1, 2, 3, 4, 5]:
            sll.add_back(x)
        self.assertEqual(sum(x for x in sll), 15)


# ══════════════════════════════════════════════════════════════
#  DOUBLY LINKED LIST — TEST SUITE
# ══════════════════════════════════════════════════════════════

class TestDLLInisialisasi(unittest.TestCase):
    """Test kondisi awal DoublyLinkedList."""

    def test_list_kosong_saat_dibuat(self):
        dll = DoublyLinkedList()
        self.assertTrue(dll.is_empty())

    def test_size_nol_saat_dibuat(self):
        dll = DoublyLinkedList()
        self.assertEqual(len(dll), 0)

    def test_head_none_saat_dibuat(self):
        self.assertIsNone(DoublyLinkedList().head)

    def test_tail_none_saat_dibuat(self):
        self.assertIsNone(DoublyLinkedList().tail)


class TestDLLAddFront(unittest.TestCase):
    """Test operasi add_front — O(1)."""

    def setUp(self):
        self.dll = DoublyLinkedList()

    def test_add_front_satu_elemen(self):
        self.dll.add_front("ALERT_1")
        self.assertEqual(self.dll.head.data, "ALERT_1")

    def test_add_front_update_head(self):
        self.dll.add_front("ALERT_1")
        self.dll.add_front("ALERT_0")
        self.assertEqual(self.dll.head.data, "ALERT_0")

    def test_add_front_pointer_prev_head_none(self):
        self.dll.add_front("A")
        self.dll.add_front("B")
        self.assertIsNone(self.dll.head.prev)

    def test_add_front_pointer_next_benar(self):
        self.dll.add_front("A")
        self.dll.add_front("B")
        self.assertEqual(self.dll.head.next.data, "A")

    def test_add_front_size_bertambah(self):
        self.dll.add_front("X")
        self.dll.add_front("Y")
        self.assertEqual(len(self.dll), 2)

    def test_add_front_urutan_benar(self):
        for x in ["C", "B", "A"]:
            self.dll.add_front(x)
        self.assertEqual(self.dll.to_list(), ["A", "B", "C"])


class TestDLLAddBack(unittest.TestCase):
    """Test operasi add_back — O(1)."""

    def setUp(self):
        self.dll = DoublyLinkedList()

    def test_add_back_satu_elemen(self):
        self.dll.add_back("ALERT_1")
        self.assertEqual(self.dll.tail.data, "ALERT_1")

    def test_add_back_update_tail(self):
        self.dll.add_back("A")
        self.dll.add_back("B")
        self.assertEqual(self.dll.tail.data, "B")

    def test_add_back_pointer_next_tail_none(self):
        self.dll.add_back("A")
        self.dll.add_back("B")
        self.assertIsNone(self.dll.tail.next)

    def test_add_back_pointer_prev_benar(self):
        self.dll.add_back("A")
        self.dll.add_back("B")
        self.assertEqual(self.dll.tail.prev.data, "A")

    def test_add_back_size_bertambah(self):
        self.dll.add_back("X")
        self.dll.add_back("Y")
        self.assertEqual(len(self.dll), 2)

    def test_add_back_urutan_benar(self):
        for x in ["A", "B", "C"]:
            self.dll.add_back(x)
        self.assertEqual(self.dll.to_list(), ["A", "B", "C"])


class TestDLLRemoveFront(unittest.TestCase):
    """Test operasi remove_front — O(1)."""

    def setUp(self):
        self.dll = DoublyLinkedList()
        for x in ["ALERT_1", "ALERT_2", "ALERT_3"]:
            self.dll.add_back(x)

    def test_remove_front_kembalikan_data_benar(self):
        self.assertEqual(self.dll.remove_front(), "ALERT_1")

    def test_remove_front_update_head(self):
        self.dll.remove_front()
        self.assertEqual(self.dll.head.data, "ALERT_2")

    def test_remove_front_prev_head_baru_none(self):
        self.dll.remove_front()
        self.assertIsNone(self.dll.head.prev)

    def test_remove_front_size_berkurang(self):
        self.dll.remove_front()
        self.assertEqual(len(self.dll), 2)

    def test_remove_front_list_kosong_return_none(self):
        self.assertIsNone(DoublyLinkedList().remove_front())

    def test_remove_front_elemen_terakhir_reset_head_tail(self):
        dll = DoublyLinkedList()
        dll.add_back("X")
        dll.remove_front()
        self.assertIsNone(dll.head)
        self.assertIsNone(dll.tail)


class TestDLLRemoveBack(unittest.TestCase):
    """Test operasi remove_back — O(1) keunggulan DLL."""

    def setUp(self):
        self.dll = DoublyLinkedList()
        for x in ["A", "B", "C"]:
            self.dll.add_back(x)

    def test_remove_back_kembalikan_data_benar(self):
        self.assertEqual(self.dll.remove_back(), "C")

    def test_remove_back_update_tail(self):
        self.dll.remove_back()
        self.assertEqual(self.dll.tail.data, "B")

    def test_remove_back_next_tail_baru_none(self):
        self.dll.remove_back()
        self.assertIsNone(self.dll.tail.next)

    def test_remove_back_size_berkurang(self):
        self.dll.remove_back()
        self.assertEqual(len(self.dll), 2)

    def test_remove_back_list_kosong_return_none(self):
        self.assertIsNone(DoublyLinkedList().remove_back())

    def test_remove_back_elemen_terakhir_reset_head_tail(self):
        dll = DoublyLinkedList()
        dll.add_back("X")
        dll.remove_back()
        self.assertIsNone(dll.head)
        self.assertIsNone(dll.tail)

    def test_remove_back_dua_elemen(self):
        dll = DoublyLinkedList()
        dll.add_back("P")
        dll.add_back("Q")
        dll.remove_back()
        self.assertEqual(dll.head.data, "P")
        self.assertEqual(dll.tail.data, "P")
        self.assertIsNone(dll.tail.next)


class TestDLLDeleteNode(unittest.TestCase):
    """Test operasi delete_node — O(1) dengan referensi node."""

    def setUp(self):
        self.dll = DoublyLinkedList()
        for x in ["A", "B", "C", "D"]:
            self.dll.add_back(x)

    def test_delete_node_tengah(self):
        node_b = self.dll.find("B")
        self.dll.delete_node(node_b)
        self.assertEqual(self.dll.to_list(), ["A", "C", "D"])

    def test_delete_node_head(self):
        self.dll.delete_node(self.dll.head)
        self.assertEqual(self.dll.head.data, "B")

    def test_delete_node_tail(self):
        self.dll.delete_node(self.dll.tail)
        self.assertEqual(self.dll.tail.data, "C")

    def test_delete_node_size_berkurang(self):
        node_c = self.dll.find("C")
        self.dll.delete_node(node_c)
        self.assertEqual(len(self.dll), 3)

    def test_delete_node_pointer_konsisten(self):
        """Setelah hapus B, A.next harus C dan C.prev harus A."""
        node_b = self.dll.find("B")
        self.dll.delete_node(node_b)
        node_a = self.dll.find("A")
        node_c = self.dll.find("C")
        self.assertEqual(node_a.next.data, "C")
        self.assertEqual(node_c.prev.data, "A")

    def test_delete_by_value_return_true(self):
        self.assertTrue(self.dll.delete_by_value("C"))

    def test_delete_by_value_return_false(self):
        self.assertFalse(self.dll.delete_by_value("Z"))


class TestDLLFind(unittest.TestCase):
    """Test operasi find, contains, find_backward — O(n)."""

    def setUp(self):
        self.dll = DoublyLinkedList()
        for x in ["SENSOR_1", "GATEWAY_0", "SERVER_1", "SENSOR_2"]:
            self.dll.add_back(x)

    def test_find_ada_return_dllnode(self):
        node = self.dll.find("GATEWAY_0")
        self.assertIsInstance(node, DLLNode)
        self.assertEqual(node.data, "GATEWAY_0")

    def test_find_tidak_ada_return_none(self):
        self.assertIsNone(self.dll.find("UNKNOWN"))

    def test_contains_ada_return_true(self):
        self.assertTrue(self.dll.contains("SERVER_1"))

    def test_contains_tidak_ada_return_false(self):
        self.assertFalse(self.dll.contains("XX99"))

    def test_find_backward_ada(self):
        node = self.dll.find_backward("SENSOR_2")
        self.assertIsNotNone(node)
        self.assertEqual(node.data, "SENSOR_2")

    def test_find_backward_tidak_ada_return_none(self):
        self.assertIsNone(self.dll.find_backward("ZZZ"))

    def test_find_backward_hasil_sama_dengan_find(self):
        node_fwd = self.dll.find("SENSOR_1")
        node_bwd = self.dll.find_backward("SENSOR_1")
        self.assertEqual(node_fwd.data, node_bwd.data)


class TestDLLUtilitas(unittest.TestCase):
    """Test to_list, to_list_reversed, clear, iterasi."""

    def setUp(self):
        self.dll = DoublyLinkedList()
        for x in ["A", "B", "C", "D"]:
            self.dll.add_back(x)

    def test_to_list_maju(self):
        self.assertEqual(self.dll.to_list(), ["A", "B", "C", "D"])

    def test_to_list_reversed(self):
        self.assertEqual(self.dll.to_list_reversed(), ["D", "C", "B", "A"])

    def test_to_list_dan_reversed_konsisten(self):
        """to_list dan to_list_reversed harus saling invers."""
        self.assertEqual(self.dll.to_list(), list(reversed(self.dll.to_list_reversed())))

    def test_clear_reset_semua(self):
        self.dll.clear()
        self.assertTrue(self.dll.is_empty())
        self.assertIsNone(self.dll.head)
        self.assertIsNone(self.dll.tail)
        self.assertEqual(len(self.dll), 0)

    def test_iterasi_for_loop(self):
        result = [x for x in self.dll]
        self.assertEqual(result, ["A", "B", "C", "D"])

    def test_to_list_kosong(self):
        self.assertEqual(DoublyLinkedList().to_list(), [])

    def test_to_list_reversed_kosong(self):
        self.assertEqual(DoublyLinkedList().to_list_reversed(), [])


# ══════════════════════════════════════════════════════════════
#  TEST INTEGRASI — Skenario IoT
# ══════════════════════════════════════════════════════════════

class TestIntegrasi(unittest.TestCase):

    def test_sll_sebagai_queue_alert(self):
        """
        SLL sebagai Queue: enqueue = add_back, dequeue = remove_front.
        Urutan FIFO harus terjaga.
        """
        queue = SinglyLinkedList()
        queue.add_back("ALERT_HIGH_LATENCY")
        queue.add_back("ALERT_PACKET_LOSS")
        queue.add_back("ALERT_DOWN")

        self.assertEqual(queue.remove_front(), "ALERT_HIGH_LATENCY")
        self.assertEqual(queue.remove_front(), "ALERT_PACKET_LOSS")
        self.assertEqual(queue.remove_front(), "ALERT_DOWN")
        self.assertTrue(queue.is_empty())

    def test_sll_sebagai_stack_history(self):
        """
        SLL sebagai Stack: push = add_front, pop = remove_front.
        Urutan LIFO harus terjaga.
        """
        stack = SinglyLinkedList()
        stack.add_front("CMD_1")
        stack.add_front("CMD_2")
        stack.add_front("CMD_3")

        self.assertEqual(stack.remove_front(), "CMD_3")
        self.assertEqual(stack.remove_front(), "CMD_2")
        self.assertEqual(stack.remove_front(), "CMD_1")

    def test_dll_remove_back_o1_keunggulan(self):
        """
        DLL remove_back harus O(1): tail.prev langsung tersedia,
        tidak perlu traverse seperti SLL.
        """
        dll = DoublyLinkedList()
        for i in range(100):
            dll.add_back(f"DEVICE_{i:03d}")

        # Remove dari belakang berulang kali — harus tetap O(1)
        for i in range(99, -1, -1):
            data = dll.remove_back()
            self.assertEqual(data, f"DEVICE_{i:03d}")

        self.assertTrue(dll.is_empty())

    def test_dll_delete_node_tengah_konsisten(self):
        """Hapus node di tengah DLL tidak merusak pointer chain."""
        dll = DoublyLinkedList()
        for x in ["R1", "SW1", "PC1", "PC2", "R2"]:
            dll.add_back(x)

        # Hapus SW1 (tengah)
        node_sw1 = dll.find("SW1")
        dll.delete_node(node_sw1)

        result = dll.to_list()
        self.assertEqual(result, ["R1", "PC1", "PC2", "R2"])

        # Verifikasi pointer DLL tetap konsisten
        node_r1  = dll.find("R1")
        node_pc1 = dll.find("PC1")
        self.assertEqual(node_r1.next.data,  "PC1")
        self.assertEqual(node_pc1.prev.data, "R1")

    def test_sll_reverse_adjacency_list(self):
        """SLL reverse berguna untuk membalik rute jaringan."""
        rute = SinglyLinkedList()
        for hop in ["R1", "SW1", "PC1"]:
            rute.add_back(hop)
        rute.reverse()
        self.assertEqual(rute.to_list(), ["PC1", "SW1", "R1"])

    def test_sll_insert_after_untuk_sisip_hop(self):
        """insert_after berguna untuk menyisipkan hop baru di rute."""
        rute = SinglyLinkedList()
        for hop in ["R1", "R2", "SERVER"]:
            rute.add_back(hop)
        rute.insert_after("R1", "SW1")
        self.assertEqual(rute.to_list(), ["R1", "SW1", "R2", "SERVER"])


# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  TEST LINKED LIST — IoT Network Monitoring  Group 8")
    print("=" * 60)
    unittest.main(verbosity=2)