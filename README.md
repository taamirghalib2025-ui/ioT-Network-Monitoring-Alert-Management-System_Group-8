# 📡 IoT Network Monitoring & Alert Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Passing-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Dependency-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Status](https://img.shields.io/badge/Status-✓%20Done-success?style=for-the-badge)
![Mata Kuliah](https://img.shields.io/badge/ELT60213-Algoritma%20%26%20Struktur%20Data-orange?style=for-the-badge)

**Sistem pemantauan jaringan IoT berbasis struktur data murni (*from scratch*) — tanpa pustaka koleksi bawaan Python.**

[Fitur](#-fitur--modul-utama) · [Cara Menjalankan](#-cara-menjalankan) · [Perintah CLI](#️-daftar-perintah-cli) · [Struktur Proyek](#-struktur-direktori) · [Tim](#-tim-pengembang)

</div>

---

## 📖 Tentang Proyek

Proyek ini dikembangkan sebagai pemenuhan tugas **Team Based Project (TA 2025/2026)** untuk mata kuliah **ELT60213 Algoritma dan Struktur Data**, Program Studi Teknik Elektro, Universitas Negeri Yogyakarta.

Sistem memodelkan jaringan perangkat IoT yang saling terhubung dengan kemampuan:
- **Memantau status perangkat** menggunakan topologi jaringan berbasis Graph
- **Mengelola antrian alert** berdasarkan tingkat prioritas dengan Priority Queue
- **Menelusuri riwayat kejadian** menggunakan Stack (LIFO)
- **Menganalisis konektivitas jaringan** dengan BFS & DFS kustom

> Seluruh struktur data dibangun **murni dari nol** (*from scratch*) sebagai demonstrasi pemahaman fundamental algoritma dan struktur data.

---

## 👥 Tim Pengembang — Kelompok 8

| Nama | NIM | GitHub | Kontribusi |
|------|-----|--------|------------|
| Muhamad Fahdillah Setyo Wibowo | 25051030081 | [@fadilwibowo373-droid](https://github.com/fadilwibowo373-droid) | Queue & BST · Modul 2 & 3 · Test BST & Queue · Benchmark · `main.py` · Laporan & Slide |
| Muhamad Padang Tazaka | 25051030121 | [@mpadangtazaka-netizen](https://github.com/mpadangtazaka-netizen) | Linked List & Stack · Modul 4 & 5 · Test Stack · Slide · README · Laporan |
| Nauval Fadhlurohman As-sidiq | 25051030120 | [@nauvalfadhluroman2025-droid](https://github.com/nauvalfadhluroman2025-droid) | Graph · Modul 1 · Test Graph · Modul 6 (CLI) · Laporan & Slide |
| Taamir Ghalib Athallah | 25051030092 | [@taamirghalib2025-ui](https://github.com/taamirghalib2025-ui) | Repository & manajemen tim · Modul 6 (CLI) · Laporan & Slide |

---

## ✨ Fitur & Modul Utama

Sistem dipecah menjadi **6 modul fungsional** yang saling terintegrasi:

### Modul 1 — Representasi Jaringan IoT (Graph)
- Menggunakan **Adjacency List** berbasis *Custom Linked List*
- Memodelkan topologi jaringan (node = perangkat, edge = koneksi berbobot)
- Kompleksitas penambahan node/edge: **O(1)**

### Modul 2 — Antrian Alert Berprioritas (Priority Queue)
- Mengelola alert dari perangkat berdasarkan tingkat prioritas: `CRITICAL` → `HIGH` → `MEDIUM` → `LOW`
- Implementasi *Custom Priority Queue* berbasis array
- Kompleksitas enqueue: **O(n)** · dequeue: **O(1)**

### Modul 3 — Direktori Perangkat (BST)
- Menyimpan dan mencari data perangkat IoT secara terurut berdasarkan `device_id`
- Implementasi **Binary Search Tree** murni
- Kompleksitas pencarian rata-rata: **O(log V)**

### Modul 4 — Riwayat Alert (Stack)
- Merekam riwayat alert yang telah diproses menggunakan *Custom Stack* (LIFO)
- Mendukung operasi **undo/rollback** kejadian terakhir
- Kompleksitas push/pop/peek: **O(1)**

### Modul 5 — Analisis Konektivitas Jaringan (Graph Routing)
- Mendeteksi perangkat yang terputus dari gateway utama
- Penelusuran jaringan dengan **BFS & DFS** berbasis struktur data kustom
- Kompleksitas traversal: **O(V+E)**

### Modul 6 — Command Line Interface (CLI)
- Antarmuka interaktif yang aman dari *crash* (penanganan error menyeluruh)
- Mendukung seluruh operasi sistem langsung dari terminal

---

## 🚀 Cara Menjalankan

### Prasyarat

Pastikan Python 3.8+ sudah terinstal, lalu install dependensi:

```bash
pip install numpy pytest
```

### Mode Interaktif

```bash
cd IoT-Network-Monitoring-Alert-Management-System_Group-8
python src/main.py
```

### Mode Demo (Otomatis / CI)

```bash
python src/main.py --demo
```

### Menjalankan Unit Test

```bash
pytest tests/ -v
```

### Eksperimen Runtime & Benchmark

```bash
python experiments/benchmark.py
```

---

## 🖥️ Daftar Perintah CLI

| Perintah | Argumen | Deskripsi |
|----------|---------|-----------|
| `BANTUAN` | — | Tampilkan semua perintah yang tersedia |
| `TAMBAH_PERANGKAT` | `<id> <tipe>` | Tambah perangkat IoT baru ke jaringan |
| `TAMBAH_KONEKSI` | `<id1> <id2> <bobot>` | Tambah koneksi antara dua perangkat |
| `KIRIM_ALERT` | `<device_id> <pesan> <prioritas>` | Kirim alert dari perangkat ke antrian |
| `PROSES_ALERT` | — | Proses alert dengan prioritas tertinggi |
| `RIWAYAT` | — | Tampilkan riwayat alert yang telah diproses (Stack) |
| `CARI_PERANGKAT` | `<device_id>` | Cari perangkat di BST direktori |
| `DIREKTORI` | — | Tampilkan semua perangkat (traversal inorder BST) |
| `TERISOLASI` | — | Deteksi perangkat yang terputus dari gateway |
| `LAPORAN_JARINGAN` | — | Tampilkan adjacency list penuh |
| `ANALISIS_BST` | — | Analisis struktur pohon BST |
| `KELUAR` | — | Keluar dari program |

---

## 🧪 Contoh Sesi

```
MONITORING > TAMBAH_PERANGKAT sensor_01 temperature
  ✓ Perangkat sensor_01 (temperature) berhasil ditambahkan.

MONITORING > TAMBAH_PERANGKAT gateway_01 gateway
  ✓ Perangkat gateway_01 (gateway) berhasil ditambahkan.

MONITORING > TAMBAH_KONEKSI sensor_01 gateway_01 10
  ✓ Koneksi sensor_01 ↔ gateway_01 (bobot: 10) berhasil ditambahkan.

MONITORING > KIRIM_ALERT sensor_01 "Suhu melebihi batas!" CRITICAL
  ✓ Alert CRITICAL dari sensor_01 masuk ke antrian.

MONITORING > PROSES_ALERT
  [CRITICAL] sensor_01: Suhu melebihi batas!
  ✓ Alert diproses dan disimpan ke riwayat.

MONITORING > RIWAYAT
  [1] [CRITICAL] sensor_01: Suhu melebihi batas!

MONITORING > TERISOLASI
  ✓ Semua perangkat terjangkau dari gateway (jaringan terhubung penuh).

MONITORING > CARI_PERANGKAT sensor_01
  ✓ Perangkat ditemukan: sensor_01 | Tipe: temperature

MONITORING > KELUAR
  👋 Keluar dari sistem monitoring.
```

---

## ⚙️ Parameter Sistem

| Parameter | Nilai |
|-----------|-------|
| Jumlah perangkat (node) simulasi | 20 |
| Jumlah koneksi jaringan (edge) | 35 berbobot |
| Algoritma traversal | BFS & DFS |
| Manajemen direktori | Binary Search Tree (BST) |
| Manajemen alert | Priority Queue |
| Seed eksperimen (`np.random.seed`) | 23 *(tetap, tidak diubah)* |

---

## 📊 Analisis Kompleksitas (Big-O)

| Modul | Operasi | Waktu | Ruang |
|-------|---------|-------|-------|
| **Graph** | `add_node`, `add_edge` | O(1) | O(V+E) |
| **Graph** | `neighbors` | O(deg(u)) | O(1) |
| **Priority Queue** | `enqueue` | O(n) | O(n) |
| **Priority Queue** | `dequeue` | O(1) | O(n) |
| **BST** | `insert` / `search` / `delete` | O(log V) rata-rata | O(V) |
| **BST** | `inorder` traversal | O(V) | O(V) |
| **Stack** | `push` / `pop` / `peek` | O(1) | O(n) |
| **Linked List** | `insert` / `delete` (head) | O(1) | O(n) |
| **BFS / DFS** | traversal | O(V+E) | O(V) |

---

## 📁 Struktur Direktori

```
IoT-Network-Monitoring-Alert-Management-System_Group-8/
│
├── 📁 AI_Log/                        # Log penggunaan AI Assistant
│   └── log_prompt.txt
│
├── 📁 docs/                          # Laporan & presentasi
│   ├── laporan_final.pdf
│   └── slide_presentasi.pdf
│
├── 📁 experiments/                   # Eksperimen & benchmark runtime
│   └── benchmark.py
│
├── 📁 src/                           # Source code utama
│   ├── 📁 data_structures/           # Struktur data murni (from scratch)
│   │   ├── graph.py                  # Graf berbasis Adjacency List
│   │   ├── linked_list.py            # Custom Linked List
│   │   ├── queue.py                  # Custom Priority Queue
│   │   ├── stack.py                  # Custom Stack (LIFO)
│   │   └── bst.py                    # Binary Search Tree
│   │
│   ├── 📁 modules/                   # Implementasi algoritma per modul
│   │   ├── modul_1.py                # Representasi jaringan IoT
│   │   ├── modul_2.py                # Antrian alert berprioritas
│   │   ├── modul_3.py                # Direktori perangkat (BST)
│   │   ├── modul_4.py                # Riwayat alert (Stack)
│   │   ├── modul_5.py                # Analisis konektivitas (BFS/DFS)
│   │   └── modul_6.py                # Command Line Interface
│   │
│   └── main.py                       # Entry point aplikasi
│
├── 📁 tests/                         # Unit testing
│   ├── test_graph.py
│   ├── test_queue.py
│   ├── test_bst.py
│   ├── test_stack.py
│   └── test_linked_list.py
│
├── .gitignore
└── README.md
```

---

## 🛠️ Teknologi

| Teknologi | Kegunaan |
|-----------|----------|
| Python 3.8+ | Bahasa pemrograman utama |
| NumPy | Keperluan eksperimen & benchmark |
| Pytest | Unit testing seluruh modul |

> **Catatan:** Seluruh struktur data (Graph, Queue, BST, Stack, Linked List) diimplementasikan **tanpa menggunakan pustaka koleksi bawaan Python** seperti `collections`, `heapq`, atau `queue`.

---

<div align="center">

Dikembangkan untuk mata kuliah **ELT60213 Algoritma dan Struktur Data**  
Teknik Elektro · Universitas Negeri Yogyakarta · TA 2025/2026

</div>
