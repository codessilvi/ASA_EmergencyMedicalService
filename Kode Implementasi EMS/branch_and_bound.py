from data import AMBULANS, NAMA_RS, PASIEN, hitung_cost

K = 2


def hitung_lower_bound(
    cost_so_far,
    included,
    index,
    daftar_pasien,
    ambulans
):
    slot_tersisa = K - len(included)

    if slot_tersisa <= 0:
        return cost_so_far

    cost_sisa = []

    for j in range(index, len(daftar_pasien)):
        cost_sisa.append(
            hitung_cost(
                ambulans,
                daftar_pasien[j]
            )
        )

    cost_sisa.sort()

    return cost_so_far + sum(
        cost_sisa[:slot_tersisa]
    )


def bnb_dispatch_one(ambulans, daftar_pasien):
    n = len(daftar_pasien)

    if n <= K:
        total = sum(
            hitung_cost(ambulans, p)
            for p in daftar_pasien
        )

        return (
            daftar_pasien[:],
            [],
            round(total, 3),
            1
        )

    cost_pasien = {
        p: hitung_cost(ambulans, p)
        for p in daftar_pasien
    }

    best_cost = float("inf")
    best_subset = []
    node_count = 0

    stack = [(0, [], 0.0)]

    while stack:
        index, included, cost_so_far = stack.pop()
        node_count += 1

        slot_terisi = len(included)
        slot_tersisa = K - slot_terisi
        pasien_tersisa = n - index

        if pasien_tersisa < slot_tersisa:
            continue

        if slot_terisi == K:
            if cost_so_far < best_cost:
                best_cost = cost_so_far
                best_subset = included[:]

            continue

        if index == n:
            continue

        lb = hitung_lower_bound(
            cost_so_far,
            included,
            index,
            daftar_pasien,
            ambulans
        )

        if lb >= best_cost:
            continue

        pasien = daftar_pasien[index]

        if pasien_tersisa - 1 >= slot_tersisa:
            stack.append(
                (
                    index + 1,
                    included[:],
                    cost_so_far
                )
            )

        cost_baru = (
            cost_so_far +
            cost_pasien[pasien]
        )

        stack.append(
            (
                index + 1,
                included + [pasien],
                cost_baru
            )
        )

    menunggu = [
        p for p in daftar_pasien
        if p not in best_subset
    ]

    return (
        best_subset,
        menunggu,
        round(best_cost, 3),
        node_count
    )


def bnb_dispatch_all(alokasi):
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

        dispatch, menunggu, best_cost, node_count = (
            bnb_dispatch_one(
                amb,
                daftar_pasien
            )
        )

        hasil[amb] = {
            "dispatch": dispatch,
            "menunggu": menunggu,
            "best_cost": best_cost,
            "node_count": node_count
        }

    return hasil


def tampilkan_hasil_bnb(hasil):
    print("=" * 50)
    print("BRANCH AND BOUND - DISPATCH SELECTION")
    print("=" * 50)
    print(f"Kapasitas dispatch per siklus: k = {K}")
    print()

    for amb in AMBULANS:
        info = hasil[amb]

        print(f"{amb} - {NAMA_RS[amb]}")

        if (
            not info["dispatch"]
            and not info["menunggu"]
        ):
            print("     Tidak ada pasien.")
        else:
            print(
                f"     Dispatch sekarang : "
                f"{info['dispatch']}"
            )

            print(
                f"     Menunggu          : "
                f"{info['menunggu']}"
            )

            print(
                f"     Best Cost         : "
                f"{info['best_cost']}"
            )

            print(
                f"     Node dieksplorasi : "
                f"{info['node_count']}"
            )

        print()


if __name__ == "__main__":
    from dynamic_programming import (
        dp_resource_allocation,
        tampilkan_hasil_dp
    )

    alokasi, total_cost_dp, memo = (
        dp_resource_allocation()
    )

    tampilkan_hasil_dp(
        alokasi,
        total_cost_dp
    )

    hasil_bnb = bnb_dispatch_all(alokasi)

    tampilkan_hasil_bnb(hasil_bnb)