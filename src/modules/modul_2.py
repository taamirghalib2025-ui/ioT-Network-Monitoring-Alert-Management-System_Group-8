"""
modul_2.py — Modul 2: Priority Alert Queue
Bertindak sebagai service layer untuk memproses antrean peringatan (alert)
dan menampilkan kompleksitas waktu (Big-O) sesuai panduan proyek.
"""

from data_structures.queue import AlertPriorityQueue

def run_tambah_alert(antrean: AlertPriorityQueue, alert) -> None:
    """
    Menjalankan fungsi tambah alert ke dalam priority queue.
    Spesifikasi: Big-O: O(n) worst-case
    """
    antrean.enqueue(alert)
    
    # Pemetaan angka prioritas ke string agar tampilan lebih enak dibaca
    prioritas_str = ["UNKNOWN", "CRITICAL", "WARNING", "INFO"]
    tipe_str = prioritas_str[alert.tipe] if 1 <= alert.tipe <= 3 else "UNKNOWN"
    
    print(f"[ENQUEUE] Alert #{alert.alert_id} dari '{alert.device_id}' ({tipe_str}) masuk ke antrean.")
    print("-> Kompleksitas Waktu: Big-O: O(n) worst-case\n")


def run_proses_alert(antrean: AlertPriorityQueue):
    """
    Mengambil dan memproses alert dengan prioritas tertinggi (dequeue).
    Spesifikasi: Big-O: O(1)
    """
    alert = antrean.dequeue()
    if alert:
        prioritas_str = ["UNKNOWN", "CRITICAL", "WARNING", "INFO"]
        tipe_str = prioritas_str[alert.tipe] if 1 <= alert.tipe <= 3 else "UNKNOWN"
        print(f"[DEQUEUE] Memproses Alert #{alert.alert_id} dari '{alert.device_id}' [{tipe_str}]: {alert.pesan}")
    else:
        print("[INFO] Antrean kosong. Tidak ada alert yang perlu diproses.")
        
    print("-> Kompleksitas Waktu: Big-O: O(1)\n")
    return alert


def run_lihat_antrean(antrean: AlertPriorityQueue) -> None:
    """
    Melihat seluruh daftar alert yang masih menunggu (pending).
    Spesifikasi: Big-O: O(n)
    """
    print("=" * 60)
    print("DAFTAR ANTREAN ALERT (PENDING)")
    print("=" * 60)
    
    if antrean.is_empty():
        print("Antrean saat ini kosong. Kondisi jaringan aman.")
    else:
        pending_list = antrean.pending_alerts()
        prioritas_str = ["UNKNOWN", "CRITICAL", "WARNING", "INFO"]
        for idx, a in enumerate(pending_list, 1):
            tipe = prioritas_str[a.tipe] if 1 <= a.tipe <= 3 else "UNKNOWN"
            print(f"  {idx}. [Alert #{a.alert_id}] {a.device_id} | {tipe} | {a.pesan}")
            
    print("=" * 60)
    print("-> Kompleksitas Waktu: Big-O: O(n)\n")