# ============================================================
# modul_4.py
# Modul 4: Alert Management System (Stack-Based)
# IoT Network Monitoring & Alert Management System
# ELT60213 Algoritma dan Struktur Data - TA 2025/2026
# ============================================================

import time
import random
import numpy as np
from dataclasses import dataclass
from typing import Optional, Dict, List

from src.data_structures.stack import Alert, AlertStack, Stack, LLNode

# ── Seed tetap ──────────────────────────────────────────────
np.random.seed(23)
random.seed(23)

# ── Konstanta tipe alert ─────────────────────────────────────
TIPE_CRITICAL = 1
TIPE_WARNING  = 2
TIPE_INFO     = 3
LABEL_TIPE    = {1: 'CRITICAL', 2: 'WARNING', 3: 'INFO'}

# ── Threshold per device type ────────────────────────────────
THRESHOLD: Dict[str, Dict[str, Dict[str, float]]] = {
    'SENSOR': {
        'temperature': {'WARNING': 60.0, 'CRITICAL': 80.0},
        'humidity':    {'WARNING': 85.0, 'CRITICAL': 95.0},
        'cpu_usage':   {'WARNING': 70.0, 'CRITICAL': 90.0},
    },
    'GATEWAY': {
        'packet_loss': {'WARNING':  5.0, 'CRITICAL': 15.0},
        'latency_ms':  {'WARNING': 150.0,'CRITICAL':300.0},
        'cpu_usage':   {'WARNING': 75.0, 'CRITICAL': 92.0},
    },
    'SERVER': {
        'cpu_usage':    {'WARNING': 80.0, 'CRITICAL': 95.0},
        'memory_usage': {'WARNING': 75.0, 'CRITICAL': 90.0},
        'disk_usage':   {'WARNING': 80.0, 'CRITICAL': 95.0},
    },
}

_alert_counter = 0   # auto-increment global untuk alert_id


# ════════════════════════════════════════════════════════════
#   FUNGSI UTILITAS
# ════════════════════════════════════════════════════════════

def _next_id() -> int:
    """Menghasilkan alert_id unik yang terus bertambah. O(1)."""
    global _alert_counter
    _alert_counter += 1
    return _alert_counter


def tentukan_tipe(device_type: str, metric: str, value: float) -> int:
    """
    Menentukan tipe alert berdasarkan threshold device.

    Args:
        device_type : 'SENSOR' | 'GATEWAY' | 'SERVER'
        metric      : nama metrik (misal 'temperature')
        value       : nilai pembacaan sensor

    Returns:
        1 = CRITICAL, 2 = WARNING, 3 = INFO

    Kompleksitas: O(1)
    """
    batas = THRESHOLD.get(device_type, {}).get(metric)
    if batas is None:
        return TIPE_INFO
    if value >= batas['CRITICAL']:
        return TIPE_CRITICAL
    if value >= batas['WARNING']:
        return TIPE_WARNING
    return TIPE_INFO


def buat_alert(device_id: str,
               device_type: str,
               metric: str,
               value: float) -> Optional[Alert]:
    """
    Membuat objek Alert jika nilai melampaui threshold WARNING/CRITICAL.
    Mengembalikan None jika kondisi normal (INFO).

    Kompleksitas: O(1)
    """
    tipe = tentukan_tipe(device_type, metric, value)
    if tipe == TIPE_INFO:
        return None

    label = LABEL_TIPE[tipe]
    batas = THRESHOLD[device_type][metric][label]
    pesan = (
        f"[{label}] Device '{device_id}' ({device_type}): "
        f"{metric} = {value:.2f} (threshold {batas:.2f})"
    )
    return Alert(
        alert_id  = _next_id(),
        device_id = device_id,
        tipe      = tipe,
        pesan     = pesan,
        timestamp = time.time(),
    )


# ════════════════════════════════════════════════════════════
#   MODUL 4 – AlertManager
# ════════════════════════════════════════════════════════════

