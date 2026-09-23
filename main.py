from search_lib import BFS, DFS
from search_lib.problems.grid import GridPathfinding, GridState, MoveAction
from search_lib.core import State, Action


# Subclasse para o teste: proíbe voltar para trás no grid e evita o loop infinito do DFS
class DirectedGridPathfinding(GridPathfinding):
    def actions(self, state: State) -> list[Action]:
        if not isinstance(state, GridState):
            return []
        
        # Apenas direções sem retorno
        moves = [
            MoveAction(0, 1, "BAIXO", (self.width, self.height)),
            MoveAction(1, 0, "DIREITA", (self.width, self.height)),
        ]

        valid_actions = []
        for move in moves:
            nxt = move.apply(state)
            if nxt and nxt not in self.obstacles:
                valid_actions.append(move)

        return valid_actions


# Configuração do problema: Grid 5x5
inicio = GridState(0, 0)
objetivo = GridState(4, 4)
obstaculos = {GridState(1, 1), GridState(2, 1)}

problema = DirectedGridPathfinding(
    map_limits=(5, 5),
    goal=objetivo,
    obstacles=obstaculos
)

# EXECUÇÃO DO BFS
print("=== BUSCA EM LARGURA (BFS) ===")
solucao_bfs = BFS(problema).search(inicio)

if solucao_bfs:
    caminho_bfs = solucao_bfs.get_path()
    print(f"Sucesso BFS! Encontrado em {len(caminho_bfs)} passos:")
    for passo in caminho_bfs:
        print(f" -> {passo}")

print("\n" + "="*35 + "\n")

# EXECUÇÃO DO DFS
print("=== BUSCA EM PROFUNDIDADE (DFS) ===")
solucao_dfs = DFS(problema).search(inicio)

if solucao_dfs:
    caminho_dfs = solucao_dfs.get_path()
    print(f"Sucesso DFS! Encontrado em {len(caminho_dfs)} passos:")
    for passo in caminho_dfs:
        print(f" -> {passo}")