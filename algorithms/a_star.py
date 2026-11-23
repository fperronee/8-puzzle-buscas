import heapq
from itertools import count
from typing import Callable, Optional

from puzzle.base_search import BaseSearch
from puzzle.result import SearchResult
from puzzle.state import GOAL_STATE, State


GOAL_POSITIONS = {tile: divmod(index, 3) for index, tile in enumerate(GOAL_STATE)}


class AStar(BaseSearch):
    def __init__(self, heuristic: Optional[Callable[[State], int]] = None):
        self._heuristic = heuristic

    def heuristic(self, state: State) -> int:
        if self._heuristic is not None:
            return self._heuristic(state)

        distance = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            row, column = divmod(index, 3)
            goal_row, goal_column = GOAL_POSITIONS[tile]
            distance += abs(row - goal_row) + abs(column - goal_column)
        return distance

    def search(self, initial: State) -> SearchResult:
        order = count()
        frontier = [(initial.cost + self.heuristic(initial), next(order), initial)]
        best_cost = {initial: initial.cost}
        result = SearchResult(None, nodes_generated=1, max_frontier_size=1)

        while frontier:
            _, _, state = heapq.heappop(frontier)
            if state.cost != best_cost[state]:
                continue
            if state.is_goal:
                result.solution = state
                result.depth = state.cost - initial.cost
                return result

            result.nodes_expanded += 1
            for child in state.neighbors():
                if child.cost >= best_cost.get(child, float("inf")):
                    continue
                best_cost[child] = child.cost
                priority = child.cost + self.heuristic(child)
                heapq.heappush(frontier, (priority, next(order), child))
                result.nodes_generated += 1
            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