class AlertManager:
    """
    Mengelola siklus hidup alert IoT dengan dua AlertStack:

        active_stack  – alert aktif yang belum di-resolve (LIFO)
        history_stack – alert yang sudah di-resolve (audit & rollback)

    Operasi tambahan:
        _resolve_log  – Stack generik untuk mendukung undo resolve

    Kompleksitas ruang : O(n) di mana n = kapasitas stack
    """

    def __init__(self, kapasitas: int = 50):
        self.active_stack:  AlertStack = AlertStack(kapasitas=kapasitas)
        self.history_stack: AlertStack = AlertStack(kapasitas=kapasitas)
        self._resolve_log:  Stack      = Stack()   # menyimpan alert_id yang di-resolve

    # ── Tambah alert baru ─────────────────────────────────────
    def tambah_alert(self, alert: Alert) -> None:
        """
        Push alert baru ke active_stack.

        Big-O waktu : O(1) normal | O(n) saat stack penuh (hapus bottom)
        """
        self.active_stack.push(alert)
        label = LABEL_TIPE[alert.tipe]
        ikon  = '🔴' if alert.tipe == TIPE_CRITICAL else '🟡'
        print(f"  [+] {ikon} Alert#{alert.alert_id} [{label}] → {alert.pesan}")

    # ── Resolve alert teratas ─────────────────────────────────
    def resolve_alert(self) -> Optional[Alert]:
        """
        Pop alert teratas dari active_stack dan pindah ke history_stack.

        Returns:
            Alert yang di-resolve, atau None jika active_stack kosong.

        Big-O waktu : O(1)
        """
        if self.active_stack.is_empty():
            print("  [resolve] Stack aktif kosong, tidak ada yang di-resolve.")
            return None

        resolved = self.active_stack.pop()
        self.history_stack.push(resolved)
        self._resolve_log.push(resolved.alert_id)

        label = LABEL_TIPE[resolved.tipe]
        print(f"  [✓] Resolved Alert#{resolved.alert_id} [{label}] → {resolved.pesan}")
        return resolved

    # ── Undo resolve terakhir ─────────────────────────────────
    def undo_resolve(self) -> Optional[Alert]:
        """
        Batalkan resolve terakhir: kembalikan alert dari
        history_stack ke active_stack (rollback LIFO).

        Returns:
            Alert yang dikembalikan, atau None jika history kosong.

        Big-O waktu : O(1)
        """
        if self.history_stack.is_empty():
            print("  [undo] Tidak ada history untuk di-undo.")
            return None

        restored = self.history_stack.pop()
        self.active_stack.push(restored)
        if not self._resolve_log.is_empty():
            self._resolve_log.pop()

        label = LABEL_TIPE[restored.tipe]
        print(f"  [↩] Undo → Alert#{restored.alert_id} [{label}] kembali aktif.")
        return restored

    # ── Peek alert teratas ────────────────────────────────────
    def lihat_alert_teratas(self) -> Optional[Alert]:
        """
        Lihat alert aktif paling baru tanpa menghapusnya.
        Big-O waktu : O(1)
        """
        top = self.active_stack.peek()
        if top:
            label = LABEL_TIPE[top.tipe]
            print(f"  [peek] Alert#{top.alert_id} [{label}] → {top.pesan}")
        else:
            print("  [peek] Active stack kosong.")
        return top

    # ── Cek keberadaan alert kritis ───────────────────────────
    def ada_alert_kritis(self) -> bool:
        """
        Traversal active_stack untuk mencari minimal satu CRITICAL.

        Big-O waktu : O(n)
        Big-O ruang : O(1)
        """
        node: Optional[LLNode] = self.active_stack.top
        while node is not None:
            if node.data.tipe == TIPE_CRITICAL:
                return True
            node = node.next
        return False

    # ── Hitung alert per tipe ─────────────────────────────────
    def hitung_per_tipe(self) -> Dict[str, int]:
        """
        Menghitung jumlah alert aktif untuk setiap tipe
        (CRITICAL / WARNING / INFO).

        Big-O waktu : O(n)
        Big-O ruang : O(1)
        """
        counts = {LABEL_TIPE[TIPE_CRITICAL]: 0,
                  LABEL_TIPE[TIPE_WARNING]:  0,
                  LABEL_TIPE[TIPE_INFO]:     0}
        node: Optional[LLNode] = self.active_stack.top
        while node is not None:
            counts[LABEL_TIPE[node.data.tipe]] += 1
            node = node.next
        return counts

    # ── Ambil alert berdasarkan device ────────────────────────
    def cari_by_device(self, device_id: str) -> List[Alert]:
        """
        Kumpulkan semua alert aktif dari device tertentu
        (tanpa mengubah stack).

        Big-O waktu : O(n)
        Big-O ruang : O(k) di mana k = jumlah alert device tsb
        """
        hasil: List[Alert] = []
        node: Optional[LLNode] = self.active_stack.top
        while node is not None:
            if node.data.device_id == device_id:
                hasil.append(node.data)
            node = node.next
        return hasil

    # ── Resolve semua alert milik device ─────────────────────
    def resolve_by_device(self, device_id: str) -> int:
        """
        Me-resolve semua alert aktif dari device tertentu
        menggunakan stack bantu (tidak mengubah urutan sisanya).

        Returns:
            Jumlah alert yang di-resolve.

        Big-O waktu : O(n)
        Big-O ruang : O(n)
        """
        tmp:    Stack = Stack()
        jumlah: int   = 0

        # Pindahkan semua node ke stack sementara
        while not self.active_stack.is_empty():
            tmp.push(self.active_stack.pop())

        # Kembalikan; yang cocok masuk history, sisanya balik ke active
        while not tmp.is_empty():
            alert: Alert = tmp.pop()
            if alert.device_id == device_id:
                self.history_stack.push(alert)
                self._resolve_log.push(alert.alert_id)
                jumlah += 1
            else:
                self.active_stack.push(alert)

        if jumlah:
            print(f"  [resolve_by_device] {jumlah} alert dari '{device_id}' di-resolve.")
        else:
            print(f"  [resolve_by_device] Tidak ada alert aktif dari '{device_id}'.")
        return jumlah

    # ── Tampilkan semua alert aktif ───────────────────────────
    def tampilkan_aktif(self) -> None:
        """
        Cetak semua alert aktif dari top ke bottom.
        Big-O waktu : O(n)
        """
        if self.active_stack.is_empty():
            print("  [info] Tidak ada alert aktif.")
            return

        print("\n  ┌── ALERT AKTIF (top → bottom) " + "─" * 28 + "┐")
        node: Optional[LLNode] = self.active_stack.top
        no = 1
        while node is not None:
            a     = node.data
            label = LABEL_TIPE[a.tipe]
            waktu = time.strftime('%H:%M:%S', time.localtime(a.timestamp))
            print(f"  │ {no:>2}. Alert#{a.alert_id:<4} [{label:<8}] {waktu}  {a.pesan}")
            node = node.next
            no  += 1
        print("  └" + "─" * 59 + "┘\n")

    # ── Laporan ringkas ───────────────────────────────────────
    def laporan(self) -> None:
        """Cetak ringkasan statistik AlertManager."""
        counts = self.hitung_per_tipe()
        kritis = self.ada_alert_kritis()

        print("\n" + "=" * 50)
        print("  LAPORAN ALERT MANAGER")
        print("=" * 50)
        print(f"  Alert aktif      : {len(self.active_stack)}")
        print(f"    - CRITICAL     : {counts['CRITICAL']}")
        print(f"    - WARNING      : {counts['WARNING']}")
        print(f"    - INFO         : {counts['INFO']}")
        print(f"  Alert history    : {len(self.history_stack)}")
        print(f"  Status kritis    : {'🔴 ADA CRITICAL' if kritis else '🟢 Aman'}")
        print()
        print("  Kompleksitas:")
        print("    tambah_alert      : O(1) normal | O(n) saat penuh")
        print("    resolve_alert     : O(1)")
        print("    undo_resolve      : O(1)")
        print("    lihat_teratas     : O(1)")
        print("    ada_alert_kritis  : O(n)")
        print("    hitung_per_tipe   : O(n)")
        print("    cari_by_device    : O(n)")
        print("    resolve_by_device : O(n)")
        print("=" * 50)


