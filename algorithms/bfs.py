from collections import deque

from puzzle.base_search import BaseSearch
from puzzle.result import SearchResult
from puzzle.state import State


class BFS(BaseSearch):
    def search(self, initial: State) -> SearchResult:
        frontier = deque([initial])
        seen = {initial}
        result = SearchResult(None, nodes_generated=1, max_frontier_size=1)

        while frontier:
            state = frontier.popleft()
            if state.is_goal:
                result.solution = state
                result.depth = state.cost - initial.cost
                return result

            result.nodes_expanded += 1
            for child in state.neighbors():
                if child in seen:
                    continue
                seen.add(child)
                frontier.append(child)
                result.nodes_generated += 1
            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
