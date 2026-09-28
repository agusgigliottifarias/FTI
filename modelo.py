from typing import Set, Dict, Tuple, FrozenSet

class Automata:
    def __init__(self, alfabeto: Set[str], estados: Set[str], inicial: str, finales: Set[str]):
        self.alfabeto = set(alfabeto)
        self.estados = set(estados)
        self.inicial = inicial
        self.finales = set(finales)
        self.transiciones: Dict[Tuple[str, str], Set[str]] = {}

    def agregar_transicion(self, origen: str, simbolo: str, destino: str):
        clave = (origen, simbolo)
        if clave not in self.transiciones:
            self.transiciones[clave] = set()
        self.transiciones[clave].add(destino)

    def clausura_lambda(self, estados: Set[str], lambda_simbolo: str = '#') -> FrozenSet[str]:
        pila = list(estados)
        clausura = set(estados)
        while pila:
            actual = pila.pop()
            alcanzables = self.transiciones.get((actual, lambda_simbolo), set())
            for sig in alcanzables:
                if sig not in clausura:
                    clausura.add(sig)
                    pila.append(sig)
        return frozenset(clausura)

    def mover(self, estados: FrozenSet[str], simbolo: str) -> Set[str]:
        destinos = set()
        for e in estados:
            destinos.update(self.transiciones.get((e, simbolo), set()))
        return destinos

    def evaluar_cadena(self, cadena: str, lambda_simbolo: str = '#') -> bool:
        actuales = self.clausura_lambda({self.inicial}, lambda_simbolo)
        for char in cadena:
            if char not in self.alfabeto:
                return False
            alcanzados = self.mover(actuales, char)
            if not alcanzados:
                return False
            actuales = self.clausura_lambda(alcanzados, lambda_simbolo)
        return any(e in self.finales for e in actuales)

    def eliminar_inalcanzables(self, lambda_simbolo: str = '#'):
        from collections import deque
        alcanzables = set(self.clausura_lambda({self.inicial}, lambda_simbolo))
        cola = deque(alcanzables)
        
        while cola:
            act = cola.popleft()
            for s in self.alfabeto:
                if s == lambda_simbolo:
                    continue
                dests = self.mover(frozenset([act]), s)
                claus = self.clausura_lambda(dests, lambda_simbolo)
                for e in claus:
                    if e not in alcanzables:
                        alcanzables.add(e)
                        cola.append(e)
                        
        self.estados = alcanzables
        self.finales = self.finales & alcanzables
        self.transiciones = {
            (orig, s): {d for d in dests if d in alcanzables}
            for (orig, s), dests in self.transiciones.items()
            if orig in alcanzables
        }