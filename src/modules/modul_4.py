"""
modul_4.py — Modul 4: Stack Alert History
Bertindak sebagai service layer untuk menyimpan dan menampilkan
riwayat peringatan (alert) per perangkat menggunakan Stack LIFO.
"""

from data_structures.stack import AlertStack

def run_tambah_riwayat(stack: AlertStack, alert) -> None:
    """
    Menambahkan alert baru ke riwayat perangkat (push).
    Jika melebihi kapasitas (20), alert paling lama (bottom) akan otomatis dihapus.
    Spesifikasi: Big-O: O(1) normal, O(n) worst-case (saat penuh)
    """
    stack.push(alert)
    print(f"[HISTORY: PUSH] Alert #{alert.alert_id} berhasil disimpan ke riwayat '{alert.device_id}'.")
    print("-> Kompleksitas Waktu: Big-O: O(1) normal / O(n) worst-case\n")


def run_ambil_riwayat_terbaru(stack: AlertStack):
    """
    Mengambil dan menghapus alert yang paling terakhir masuk ke riwayat (pop).
    Spesifikasi: Big-O: O(1)
    """
    alert = stack.pop()
    if alert:
        prioritas_str = ["UNKNOWN", "CRITICAL", "WARNING", "INFO"]
        tipe_str = prioritas_str[alert.tipe] if 1 <= alert.tipe <= 3 else "UNKNOWN"
        print(f"[HISTORY: POP] Riwayat ditarik: Alert #{alert.alert_id} [{tipe_str}] - {alert.pesan}")
    else:
        print("[HISTORY: INFO] Riwayat kosong. Tidak ada alert yang bisa ditarik.")
        
    print("-> Kompleksitas Waktu: Big-O: O(1)\n")
    return alert


def run_lihat_riwayat(stack: AlertStack, device_id: str) -> None:
    """
    Menampilkan seluruh riwayat alert pada suatu perangkat.
    Urutan dari yang paling baru (top) ke yang paling lama (bottom).
    Spesifikasi: Big-O: O(n)
    """
    print("=" * 60)
    print(f"RIWAYAT ALERT PERANGKAT: {device_id}")
    print("=" * 60)
    
    if stack.is_empty():
        print("Belum ada riwayat alert untuk perangkat ini.")
    else:
        # Menggunakan to_list() yang mengembalikan urutan dari Top ke Bottom
        history = stack.to_list()
        prioritas_str = ["UNKNOWN", "CRITICAL", "WARNING", "INFO"]
        
        for idx, a in enumerate(history, 1):
            tipe = prioritas_str[a.tipe] if 1 <= a.tipe <= 3 else "UNKNOWN"
            print(f"  {idx}. [Alert #{a.alert_id}] {tipe} | {a.pesan}")
            
    print("=" * 60)
    print("-> Kompleksitas Waktu: Big-O: O(n)\n")


def run_rollback_status(stack: AlertStack, device_id: str, registry=None) -> None:
    """
    Menjalankan perintah ROLLBACK_STATUS.
    Menarik (pop) alert terakhir dari riwayat dan mengembalikan status perangkat.
    Spesifikasi: Big-O: O(1) untuk operasi Stack
    """
    # 1. Pop dari Stack (Big-O: O(1))
    alert_terakhir = stack.pop()
    
    if alert_terakhir:
        print(f"[ROLLBACK] Membatalkan Alert #{alert_terakhir.alert_id} pada perangkat '{device_id}'.")
        
        # 2. Jika registry disertakan, kembalikan status perangkat
        # (Asumsi logika: Pembatalan alert mengembalikan perangkat ke status normal/ONLINE)
        if registry:
            # Karena update_status di BST memakan waktu O(log n), 
            # eksekusi gabungannya nanti menjadi O(log n). Namun operasi stack-nya tetap O(1).
            berhasil = registry.update_status(device_id, "ONLINE")
            if berhasil:
                print(f"[STATUS] Perangkat '{device_id}' berhasil dipulihkan ke status ONLINE.")
            else:
                print(f"[WARNING] Perangkat '{device_id}' tidak ditemukan di sistem registri.")
    else:
        print(f"[ERROR] Rollback gagal. Riwayat alert pada '{device_id}' kosong.")
        
    print("-> Kompleksitas Waktu: Big-O: O(1) (Operasi Stack)\n")