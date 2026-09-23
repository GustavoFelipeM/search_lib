
from typing import Optional

from search_lib.core import SearchNode, SearchStrategy, State


class DFS(SearchStrategy):
    """Busca em Profundidade (Depth-First Search). Nota: Pode entrar em loop se o grafo tiver ciclos."""

    def search(self, initial_state: State) -> Optional[SearchNode]:
        root = SearchNode(initial_state)
        frontier = [root]  # Pilha LIFO

        while frontier:
            node = frontier.pop()

            if self.problem.is_goal(node.state):
                return node

            for action in self.problem.actions(node.state):
                next_state = action.apply(node.state)
                if next_state is not None:
                    child = SearchNode(
                        state=next_state,
                        parent=node,
                        action=action,
                        cost=node.cost + 1.0
                    )
                    frontier.append(child)

        return None