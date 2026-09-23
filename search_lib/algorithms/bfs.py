
from collections import deque
from typing import Optional

from search_lib.core import SearchNode, SearchStrategy, State


class BFS(SearchStrategy):
    """Busca em Largura (Breadth-First Search)."""

    def search(self, initial_state: State) -> Optional[SearchNode]:
        root = SearchNode(initial_state)
        frontier = deque([root])

        while frontier:
            node = frontier.popleft()

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
