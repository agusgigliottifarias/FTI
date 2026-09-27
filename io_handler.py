import json
import uuid
from modelo import Automata

def cargar_automata_json(ruta: str) -> Automata:
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    id_a_label = {}
    inicial = ""
    finales = set()
    estados = set()
    
    if "states" in data:
        for s in data["states"]:
            sid = s["id"]
            lbl = s.get("label", sid)
            id_a_label[sid] = lbl
            estados.add(lbl)
            if s.get("isStart", False):
                inicial = lbl
            if s.get("isAccept", False):
                finales.add(lbl)
        
        alfabeto = set(data.get("alphabet", []))
        aut = Automata(alfabeto, estados, inicial, finales)
        
        for t in data.get("transitions", []):
            orig = id_a_label.get(t["from"], t["from"])
            dest = id_a_label.get(t["to"], t["to"])
            is_eps = t.get("isEpsilon", False)
            symb = "#" if is_eps or t.get("symbol", "") == "" else t["symbol"]
            if symb != "#":
                aut.alfabeto.add(symb)
            aut.agregar_transicion(orig, symb, dest)
        return aut
    else:
        alfabeto = set(data.get("alfabeto", []))
        estados = set(data.get("estados", []))
        inicial = data.get("inicial", "")
        finales = set(data.get("finales", []))
        aut = Automata(alfabeto, estados, inicial, finales)
        for t in data.get("transiciones", []):
            orig = t.get("origen") or t.get("from")
            dest = t.get("destino") or t.get("to")
            symb = t.get("simbolo") if "simbolo" in t else t.get("symbol", "")
            if t.get("isEpsilon") or symb == "":
                symb = "#"
            aut.agregar_transicion(orig, symb, dest)
        return aut

def exportar_automata_json(automata: Automata, ruta: str, nombre: str = "Automata Minimo"):
    state_list = []
    id_map = {}
    
    for i, e in enumerate(sorted(automata.estados)):
        sid = str(uuid.uuid4())
        id_map[e] = sid
        state_list.append({
            "id": sid,
            "label": e,
            "x": 100.0 + (i % 5) * 150.0,
            "y": 100.0 + (i // 5) * 150.0,
            "isStart": (e == automata.inicial),
            "isAccept": (e in automata.finales)
        })
        
    trans_list = []
    for (orig, s), dests in sorted(automata.transiciones.items()):
        for d in dests:
            is_eps = (s == "#" or s == "")
            trans_list.append({
                "id": str(uuid.uuid4()),
                "from": id_map[orig],
                "to": id_map[d],
                "symbol": "" if is_eps else s,
                "isEpsilon": is_eps
            })
            
    out_data = {
        "name": nombre,
        "type": "DFA",
        "alphabet": sorted(list(automata.alfabeto)),
        "states": state_list,
        "transitions": trans_list,
        "alfabeto": sorted(list(automata.alfabeto)),
        "estados": sorted(list(automata.estados)),
        "inicial": automata.inicial,
        "finales": sorted(list(automata.finales)),
        "transiciones": [
            {
                "origen": orig,
                "simbolo": s,
                "destino": d
            }
            for (orig, s), dests in sorted(automata.transiciones.items())
            for d in dests
        ]
    }
    
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(out_data, f, indent=2, ensure_ascii=False)

def cargar_automata_auto(ruta: str) -> Automata:
    if ruta.endswith(".json"):
        return cargar_automata_json(ruta)
    return cargar_automata_texto(ruta)

def cargar_automata_texto(ruta: str) -> Automata:
    with open(ruta, "r", encoding="utf-8") as f:
        lineas = [l.strip() for l in f if l.strip()]

    alfabeto, estados, inicial, finales = set(), set(), "", set()
    transiciones = []
    seccion_trans = False

    for linea in lineas:
        if linea.startswith("ALFABETO:"):
            alfabeto = {s.strip() for s in linea.split(":")[1].split(",")}
        elif linea.startswith("ESTADOS:"):
            estados = {e.strip() for e in linea.split(":")[1].split(",")}
        elif linea.startswith("INICIAL:"):
            inicial = linea.split(":")[1].strip()
        elif linea.startswith("FINALES:"):
            finales = {e.strip() for e in linea.split(":")[1].split(",")}
        elif linea.startswith("TRANSICIONES:"):
            seccion_trans = True
        elif seccion_trans and "->" in linea:
            orig_simb, dest = linea.split("->")
            orig, simb = orig_simb.split(",")
            transiciones.append((orig.strip(), simb.strip(), dest.strip()))

    aut = Automata(alfabeto, estados, inicial, finales)
    for o, s, d in transiciones:
        aut.agregar_transicion(o, s, d)
    return aut

def exportar_automata(automata: Automata, ruta: str):
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"ALFABETO:{','.join(sorted(automata.alfabeto))}\n")
        f.write(f"ESTADOS:{','.join(sorted(automata.estados))}\n")
        f.write(f"INICIAL:{automata.inicial}\n")
        f.write(f"FINALES:{','.join(sorted(automata.finales))}\n")
        f.write("TRANSICIONES:\n")
        for (orig, s), dests in sorted(automata.transiciones.items()):
            for d in dests:
                f.write(f"{orig},{s}->{d}\n")