# ════════════════════════════════════════════════════════════
#   Generator pembacaan sensor (simulasi)
# ════════════════════════════════════════════════════════════

def generate_readings(n_devices: int = 10, seed: int = 23):
    """
    Menghasilkan daftar (device_id, device_type, metric, value)
    secara acak untuk simulasi.
    """
    rng     = np.random.default_rng(seed)
    configs = [
        ('SENSOR',  'temperature', 40.0, 100.0),
        ('SENSOR',  'humidity',    50.0, 100.0),
        ('GATEWAY', 'packet_loss',  0.0,  25.0),
        ('GATEWAY', 'latency_ms',  10.0, 400.0),
        ('SERVER',  'cpu_usage',   20.0, 100.0),
        ('SERVER',  'memory_usage',20.0, 100.0),
    ]
    readings = []
    for i in range(n_devices):
        dtype, metric, lo, hi = configs[i % len(configs)]
        prefix = {'SENSOR': 'SENSOR', 'GATEWAY': 'GATEWAY', 'SERVER': 'SERVER'}[dtype]
        device_id = f"{prefix}_{i}"
        value     = float(rng.uniform(lo, hi))
        readings.append((device_id, dtype, metric, value))
    return readings


# ════════════════════════════════════════════════════════════
#   Demo / Uji Modul 4
# ════════════════════════════════════════════════════════════

