from abc import ABC, abstractmethod
from typing import Optional
from collections import deque
from dataclasses import dataclass
import random


class State(ABC):
    """Classe abstrata para representar o estado. Deve ser imutável/hashável nas subclasses."""
    pass


class Action(ABC):
    """Classe abstrata para representação de ações."""
    
    @abstractmethod
    def apply(self, state: State) -> Optional[State]:
        """Aplica a ação no estado. Retorna o novo estado ou None se a ação for inválida."""
        pass


class SearchNode:
    """Nó interno da árvore de busca. Controla pai, ação geradora e custo acumulado."""
    
    def __init__(
        self, 
        state: State, 
        parent: Optional['SearchNode'] = None, 
        action: Optional[Action] = None, 
        cost: float = 0.0
    ):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def get_path(self) -> list[Action]:
        """Reconstrói a lista de ações da raiz até este nó."""
        path = []
        curr = self
        while curr.action is not None:
            path.append(curr.action)
            curr = curr.parent
        return list(reversed(path))


class Problem(ABC):
    """Representa o espaço de estados, transições e teste de objetivo."""

    @abstractmethod
    def actions(self, state: State) -> list[Action]:
        """Retorna o conjunto de ações aplicáveis em um estado."""
        pass

    @abstractmethod
    def is_goal(self, state: State) -> bool:
        """Verifica se o estado atinge o objetivo."""
        pass

    def heuristic(self, state: State) -> float:
        """Retorna o valor heurístico estimado até o objetivo (opcional)."""
        return 0.0

    def random_walk(self, initial_state: State, n: int, avoid_repeats: bool = False) -> State:
        """Gera um estado realizando n passos aleatórios a partir do estado inicial."""
        current = initial_state
        visited = {current} if avoid_repeats else set()

        for _ in range(n):
            possible_actions = self.actions(current)
            valid_transitions = []

            for act in possible_actions:
                nxt = act.apply(current)
                if nxt is not None and (not avoid_repeats or nxt not in visited):
                    valid_transitions.append((act, nxt))

            if not valid_transitions:
                break

            _, current = random.choice(valid_transitions)
            if avoid_repeats:
                visited.add(current)

        return current


class SearchStrategy(ABC):
    """Estratégia genérica de busca."""
    
    def __init__(self, problem: Problem):
        self.problem = problem

    @abstractmethod
    def search(self, initial_state: State) -> Optional[SearchNode]:
        """Executa a busca a partir de um estado inicial."""
        pass