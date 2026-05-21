# ============================================================
# modul_4.py
# Modul 4: Alert Management System (Stack-Based)
# IoT Network Monitoring & Alert Management System
# ============================================================

import time
import random
import numpy as np
import sys
import os
from dataclasses import dataclass
from typing import Optional, Dict, List

# Tambahkan path agar bisa mengenali folder 'src' meskipun dijalankan langsung
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from src.data_structures.stack import Alert, AlertStack, Stack, LLNode
except ImportError:
    print("Error: Pastikan folder 'src/data_structures' berisi file 'stack.py' yang benar.")
    sys.exit(1)

# ── Seed tetap ──────────────────────────────────────────────
np.random.seed(23)
random.seed(23)

# ── Konstanta tipe alert ─────────────────────────────────────
TIPE_CRITICAL = 1
TIPE_WARNING  = 2
TIPE_INFO      = 3
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

_alert_counter = 0  # auto-increment global untuk alert_id

# ════════════════════════════════════════════════════════════
#    FUNGSI UTILITAS
# ════════════════════════════════════════════════════════════

def _next_id() -> int:
    global _alert_counter
    _alert_counter += 1
    return _alert_counter

def tentukan_tipe(device_type: str, metric: str, value: float) -> int:
    batas = THRESHOLD.get(device_type, {}).get(metric)
    if batas is None: return TIPE_INFO
    if value >= batas['CRITICAL']: return TIPE_CRITICAL
    if value >= batas['WARNING']: return TIPE_WARNING
    return TIPE_INFO

def buat_alert(device_id: str, device_type: str, metric: str, value: float) -> Optional[Alert]:
    tipe = tentukan_tipe(device_type, metric, value)
    if tipe == TIPE_INFO: return None

    label = LABEL_TIPE[tipe]
    batas = THRESHOLD[device_type][metric][label]
    pesan = f"[{label}] {device_id} ({device_type}): {metric}={value:.2f} (thresh {batas:.2f})"
    
    return Alert(
        alert_id  = _next_id(),
        device_id = device_id,
        tipe      = tipe,
        pesan     = pesan,
        timestamp = time.time(),
    )

# ════════════════════════════════════════════════════════════
#    MODUL 4 – AlertManager
# ════════════════════════════════════════════════════════════

class AlertManager:
    def __init__(self, kapasitas: int = 50):
        self.active_stack:  AlertStack = AlertStack(kapasitas=kapasitas)
        self.history_stack: AlertStack = AlertStack(kapasitas=kapasitas)
        self._resolve_log:  Stack      = Stack()

    def tambah_alert(self, alert: Alert) -> None:
        self.active