def demo_modul4():
    print("=" * 50)
    print("  MODUL 4 – Alert Management System (Stack)")
    print("  IoT Network Monitoring System")
    print("=" * 50)

    manager = AlertManager(kapasitas=50)

    # ── 1. Generate dan tambahkan alert ──────────────────────
    print("\n[1] Proses pembacaan sensor (10 device):")
    readings = generate_readings(n_devices=10, seed=23)
    for device_id, dtype, metric, value in readings:
        alert = buat_alert(device_id, dtype, metric, value)
        if alert:
            manager.tambah_alert(alert)

    # ── 2. Tampilkan semua alert aktif ────────────────────────
    print("\n[2] Tampilkan semua alert aktif:")
    manager.tampilkan_aktif()

    # ── 3. Peek alert teratas ─────────────────────────────────
    print("[3] Peek alert teratas:")
    manager.lihat_alert_teratas()

    # ── 4. Cek alert kritis ───────────────────────────────────
    kritis = manager.ada_alert_kritis()
    print(f"\n[4] Ada alert CRITICAL: {'YA 🔴' if kritis else 'TIDAK 🟢'}")

    # ── 5. Resolve 2 alert terbaru ────────────────────────────
    print("\n[5] Resolve 2 alert teratas:")
    manager.resolve_alert()
    manager.resolve_alert()

    # ── 6. Undo resolve terakhir ──────────────────────────────
    print("\n[6] Undo resolve terakhir:")
    manager.undo_resolve()

    # ── 7. Cari alert berdasarkan device ──────────────────────
    print("\n[7] Cari alert dari 'SENSOR_0':")
    hasil = manager.cari_by_device('SENSOR_0')
    if hasil:
        for a in hasil:
            print(f"    Alert#{a.alert_id} [{LABEL_TIPE[a.tipe]}] {a.pesan}")
    else:
        print("    Tidak ada alert aktif dari SENSOR_0.")

    # ── 8. Resolve semua alert dari GATEWAY_2 ────────────────
    print("\n[8] Resolve semua alert dari 'GATEWAY_2':")
    manager.resolve_by_device('GATEWAY_2')

    # ── 9. Laporan akhir ──────────────────────────────────────
    manager.laporan()


# ════════════════════════════════════════════════════════════
if __name__ == '__main__':
    demo_modul4()