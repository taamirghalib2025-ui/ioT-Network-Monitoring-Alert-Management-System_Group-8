
"""
modul_3.py — Modul 3: BST Device Registry
Bertindak sebagai service layer untuk manajemen registrasi perangkat IoT 
menggunakan Binary Search Tree dan menampilkan kompleksitas waktu (Big-O).
"""

from data_structures.bst import BSTRegistry

def run_register_device(registry: BSTRegistry, device) -> None:
    """
    Menambahkan perangkat baru ke dalam sistem registri BST.
    Spesifikasi: Big-O: O(log n) rata-rata
    """
    try:
        registry.insert(device)
        print(f"[REGISTER] Perangkat '{device.device_id}' ({device.tipe}) berhasil diregistrasi.")
    except ValueError as e:
        # Menangkap error jika device_id sudah ada di dalam sistem
        print(f"[ERROR] Registrasi gagal: {e}")
        
    print("-> Kompleksitas Waktu: Big-O: O(log n) rata-rata\n")


def run_search_device(registry: BSTRegistry, device_id: str):
    """
    Mencari perangkat berdasarkan device_id secara efisien.
    Spesifikasi: Big-O: O(log n) rata-rata
    """
    device = registry.search(device_id)
    if device:
        print(f"[FOUND] Perangkat ditemukan: ID={device.device_id} | Tipe={device.tipe} | Status={device.status} | Reading={device.last_reading}")
    else:
        print(f"[NOT FOUND] Perangkat '{device_id}' tidak ditemukan di registri.")
        
    print("-> Kompleksitas Waktu: Big-O: O(log n) rata-rata\n")
    return device


def run_update_status(registry: BSTRegistry, device_id: str, new_status: str, last_reading=None) -> None:
    """
    Memperbarui status (ONLINE/OFFLINE) dan nilai bacaan sensor terakhir perangkat.
    Spesifikasi: Big-O: O(log n) rata-rata
    """
    success = registry.update_status(device_id, new_status, last_reading)
    if success:
        bacaan_str = f" | Reading: {last_reading}" if last_reading is not None else ""
        print(f"[UPDATE] Status '{device_id}' diperbarui menjadi {new_status}{bacaan_str}.")
    else:
        print(f"[ERROR] Gagal update: Perangkat '{device_id}' tidak ditemukan di registri.")
        
    print("-> Kompleksitas Waktu: Big-O: O(log n) rata-rata\n")


def run_list_devices(registry: BSTRegistry) -> None:
    """
    Menampilkan semua perangkat yang terdaftar secara terurut abjad berdasarkan ID.
    Spesifikasi: Big-O: O(n)
    """
    print("=" * 60)
    print("DAFTAR PERANGKAT IoT TERREGISTRASI (TERURUT)")
    print("=" * 60)
    
    devices = registry.inorder()
    if not devices:
        print("Belum ada perangkat yang terdaftar.")
    else:
        for idx, dev in enumerate(devices, 1):
            print(f"  {idx}. {dev.device_id} | {dev.tipe} | Status: {dev.status} | Last Reading: {dev.last_reading}")
            
    print("=" * 60)
    print("-> Kompleksitas Waktu: Big-O: O(n)\n")