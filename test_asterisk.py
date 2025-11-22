from src.sudoku import AsteriskSudoku
from src.algorithms import backtracking_search

grid = (
    "530070000"
    "600195000"
    "098000060"
    "800060003"
    "400803001"
    "700020006"
    "060000280"
    "000419005"
    "000080079"
)

csp = AsteriskSudoku(grid)
solution = backtracking_search(csp)
print("Solution dict:", solution)
print("Assignments made:", csp.nassigns)