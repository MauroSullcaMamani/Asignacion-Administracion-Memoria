
BLOQUES = [100, 500, 200, 300, 600]
PROCESOS = [212, 417, 112, 426]
CAPACIDAD_PARTICIONES = 800
PARTICIONES_FIJAS = [200, 200, 200, 200]
SOLICITUDES_PARTICIONES = [100, 150, 180, 120]


def particionamiento_fijo():
    print("\n=== PARTICIONAMIENTO FIJO ===")
    print("Memoria: 800 MB | 4 particiones de 200 MB")
    print(f"{'Proceso':<10}{'Partición':<12}{'Solicitado':>12}{'Interna':>12}")

    desperdicio = 0

    for i, (capacidad, solicitud) in enumerate(
        zip(PARTICIONES_FIJAS, SOLICITUDES_PARTICIONES), 1
    ):
        interna = capacidad - solicitud
        desperdicio += interna
        print(f"P{i:<9}P{i:<11}{solicitud:>9} MB{interna:>9} MB")

    print(f"Memoria total: {CAPACIDAD_PARTICIONES} MB")
    print(f"Memoria utilizada por procesos: {sum(SOLICITUDES_PARTICIONES)} MB")
    print(f"Fragmentación interna total: {desperdicio} MB")

    return desperdicio
