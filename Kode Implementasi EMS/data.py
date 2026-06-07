AMBULANS = ["A1", "A2", "A3", "A4", "A5"]

NAMA_RS = {
    "A1": "RSUP Dr. Kariadi",
    "A2": "RS Nasional Diponegoro",
    "A3": "RS St. Elisabeth",
    "A4": "RSUD KRMT Wongsonegoro",
    "A5": "PMI Kota Semarang"
}

PASIEN = [
    "P1", "P2", "P3", "P4", "P5",
    "P6", "P7", "P8", "P9", "P10"
]

PRIORITAS = {
    "P1": 3,
    "P2": 2,
    "P3": 5,
    "P4": 1,
    "P5": 4,
    "P6": 2,
    "P7": 5,
    "P8": 3,
    "P9": 1,
    "P10": 4
}

JARAK = {
    "A1": [3.2, 7.5, 1.8, 9.1, 5.4, 6.3, 4.7, 8.2, 2.9, 6.1],
    "A2": [8.4, 2.1, 6.5, 3.8, 7.2, 4.9, 9.3, 1.6, 7.8, 3.4],
    "A3": [5.7, 4.3, 8.9, 2.6, 3.1, 7.8, 2.4, 6.5, 4.2, 8.7],
    "A4": [6.1, 9.2, 3.4, 7.5, 2.8, 1.9, 6.8, 4.3, 8.6, 2.1],
    "A5": [4.8, 6.7, 5.2, 4.1, 8.3, 3.6, 3.9, 7.1, 1.4, 5.8]
}

KOORDINAT = {
    "P1": (0.0, 0.0),
    "P2": (3.5, 2.1),
    "P3": (1.2, 4.8),
    "P4": (6.1, 1.3),
    "P5": (2.8, 6.4),
    "P6": (5.3, 4.7),
    "P7": (0.9, 2.6),
    "P8": (4.4, 0.8),
    "P9": (3.1, 5.9),
    "P10": (1.7, 3.3)
}


def hitung_cost(ambulans, pasien):
    idx = PASIEN.index(pasien)

    jarak = JARAK[ambulans][idx]
    prioritas = PRIORITAS[pasien]

    return jarak - prioritas


def tampilkan_data():
    print("=== DATA EMS KOTA SEMARANG ===")
    print()

    print("Ambulans:")
    for amb in AMBULANS:
        print(f"  {amb} - {NAMA_RS[amb]}")

    print()

    print("Pasien:")
    for pas in PASIEN:
        print(f"  {pas} | Prioritas: {PRIORITAS[pas]}")

    print()

    print("Contoh cost (A1):")

    for pas in PASIEN:
        idx = PASIEN.index(pas)

        print(
            f"  A1 -> {pas}: "
            f"jarak={JARAK['A1'][idx]} km, "
            f"prioritas={PRIORITAS[pas]}, "
            f"cost={hitung_cost('A1', pas):.1f}"
        )


if __name__ == "__main__":
    tampilkan_data()