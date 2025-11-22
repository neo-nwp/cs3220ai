from src.csp import CSP
from src.utils import different_values_constraint

class AsteriskSudoku(CSP):
    def __init__(self, grid81: str):
        # 0-80 variables
        vars = list(range(81))
        # domains
        domains = {i: [int(ch)] if ch in "123456789" else list(range(1, 10))
                   for i, ch in enumerate(grid81)}
        # neighbours
        neigh = {v: set() for v in vars}
        get = lambda r, c: r * 9 + c
        self.asterisk = {
            get(1, 4), get(2, 2), get(2, 6),
            get(4, 1), get(4, 4), get(4, 7),
            get(6, 2), get(6, 6), get(7, 4)
        }

        for v in vars:
            r, c = divmod(v, 9)
            # row
            for cc in range(9):
                neigh[v].add(get(r, cc))
            # col
            for rr in range(9):
                neigh[v].add(get(rr, c))
            # box
            br, bc = (r // 3) * 3, (c // 3) * 3
            for rr in range(3):
                for cc in range(3):
                    neigh[v].add(get(br + rr, bc + cc))
            # asterisk
            if v in self.asterisk:
                for u in self.asterisk:
                    neigh[v].add(u)
            neigh[v].discard(v)          # remove self
        # convert sets -> lists
        for v in neigh:
            neigh[v] = list(neigh[v])

        super().__init__(vars, domains, neigh, different_values_constraint)