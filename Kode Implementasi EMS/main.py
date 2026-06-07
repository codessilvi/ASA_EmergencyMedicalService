import time
import random

from data import AMBULANS, NAMA_RS, PASIEN, PRIORITAS, JARAK
from dynamic_programming import dp_resource_allocation
from branch_and_bound import bnb_dispatch_all, K
from genetic_algorithm import ga_optimize_all, hitung_total_jarak


def cetak_garis(karakter="=",panjang=52):
    # Mencetak garis pembatas ke terminal
    print(karakter * panjang)


def cetak_header(judul):
    # Mencetak judul menu atau modul dengan pembatas garis
    cetak_garis()
    print(f"  {judul}")
    cetak_garis()
    print()


def tampilkan_dp(alokasi,total_cost,jumlah_memo,waktu_dp):
    # Menampilkan detail alokasi pasien dari modul Dynamic Programming
    cetak_header("DYNAMIC PROGRAMMING - RESOURCE ALLOCATION")

    for amb in AMBULANS:
        daftar = alokasi[amb]
        print(f"  {amb}  {NAMA_RS[amb]}")

        if not daftar:
            print("       Tidak ada pasien")
        else:
            print(f"       Pasien  : {daftar}")
            for pas in daftar:
                idx = PASIEN.index(pas)
                j = JARAK[amb][idx]
                p = PRIORITAS[pas]
                c = round(j - p, 2)
                print(f"       -> {pas}  jarak={j} km  prioritas={p}  cost={c}")
        print()

    print(f"  Total Cost Seluruh Alokasi : {total_cost}")
    print(f"  Jumlah State di Memo       : {jumlah_memo}")
    print(f"  Waktu Eksekusi DP          : {waktu_dp:.4f} detik")
    print()


def tampilkan_bnb(hasil_bnb,waktu_bnb):
    # Menampilkan detail seleksi dispatch dari modul Branch and Bound
    cetak_header(f"BRANCH AND BOUND - DISPATCH SELECTION  (k = {K})")

    total_node = 0
    for amb in AMBULANS:
        info = hasil_bnb[amb]
        total_node += info["node_count"]

        print(f"  {amb}  {NAMA_RS[amb]}")

        if not info["dispatch"] and not info["menunggu"]:
            print("       Tidak ada pasien.")
        else:
            print(f"       Dispatch Sekarang  : {info['dispatch']}")
            print(f"       Menunggu           : {info['menunggu']}")
            print(f"       Best Cost          : {info['best_cost']}")
            print(f"       Node Dieksplorasi  : {info['node_count']}")
        print()

    print(f"  Total Node Dieksplorasi    : {total_node}")
    print(f"  Waktu Eksekusi B&B         : {waktu_bnb:.4f} detik")
    print()


def tampilkan_ga(hasil_ga,waktu_ga):
    # Menampilkan detail rute optimal dari modul Genetic Algorithm
    cetak_header("GENETIC ALGORITHM - ROUTE OPTIMIZATION")

    total_jarak_semua = 0.0
    for amb in AMBULANS:
        info = hasil_ga[amb]
        total_jarak_semua += info["total_jarak"]

        print(f"  {amb}  {NAMA_RS[amb]}")

        if not info["dispatch"]:
            print("       Tidak ada pasien untuk dirutekan.")
        else:
            rute_str = " -> ".join(info["rute"]) if info["rute"] else "-"
            print(f"       Dispatch       : {info['dispatch']}")
            print(f"       Rute Terbaik   : {rute_str}")
            print(f"       Total Distance : {info['total_jarak']} km")
            print(f"       Fitness        : {info['fitness']}")
        print()

    print(f"  Total Jarak Seluruh Rute   : {round(total_jarak_semua, 4)} km")
    print(f"  Waktu Eksekusi GA          : {waktu_ga:.4f} detik")
    print()


