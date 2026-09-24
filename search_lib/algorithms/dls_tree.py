import time
from typing import Optional

from search_lib.core import (
    SearchNode, 
    SearchStrategy, 
    State, 
    SearchMetrics, 
    SearchResult,
    SearchCallbacks,
    Problem
)


class DLS(SearchStrategy):
    """Busca em Profundidade Limitada em Árvore (Tree-DLS)."""

    def __init__(self, problem: Problem, depth_limit: int):
        super().__init__(problem)
        self.depth_limit = depth_limit

    def search(
        self, 
        initial_state: State, 
        callbacks: Optional[SearchCallbacks] = None
    ) -> SearchResult:
        if callbacks and callbacks.on_start:
            callbacks.on_start()

        start_time = time.perf_counter()
        metrics = SearchMetrics()

        root = SearchNode(initial_state)
        metrics.nodes_generated += 1

        frontier = [root]
        metrics.max_frontier_size = max(metrics.max_frontier_size, len(frontier))

        while frontier:
            node = frontier.pop()
            metrics.nodes_expanded += 1

            if callbacks and callbacks.on_node_expanded:
                callbacks.on_node_expanded(node, frontier)

            if self.problem.is_goal(node.state):
                metrics.execution_time = time.perf_counter() - start_time
                res = SearchResult(solution_node=node, metrics=metrics)
                if callbacks and callbacks.on_finish:
                    callbacks.on_finish(res)
                return res

            # Corta a expansão caso o limite de profundidade seja atingido
            if node.depth < self.depth_limit:
                for action in self.problem.actions(node.state):
                    res_action = action.apply(node.state)
                    if callbacks and callbacks.on_action_applied:
                        callbacks.on_action_applied(node, action, res_action)

                    if res_action is not None:
                        next_state, action_cost = res_action
                        child = SearchNode(
                            state=next_state,
                            parent=node,
                            action=action,
                            cost=node.cost + action_cost
                        )
                        metrics.nodes_generated += 1
                        frontier.append(child)
                        metrics.max_frontier_size = max(
                            metrics.max_frontier_size, len(frontier)
                        )

                        if callbacks and callbacks.on_node_generated:
                            callbacks.on_node_generated(child, frontier)

        metrics.execution_time = time.perf_counter() - start_time
        res = SearchResult(solution_node=None, metrics=metrics)
        if callbacks and callbacks.on_finish:
            callbacks.on_finish(res)
        return res