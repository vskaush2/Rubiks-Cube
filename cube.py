import numpy as np

WHITE = 0
YELLOW = 1
GREEN = 2
BLUE = 3
RED = 4
ORANGE = 5

UP = 0
DOWN = 1
BACK = 2
FRONT = 3
LEFT = 4
RIGHT = 5

color_list = ['W', 'Y', 'G', 'B', 'R', 'O', ' ']


def rotated_cw(array_2d):
    list_of_tuples = zip(*array_2d[::-1])
    return [list(elem) for elem in list_of_tuples]

def rotated_prime(array_2d):
    return (rotated_cw(rotated_cw(rotated_cw(array_2d))))

def rotated(array_2d, prime):
    if (prime):
        return rotated_prime(array_2d)
    else:
        return rotated_cw(array_2d)

class Cube:

    def __init__(self):
        self.moves = []
        self.stickers = np.array([[[-1 for i in range(5)] for j in range(5)] for k in range(5)])
        # white and yellow #
        for i in range(1, 4):
            for j in range(1, 4):
                self.stickers[0][i][j] = WHITE
                self.stickers[4][i][j] = YELLOW

        # other colors #
        for i in range(1, 4):
            for j in range(1, 4):
                self.stickers[i][0][j] = GREEN
                self.stickers[i][j][0] = RED
                self.stickers[i][4][j] = BLUE
                self.stickers[i][j][4] = ORANGE

    def isSolved(self):
        other = Cube()
        return np.array_equal(other.stickers, self.stickers)

    '''
    Returns a list of the sticker colors for the edge. Layer starts at 0 and
    goes to 2 (white to middle to yellow). Num refers to one of four edges in
    that layer (0-3). Counting starts at the back-left in that order. (e.g.
    layer=1 num=0 is red green edge, layer=0 num=0 is white green edge, layer=0
    num=1 is white orange edge). List return is order specific. The order will
    always have stickers on higher priority sides first. Specifically, up-down
    before front-back before left-right.
    '''
    def getEdge(self, layer, num):
        ret = [0, 0]
        stick_x = 0
        stick_y = 0
        if (layer == 0 or layer == 2):
            z = layer * 2
            if (num == 0):
                ret[0] = self.stickers[z][1][2]
                ret[1] = self.stickers[z + 1 - layer][0][2]
            elif (num == 1):
                ret[0] = self.stickers[z][2][3]
                ret[1] = self.stickers[z + 1 - layer][2][4]
            elif (num == 2):
                ret[0] = self.stickers[z][3][2]
                ret[1] = self.stickers[z + 1 - layer][4][2]
            elif (num == 3):
                ret[0] = self.stickers[z][2][1]
                ret[1] = self.stickers[z + 1 - layer][2][0]
            else:
                raise()
        elif (layer == 1):
            if (num == 0):
                ret[0] = self.stickers[2][0][1]
                ret[1] = self.stickers[2][1][0]
            elif (num == 1):
                ret[0] = self.stickers[2][0][3]
                ret[1] = self.stickers[2][1][4]
            elif (num == 2):
                ret[0] = self.stickers[2][4][3]
                ret[1] = self.stickers[2][3][4]
            elif (num == 3):
                ret[0] = self.stickers[2][4][1]
                ret[1] = self.stickers[2][3][0]
            else:
                raise()
        else:
            raise()

        return ret

    def getEdge_num(self, num):
        return self.getEdge(int(num / 4), num % 4)

    '''
    0-3 top corners, start back left, move clockwise. Same with 4-7. Returns
    list of colors with the following format: [up/down, front/back, left/right]
    '''
    def getCorner(self, num):
        ret = [0, 0, 0]
        z1 = 0
        z2 = 1

        if (num >= 4):
            z1 = 4
            z2 = 3

        num = num%4

        if (num == 0):
            ret[0] = self.stickers[z1][1][1]
            ret[1] = self.stickers[z2][0][1]
            ret[2] = self.stickers[z2][1][0]
        elif (num == 1):
            ret[0] = self.stickers[z1][1][3]
            ret[1] = self.stickers[z2][0][3]
            ret[2] = self.stickers[z2][1][4]
        elif (num == 2):
            ret[0] = self.stickers[z1][3][3]
            ret[1] = self.stickers[z2][4][3]
            ret[2] = self.stickers[z2][3][4]
        elif (num == 3):
            ret[0] = self.stickers[z1][3][1]
            ret[1] = self.stickers[z2][4][1]
            ret[2] = self.stickers[z2][3][0]
        return ret


    def rotate_seq(self, seq):
        for f in seq:
            self.rotate(abs(f) % 6, f < 0)
    def rotate(self, face, prime):
        if (face == UP and prime):
            self.moves.append(-6)
        else:
            self.moves.append(face * (1 - 2 * prime))

        if (face == UP):
            self.stickers[0] = rotated(self.stickers[0], prime)
            self.stickers[1] = rotated(self.stickers[1], prime)
        elif (face == DOWN):
            self.stickers[3] = rotated(self.stickers[3], not prime)
            self.stickers[4] = rotated(self.stickers[4], not prime)
        elif (face == BACK):
            self.stickers[:,0] = rotated(self.stickers[:,0], not prime)
            self.stickers[:,1] = rotated(self.stickers[:,1], not prime)
        elif (face == FRONT):
            self.stickers[:,3] = rotated(self.stickers[:,3], prime)
            self.stickers[:,4] = rotated(self.stickers[:,4], prime)
        elif (face == LEFT):
            self.stickers[:,0:,0] = rotated(self.stickers[:,0:,0], prime)
            self.stickers[:,0:,1] = rotated(self.stickers[:,0:,1], prime)
        elif (face == RIGHT):
            self.stickers[:,0:,3] = rotated(self.stickers[:,0:,3], not prime)
            self.stickers[:,0:,4] = rotated(self.stickers[:,0:,4], not prime)

    def get_moves(self):
        return self.moves
    def clear_moves(self):
        self.moves = []

    def print_cube(self):
        for i in range(5):
            for j in range(5):
                for k in range(5):
                    print(color_list[self.stickers[i][j][k]], end='')
                print("\n", end='')
            print("\n", end='')
        print("-------")
