import random
import copy
from optparse import OptionParser
import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0 
        iter_allowance = 20
        restart = 0
        restart_allowance = 3

        

        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            
            
            if currentNumberOfAttacks == 0 and restart > restart_allowance:
                return newBoard
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()

            i += 1
            if currentNumberOfAttacks <= newNumberOfAttacks and i > iter_allowance:
                
                i = 0
                newBoard = Board(squareArray = [[]])
                
                restart += 1
                
                
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray
          
    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s 

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For exmaple: 
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """

        costBoard = self.getCostBoard()
        

        THRES = 9999
        minNumOfAttack = THRES

        oldRow = None
        oldCol = None
        newRow = None
        newCol = None

        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            if minNumOfAttack > costBoard.squareArray[rr][c]:
                                oldRow, oldCol = r, c
                                newRow, newCol = rr, c 
                                minNumOfAttack = costBoard.squareArray[rr][c]

        if minNumOfAttack == THRES:
            return (self, self.getNumberOfAttacks(), newRow, newCol)
                                

        betterBoard = copy.deepcopy(self)
        betterBoard.squareArray[oldRow][oldCol] = 0
        betterBoard.squareArray[newRow][newCol] = 1

        return (betterBoard, minNumOfAttack, newRow, newCol)
                            
        
        

    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        N = len(self.squareArray)
        row_array = [0 for i in range(N)]
        col_array = [0 for i in range(N)]
        diag1_array = [0 for i in range(2 * N)]
        diag2_array = [0 for i in range(2 * N)]

        def nC2(x):
            return 0.5 * x * (x - 1)


        for i in range(N):
            row_array[i] += sum(self.squareArray[i])

            for j in range(N):
                col_array[i] += self.squareArray[j][i]
                diag1_array[i+j] += self.squareArray[i][j]
                diag2_array[N-i+j] += self.squareArray[i][j]

        sum_row_col = sum([nC2(row_array[i]) + nC2(col_array[i]) for i in range(N)])
        sum_diag1_diag2 = sum([nC2(diag1_array[i]) + nC2(diag2_array[i]) for i in range(2 * N)])

        return int(sum_diag1_diag2 + sum_row_col)

if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
