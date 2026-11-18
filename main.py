BLOQUES = [100, 500, 200, 300, 600]
PROCESOS = [212, 417, 112, 426]
CAPACIDAD_PARTICIONES = 800
PARTICIONES_FIJAS = [200, 200, 200, 200]
SOLICITUDES_PARTICIONES = [100, 150, 180, 120]


def asignar(bloques, procesos, algoritmo):
    """Devuelve (asignaciones, remanentes) sin modificar los datos originales."""
    if algoritmo not in ("First Fit", "Best Fit"):
        raise ValueError("Algoritmo desconocido")
    if any(type(x) is not int or x <= 0 for x in bloques + procesos):
        raise ValueError("Los tamaños deben ser enteros positivos")

    libres = bloques.copy()
    asignaciones = []
    for solicitud in procesos:
        elegido = None
        if algoritmo == "First Fit":
            elegido = next((i for i, espacio in enumerate(libres) if espacio >= solicitud), None)
        elif algoritmo == "Best Fit":
            candidatos = [i for i, espacio in enumerate(libres) if espacio >= solicitud]
            elegido = min(candidatos, key=lambda i: libres[i]) if candidatos else None
        if elegido is not None:
            libres[elegido] -= solicitud
        asignaciones.append(elegido)
    return asignaciones, libres


def particionamiento_fijo():
    print("\n=== PARTICIONAMIENTO FIJO ===")
    print("Memoria: 800 MB | 4 particiones de 200 MB")
    print(f"{'Proceso':<10}{'Partición':<12}{'Solicitado':>12}{'Interna':>12}")
    desperdicio = 0
    for i, (capacidad, solicitud) in enumerate(zip(PARTICIONES_FIJAS, SOLICITUDES_PARTICIONES), 1):
        interna = capacidad - solicitud
        desperdicio += interna
        print(f"P{i:<9}P{i:<11}{solicitud:>9} MB{interna:>9} MB")
    print(f"Memoria total: {CAPACIDAD_PARTICIONES} MB")
    print(f"Memoria utilizada por procesos: {sum(SOLICITUDES_PARTICIONES)} MB")
    print(f"Fragmentación interna total: {desperdicio} MB")
    return desperdicio


def particionamiento_variable():
    print("\n=== PARTICIONAMIENTO VARIABLE ===")
    print(f"Memoria inicial: {CAPACIDAD_PARTICIONES} MB")
    disponible = CAPACIDAD_PARTICIONES
    for i, solicitud in enumerate(SOLICITUDES_PARTICIONES, 1):
        if solicitud <= disponible:
            disponible -= solicitud
            print(f"P{i}: asignados {solicitud} MB | libre: {disponible} MB")
        else:
            print(f"P{i}: rechazado")
    print(f"Memoria utilizada: {CAPACIDAD_PARTICIONES - disponible} MB")
    print(f"Memoria libre: {disponible} MB")
    return disponible
