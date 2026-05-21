import numpy as np
import random
import time
from dataclasses import dataclass
from typing import Optional, List

# ── Seed tetap ──────────────────────────────────────────────
np.random.seed(23)
random.seed(23)

DEVICE_TYPES = ['SENSOR', 'GATEWAY', 'SERVER']
ALERT_TYPES  = {'CRITICAL': 1, 'WARNING': 2, 'INFO': 3}
TIPE_LABEL   = {1: 'CRITICAL', 2: 'WARNING', 3: 'INFO'}


# ── Dataclass ────────────────────────────────────────────────
@dataclass
class Device:
    device_id: str
    tipe: str
    status: str = 'ONLINE'
    last_reading: float = 0.0


@dataclass
class Alert:
    alert_id: int
    device_id: str
    tipe: int           # 1=CRITICAL, 2=WARNING, 3=INFO
    pesan: str
    timestamp: float


# ── Node Linked List ─────────────────────────────────────────
class LLNode:
    """Node serbaguna untuk Linked List."""
    def __init__(self, data=None):
        self.data = data
        self.next: Optional['LLNode'] = None


# ════════════════════════════════════════════════════════════
#   MODUL 2 – AlertPriorityQueue
# ════════════════════════════════════════════════════════════
class AlertPriorityQueue:
    
    def __init__(self):
        self.head: Optional[LLNode] = None
        self._size: int = 0

    # ── Enqueue ───────────────────────────────────────────────
    def enqueue(self, alert: Alert) -> None:
        
        new_node = LLNode(alert)

        # Kasus 1: list kosong atau alert lebih prioritas dari head
        if self.head is None or alert.tipe < self.head.data.tipe:
            new_node.next = self.head
            self.head     = new_node
            self._size   += 1
            return

        # Kasus 2: cari posisi sisip
        # → lewati node yang tipenya <= tipe baru (prioritas >= atau sama)
        #   sehingga node baru masuk di belakang kelompok tipe yang sama
        prev = self.head
        curr = self.head.next
        while curr is not None and curr.data.tipe <= alert.tipe:
            prev = curr
            curr = curr.next

        # Sisipkan di antara prev dan curr
        new_node.next = curr
        prev.next     = new_node
        self._size   += 1

    # ── Dequeue ───────────────────────────────────────────────
    def dequeue(self) -> Optional[Alert]:
       
        if self.head is None:
            return None
        alert      = self.head.data
        self.head  = self.head.next
        self._size -= 1
        return alert

    # ── Peek ──────────────────────────────────────────────────
    def peek(self) -> Optional[Alert]:
       
        return self.head.data if self.head else None

    # ── Ukuran queue ──────────────────────────────────────────
    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    # ── Pending Alerts ────────────────────────────────────────
    def pending_alerts(self) -> List[Alert]:
        
        result: List[Alert] = []
        curr = self.head
        while curr is not None:
            result.append(curr.data)
            curr = curr.next
        return result

    # ── Representasi teks ─────────────────────────────────────
    def __repr__(self) -> str:
        if self.is_empty():
            return "AlertPriorityQueue(kosong)"
        items = [
            f"[{TIPE_LABEL[a.tipe]}] {a.device_id}: {a.pesan}"
            for a in self.pending_alerts()
        ]
        return "AlertPriorityQueue(\n  " + "\n  ".join(items) + "\n)"


# ════════════════════════════════════════════════════════════
#   Fungsi CLI Modul 2
# ════════════════════════════════════════════════════════════
_alert_counter = 0   # global counter id alert

def alert_in(queue: AlertPriorityQueue,
             device_id: str,
             tipe_str: str,
             pesan: str) -> Alert:
    
    global _alert_counter
    tipe_str = tipe_str.upper()
    if tipe_str not in ALERT_TYPES:
        raise ValueError(f"Tipe alert tidak valid: {tipe_str}. "
                         f"Pilihan: {list(ALERT_TYPES.keys())}")

    _alert_counter += 1
    alert = Alert(
        alert_id  = _alert_counter,
        device_id = device_id,
        tipe      = ALERT_TYPES[tipe_str],
        pesan     = pesan,
        timestamp = time.time()
    )
    queue.enqueue(alert)
    print(f"  [ALERT_IN] #{alert.alert_id} {TIPE_LABEL[alert.tipe]:8s} "
          f"dari {device_id}: \"{pesan}\"  "
          f"→ queue size={len(queue)}  Big-O: O(n)")
    return alert


def process_alert(queue: AlertPriorityQueue) -> Optional[Alert]:
    
    alert = queue.dequeue()
    if alert is None:
        print("  [PROCESS_ALERT] Queue kosong, tidak ada alert.  Big-O: O(1)")
        return None
    print(f"  [PROCESS_ALERT] Memproses #{alert.alert_id} "
          f"{TIPE_LABEL[alert.tipe]:8s} dari {alert.device_id}: "
          f"\"{alert.pesan}\"  → sisa queue={len(queue)}  Big-O: O(1)")
    return alert


def pending_alerts(queue: AlertPriorityQueue) -> None:
    
    alerts = queue.pending_alerts()
    print(f"\n  [PENDING_ALERTS] Total antrian: {len(alerts)}  Big-O: O(n)")
    if not alerts:
        print("    (queue kosong)")
        return
    print(f"  {'No':>4}  {'ID':>5}  {'Prioritas':<10}  {'Device':<15}  Pesan")
    print("  " + "-" * 65)
    for i, a in enumerate(alerts, 1):
        tipe_nama = TIPE_LABEL[a.tipe]
        print(f"  {i:>4}  #{a.alert_id:<4}  {tipe_nama:<10}  "
              f"{a.device_id:<15}  {a.pesan}")
    print()


