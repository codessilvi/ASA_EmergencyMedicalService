from data import AMBULANS, NAMA_RS, PASIEN, hitung_cost

# Batas maksimal pasien yang bisa di-dispatch per siklus
K = 2


def hitung_lower_bound(cost_so_far,included,index,daftar_pasien,ambulans):
    # Menghitung estimasi biaya minimum (lower bound) untuk sisa slot
    slot_tersisa = K - len(included)
    if slot_tersisa <= 0:
        return cost_so_far

    cost_sisa = []
    for j in range(index, len(daftar_pasien)):
        cost_sisa.append(hitung_cost(ambulans,daftar_pasien[j]))

    # Urutkan dari terkecil untuk mendapatkan estimasi paling optimis
    cost_sisa.sort()
    return cost_so_far + sum(cost_sisa[:slot_tersisa])


def bnb_dispatch_one(ambulans,daftar_pasien):
    # Memilih kombinasi pasien terbaik untuk satu ambulans menggunakan BnB
    n = len(daftar_pasien)

    # Base case jika jumlah pasien tidak melebihi kapasitas siklus
    if n <= K:
        total = sum(hitung_cost(ambulans,p) for p in daftar_pasien)
        return (daftar_pasien[:], [], round(total, 3), 1)

    # Pra-perhitungan cost untuk menghemat komputasi
    cost_pasien = {p: hitung_cost(ambulans,p) for p in daftar_pasien}

    best_cost = float("inf")
    best_subset = []
    node_count = 0

    # Stack untuk DFS (index, included_list, cost_so_far)
    stack = [(0, [], 0.0)]

    while stack:
        index, included, cost_so_far = stack.pop()
        node_count += 1

        slot_terisi = len(included)
        slot_tersisa = K - slot_terisi
        pasien_tersisa = n - index

        # Pruning jika sisa pasien tidak cukup memenuhi slot
        if pasien_tersisa < slot_tersisa:
            continue

        # Validasi jika solusi lengkap tercapai
        if slot_terisi == K:
            if cost_so_far < best_cost:
                best_cost = cost_so_far
                best_subset = included[:]
            continue

        if index == n:
            continue

        # Pruning berdasarkan estimasi lower bound
        lb = hitung_lower_bound(cost_so_far,included,index,daftar_pasien,ambulans)
        if lb >= best_cost:
            continue

        pasien = daftar_pasien[index]

        # Cabang 1: Pasien tidak dimasukkan ke dalam subset
        if pasien_tersisa - 1 >= slot_tersisa:
            stack.append((index + 1, included[:], cost_so_far))

        # Cabang 2: Pasien dimasukkan ke dalam subset
        cost_baru = cost_so_far + cost_pasien[pasien]
        stack.append((index + 1, included + [pasien], cost_baru))

    # Identifikasi pasien yang belum terangkut (masuk daftar tunggu)
    menunggu = [p for p in daftar_pasien if p not in best_subset]

    return (best_subset, menunggu, round(best_cost, 3), node_count)


def bnb_dispatch_all(alokasi):
    # Menjalankan pemilihan dispatch untuk semua ambulans tersedia
    hasil = {}

    for amb in AMBULANS:
        daftar_pasien = alokasi.get(amb, [])

        if not daftar_pasien:
            hasil[amb] = {
                "dispatch": [],
                "menunggu": [],
                "best_cost": 0,
                "node_count": 0
            }
            continue

        dispatch, menunggu, best_cost, node_count = bnb_dispatch_one(amb,daftar_pasien)

        hasil[amb] = {
            "dispatch": dispatch,
            "menunggu": menunggu,
            "best_cost": best_cost,
            "node_count": node_count
        }

    return hasil


def tampilkan_hasil_bnb(hasil):
    # Menampilkan hasil dispatch selection ke terminal
    print("=" * 50)
    print("BRANCH AND BOUND - DISPATCH SELECTION")
    print("=" * 50)
    print(f"Kapasitas dispatch per siklus: k = {K}")
    print()

    for amb in AMBULANS:
        info = hasil[amb]
        print(f"{amb} - {NAMA_RS[amb]}")

        if not info["dispatch"] and not info["menunggu"]:
            print("     Tidak ada pasien.")
        else:
            print(f"     Dispatch sekarang : {info['dispatch']}")
            print(f"     Menunggu          : {info['menunggu']}")
            print(f"     Best Cost         : {info['best_cost']}")
            print(f"     Node dieksplorasi : {info['node_count']}")
        print()


if __name__ == "__main__":
    from dynamic_programming import dp_resource_allocation, tampilkan_hasil_dp

    # Langkah 1: Jalankan alokasi resource dari modul DP
    alokasi, total_cost_dp, memo = dp_resource_allocation()
    tampilkan_hasil_dp(alokasi, total_cost_dp)

    # Langkah 2: Evaluasi prioritas dispatch menggunakan BnB
    hasil_bnb = bnb_dispatch_all(alokasi)
    tampilkan_hasil_bnb(hasil_bnb)
