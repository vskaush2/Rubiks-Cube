from cube import *
from g1 import *
from g2 import *
from random import randint

def reorder_moves(moves):
    did_change = False
    mapping = [DOWN, UP, FRONT, BACK, RIGHT, LEFT]
    for i in range(len(moves) - 1):
        if (mapping[abs(moves[i]) % 6] == abs(moves[i + 1]) % 6 and abs(moves[i]) % 6 < abs(moves[i + 1]) % 6):
            moves[i], moves[i + 1] = moves[i + 1], moves[i]
            did_change = True
    if (did_change):
        moves = reorder_moves(moves)
    return moves

def reduce_moves(moves):
    mapping = [DOWN, UP, FRONT, BACK, RIGHT, LEFT]

    moves = reorder_moves(moves)

    i = 0
    while (i < len(moves) - 2):
        if (moves[i] == moves[i + 1] and moves[i + 1] == moves[i + 2]):
            moves[i] = -moves[i]
            if (moves[i] == 0):
                moves[i] = -6
            elif (moves[i] == 6):
                moves[i] = 0
            del moves[i+1]
            del moves[i+1]
        else:
            i += 1

    moves = reorder_moves(moves)

    i = 0
    while (i < len(moves) - 1):
        c_move = moves[i]
        j = 1
        while (i + j < len(moves) - 1 and abs(moves[i + j]) % 6 == mapping[abs(moves[i]) % 6]):
            j += 1
        next_move = moves[i + j]

        assert(abs(next_move) % 6 != abs(c_move) % 6 or j == 1)

        if (c_move == -6 and next_move == 0 or\
            c_move == 0 and next_move == -6 or\
            c_move + next_move == 0 and c_move and next_move):
            del moves[i + j]
            del moves[i]
            continue
        i += 1

    return moves

def printMoves(moves):
    mapping = ["U", "D", "B", "F", "L", "R"]
    i = 0
    while (i < len(moves)):
        print(mapping[abs(moves[i]) % 6], end='')
        if (i + 1 < len(moves) and moves[i + 1] == moves[i]):
            print("2", end='')
            i += 1
        elif (moves[i] < 0):
            print("'", end='')
        print(" ", end='')
        i += 1
    print("")


if __name__ == "__main__":
    cube = Cube()

    ## Scramble the cube ##
    for i in range(24):
        cube.rotate(randint(0, 5), randint(0, 1))
    print("Scramble:")
    printMoves(cube.get_moves())
    cube.clear_moves()

    print("-----------------")

    ## Solve the cube ##
    # G0 -> G1
    G1_to_G2(cube) # dont mind the name
    g0_moves = reduce_moves(cube.get_moves().copy())
    print("G0 -> G1: ", end='')
    printMoves(g0_moves)
    cube.clear_moves()

    # G1 -> G2
    place_edges(cube)
    orient_corners(cube)
    g1_moves = reduce_moves(cube.get_moves().copy())
    print("G1 -> G2: ", end='')
    printMoves(g1_moves)
    cube.clear_moves()

    # G2 -> G3
    permute_corners_1(cube)
    permute_corners_2(cube)
    permute_edges(cube)
    g2_moves = reduce_moves(cube.get_moves().copy())
    print("G2 -> G3: ", end='')
    printMoves(g2_moves)
    cube.clear_moves()

    # G3 -> solved
    domino_solve(cube)
    g3_moves = reduce_moves(cube.get_moves().copy())
    print("G3 -> G4: ", end='')
    printMoves(g3_moves)
    cube.clear_moves()


'''
if __name__ == "__main__":

    for j in range(1000):
        c = Cube()
        for i in range(20):
            c.rotate(randint(0, 5), randint(0, 1))
        print(str(j) + " scamble:")
        printMoves(c.get_moves())
        print(str(j) + " scamble: " + str(c.get_moves()))
        c.clear_moves()
        G1_to_G2(c)
        place_edges(c)
        orient_corners(c)
        permute_corners_1(c)
        permute_corners_2(c)
        permute_edges(c)
        domino_solve(c)
        assert(c.isSolved())

        these_moves = c.get_moves()

        print("Solution:")
        printMoves(these_moves)
        these_moves = reduce_moves(these_moves)
        print("Reduced solution:")
        printMoves(these_moves)
        print("---")
'''
