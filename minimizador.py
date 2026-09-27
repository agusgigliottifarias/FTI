from collections import deque
from typing import Dict, Tuple, Set
from modelo import Automata

def minimizar_afd(afd: Automata) -> Automata:
    afd.eliminar_inalcanzables()

    estados_validos = afd.estados
    finales_validos = afd.finales
    no_finales_validos = estados_validos - finales_validos

    particiones = []
    if finales_validos:
        particiones.append(frozenset(finales_validos))
    if no_finales_validos:
        particiones.append(frozenset(no_finales_validos))

    cambio = True
    while cambio:
        nueva_particion = []
        cambio = False

        for grupo in particiones:
            subgrupos: Dict[Tuple, Set[str]] = {}
            for estado in grupo:
                firma = []
                for s in sorted(afd.alfabeto):
                    dest = list(afd.transiciones.get((estado, s), set()))
                    if not dest:
                        firma.append(None)
                    else:
                        d = dest[0]
                        idx_grupo = next((i for i, g in enumerate(particiones) if d in g), None)
                        firma.append(idx_grupo)
                subgrupos.setdefault(tuple(firma), set()).add(estado)

            if len(subgrupos) > 1:
                cambio = True
            for sg in subgrupos.values():
                nueva_particion.append(frozenset(sg))

        particiones = nueva_particion

    mapeo_min: Dict[str, str] = {}
    for i, grupo in enumerate(particiones):
        nombre = f"M{i}"
        for e in grupo:
            mapeo_min[e] = nombre

    inicial_min = mapeo_min[afd.inicial]
    estados_min = set(mapeo_min.values())
    finales_min = {mapeo_min[e] for e in finales_validos}

    min_dfa = Automata(afd.alfabeto, estados_min, inicial_min, finales_min)
    for (orig, s), dests in afd.transiciones.items():
        if orig in estados_validos and dests:
            d = list(dests)[0]
            if d in estados_validos:
                min_dfa.agregar_transicion(mapeo_min[orig], s, mapeo_min[d])

    return min_dfa