# ════════════════════════════════════════════════════════════
#   Generator data awal
# ════════════════════════════════════════════════════════════
def generate_iot_network(n_devices: int = 40,
                         n_extra_edges: int = 20,
                         seed: int = 23):
    rng     = np.random.default_rng(seed)
    devices = []
    devices.append(Device('GATEWAY_0', 'GATEWAY'))
    for i in range(1, 5):
        devices.append(Device(f'SERVER_{i}', 'SERVER'))
    for i in range(5, n_devices):
        devices.append(Device(f'SENSOR_{i}', 'SENSOR',
                               last_reading=float(rng.uniform(0, 100))))
    return devices


# ════════════════════════════════════════════════════════════
#   Demo / Uji Modul 2
# ════════════════════════════════════════════════════════════
def demo_modul2():
    print("=" * 60)
    print("  MODUL 2 – Priority Alert Queue")
    print("  IoT Network Monitoring System  (seed=23)")
    print("=" * 60)

    queue   = AlertPriorityQueue()
    devices = generate_iot_network(40, 20, seed=23)

    # ── 1. Enqueue dalam urutan acak (bukan urutan prioritas) ─
    print("\n[1] ALERT_IN – Masukkan 10 alert dalam urutan acak:")
    print("-" * 60)
    skenario = [
        ('SENSOR_5',   'INFO',     'Suhu normal: 24.3°C'),
        ('SENSOR_8',   'WARNING',  'Suhu tinggi: 78.2°C'),
        ('GATEWAY_0',  'CRITICAL', 'Koneksi server terputus!'),
        ('SENSOR_12',  'INFO',     'CO2 normal: 412 ppm'),
        ('SERVER_2',   'CRITICAL', 'CPU 98% – beban kritis!'),
        ('SENSOR_15',  'WARNING',  'Daya listrik drop: 185V'),
        ('SENSOR_7',   'INFO',     'Kelembaban: 65%'),
        ('SERVER_1',   'CRITICAL', 'Disk penuh – I/O error!'),
        ('SENSOR_20',  'WARNING',  'Koneksi mesh tidak stabil'),
        ('SENSOR_33',  'INFO',     'Last reading: 55.1'),
    ]
    for device_id, tipe_str, pesan in skenario:
        alert_in(queue, device_id, tipe_str, pesan)

    # ── 2. Tampilkan antrian setelah semua dimasukkan ─────────
    print()
    pending_alerts(queue)

    # ── 3. Verifikasi urutan: CRITICAL harus duluan ───────────
    print("[2] Verifikasi urutan prioritas (head → tail):")
    print("-" * 60)
    all_pending = queue.pending_alerts()
    prev_tipe = 0
    urutan_benar = True
    for a in all_pending:
        marker = "✓" if a.tipe >= prev_tipe else "✗"
        print(f"  {marker} #{a.alert_id:<3} {TIPE_LABEL[a.tipe]:<10} "
              f"{a.device_id:<15} {a.pesan}")
        if a.tipe < prev_tipe:
            urutan_benar = False
        prev_tipe = a.tipe
    print(f"\n  Urutan ASC (CRITICAL→WARNING→INFO): "
          f"{'BENAR ✓' if urutan_benar else 'SALAH ✗'}")

    # ── 4. Proses satu-per-satu (CRITICAL harus keluar dulu) ──
    print("\n[3] PROCESS_ALERT – Proses 5 alert (CRITICAL harus keluar duluan):")
    print("-" * 60)
    for _ in range(5):
        process_alert(queue)

    # ── 5. Sisa antrian ───────────────────────────────────────
    pending_alerts(queue)

    # ── 6. Enqueue saat queue aktif (sisip di tengah) ─────────
    print("[4] ALERT_IN tambahan di tengah proses:")
    print("-" * 60)
    alert_in(queue, 'SENSOR_9',  'CRITICAL', 'Suhu sangat kritis: 99.1°C')
    alert_in(queue, 'SENSOR_11', 'WARNING',  'Tegangan tidak stabil')
    pending_alerts(queue)

    # ── 7. Kosongkan seluruh queue ────────────────────────────
    print("[5] PROCESS_ALERT – Proses semua sisa alert:")
    print("-" * 60)
    while not queue.is_empty():
        process_alert(queue)

    # ── 8. Coba process saat kosong ───────────────────────────
    print()
    process_alert(queue)

    # ── 9. Ringkasan Big-O ────────────────────────────────────
    print("\n" + "=" * 60)
    print("  RINGKASAN KOMPLEKSITAS MODUL 2")
    print("=" * 60)
    print(f"  {'Operasi':<25} {'Big-O':<15} Keterangan")
    print("  " + "-" * 55)
    ops = [
        ("enqueue(alert)",    "O(n)",  "insertion sorted – cari posisi sisip"),
        ("dequeue()",         "O(1)",  "hapus head → CRITICAL selalu duluan"),
        ("peek()",            "O(1)",  "baca head tanpa hapus"),
        ("pending_alerts()",  "O(n)",  "traverse seluruh linked list"),
        ("process_alert()",   "O(1)",  "wrapper dequeue + cetak"),
    ]
    for op, bigo, ket in ops:
        print(f"  {op:<25} {bigo:<15} {ket}")
    print("=" * 60)


# ════════════════════════════════════════════════════════════
if __name__ == '__main__':
    demo_modul2()