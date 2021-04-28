Location = TypeVar("Location")
class Graph(Protocol):
    def neighbors(self, id: Location) -> List[Location]: pass


class SimpleGraph:
    def __init__(self):
        