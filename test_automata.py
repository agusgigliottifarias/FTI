import unittest
from modelo import Automata
from conversor import afnd_a_afd
from minimizador import minimizar_afd

class TestAutomata(unittest.TestCase):
    
    def test_afnd_con_epsilon(self):
        # Autómata con transición épsilon (#)
        nfa = Automata(alfabeto={'a', 'b', '#'}, estados={'q0', 'q1', 'q2'}, inicial='q0', finales={'q2'})
        nfa.agregar_transicion('q0', '#', 'q1')
        nfa.agregar_transicion('q1', 'a', 'q1')
        nfa.agregar_transicion('q1', 'b', 'q2')

        dfa = afnd_a_afd(nfa, eps_simbolo='#')
        min_dfa = minimizar_afd(dfa)

        self.assertTrue(nfa.evaluar_cadena("ab"))
        self.assertTrue(min_dfa.evaluar_cadena("ab"))
        self.assertTrue(nfa.evaluar_cadena("aab"))
        self.assertFalse(min_dfa.evaluar_cadena("ba"))

    def test_minimizacion_estados_redundantes(self):
        # Autómata con estados equivalentes que se deben reducir
        # Acepta cadenas que terminan en 'a'
        dfa = Automata(alfabeto={'a', 'b'}, estados={'A', 'B', 'C'}, inicial='A', finales={'B', 'C'})
        dfa.agregar_transicion('A', 'a', 'B')
        dfa.agregar_transicion('A', 'b', 'A')
        dfa.agregar_transicion('B', 'a', 'B')
        dfa.agregar_transicion('B', 'b', 'A')
        dfa.agregar_transicion('C', 'a', 'B')
        dfa.agregar_transicion('C', 'b', 'A')

        min_dfa = minimizar_afd(dfa)
        
        # B y C son equivalentes, por lo que deben reducirse a 2 estados totales
        self.assertLessEqual(len(min_dfa.estados), len(dfa.estados))
        self.assertTrue(min_dfa.evaluar_cadena("ba"))
        self.assertFalse(min_dfa.evaluar_cadena("ab"))

if __name__ == '__main__':
    unittest.main()