def imprimir_tabla_terminal(automata: Automata, titulo: str = "AUTÓMATA"):
    alfabeto_ordenado = sorted(automata.alfabeto)
    estados_ordenados = sorted(automata.estados)
    
    print("\n" + "=" * 60)
    print(f" {titulo.upper()} ")
    print("=" * 60)
    print(f"Alfabeto : {{{', '.join(alfabeto_ordenado)}}}")
    print(f"Estados  : {{{', '.join(estados_ordenados)}}}")
    print(f"Inicial  : {automata.inicial}")
    print(f"Finales  : {{{', '.join(sorted(automata.finales))}}}")
    print("\nTabla de Transiciones:")
    
    # Encabezado
    col_estado_w = 12
    col_w = max(10, max(len(s) for s in alfabeto_ordenado) + 4)
    
    header = f"| {'Estado':<{col_estado_w}} | " + " | ".join(f"{s:^{col_w}}" for s in alfabeto_ordenado) + " |"
    separador = "+" + "-" * (col_estado_w + 2) + "+" + "+".join("-" * (col_w + 2) for _ in alfabeto_ordenado) + "+"
    
    print(separador)
    print(header)
    print(separador)
    
    for e in estados_ordenados:
        prefix = ""
        if e == automata.inicial and e in automata.finales:
            prefix = "->*"
        elif e == automata.inicial:
            prefix = "->"
        elif e in automata.finales:
            prefix = "*"
            
        estado_label = f"{prefix} {e}".strip()
        fila = [f"| {estado_label:<{col_estado_w}} |"]
        
        for s in alfabeto_ordenado:
            dests = automata.transiciones.get((e, s), set())
            if not dests:
                celda = "--"
            elif len(dests) == 1:
                celda = list(dests)[0]
            else:
                celda = "{" + ", ".join(sorted(dests)) + "}"
            fila.append(f" {celda:^{col_w}} |")
            
        print("".join(fila))
    print(separador)

def exportar_grafico_dot(automata: Automata, ruta_salida: str, titulo: str = "Automata"):
    try:
        import graphviz
        dot = graphviz.Digraph(comment=titulo, format="png")
        dot.attr(rankdir="LR")
        
        # Nodo inicial invisible
        dot.node("", shape="none", height="0", width="0")
        
        for e in sorted(automata.estados):
            shape = "doublecircle" if e in automata.finales else "circle"
            dot.node(e, shape=shape)
            
        dot.edge("", automata.inicial)
        
        trans_agrupadas = {}
        for (orig, s), dests in automata.transiciones.items():
            for d in dests:
                trans_agrupadas.setdefault((orig, d), []).append(s)
                
        for (orig, d), simbolos in sorted(trans_agrupadas.items()):
            dot.edge(orig, d, label=", ".join(sorted(simbolos)))
            
        dot.save(ruta_salida)
        try:
            dot.render(filename=ruta_salida, cleanup=False)
            print(f"[Graphviz] Diagrama guardado y renderizado: {ruta_salida}.png / {ruta_salida}")
        except Exception:
            print(f"[Graphviz] Archivo DOT guardado en: {ruta_salida}")
    except ImportError:
        print("[Graphviz] No se pudo cargar el paquete 'graphviz'.")

def mostrar_ventana_grafica(automata: Automata, titulo: str = "Automata"):
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
        
        G = nx.DiGraph()
        for e in automata.estados:
            G.add_node(e)
            
        edge_labels = {}
        for (orig, s), dests in automata.transiciones.items():
            for d in dests:
                G.add_edge(orig, d)
                edge_labels.setdefault((orig, d), []).append(s)
                
        edge_labels_str = {k: ", ".join(sorted(v)) for k, v in edge_labels.items()}
        
        pos = nx.spring_layout(G, k=1.5, seed=42)
        plt.figure(figsize=(10, 7))
        plt.title(f"{titulo} (Inicial: {automata.inicial})", fontsize=14, fontweight="bold")
        
        node_colors = []
        for n in G.nodes():
            if n in automata.finales:
                node_colors.append("#90ee90")  # verde claro
            elif n == automata.inicial:
                node_colors.append("#add8e6")  # azul claro
            else:
                node_colors.append("#f5f5f5")  # gris claro
                
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1500, edgecolors="black", linewidths=2)
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
        nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20, edge_color="gray", connectionstyle="arc3,rad=0.1")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_str, font_size=9, font_color="red")
        
        plt.tight_layout()
        print(f"[Visualizador] Mostrando ventana emergente para: {titulo}")
        plt.show()
    except ImportError:
        pass