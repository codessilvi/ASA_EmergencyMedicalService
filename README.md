# ASA_EmergencyMedicalService
Kode Implementasi Python untuk Makalah: Optimalisasi Sistem Emergency Medical Services (EMS): Analisis Performa Dynamic Programming, Branch and Bound, dan Genetic Algorithm dalam Penugasan Ambulans Berdasarkan Jarak dan Prioritas Pasien di Kota Semarang

Nama : Silvani Salsabilla
NIM  : 24060124130066
Departemen Informatika, Universitas Diponegoro


## Deskripsi

Sistem ini mengimplementasikan **pipeline sekuensial tiga algoritma** untuk menyelesaikan permasalahan penugasan ambulans pada sistem EMS secara bertahap:

| Tahap | Algoritma | Fungsi |
|-------|-----------|--------|
| 1 | **Dynamic Programming** | Resource Allocation — >alokasi global 10 pasien ke 5 ambulans dengan total cost minimum |
| 2 | **Branch and Bound** | Dispatch Selection —> memilih subset k pasien terbaik per ambulans untuk batch dispatch pertama |
| 3 | **Genetic Algorithm** | Route Optimization —> mengoptimalkan urutan rute pelayanan ambulans |

Fungsi biaya yang digunakan mengintegrasikan jarak dan prioritas pasien:

```
Cost(i, j) = Distance(i, j) − w × Priority(j)
```

sehingga pasien dengan prioritas tinggi secara alami mendapat penugasan yang lebih menguntungkan.

---

## Cara Menjalankan

### Menjalankan Pipeline Lengkap

```bash
python main.py
```

### Menjalankan Modul Secara Terpisah

```bash
# Hanya Dynamic Programming
python dynamic_programming.py

# Hanya Branch and Bound (membutuhkan output DP)
python branch_and_bound.py

# Hanya Genetic Algorithm (membutuhkan output DP + B&B)
python genetic_algorithm.py

# Lihat data mentah
python data.py
```

---


