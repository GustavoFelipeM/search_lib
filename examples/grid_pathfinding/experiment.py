import os
import sys
import random
import csv
import time
from collections import deque

DIR_ATUAL = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROJETO = os.path.abspath(os.path.join(DIR_ATUAL, "../.."))

if DIR_ATUAL not in sys.path:
    sys.path.insert(0, DIR_ATUAL)
if RAIZ_PROJETO not in sys.path:
    sys.path.insert(0, RAIZ_PROJETO)

from search_lib.core import SearchNode, SearchMetrics, SearchResult
from problem import GridPathfinding, GridState


def bfs_graph_search(problem, initial_state):
    """BFS com lista de visitados - O(N^2)"""
    start_time = time.perf_counter()
    metrics = SearchMetrics()

    root = SearchNode(initial_state)
    metrics.nodes_generated += 1

    frontier = deque([root])
    explored = {initial_state}

    while frontier:
        node = frontier.popleft()
        metrics.nodes_expanded += 1

        if problem.is_goal(node.state):
            metrics.execution_time = time.perf_counter() - start_time
            return SearchResult(solution_node=node, metrics=metrics)

        for action in problem.actions(node.state):
            res_action = action.apply(node.state)
            if res_action is not None:
                next_state, action_cost = res_action
                if next_state not in explored:
                    explored.add(next_state)
                    child = SearchNode(
                        state=next_state,
                        parent=node,
                        action=action,
                        cost=node.cost + action_cost
                    )
                    metrics.nodes_generated += 1
                    frontier.append(child)

    metrics.execution_time = time.perf_counter() - start_time
    return SearchResult(solution_node=None, metrics=metrics)


def dls_graph_search(problem, initial_state, depth_limit):
    """DLS com lista de visitados - O(N^2)"""
    start_time = time.perf_counter()
    metrics = SearchMetrics()

    root = SearchNode(initial_state)
    metrics.nodes_generated += 1

    frontier = [root]
    explored = {initial_state: 0}

    while frontier:
        node = frontier.pop()
        metrics.nodes_expanded += 1

        if problem.is_goal(node.state):
            metrics.execution_time = time.perf_counter() - start_time
            return SearchResult(solution_node=node, metrics=metrics)

        if node.depth < depth_limit:
            for action in problem.actions(node.state):
                res_action = action.apply(node.state)
                if res_action is not None:
                    next_state, action_cost = res_action
                    next_depth = node.depth + 1
                    
                    if next_state not in explored or next_depth < explored[next_state]:
                        explored[next_state] = next_depth
                        child = SearchNode(
                            state=next_state,
                            parent=node,
                            action=action,
                            cost=node.cost + action_cost
                        )
                        metrics.nodes_generated += 1
                        frontier.append(child)

    metrics.execution_time = time.perf_counter() - start_time
    return SearchResult(solution_node=None, metrics=metrics)


def gerar_grafico_svg(tamanhos, bfs_data, dls_data, titulo, y_label, file_name):
    """Gera gráfico vetorial SVG puro sem bibliotecas externas"""
    width, height = 650, 380
    pad_left, pad_bottom, pad_top, pad_right = 80, 50, 40, 30
    
    max_val = max(max(bfs_data), max(dls_data)) if max(max(bfs_data), max(dls_data)) > 0 else 1
    num_points = len(tamanhos)
    
    def get_x(i):
        return pad_left + i * (width - pad_left - pad_right) / (num_points - 1)
    
    def get_y(val):
        return height - pad_bottom - (val / max_val) * (height - pad_top - pad_bottom)
    
    pts_bfs = " ".join([f"{get_x(i):.1f},{get_y(v):.1f}" for i, v in enumerate(bfs_data)])
    pts_dls = " ".join([f"{get_x(i):.1f},{get_y(v):.1f}" for i, v in enumerate(dls_data)])
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" style="background:#ffffff; font-family:Segoe UI, sans-serif;">
    <rect width="100%" height="100%" fill="#ffffff"/>
    <text x="{width/2}" y="25" text-anchor="middle" font-size="15" font-weight="bold" fill="#333333">{titulo}</text>
    
    <!-- Linhas de Grade Verticais -->
    '''
    for i, t in enumerate(tamanhos):
        x = get_x(i)
        svg += f'<line x1="{x}" y1="{pad_top}" x2="{x}" y2="{height - pad_bottom}" stroke="#eeeeee" stroke-width="1"/>'
        svg += f'<text x="{x}" y="{height - pad_bottom + 20}" text-anchor="middle" font-size="11" fill="#444444">{t}</text>'

    svg += f'''
    <!-- Eixos -->
    <line x1="{pad_left}" y1="{height - pad_bottom}" x2="{width - pad_right}" y2="{height - pad_bottom}" stroke="#888888" stroke-width="2"/>
    <line x1="{pad_left}" y1="{pad_top}" x2="{pad_left}" y2="{height - pad_bottom}" stroke="#888888" stroke-width="2"/>
    
    <text x="{width/2}" y="{height - 10}" text-anchor="middle" font-size="12" fill="#555555">Dimensão da Grelha (N x N)</text>
    <text x="25" y="{height/2}" text-anchor="middle" font-size="12" fill="#555555" transform="rotate(-90 25,{height/2})">{y_label}</text>
    
    <!-- Linhas dos Dados -->
    <polyline points="{pts_bfs}" fill="none" stroke="#1f77b4" stroke-width="3"/>
    <polyline points="{pts_dls}" fill="none" stroke="#d62728" stroke-width="3"/>
    '''
    
    # Marcadores e Valores
    for i in range(num_points):
        xb, yb = get_x(i), get_y(bfs_data[i])
        xd, yd = get_x(i), get_y(dls_data[i])
        
        svg += f'<circle cx="{xb:.1f}" cy="{yb:.1f}" r="4" fill="#1f77b4"/>'
        svg += f'<circle cx="{xd:.1f}" cy="{yd:.1f}" r="4" fill="#d62728"/>'
        svg += f'<text x="{xb:.1f}" y="{yb - 8:.1f}" text-anchor="middle" font-size="9" fill="#1f77b4">{bfs_data[i]}</text>'
        svg += f'<text x="{xd:.1f}" y="{yd - 8:.1f}" text-anchor="middle" font-size="9" fill="#d62728">{dls_data[i]}</text>'

    # Legenda
    svg += f'''
    <rect x="{width - 170}" y="{pad_top}" width="14" height="12" fill="#1f77b4"/>
    <text x="{width - 150}" y="{pad_top + 10}" font-size="11" fill="#333333">BFS (Largura)</text>
    <rect x="{width - 170}" y="{pad_top + 20}" width="14" height="12" fill="#d62728"/>
    <text x="{width - 150}" y="{pad_top + 30}" font-size="11" fill="#333333">DLS (Profundidade)</text>
