from cube import *

'''
The functions in this file are used to get the cube from G0 to G1
'''

# returns whether or not edge at spot num is oriented correctly
def is_good_edge(cube, num):
    edge = cube.getEdge_num(num)
    return edge[0] < edge[1]
# gets all edges that are not oriented correctly
def get_bad_edges(cube):
    bad_edges = []
    for i in range(12):
        if (not is_good_edge(cube, i)):
            bad_edges.append(i)
    return bad_edges
# gets all edges that are not oriented correctly and are not in the front layer
def get_nonfront_bad_edges(cube):
    bad_edges = []
    for i in range(12):
        if (not is_good_edge(cube, i) and (i != 2 and i != 6 and i != 7 and i != 10)):
            bad_edges.append(i)
    return bad_edges
# moves an edge in spot edge num to spot in front
def move_to_front(cube, edge_num, spot):
    if (edge_num == 0):
        if (spot == 0):
            cube.rotate_seq([UP, UP])
        elif (spot == 1):
            cube.rotate_seq([UP, -RIGHT, -6])
        elif (spot == 2):
            cube.rotate_seq([BACK, BACK, DOWN, DOWN])
        elif (spot == 3):
            cube.rotate_seq([-6, LEFT, UP])
        else:
            raise()
    elif (edge_num == 1):
        if (spot == 0):
            cube.rotate_seq([UP])
        elif (spot == 1):
            cube.rotate_seq([-RIGHT])
        elif (spot == 2):
            cube.rotate_seq([RIGHT, RIGHT, -DOWN, RIGHT, RIGHT])
        elif (spot == 3):
            cube.rotate_seq([UP, UP, LEFT, UP, UP])
        else:
            raise()
    elif (edge_num == 2):
        if (spot == 0):
            cube.rotate_seq([])
        elif (spot == 1):
            cube.rotate_seq([-6, -RIGHT])
        elif (spot == 2):
            cube.rotate_seq([UP, UP, BACK, BACK, DOWN, DOWN])
        elif (spot == 3):
            cube.rotate_seq([UP, LEFT])
        else:
            raise()
    elif (edge_num == 3):
        if (spot == 0):
            cube.rotate_seq([-6])
        elif (spot == 1):
            cube.rotate_seq([UP, UP, -RIGHT, UP, UP])
        elif (spot == 2):
            cube.rotate_seq([LEFT, LEFT, DOWN, LEFT, LEFT])
        elif (spot == 3):
            cube.rotate_seq([LEFT])
        else:
            raise()
    elif (edge_num == 4):
        if (spot == 0):
            cube.rotate_seq([LEFT, -6, -LEFT])
        elif (spot == 1):
            cube.rotate_seq([BACK, BACK, RIGHT, RIGHT])
        elif (spot == 2):
            cube.rotate_seq([-LEFT, DOWN, LEFT])
        elif (spot == 3):
            cube.rotate_seq([LEFT, LEFT])
        else:
            raise()
    elif (edge_num == 5):
        if (spot == 0):
            cube.rotate_seq([-RIGHT, UP, RIGHT])
        elif (spot == 1):
            cube.rotate_seq([RIGHT, RIGHT])
        elif (spot == 2):
            cube.rotate_seq([RIGHT, -DOWN, -RIGHT])
        elif (spot == 3):
            cube.rotate_seq([BACK, BACK, LEFT, LEFT])
        else:
            raise()
    elif (edge_num == 6):
        if (spot == 0):
            cube.rotate_seq([RIGHT, UP])
        elif (spot == 1):
            cube.rotate_seq([])
        elif (spot == 2):
            cube.rotate_seq([-RIGHT, -DOWN])
        elif (spot == 3):
            cube.rotate_seq([RIGHT, RIGHT, BACK, BACK, LEFT, LEFT])
        else:
            raise()
    elif (edge_num == 7):
        if (spot == 0):
            cube.rotate_seq([-LEFT, -6])
        elif (spot == 1):
            cube.rotate_seq([LEFT, LEFT, BACK, BACK, RIGHT, RIGHT])
        elif (spot == 2):
            cube.rotate_seq([LEFT, DOWN])
        elif (spot == 3):
            cube.rotate_seq([])
        else:
            raise()
    elif (edge_num == 8):
        if (spot == 0):
            cube.rotate_seq([BACK, BACK, UP, UP])
        elif (spot == 1):
            cube.rotate_seq([-DOWN, RIGHT, DOWN])
        elif (spot == 2):
            cube.rotate_seq([DOWN, DOWN])
        elif (spot == 3):
            cube.rotate_seq([DOWN, -LEFT, -DOWN])
        else:
            raise()
    elif (edge_num == 9):
        if (spot == 0):
            cube.rotate_seq([RIGHT, RIGHT, UP, RIGHT, RIGHT])
        elif (spot == 1):
            cube.rotate_seq([RIGHT])
        elif (spot == 2):
            cube.rotate_seq([-DOWN])
        elif (spot == 3):
            cube.rotate_seq([DOWN, DOWN, -LEFT, DOWN, DOWN])
        else:
            raise()
    elif (edge_num == 10):
        if (spot == 0):
            cube.rotate_seq([DOWN, DOWN, BACK, BACK, UP, UP])
        elif (spot == 1):
            cube.rotate_seq([DOWN, RIGHT])
        elif (spot == 2):
            cube.rotate_seq([])
        elif (spot == 3):
            cube.rotate_seq([-DOWN, -LEFT])
        else:
            raise()
    elif (edge_num == 11):
        if (spot == 0):
            cube.rotate_seq([LEFT, LEFT, -6, LEFT, LEFT])
        elif (spot == 1):
            cube.rotate_seq([DOWN, DOWN, RIGHT, DOWN, DOWN])
        elif (spot == 2):
            cube.rotate_seq([DOWN])
        elif (spot == 3):
            cube.rotate_seq([-LEFT])
        else:
            raise()
    else:
        print("whoops")
        raise()

# solves cube from G0 to G1. Disregard the silly name
def G1_to_G2(cube):
    bad_edges = get_bad_edges(cube)
    assert(len(bad_edges) % 2 == 0)

    if (len(bad_edges) > 2):
        nfbe = get_nonfront_bad_edges(cube)
        if (len(nfbe) == 0):
            cube.rotate_seq([FRONT])
            return
        for i in range(4):
            if (len(nfbe) == 0):
                break
            move_to_front(cube, nfbe[0], i)
            nfbe = get_nonfront_bad_edges(cube)
        cube.rotate_seq([FRONT])
        G1_to_G2(cube)
    elif (len(bad_edges) == 2):
        move_to_front(cube, bad_edges[0], 0)
        bad_edges = get_bad_edges(cube)
        if (bad_edges[0] == 2):
            move_to_front(cube, bad_edges[1], 1)
        else:
            move_to_front(cube, bad_edges[0], 1)
        cube.rotate_seq([UP, -FRONT, -6, FRONT])

    bad_edges = get_bad_edges(cube)
    assert(len(bad_edges) == 0)