def tampilkan_ringkasan(alokasi,hasil_bnb,hasil_ga,waktu_dp,waktu_bnb,waktu_ga,total_cost_dp,jumlah_memo):
    # Menampilkan rangkuman performa dan hasil akhir komparasi algoritma
    cetak_header("RINGKASAN EKSPERIMEN")

    total_node = sum(hasil_bnb[a]["node_count"] for a in AMBULANS)
    total_jarak = sum(hasil_ga[a]["total_jarak"] for a in AMBULANS)

    total_dispatch = sum(len(hasil_bnb[a]["dispatch"]) for a in AMBULANS)
    total_menunggu = sum(len(hasil_bnb[a]["menunggu"]) for a in AMBULANS)

    lebar = 70
    print(f"  {'Algoritma':<22} {'Fungsi':<22} {'Hasil Utama':<16} {'Waktu':>8}")
    cetak_garis("-",lebar)

    print(f"  {'Dynamic Programming':<22} {'Resource Allocation':<22} {'Cost = ' + str(total_cost_dp):<16} {waktu_dp:.4f} s")
    print(f"  {'Branch and Bound':<22} {'Dispatch Selection':<22} {str(total_node) + ' node':<16} {waktu_bnb:.4f} s")
    print(f"  {'Genetic Algorithm':<22} {'Route Optimization':<22} {str(round(total_jarak, 2)) + ' km total':<16} {waktu_ga:.4f} s")

    cetak_garis("-",lebar)
    print()

    print("  Detail Hasil:")
    print(f"    Jumlah Pasien              : {len(PASIEN)}")
    print(f"    Jumlah Ambulans            : {len(AMBULANS)}")
    print(f"    Pasien ter-dispatch        : {total_dispatch}")
    print(f"    Pasien menunggu            : {total_menunggu}")
    print(f"    State tersimpan di memo    : {jumlah_memo}")
    print(f"    Total node B&B             : {total_node}")
    print(f"    Total jarak seluruh rute   : {round(total_jarak, 4)} km")
    print(f"    Total waktu eksekusi       : {round(waktu_dp + waktu_bnb + waktu_ga, 4)} detik")
    print()

    print("  Rekap Alokasi per Ambulans:")
    cetak_garis("-",lebar)
    print(f"  {'Amb':<6} {'Alokasi DP':<20} {'Dispatch (B&B)':<20} {'Rute (GA)'}")
    cetak_garis("-",lebar)

    for amb in AMBULANS:
        alok_str = str(alokasi[amb])
        dispatch_str = str(hasil_bnb[amb]["dispatch"])
        rute_str = " -> ".join(hasil_ga[amb]["rute"]) if hasil_ga[amb]["rute"] else "-"
        print(f"  {amb:<6} {alok_str:<20} {dispatch_str:<20} {rute_str}")

    cetak_garis("-",lebar)
    print()


def main():
    # Fungsi utama untuk menjalankan seluruh rangkaian pipeline pengujian EMS
    random.seed(42)

    print()
    print("  SISTEM OPTIMALISASI EMS - KOTA SEMARANG")
    print("  Analisis dan Strategi Algoritma 2026")
    print()

    # Eksekusi Tahap 1: Dynamic Programming
    print(" Dynamic Programming...")
    t_mulai = time.perf_counter()
    alokasi, total_cost_dp, memo = dp_resource_allocation()
    waktu_dp = time.perf_counter() - t_mulai
    jumlah_memo = len(memo)

    print(f"        Selesai dalam ({waktu_dp:.4f} detik)")
    print()
    tampilkan_dp(alokasi,total_cost_dp,jumlah_memo,waktu_dp)

    # Eksekusi Tahap 2: Branch and Bound
    print("  Branch and Bound...")
    t_mulai = time.perf_counter()
    hasil_bnb = bnb_dispatch_all(alokasi)
    waktu_bnb = time.perf_counter() - t_mulai

    print(f"        Selesai dalam ({waktu_bnb:.4f} detik)")
    print()
    tampilkan_bnb(hasil_bnb,waktu_bnb)

    # Eksekusi Tahap 3: Genetic Algorithm
    print("  Genetic Algorithm...")
    t_mulai = time.perf_counter()
    hasil_ga = ga_optimize_all(hasil_bnb)
    waktu_ga = time.perf_counter() - t_mulai

    print(f"        Selesai dalam({waktu_ga:.4f} detik)")
    print()
    tampilkan_ga(hasil_ga,waktu_ga)

    # Menampilkan evaluasi akhir kesimpulan eksperimen
    tampilkan_ringkasan(alokasi,hasil_bnb,hasil_ga,waktu_dp,waktu_bnb,waktu_ga,total_cost_dp,jumlah_memo)


if __name__ == "__main__":
    main()