</svg>'''

    output_path = os.path.join(DIR_ATUAL, file_name)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    return output_path


def run_experiments():
    sizes = [10, 20, 30, 40, 50]
    results = []
    
    tamanhos_str = []
    bfs_nodes, dls_nodes = [], []
    bfs_times, dls_times = [], []

    print("=== EXPERIMENTO COM BUSCA EM GRAFO (SEM TRAVAMENTOS) ===\n")
    print(f"{'Grelha':<8} | {'Algo':<5} | {'Status':<12} | {'Nós Expandidos':<15} | {'Tempo (ms)':<10}")
    print("-" * 62)

    for N in sizes:
        depth_limit = N * N
        
        blocked_zones = {
            (0, 0), (0, 1), (1, 0),
            (N - 1, N - 1), (N - 2, N - 1), (N - 1, N - 2)
        }
        
        obstacles = set()
        random.seed(42)
        num_obstacles = int(N * N * 0.15)
        
        while len(obstacles) < num_obstacles:
            ox, oy = random.randint(0, N - 1), random.randint(0, N - 1)
            if (ox, oy) not in blocked_zones:
                obstacles.add(GridState(ox, oy))

        problema = GridPathfinding(
            map_limits=(N, N),
            initial_state=GridState(0, 0),
            goal=GridState(N - 1, N - 1),
            obstacles=obstacles
        )

        # BFS
        res_bfs = bfs_graph_search(problema, problema.initial_state)
        status_bfs = "Sucesso" if res_bfs.solution_node else "Sem Solução"
        b_nodes = res_bfs.metrics.nodes_expanded
        b_time = round(res_bfs.metrics.execution_time * 1000, 2)
        print(f"{f'{N}x{N}':<8} | {'BFS':<5} | {status_bfs:<12} | {b_nodes:<15} | {b_time:.2f} ms")

        # DLS
        res_dls = dls_graph_search(problema, problema.initial_state, depth_limit=depth_limit)
        status_dls = "Sucesso" if res_dls.solution_node else "Sem Solução"
        d_nodes = res_dls.metrics.nodes_expanded
        d_time = round(res_dls.metrics.execution_time * 1000, 2)
        print(f"{f'{N}x{N}':<8} | {'DLS':<5} | {status_dls:<12} | {d_nodes:<15} | {d_time:.2f} ms")
        print("-" * 62)

        tamanhos_str.append(f"{N}x{N}")
        bfs_nodes.append(b_nodes)
        dls_nodes.append(d_nodes)
        bfs_times.append(b_time)
        dls_times.append(d_time)

        results.append({"Tamanho": f"{N}x{N}", "Algoritmo": "BFS", "Status": status_bfs, "Nos_Expandidos": b_nodes, "Tempo_ms": b_time})
        results.append({"Tamanho": f"{N}x{N}", "Algoritmo": "DLS", "Status": status_dls, "Nos_Expandidos": d_nodes, "Tempo_ms": d_time})

    # 1. Salvar CSV
    csv_path = os.path.join(DIR_ATUAL, "resultados_experimento.csv")
    with open(csv_path, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Tamanho", "Algoritmo", "Status", "Nos_Expandidos", "Tempo_ms"])
        writer.writeheader()
        writer.writerows(results)

    # 2. Gerar Gráficos SVG (Zero dependências externas)
    path_nodes = gerar_grafico_svg(tamanhos_str, bfs_nodes, dls_nodes, "Nós Expandidos por Tamanho de Grelha", "Quantidade de Nós", "grafico_nos.svg")
    path_times = gerar_grafico_svg(tamanhos_str, bfs_times, dls_times, "Tempo de Execução (ms)", "Tempo (ms)", "grafico_tempo.svg")

    print(f"\n[OK] CSV salvo em: {csv_path}")
    print(f"[OK] Gráfico de Nós salvo em: {path_nodes}")
    print(f"[OK] Gráfico de Tempo salvo em: {path_times}")


if __name__ == "__main__":
    run_experiments()