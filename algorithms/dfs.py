from puzzle.base_search import BaseSearch
from puzzle.result import SearchResult
from puzzle.state import State

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):
    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        frontier = [initial]
        shallowest = {initial: 0}
        result = SearchResult(None, nodes_generated=1, max_frontier_size=1)

        while frontier:
            state = frontier.pop()
            depth = state.cost - initial.cost
            if depth != shallowest[state]:
                continue
            if state.is_goal:
                result.solution = state
                result.depth = depth
                return result
            if depth >= self.depth_limit:
                continue

            result.nodes_expanded += 1
            for child in reversed(state.neighbors()):
                child_depth = depth + 1
                # Um caminho mais curto permite explorar mais abaixo do limite.
                if child_depth >= shallowest.get(child, float("inf")):
                    continue
                shallowest[child] = child_depth
                frontier.append(child)
                result.nodes_generated += 1
            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
