from collections import deque
from typing import Dict, Tuple, FrozenSet
from modelo import Automata

def afnd_a_afd(afnd: Automata, eps_simbolo: str = '#') -> Automata:
    alfabeto_limpio = {s for s in afnd.alfabeto if s != eps_simbolo}
    inicio_clausura = afnd.clausura_epsilon({afnd.inicial}, eps_simbolo)
    mapeo_estados: Dict[FrozenSet[str], str] = {inicio_clausura: "S0"}
    cola = deque([inicio_clausura])
    
    afd_trans: Dict[Tuple[str, str], str] = {}
    contador = 1

    while cola:
        actual_set = cola.popleft()
        nombre_actual = mapeo_estados[actual_set]

        for s in sorted(alfabeto_limpio):
            mov = afnd.mover(actual_set, s)
            if not mov:
                continue
            destino_set = afnd.clausura_epsilon(mov, eps_simbolo)

            if destino_set not in mapeo_estados:
                mapeo_estados[destino_set] = f"S{contador}"
                contador += 1
                cola.append(destino_set)

            nombre_dest = mapeo_estados[destino_set]
            afd_trans[(nombre_actual, s)] = nombre_dest

    estados_afd = set(mapeo_estados.values())
    finales_afd = {
        nombre for conjunto, nombre in mapeo_estados.items()
        if any(e in afnd.finales for e in conjunto)
    }

    afd = Automata(alfabeto_limpio, estados_afd, "S0", finales_afd)
    for (orig, s), dest in afd_trans.items():
        afd.agregar_transicion(orig, s, dest)

    return afd