BLOQUES = [100, 500, 200, 300, 600]
PROCESOS = [212, 417, 112, 426]
CAPACIDAD_PARTICIONES = 800
PARTICIONES_FIJAS = [200, 200, 200, 200]
SOLICITUDES_PARTICIONES = [100, 150, 180, 120]


def asignar(bloques, procesos, algoritmo):
    """Devuelve (asignaciones, remanentes) sin modificar los datos originales.

    Cada bloque conserva su índice de origen. Next Fit busca desde el bloque
    elegido anteriormente, inclusive, y recorre circularmente la lista.
    """
    if algoritmo not in ("First Fit", "Best Fit", "Worst Fit", "Next Fit"):
        raise ValueError("Algoritmo desconocido")
    if any(type(x) is not int or x <= 0 for x in bloques + procesos):
        raise ValueError("Los tamaños deben ser enteros positivos")

    libres = bloques.copy()
    asignaciones = []
    cursor = 0
    for solicitud in procesos:
        elegido = None
        if algoritmo == "First Fit":
            elegido = next((i for i, espacio in enumerate(libres) if espacio >= solicitud), None)
        elif algoritmo == "Best Fit":
            candidatos = [i for i, espacio in enumerate(libres) if espacio >= solicitud]
            elegido = min(candidatos, key=lambda i: libres[i]) if candidatos else None
        elif algoritmo == "Worst Fit":
            candidatos = [i for i, espacio in enumerate(libres) if espacio >= solicitud]
            elegido = max(candidatos, key=lambda i: libres[i]) if candidatos else None
        else:  # Next Fit: incluye el bloque actual y da como máximo una vuelta.
            for paso in range(len(libres)):
                i = (cursor + paso) % len(libres)
                if libres[i] >= solicitud:
                    elegido = i
                    cursor = i
                    break

        if elegido is not None:
            libres[elegido] -= solicitud
        asignaciones.append(elegido)
    return asignaciones, libres


def texto_bloque(indice):
    return f"B{indice + 1}" if indice is not None else "Rechazado"


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


def comparar_algoritmos():
    print("\n=== COMPARACIÓN DE ALGORITMOS ===")
    print("Bloques B1..B5:", BLOQUES, "MB")
    print("Procesos P1..P4:", PROCESOS, "MB")
    print("Regla Next Fit: el siguiente recorrido empieza en el último bloque elegido.")
    nombres = ("First Fit", "Best Fit", "Worst Fit", "Next Fit")
    print(f"{'Algoritmo':<12} {'P1':<11}{'P2':<11}{'P3':<11}{'P4':<11}")
    resultados = {}
    for nombre in nombres:
        destinos, libres = asignar(BLOQUES, PROCESOS, nombre)
        asignados = sum(s for s, indice in zip(PROCESOS, destinos) if indice is not None)
        exitos = sum(indice is not None for indice in destinos)
        resultados[nombre] = (destinos, libres, asignados, exitos)
        celdas = [texto_bloque(i) for i in destinos]
        print(f"{nombre:<12} {celdas[0]:<11}{celdas[1]:<11}{celdas[2]:<11}{celdas[3]:<11}")

    print("\nRESUMEN (mismos datos iniciales para cada algoritmo)")
    print(f"{'Algoritmo':<12}{'Asignados':>11}{'Rechazados':>12}{'Usada':>12}{'Libre':>12}{'Atención':>12}")
    for nombre, (_, libres, usada, exitos) in resultados.items():
        print(f"{nombre:<12}{exitos:>11}{len(PROCESOS)-exitos:>12}{str(usada)+' MB':>12}{str(sum(libres))+' MB':>12}{str(exitos*100//len(PROCESOS))+' %':>12}")
    return resultados


def analizar_fragmentacion():
    print("\n=== ANÁLISIS DE FRAGMENTACIÓN ===")
    interna = sum(cap - usado for cap, usado in zip(PARTICIONES_FIJAS, SOLICITUDES_PARTICIONES))
    print(f"Interna: 800 MB reservados - 550 MB utilizados = {interna} MB")
    huecos = [100, 150, 200]
    solicitud = 300
    total = sum(huecos)
    mayor = max(huecos)
    print(f"Externa: huecos separados {huecos} MB")
    print(f"Libre total: {total} MB | Mayor hueco: {mayor} MB")
    print(f"Solicitud contigua: {solicitud} MB")
    print("Resultado: RECHAZADO por dispersión de bloques" if mayor < solicitud <= total else "Sin rechazo por dispersión")
    return interna, total, mayor
