from data import AMBULANS, PASIEN, hitung_cost

# Maksimal pasien yang bisa dilayani oleh satu ambulans
MAKS_PASIEN_PER_AMBULANS = 4


def dp(index_pasien, beban, memo):
    # Base case: semua pasien telah diproses
    if index_pasien == len(PASIEN):
        return 0

    # Representasi state untuk memoization
    state = (index_pasien, beban)

    # Cek apakah state sudah pernah dihitung sebelumnya
    if state in memo:
        return memo[state]

    pasien = PASIEN[index_pasien]
    best_cost = float("inf")

    # Evaluasi semua kemungkinan alokasi ambulans
    for i, ambulans in enumerate(AMBULANS):
        # Abaikan ambulans yang sudah mencapai kapasitas maksimal
        if beban[i] >= MAKS_PASIEN_PER_AMBULANS:
            continue

        # Hitung biaya penugasan ambulans ke pasien
        cost = hitung_cost(ambulans, pasien)

        # Update beban ambulans untuk pasien berikutnya
        beban_baru = list(beban)
        beban_baru[i] += 1
        beban_baru = tuple(beban_baru)

        # Rekursi untuk pasien berikutnya dan hitung total biaya
        total = cost + dp(index_pasien + 1, beban_baru, memo)

        # Update best_cost jika total biaya saat ini lebih kecil
        if total < best_cost:
            best_cost = total

    # Simpan hasil perhitungan ke memo
    memo[state] = best_cost
    return best_cost


def backtrack(index_pasien, beban, memo):
    # Base case: semua pasien telah diproses
    if index_pasien == len(PASIEN):
        return []

    pasien = PASIEN[index_pasien]

    best_cost = float("inf")
    ambulans_pilihan = None
    beban_pilihan = None

    # Cari ambulans pilihan berdasarkan nilai optimal yang tersimpan di memo
    for i, ambulans in enumerate(AMBULANS):
        if beban[i] >= MAKS_PASIEN_PER_AMBULANS:
            continue

        cost = hitung_cost(ambulans, pasien)

        beban_baru = list(beban)
        beban_baru[i] += 1
        beban_baru = tuple(beban_baru)

        # Ambil nilai sisa biaya dari memo
        cost_sisa = memo.get((index_pasien + 1, beban_baru), 0)
        total = cost + cost_sisa

        # Update ambulans pilihan jika total biaya saat ini lebih kecil
        if total < best_cost:
            best_cost = total
            ambulans_pilihan = ambulans
            beban_pilihan = beban_baru

    # Rekursi untuk pasien berikutnya dan kembalikan urutan keputusan
    return [
        (pasien, ambulans_pilihan)
    ] + backtrack(index_pasien + 1, beban_pilihan, memo)


def dp_resource_allocation():
    # Inisialisasi memoization dan beban awal ambulans
    memo = {}
    beban_awal = (0, 0, 0, 0, 0)

    # Hitung total biaya optimal menggunakan DP
    total_cost = dp(0, beban_awal, memo)
    # Temukan urutan keputusan terbaik menggunakan backtrack
    keputusan = backtrack(0, beban_awal, memo)

    # Kelompokkan pasien berdasarkan ambulans yang ditugaskan
    alokasi = {amb: [] for amb in AMBULANS}
    for pasien, ambulans in keputusan:
        alokasi[ambulans].append(pasien)

    return alokasi, round(total_cost, 3), memo


def tampilkan_hasil_dp(alokasi, total_cost):
    # Menampilkan hasil resource allocation
    print("=" * 50)
    print("DYNAMIC PROGRAMMING - RESOURCE ALLOCATION")
    print("=" * 50)
    print()

    from data import NAMA_RS, JARAK, PASIEN, PRIORITAS

    # Loop setiap ambulans dan tampilkan daftar pasien yang ditugaskan
    for amb in AMBULANS:
        daftar = alokasi[amb]
        print(f"{amb} - {NAMA_RS[amb]}")

        # Tampilkan pesan jika ambulans tidak memiliki pasien
        if not daftar:
            print("     Tidak ada pasien")
        else:
            print(f"     Pasien: {daftar}")
            # Tampilkan detail setiap pasien (jarak, prioritas, cost)
            for pas in daftar:
                idx = PASIEN.index(pas)
                jarak = JARAK[amb][idx]
                prioritas = PRIORITAS[pas]
                cost = round(jarak - prioritas, 2)
                print(
                    f"     -> {pas} | jarak={jarak} km | "
                    f"prioritas={prioritas} | cost={cost}"
                )
        print()

    # Tampilkan total biaya keseluruhan
    print(f"Total Cost Keseluruhan : {total_cost}")
    print()


if __name__ == "__main__":
    # Menjalankan resource allocation dengan DP
    alokasi, total_cost, memo = dp_resource_allocation()

    # Menampilkan hasil resource allocation
    tampilkan_hasil_dp(alokasi, total_cost)

    # Menampilkan jumlah state dalam memo
    print(f"Jumlah state memo : {len(memo)}")
    print()

    # Menampilkan beberapa contoh state dalam memo
    print("Contoh state memo:")
    for i, (state, nilai) in enumerate(memo.items()):
        if i >= 5:
            break
        print(f"  {state} -> {round(nilai, 3)}")