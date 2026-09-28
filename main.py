import sys
import os
from modelo import Automata
from conversor import afnd_a_afd
from minimizador import minimizar_afd
from io_handler import (
    cargar_automata_auto, 
    exportar_automata, 
    exportar_automata_json, 
    imprimir_tabla_terminal, 
    mostrar_ventana_grafica
)

if __name__ == "__main__":
    ruta_entrada = sys.argv[1] if len(sys.argv) > 1 else "entrada.json"
    
    if not os.path.exists(ruta_entrada):
        print(f"\n[ERROR] No se encontró el archivo de entrada '{ruta_entrada}'.")
        print("Por favor crea un archivo 'entrada.json' o pasa la ruta por parámetro: python main.py mi_archivo.json")
        sys.exit(1)
        
    print(f"\n[INFO] Cargando autómata desde archivo: {ruta_entrada}")
    nfa = cargar_automata_auto(ruta_entrada)

    dfa = afnd_a_afd(nfa)
    min_dfa = minimizar_afd(dfa)

    imprimir_tabla_terminal(nfa, f"1. Autómata Original (AFND) - [{ruta_entrada}]")
    imprimir_tabla_terminal(dfa, "2. Autómata Determinista Intermedio (AFD)")
    imprimir_tabla_terminal(min_dfa, "3. Autómata Determinista Mínimo (AFD Mínimo)")

    exportar_automata(min_dfa, "resultado_minimo.txt")
    exportar_automata_json(min_dfa, "resultado_minimo.json")
    print(f"\n[INFO] Resultado exportado a 'resultado_minimo.json' y 'resultado_minimo.txt'")

    mostrar_ventana_grafica(min_dfa, "Autómata Determinista Mínimo")
    print("\n" + "=" * 60)
    print(" RESUMEN DE MÉTRICAS ")
    print("=" * 60)
    print(f"• Estados AFND Original : {len(nfa.estados)}")
    print(f"• Estados AFD Intermedio: {len(dfa.estados)}")
    print(f"• Estados AFD Mínimo    : {len(min_dfa.estados)}")

    pruebas = ["ab", "aab", "bba", "aaab", "b", ""]
    print("\n" + "=" * 60)
    print(" VALIDACIÓN DE CADENAS Y DEMOSTRACIÓN DE EQUIVALENCIA ")
    print("=" * 60)
    print(f"{'Cadena':<12} | {'AFND Original':<15} | {'AFD Mínimo':<15} | {'Equivalentes?':<12}")
    print("-" * 62)
    
    for cad in pruebas:
        res_nfa = "ACEPTADA" if nfa.evaluar_cadena(cad) else "RECHAZADA"
        res_min = "ACEPTADA" if min_dfa.evaluar_cadena(cad) else "RECHAZADA"
        equiv = "OK" if res_nfa == res_min else "ERROR"
        cad_disp = f"'{cad}'" if cad != "" else "'' (vacía)"
        print(f"{cad_disp:<12} | {res_nfa:<15} | {res_min:<15} | {equiv:<12}")
    print("-" * 62 + "\n")