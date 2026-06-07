import random
import math
from data import AMBULANS, NAMA_RS, KOORDINAT

POPULATION_SIZE = 30
GENERATIONS = 100
MUTATION_RATE = 0.1
TOURNAMENT_SIZE = 3


def jarak_dua_pasien(p1, p2):
    x1, y1 = KOORDINAT[p1]
    x2, y2 = KOORDINAT[p2]

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def hitung_total_jarak(kromosom):
    if len(kromosom) <= 1:
        return 0.0

    total = 0.0

    for i in range(len(kromosom) - 1):
        total += jarak_dua_pasien(kromosom[i], kromosom[i + 1])

    return round(total, 4)


def hitung_fitness(kromosom):
    total = hitung_total_jarak(kromosom)
    return 1 / (1 + total)


def buat_populasi_awal(daftar_pasien, pop_size):
    populasi = []

    for _ in range(pop_size):
        kromosom = daftar_pasien[:]
        random.shuffle(kromosom)
        populasi.append(kromosom)

    return populasi


def tournament_selection(populasi, fitness_scores):
    kandidat = random.sample(
        range(len(populasi)),
        TOURNAMENT_SIZE
    )

    pemenang = kandidat[0]

    for idx in kandidat[1:]:
        if fitness_scores[idx] > fitness_scores[pemenang]:
            pemenang = idx

    return populasi[pemenang][:]


def order_crossover(parent1, parent2):
    n = len(parent1)

    if n == 1:
        return parent1[:]

    start = random.randint(0, n - 1)
    end = random.randint(start + 1, n)

    child = [None] * n

    child[start:end] = parent1[start:end]
    used = set(child[start:end])

    pos = end % n

    for pasien in parent2[end:] + parent2[:end]:
        if pasien not in used:
            child[pos] = pasien
            used.add(pasien)
            pos = (pos + 1) % n

    return child


def swap_mutation(kromosom):
    hasil = kromosom[:]

    if len(hasil) >= 2 and random.random() < MUTATION_RATE:
        i, j = random.sample(range(len(hasil)), 2)
        hasil[i], hasil[j] = hasil[j], hasil[i]

    return hasil


def ga_optimize_one(daftar_pasien):
    if len(daftar_pasien) == 0:
        return [], 0.0

    if len(daftar_pasien) == 1:
        return daftar_pasien[:], 0.0

    populasi = buat_populasi_awal(
        daftar_pasien,
        POPULATION_SIZE
    )

    rute_terbaik = populasi[0][:]
    jarak_terbaik = hitung_total_jarak(rute_terbaik)

    for _ in range(GENERATIONS):
        fitness_scores = [
            hitung_fitness(ind)
            for ind in populasi
        ]

        for ind in populasi:
            jarak = hitung_total_jarak(ind)

            if jarak < jarak_terbaik:
                jarak_terbaik = jarak
                rute_terbaik = ind[:]

        generasi_baru = []

        urutan = sorted(
            range(len(populasi)),
            key=lambda i: fitness_scores[i],
            reverse=True
        )

        generasi_baru.append(
            populasi[urutan[0]][:]
        )

        if POPULATION_SIZE > 1:
            generasi_baru.append(
                populasi[urutan[1]][:]
            )

        while len(generasi_baru) < POPULATION_SIZE:
            parent1 = tournament_selection(
                populasi,
                fitness_scores
            )

            parent2 = tournament_selection(
                populasi,
                fitness_scores
            )

            anak = order_crossover(
                parent1,
                parent2
            )

            anak = swap_mutation(anak)

            generasi_baru.append(anak)

        populasi = generasi_baru

    return rute_terbaik, round(jarak_terbaik, 4)


def ga_optimize_all(hasil_bnb):
    hasil_ga = {}

    for amb in AMBULANS:
        dispatch = hasil_bnb[amb]["dispatch"]

        rute, total_jarak = ga_optimize_one(dispatch)

        fitness = (
            round(hitung_fitness(rute), 6)
            if rute else 0.0
        )

        hasil_ga[amb] = {
            "dispatch": dispatch,
            "rute": rute,
            "total_jarak": total_jarak,
            "fitness": fitness
        }

    return hasil_ga


def tampilkan_hasil_ga(hasil_ga):
    print("=" * 50)
    print("GENETIC ALGORITHM - ROUTE OPTIMIZATION")
    print("=" * 50)
    print(
        f"Pop size={POPULATION_SIZE}, "
        f"Generasi={GENERATIONS}, "
        f"Mutasi={MUTATION_RATE}"
    )
    print()

    for amb in AMBULANS:
        info = hasil_ga[amb]

        print(f"{amb} - {NAMA_RS[amb]}")

        if not info["dispatch"]:
            print("     Tidak ada pasien untuk dirutekan.")
        else:
            rute_str = (
                " -> ".join(info["rute"])
                if info["rute"]
                else "-"
            )

            print(f"     Dispatch       : {info['dispatch']}")
            print(f"     Rute Terbaik   : {rute_str}")
            print(f"     Total Distance : {info['total_jarak']} km")
            print(f"     Fitness        : {info['fitness']}")

        print()


if __name__ == "__main__":
    random.seed(42)

    from dynamic_programming import (
        dp_resource_allocation,
        tampilkan_hasil_dp
    )

    from branch_and_bound import (
        bnb_dispatch_all,
        tampilkan_hasil_bnb
    )

    alokasi, total_cost_dp, memo = dp_resource_allocation()
    tampilkan_hasil_dp(alokasi, total_cost_dp)

    hasil_bnb = bnb_dispatch_all(alokasi)
    tampilkan_hasil_bnb(hasil_bnb)

    hasil_ga = ga_optimize_all(hasil_bnb)
    tampilkan_hasil_ga(hasil_ga)