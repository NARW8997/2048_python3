from BaseAI import BaseAI


PerfectSnakeHeuristic = [[4**15,   4**14, 4**13, 4**12],
                        [4**8,    4**9, 4**10, 4**11],
                        [4**7,    4**6, 4**5, 4**4],
                        [1,    4, 4**2,    4**3]]
INF = 4**32

# 50 times test cases
# 2048, 4096, 1024, 4096, 2048, 2048, 1024, 1024, 1024, 2048
# 4096, 2048, 2048, 2048, 1024, 1024, 4096, 2048, 2048, 2048
# 2048, 2048, 4096, 1024, 1024, 1024, 512,  2048, 512,  512
# 2048, 1024, 1024, 1024, 2048, 2048, 2048, 1024, 2048, 2048
# 2048, 1024, 512,  256,  2048, 1024, 4096, 2048, 1024, 2048

def snakeHeuristic(grid):
    h = 0
    for i in range(grid.size):
        for j in range(grid.size):
            h += grid.map[i][j] * PerfectSnakeHeuristic[i][j]

    return h


class IntelligentAgent(BaseAI):
    def getMove(self, grid):
        res = self.Maximize(grid, -INF, INF, 4)
        return res[1]


    def Maximize(self, grid, a, b, depth) -> tuple: # (maxH, dir)
        if self.isTerminal(grid) or depth <= 0:
            return snakeHeuristic(grid), None

        maxUtility = -INF
        dir = None
        res = maxUtility, dir

        for moveset in grid.getAvailableMoves():
            childRes = self.Minimize(moveset[1], a, b, depth - 1)

            if childRes[0] > maxUtility:
                maxUtility = childRes[0]
                dir = moveset[0]
                res = maxUtility, dir
            if maxUtility >= b:
                break

            if maxUtility > a:
                a = maxUtility
        return  res

    def Minimize(self, grid, a, b, depth) -> tuple: # (minH, dir)
        minUtility = INF
        dir = None
        res = (minUtility, dir)
        freeCells = grid.getAvailableCells()
        for pos in freeCells:
            if freeCells.index(pos) >= depth:
                break
            cloneGrid = grid.clone()
            cloneGrid.insertTile(pos, 2)
            childRes2 = self.Maximize(cloneGrid, a, b, depth - 1)
            cloneGrid.setCellValue(pos, 4)
            childRes4 = self.Maximize(cloneGrid, a, b, depth - 1)
            utility = childRes4[0] * 0.1 + childRes2[0] * 0.9
            childDir = childRes2[1] if min(childRes2[0], childRes4[0]) == childRes2[0] else childRes4[1]
            childRes = (utility, childDir)
            if utility < minUtility:
                minUtility = utility
                dir = childDir
                res = minUtility, dir
            if minUtility <= a:
                break

            if minUtility < b:
                b = minUtility
        return res

    def isTerminal(self, grid):
        return grid.canMove() == False

