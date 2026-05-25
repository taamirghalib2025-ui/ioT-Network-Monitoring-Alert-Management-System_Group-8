"""
modul_6.py — Modul 6: CLI Monitoring
Menyediakan antarmuka Command Line (CLI) interaktif untuk mengelola
Sistem Monitoring Jaringan IoT dengan format perintah sesuai panduan.
"""

import time
import sys

# Mengimpor service modul
from modules import modul_1, modul_2, modul_3, modul_4, modul_5

class Device:
    def __init__(self, device_id, tipe, status="ONLINE", last_reading=0.0):
        self.device_id = device_id
        self.tipe = tipe
        self.status = status
        self.last_reading = last_reading

class Alert:
    def __init__(self, alert_id, device_id, tipe, pesan):
        self.alert_id = alert_id
        self.device_id = device_id
        self.tipe = int(tipe)  # 1=CRITICAL, 2=WARNING, 3=INFO
        self.pesan = pesan
        self.timestamp = time.time()

def cetak_menu_bantuan():
    """Mencetak daftar perintah"""
    print("\n" + "=" * 65)
    print(" 💡 DAFTAR PERINTAH:")
    print("=" * 65)
    print(" 1. ADD_DEVICE SENSOR_1 SENSOR")
    print(" 2. ADD_DEVICE SERVER_A SERVER")
    print(" 3. ADD_LINK GATEWAY_0 SENSOR_1 15")
    print(" 4. ADD_LINK SENSOR_1 SERVER_A 20")
    print(" 5. LAPORAN_JARINGAN")
    print(" 6. ALERT_IN SENSOR_1 1 Suhu_Melebihi_Batas")
    print(" 7. ALERT_IN SERVER_A 3 Memori_Penuh")
    print(" 8. PENDING_ALERTS")
    print(" 9. PROCESS_ALERT")
    print(" 10. ROUTING GATEWAY_0")
    print(" 11. AUDIT_LATENSI")
    print(" 12. HISTORY SENSOR_1")
    print(" 13. EXIT")
    print("-" * 65)
    print(" -> Ketik 'HELP' kapan saja untuk memunculkan daftar ini lagi.")
    print("=" * 65 + "\n")

def run_cli(graph, queue, registry, stacks):
    print("=" * 65)
    print("  MEMULAI SISTEM MONITORING JARINGAN IoT...")
    print("=" * 65)
    
    alert_counter = 1  

    # Menampilkan menu bantuan di awal
    cetak_menu_bantuan()

    while True:
        try:
            print("-" * 65)
            command_line = input("IoT-CLI> ").strip()
            if not command_line:
                continue
                
            parts = command_line.split()
            cmd = parts[0].upper()
            args = parts[1:]

            # ── PERINTAH BANTUAN ──
            if cmd == "HELP":
                cetak_menu_bantuan()

            # ── PERINTAH SESUAI SPESIFIKASI ──
            elif cmd == "ADD_DEVICE":
                if len(args) < 2:
                    print("Format salah! Gunakan: ADD_DEVICE <id> <tipe>")
                    continue
                dev_id, tipe = args[0], args[1]
                baru = Device(dev_id, tipe.upper())
                modul_3.run_register_device(registry, baru)
                modul_1.run_add_device(graph, baru)
                stacks[dev_id] = modul_4.AlertStack(kapasitas=20)

            elif cmd == "ADD_LINK":
                if len(args) < 3:
                    print("Format salah! Gunakan: ADD_LINK <u> <v> <latensi>")
                    continue
                modul_1.run_add_link(graph, args[0], args[1], int(args[2]))

            elif cmd == "ALERT_IN":
                if len(args) < 3:
                    print("Format salah! Gunakan: ALERT_IN <device> <type> <pesan>")
                    continue
                dev_id, tipe_str = args[0], args[1]
                pesan = " ".join(args[2:])
                new_alert = Alert(alert_counter, dev_id, tipe_str, pesan)
                alert_counter += 1
                
                modul_2.run_tambah_alert(queue, new_alert)
                if dev_id in stacks:
                    modul_4.run_tambah_riwayat(stacks[dev_id], new_alert)
                modul_3.run_update_status(registry, dev_id, "OFFLINE")

            elif cmd == "PROCESS_ALERT":
                modul_2.run_proses_alert(queue)

            elif cmd == "HISTORY":
                if len(args) < 1:
                    print("Format salah! Gunakan: HISTORY <device>")
                    continue
                dev_id = args[0]
                if dev_id in stacks:
                    modul_4.run_lihat_riwayat(stacks[dev_id], dev_id)
                else:
                    print(f"[ERROR] Stack untuk '{dev_id}' tidak ditemukan.")

            elif cmd == "ISOLASI":
                modul_1.run_deteksi_isolasi(graph, "GATEWAY_0")

            elif cmd == "ROUTING":
                if len(args) < 1:
                    print("Format salah! Gunakan: ROUTING <device>")
                    continue
                start_device = args[0]
                modul_5.run_routing_optimal(graph, start_device)

            elif cmd == "AUDIT_LATENSI":
                print("[INFO] Menghitung jalur dari GATEWAY_0 untuk diaudit...")
                distances = modul_5.run_routing_optimal(graph, 'GATEWAY_0')
                if distances:
                    modul_5.run_audit_latensi(graph, distances)

            elif cmd == "LAPORAN_JARINGAN":
                modul_1.run_laporan_jaringan(graph)

            elif cmd == "PENDING_ALERTS":
                modul_2.run_lihat_antrean(queue)
                
            elif cmd == "ROLLBACK_STATUS":
                if len(args) < 1: continue
                modul_4.run_rollback_status(stacks[args[0]], args[0], registry)
                
            elif cmd == "EXIT":
                print("Menutup Sistem Monitoring IoT... Selamat tinggal!")
                sys.exit(0)
                
            else:
                print(f"[ERROR] Perintah '{cmd}' tidak dikenali. Ketik HELP untuk melihat daftar perintah.")

        except Exception as e:
            print(f"[CRITICAL ERROR] Terjadi kesalahan sistem: {e}")

if __name__ == "__main__":
    pass