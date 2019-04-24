from cube import *


# places white and yellow edges into top and bottom layers (irrespectively [it doesn't matter if it's white and yellow on top])
def place_edges(cube):
    # up first #
    while (True):
        # get open slot
        slot = -1
        for i in range(4):
            if (cube.getEdge_num(i)[0] >= 2):
                slot = i
                break
        if (slot == -1):
            break

        # get new piece
        replacement_piece = -1
        for i in range(4):
            if (cube.getEdge(1, i)[0] <= 1):
                replacement_piece = i
                break
        assert(replacement_piece != -1)

        if (replacement_piece == 0 or replacement_piece == 3):
            cube.rotate_seq([UP for i in range(3 - slot)])
            cube.rotate(LEFT, replacement_piece == 3)
        elif (replacement_piece == 1 or replacement_piece == 2):
            cube.rotate_seq([UP for i in range(3 - (slot + 2)%4)])
            cube.rotate(RIGHT, replacement_piece == 1)
        else:
            raise()

    # down next #
    while (True):
        # get open slot
        slot = -1
        spec = [0, 2, 1, 3]
        for i in spec:
            if (cube.getEdge(2, i)[0] >= 2):
                slot = i
                break
        if (slot == -1):
            break

        # get new piece
        replacement_piece = -1
        for i in range(4):
            if (cube.getEdge(1, i)[0] <= 1):
                replacement_piece = i
                break
        assert(replacement_piece != -1)

        if (slot == 1 or slot == 3):
            cube.rotate(DOWN, False)
            continue

        assert(slot != 1 and slot != 3)

        if (replacement_piece == 0 or replacement_piece == 3):
            cube.rotate(LEFT, replacement_piece == 0)
            cube.rotate(DOWN, slot == 2)
            cube.rotate(LEFT, replacement_piece != 0)
        elif (replacement_piece == 1 or replacement_piece == 2):
            cube.rotate(RIGHT, replacement_piece == 2)
            cube.rotate(DOWN, slot == 0)
            cube.rotate(RIGHT, replacement_piece != 2)
        else:
            raise()

# twists corners so that they are all white and yellow facing up and down
def orient_corners(cube):
    # get the kind of corner in top and bottom layers #
    top_corners = []
    top_count = 0
    bot_corners = []
    bot_count = 0
    for i in range(4):
        if (cube.getCorner(i)[0] <= 1):
            top_corners.append(0)
        elif (cube.getCorner(i)[1 + i % 2] <= 1):
            top_corners.append(1)
            top_count += 1
        elif (cube.getCorner(i)[2 - i % 2] <= 1):
            top_corners.append(2)
            top_count += 1
        else:
            raise()
    for i in range(4):
        if (cube.getCorner(i + 4)[0] <= 1):
            bot_corners.append(0)
        elif (cube.getCorner(i + 4)[2 - i % 2] <= 1):
            bot_corners.append(1)
            bot_count += 1
        elif (cube.getCorner(i + 4)[1 + i % 2] <= 1):
            bot_corners.append(2)
            bot_count += 1
        else:
            raise()

    if (top_count + bot_count == 0):
        return
    elif (top_count == 0):
        if (bot_count >= 3):
            cube.rotate_seq([RIGHT, RIGHT])
        elif (bot_count == 2):
            if (cube.getCorner(4)[0] >= 2 and cube.getCorner(7)[0] >= 2):
                cube.rotate_seq([FRONT, FRONT])
            elif (cube.getCorner(4)[0] <= 1 and cube.getCorner(7)[0] <= 1):
                cube.rotate_seq([FRONT, FRONT])
            else:
                cube.rotate_seq([LEFT, LEFT])
        else:
            raise()
        orient_corners(cube)
        return
    elif (bot_count == 0):
        if (top_count >= 3):
            cube.rotate_seq([RIGHT, RIGHT])
        elif (top_count == 2):
            if (cube.getCorner(0)[0] >= 2 and cube.getCorner(3)[0] >= 2):
                cube.rotate_seq([FRONT, FRONT])
            elif (cube.getCorner(0)[0] <= 1 and cube.getCorner(3)[0] <= 1):
                cube.rotate_seq([FRONT, FRONT])
            else:
                cube.rotate_seq([LEFT, LEFT])
        else:
            raise()
        orient_corners(cube)
        return

    # now we can guarantee there is a corner in the top and the bottom #
    if (1 in top_corners and 2 in bot_corners):
        while (cube.getCorner(3)[2] >= 2):
            cube.rotate(UP, False)
        while (cube.getCorner(6)[1] >= 2):
            cube.rotate(DOWN, False)
    elif (2 in top_corners and 1 in bot_corners):
        while (cube.getCorner(3)[1] >= 2):
            cube.rotate(UP, False)
        while (cube.getCorner(6)[2] >= 2):
            cube.rotate(DOWN, False)
        cube.rotate_seq([FRONT, FRONT])
    else:
        while (cube.getCorner(3)[0] <= 1):
            cube.rotate(UP, False)
        while (cube.getCorner(6)[0] <= 1):
            cube.rotate(DOWN, False)

    cube.rotate_seq([-RIGHT, DOWN, LEFT, LEFT, -DOWN, RIGHT])
    orient_corners(cube)



# congrats on getting to g2!
# The following functions are used to get the cube from G2 to G3

# gets corners in correct layer
def permute_corners_1(cube):
    top_corners = []
    bot_corners = []
    for i in range(4):
        top_corners.append(cube.getCorner(i)[0])
        bot_corners.append(cube.getCorner(i + 4)[0])

    if (sum(top_corners) == 0):
        return
    elif (sum(top_corners) == 4):
        cube.rotate_seq([RIGHT, RIGHT, LEFT, LEFT])
        return
    elif (sum(top_corners) == 3):
        cube.rotate_seq([RIGHT, RIGHT, LEFT, LEFT])
        permute_corners_1(cube)
    elif (sum(top_corners) == 2):
        # sad...
        top_bar = False
        bot_bar = False
        for i in range(4):
            if (cube.getCorner(i)[0] == cube.getCorner((i + 1)%4)[0]):
                top_bar = True
            if (cube.getCorner(4 + i)[0] == cube.getCorner(4 + (i + 1)%4)[0]):
                bot_bar = True

        if (top_bar and bot_bar):
            while (cube.getCorner(0)[0] != cube.getCorner(4)[0] or \
                   cube.getCorner(1)[0] != cube.getCorner(5)[0] or \
                   cube.getCorner(2)[0] != cube.getCorner(6)[0] or \
                   cube.getCorner(3)[0] != cube.getCorner(7)[0]):
                cube.rotate(DOWN, False)
            cube.rotate_seq([DOWN, DOWN])
            if (cube.getCorner(0)[0] == cube.getCorner(1)[0]):
                cube.rotate_seq([BACK + cube.getCorner(3)[0], BACK + cube.getCorner(3)[0]])
            elif (cube.getCorner(0)[0] == cube.getCorner(3)[0]):
                cube.rotate_seq([LEFT + cube.getCorner(1)[0], LEFT + cube.getCorner(1)[0]])
            else:
                raise()
        elif (bot_bar or top_bar):
            mapping = [BACK, RIGHT, FRONT, LEFT]
            for i in range(4):
                if (cube.getCorner(4 * bot_bar + i)[0] == cube.getCorner(4 * bot_bar + (i + 1)%4)[0]):
                    cube.rotate(mapping[i], False)
                    cube.rotate(mapping[i], False)
                    break
        else:
            while (cube.getCorner(0)[0] != cube.getCorner(4)[0] or \
                   cube.getCorner(1)[0] != cube.getCorner(5)[0] or \
                   cube.getCorner(2)[0] != cube.getCorner(6)[0] or \
                   cube.getCorner(3)[0] != cube.getCorner(7)[0]):
                cube.rotate(DOWN, False)
            cube.rotate_seq([RIGHT, RIGHT])
        permute_corners_1(cube)
    elif (sum(top_corners) == 1):
        mapping = [5, 4, 7, 6]
        stray_corner = top_corners.index(1)
        bot_stray = bot_corners.index(0) + 4
        bot_stray_goal = mapping[stray_corner]

        cube.rotate_seq([-DOWN for i in range((4 + bot_stray_goal - bot_stray) % 4)])
        if (stray_corner == 0 or stray_corner == 3):
            cube.rotate_seq([LEFT, LEFT])
            cube.rotate(DOWN, stray_corner == 3)
            cube.rotate_seq([LEFT, LEFT])
        elif (stray_corner == 1 or stray_corner == 2):
            cube.rotate_seq([RIGHT, RIGHT])
            cube.rotate(DOWN, stray_corner == 1)
            cube.rotate_seq([RIGHT, RIGHT])
        else:
            raise()
        permute_corners_1(cube) # this is a sanity check; it should not actually do anything to the cube in the end
    else:
        raise()

# gets corners into solved spot
def permute_corners_2(cube):
    top_state = 0
    bot_state = 0
    if (cube.getCorner(0)[1] == cube.getCorner(1)[1] or\
        cube.getCorner(1)[2] == cube.getCorner(2)[2] or\
        cube.getCorner(2)[1] == cube.getCorner(3)[1] or\
        cube.getCorner(3)[2] == cube.getCorner(0)[2]):
        top_state = 1
    if (cube.getCorner(0)[1] == cube.getCorner(1)[1] and\
        cube.getCorner(1)[2] == cube.getCorner(2)[2] and\
        cube.getCorner(2)[1] == cube.getCorner(3)[1] and\
        cube.getCorner(3)[2] == cube.getCorner(0)[2]):
        top_state = 2
    if (cube.getCorner(4)[1] == cube.getCorner(5)[1] or\
        cube.getCorner(5)[2] == cube.getCorner(6)[2] or\
        cube.getCorner(6)[1] == cube.getCorner(7)[1] or\
        cube.getCorner(7)[2] == cube.getCorner(4)[2]):
        bot_state = 1
    if (cube.getCorner(4)[1] == cube.getCorner(5)[1] and\
        cube.getCorner(5)[2] == cube.getCorner(6)[2] and\
        cube.getCorner(6)[1] == cube.getCorner(7)[1] and\
        cube.getCorner(7)[2] == cube.getCorner(4)[2]):
        bot_state = 2

    if (bot_state == 0 and top_state == 0):
        cube.rotate_seq([RIGHT, RIGHT, FRONT, FRONT, RIGHT, RIGHT])
    elif (bot_state == 0 and top_state == 1):
        while (cube.getCorner(0)[2] != cube.getCorner(3)[2]):
            cube.rotate(UP, False)
        cube.rotate_seq([RIGHT, RIGHT, -DOWN, RIGHT, RIGHT, DOWN, RIGHT, RIGHT, -DOWN, RIGHT, RIGHT, DOWN, RIGHT, RIGHT])
    elif (bot_state == 1 and top_state == 0):
        while (cube.getCorner(4)[2] != cube.getCorner(7)[2]):
            cube.rotate(DOWN, False)
        cube.rotate_seq([RIGHT, RIGHT, UP, RIGHT, RIGHT, -6, RIGHT, RIGHT, UP, RIGHT, RIGHT, -6, RIGHT, RIGHT])
    elif (bot_state == 1 and top_state == 1):
        while (cube.getCorner(1)[2] != cube.getCorner(2)[2]):
            cube.rotate(UP, False)
        cube.rotate_seq([RIGHT, RIGHT, -DOWN, RIGHT, RIGHT, DOWN, RIGHT, RIGHT, -DOWN, RIGHT, RIGHT, DOWN, RIGHT, RIGHT])
        # now in top 0 bot 1
        permute_corners_2(cube)
    elif (bot_state == 2 and top_state == 0):
        cube.rotate_seq([RIGHT, RIGHT, -DOWN, RIGHT, RIGHT, DOWN, RIGHT, RIGHT, -DOWN, RIGHT, RIGHT, DOWN, RIGHT, RIGHT])
        # now in top 1 bot 0 i think
        permute_corners_2(cube)
    elif (bot_state == 2 and top_state == 1):
        cube.rotate_seq([RIGHT, RIGHT, FRONT, FRONT, RIGHT, RIGHT])
        # now in top 1 bot 0 i think (strongly)
        permute_corners_2(cube)
    elif (bot_state == 0 and top_state == 2):
        cube.rotate_seq([RIGHT, RIGHT, UP, RIGHT, RIGHT, -6, RIGHT, RIGHT, UP, RIGHT, RIGHT, -6, RIGHT, RIGHT])
        # now in top 0 bot 1 i think
        permute_corners_2(cube)
    elif (bot_state == 1 and top_state == 2):
        cube.rotate_seq([RIGHT, RIGHT, FRONT, FRONT, RIGHT, RIGHT])
        # now in top 0 bot 1 i think (strongly)
        permute_corners_2(cube)
    else:
        assert(bot_state == 2 and top_state == 2)

    #print("ping")
    while (cube.getCorner(0)[1] != GREEN):
        cube.rotate(UP, False)
    while (cube.getCorner(4)[1] != GREEN):
        cube.rotate(DOWN, False)

# checks to see if edge is in an okay spot
def check_edges(cube):
    bad_edges = []
    mapping1 = [GREEN, ORANGE, BLUE, RED]
    mapping2 = [BLUE, RED, GREEN, ORANGE]

    for i in range(4):
        if (cube.getEdge_num(i)[1] != mapping1[i % 4] and cube.getEdge_num(i)[1] != mapping2[i % 4]):
            bad_edges.append(i)
    for i in range(8, 12):
        if (cube.getEdge_num(i)[1] != mapping1[i % 4] and cube.getEdge_num(i)[1] != mapping2[i % 4]):
            bad_edges.append(i)

    assert(len(bad_edges) == 0)

# puts bad edges into correct orbits
def permute_edges(cube):
    bad_edges = []
    mapping1 = [GREEN, ORANGE, BLUE, RED]
    mapping2 = [BLUE, RED, GREEN, ORANGE]

    for i in range(4):
        if (cube.getEdge_num(i)[1] != mapping1[i % 4] and cube.getEdge_num(i)[1] != mapping2[i % 4]):
            bad_edges.append(i)
    for i in range(8, 12):
        if (cube.getEdge_num(i)[1] != mapping1[i % 4] and cube.getEdge_num(i)[1] != mapping2[i % 4]):
            bad_edges.append(i)

    assert(len(bad_edges) % 2 == 0)

    if (len(bad_edges) == 0):
        return

    if (len(bad_edges) == 2):
        assert(bad_edges[0] % 2 != bad_edges[1] % 2) # they cannot be across from each other
                                                     # ie they must be adjacent
        # if they're both in the top layer...
        if (bad_edges[1] <= 3):
            if (bad_edges[0] == 0):
                cube.rotate_seq([RIGHT, RIGHT, LEFT, LEFT, DOWN, DOWN, RIGHT, RIGHT, LEFT, LEFT, UP, UP])
                #cube.rotate(UP, bad_edges[1] == 3)

            if (bad_edges[1] == 3): # left and front
                cube.rotate_seq([-DOWN, LEFT, LEFT, DOWN, FRONT, FRONT, RIGHT, RIGHT, LEFT, LEFT, BACK, BACK, RIGHT, RIGHT, LEFT, LEFT, -DOWN, LEFT, LEFT, DOWN])
            else: # right and front
                cube.rotate_seq([DOWN, RIGHT, RIGHT, -DOWN, FRONT, FRONT, RIGHT, RIGHT, LEFT, LEFT, BACK, BACK, RIGHT, RIGHT, LEFT, LEFT, DOWN, RIGHT, RIGHT, -DOWN])

            # undo setup move
            #if (bad_edges[0] == 0):
            #    cube.rotate(UP, bad_edges[1] != 3)
            return
        # if they're in different layers...
        elif (bad_edges[0] <= 3):
            cube.rotate_seq([-6 for i in range(bad_edges[0])])
            cube.rotate_seq([DOWN for i in range(2 + bad_edges[1] % 4)])
            # now there is one in spot 0 and one in spot 10
            cube.rotate_seq([FRONT, FRONT, UP, UP, LEFT, LEFT, UP, UP, LEFT, LEFT, UP, UP, LEFT, LEFT, FRONT, FRONT])
            cube.rotate_seq([UP for i in range(bad_edges[0])])
            cube.rotate_seq([-DOWN for i in range(2 + bad_edges[1] % 4)])
            return
        # if they are both in the bottom layer...
        else:
            assert(bad_edges[0] >= 8)
            cube.rotate_seq([RIGHT, RIGHT, LEFT, LEFT, BACK, BACK, FRONT, FRONT, UP, UP, DOWN, DOWN])
            permute_edges(cube)
            return
    else:
        assert(len(bad_edges) >= 4)

        # top perp, bot par
        if (set([0, 2, 9, 11]).issubset(bad_edges)):
            cube.rotate_seq([DOWN, RIGHT, RIGHT, LEFT, LEFT, -6, LEFT, LEFT, RIGHT, RIGHT])
            permute_edges(cube)
            return
        # top par, bot perp
        elif (set([1, 3, 8, 10]).issubset(bad_edges)):
            cube.rotate_seq([-6, RIGHT, RIGHT, LEFT, LEFT, DOWN, LEFT, LEFT, RIGHT, RIGHT])
            permute_edges(cube)
            return
        elif (len(bad_edges) == 4):
            # z-perm top
            if (set([0, 1, 2, 3]).issubset(bad_edges)):
                cube.rotate_seq([RIGHT, RIGHT, LEFT, LEFT, DOWN, LEFT, LEFT, RIGHT, RIGHT, -6])
                return
            # z-perm bot
            elif (set([8, 9, 10, 11]).issubset(bad_edges)):
                cube.rotate_seq([RIGHT, RIGHT, LEFT, LEFT, UP, RIGHT, RIGHT, LEFT, LEFT, -DOWN])
                return
            # top has three
            elif (bad_edges[2] <= 3):
                cube.rotate_seq([-6 for i in range((2 + bad_edges[3]) % 4)])
                cube.rotate_seq([DOWN for i in range((2 + bad_edges[3]) % 4)])
                if ((bad_edges[3] % 4) in bad_edges):
                    cube.rotate_seq([UP, UP])
                cube.rotate_seq([BACK, BACK])
                # now top par, bot perp
                cube.rotate_seq([-6, RIGHT, RIGHT, LEFT, LEFT, DOWN, LEFT, LEFT, RIGHT, RIGHT])
                cube.rotate_seq([BACK, BACK])
                if ((bad_edges[3] % 4) in bad_edges):
                    cube.rotate_seq([UP, UP])
                cube.rotate_seq([UP for i in range((2 + bad_edges[3]) % 4)])
                cube.rotate_seq([-DOWN for i in range((2 + bad_edges[3]) % 4)])
                return
            # bot has three
            elif (bad_edges[1] >= 8):
                # 'flip cube'
                cube.rotate_seq([RIGHT, RIGHT, LEFT, LEFT, BACK, BACK, FRONT, FRONT, UP, UP, DOWN, DOWN])
                permute_edges(cube)
                return
            # two and two
            else:
                assert(bad_edges[1] <= 3 and bad_edges[2] >= 8)
                # all overlap or no overlap
                if (set([bad_edges[2]%4, bad_edges[3]%4]).issubset(bad_edges) or
                    (not bad_edges[2]%4 in bad_edges and not bad_edges[3]%4 in bad_edges)):
                    f1 = mapping1[bad_edges[0]]
                    f2 = mapping1[bad_edges[1]]
                    cube.rotate_seq([DOWN, f1, f1, f2, f2, f1, f1, f2, f2, f1, f1, f2, f2, -DOWN]) # hand it off to some other case...
                    permute_edges(cube)
                    return
                # one overlap
                else:
                    f1 = mapping1[bad_edges[0]]
                    f2 = mapping1[bad_edges[1]]
                    spec_bool = set([(bad_edges[2] + 1) % 4, (bad_edges[2] + 1) % 4]).issubset(bad_edges)
                    cube.rotate(DOWN, spec_bool)#(bad_edges[3] + 1) % 4 == bad_edges[0])
                    cube.rotate_seq([f1, f1, f2, f2, f1, f1, f2, f2, f1, f1, f2, f2])
                    cube.rotate(DOWN, not spec_bool)#(bad_edges[3] + 1) % 4 != bad_edges[0])
                    return
        elif (len(bad_edges) == 6):
            # four in top
            if (bad_edges[3] <= 3):
                assert(bad_edges[3] == 3)
                cube.rotate_seq([RIGHT, RIGHT, LEFT, LEFT, DOWN, LEFT, LEFT, RIGHT, RIGHT, -6]) # z perm
                permute_edges(cube)
                return
            # four in bot
            elif (bad_edges[2] >= 8):
                assert(bad_edges[2] == 8)
                cube.rotate_seq([RIGHT, RIGHT, LEFT, LEFT, UP, RIGHT, RIGHT, LEFT, LEFT, -DOWN]) # z perm bot
                permute_edges(cube)
                return
            # 3 and 3
            else:
                assert(False) # we should have caught this already.
        else:
            assert(False) # we should have caught this too...



# congrats on getting to g3!
# the following functions are used to get from G3 to solved

# R2 F2 R2 F2 R2 F2
def adj_four_swap(cube, f1, f2):
    cube.rotate_seq([f1, f1, f2, f2, f1, f1, f2, f2, f1, f1, f2, f2])
# U2 M2 U2 M2
def across_four_swap(cube, swap1, swap2, m1, m2):
    cube.rotate_seq([swap1, swap1, m1, m1, m2, m2, swap1, swap1, m1, m1, m2, m2, swap1, swap1, swap2, swap2])
# like adj four swap
def t_swap(cube, stem, top, side):
    cube.rotate_seq([side, side, top, top, stem, stem, side, side, stem, stem, top, top, side, side, stem, stem])
# gives the edge number of an edge if said edge were in it's solved spot
def desired_location(cubie):
    ret = 0
    if (cubie[0] <= YELLOW):
        ret += 8 * int(cubie[0] == YELLOW) + int(cubie[1] == ORANGE) + 2 * int(cubie[1] == BLUE) + 3 * int(cubie[1] == RED)
    else:
        ret += 4 + 2 * int(cubie[0] == BLUE) + int(cubie == [GREEN, ORANGE] or cubie == [BLUE, RED])
    return ret
# gets all edges in a cycle with the edge provided. A solved edge is in a cycle
# with only itself
def getCycle(cube, edge):
    c_cubie = cube.getEdge_num(edge)
    ret = [edge]
    while (desired_location(c_cubie) != edge):
        ret.append(desired_location(c_cubie))
        c_cubie = cube.getEdge_num(desired_location(c_cubie)) # get the piece at the place where c_cubie wants to be
    return ret
# returns whether or not the edge at edge num is in it's desired location
def is_edge_solved(cube, edge_num):
    return edge_num == desired_location(cube.getEdge_num(edge_num))

# solves the cube from g3. This is done much like a domino cube, or a 180 cube
def domino_solve(cube):
    # first solve the top layer
    cycle = []
    for i in range(4):
        cycle = getCycle(cube, i)
        if (len(cycle) >= 2):
            break

    if (len(cycle) == 4):
        # front fish, backwards N, or m-ccw => bot white good, top yellow bad
        if (cycle == [0, 10, 2, 8] or cycle == [0, 8, 2, 10] or cycle == [0, 2, 10, 8]):
            across_four_swap(cube, FRONT, BACK, LEFT, RIGHT)
        # down fish, backwards Z, or m-cw => front to swap good with back, back bad
        elif (cycle == [0, 10, 8, 2] or cycle == [0, 2, 8, 10] or cycle == [0, 8, 10, 2]):
            across_four_swap(cube, UP, DOWN, LEFT, RIGHT)
        # standing (s) of first `if`
        elif (cycle == [1, 11, 3, 9] or cycle == [1, 9, 3, 11] or cycle == [1, 3, 11, 9]):
            across_four_swap(cube, LEFT, RIGHT, FRONT, BACK)
        # standing (s) of second `if`
        elif (cycle == [1, 11, 9, 3] or cycle == [1, 3, 9, 11] or cycle == [1, 9, 11, 3]):
            across_four_swap(cube, UP, DOWN, FRONT, BACK)
        else:
            assert(False)

        # now, top is not solved yet, but it is closer to being solved.
        domino_solve(cube)
        return
    elif (len(cycle) == 3):
        if (cycle[0] % 2 == 0):
            cube.rotate_seq([UP, UP, RIGHT, RIGHT, FRONT, FRONT, RIGHT, RIGHT, UP, UP, RIGHT, RIGHT, FRONT, FRONT, RIGHT, RIGHT])
        else:
            cube.rotate_seq([UP, UP, FRONT, FRONT, RIGHT, RIGHT, FRONT, FRONT, UP, UP, FRONT, FRONT, RIGHT, RIGHT, FRONT, FRONT])

        # the cube should now be in a different, easier state, or this will run ONLY once more.
        domino_solve(cube)
        return
    elif (len(cycle) == 2):
        # in the top layer only...
        if (cycle[1] <= 3):
            if (cycle[0] == 0):
                adj_four_swap(cube, UP, RIGHT)
            elif (cycle[0] == 1):
                adj_four_swap(cube, UP, FRONT)
            else:
                assert(False)
        # above its counterpart
        elif (cycle[0] == cycle[1] % 4):
            mapping = [BACK, RIGHT, FRONT, LEFT]
            # a very slight optimization
            if (desired_location(cube.getEdge_num((cycle[0] + 1)%4)) != (cycle[0] + 1) % 4):
                adj_four_swap(cube, mapping[cycle[0]], mapping[(cycle[0] + 1) % 4])
            else:
                t_swap(cube, mapping[(cycle[0] + 1) % 4], mapping[cycle[0]], UP)
        # diagonal from its counterpart
        elif (cycle[0] == (cycle[1] + 2) % 4):
            cube.rotate_seq([DOWN, DOWN])
            mapping = [BACK, RIGHT, FRONT, LEFT]
            # a very slight optimization
            if (desired_location(cube.getEdge_num((cycle[0] + 1)%4)) != (cycle[0] + 1) % 4):
                adj_four_swap(cube, mapping[cycle[0]], mapping[(cycle[0] + 1) % 4])
            else:
                t_swap(cube, mapping[(cycle[0] + 1) % 4], mapping[cycle[0]], UP)
            cube.rotate_seq([DOWN, DOWN])
        else:
            assert(False)

        # top is now closer to being solved.
        domino_solve(cube)
        return
    else:
        assert(len(cycle) == 1)

    # now solve bottom
    cycle = []
    for i in range(8, 12):
        cycle = getCycle(cube, i)
        if (len(cycle) >= 2):
            break

    if (len(cycle) == 2):
        if (cycle[0] == 8):
            adj_four_swap(cube, DOWN, LEFT)
        elif (cycle[0] == 9):
            adj_four_swap(cube, DOWN, FRONT)
        else:
            assert(False)
        # bot is closer, but not done
        domino_solve(cube)
        return
    else:
        assert(len(cycle) == 1)

    # now solve middle layer!
    cycle = []
    for i in range(4, 8):
        cycle = getCycle(cube, i)
        if (len(cycle) >= 2):
            break

    if (len(cycle) == 2):
        if (cycle[0] == 4 and cycle[1] == 5):
            across_four_swap(cube, BACK, FRONT, UP, DOWN)
        elif (cycle[0] == 4 and cycle[1] == 7):
            across_four_swap(cube, LEFT, RIGHT, UP, DOWN)
        elif (cycle[0] == 4 and cycle[1] == 6):
            across_four_swap(cube, LEFT, RIGHT, UP, DOWN)
        else:
            assert(False)
        # cube is now very close to being solved, although not necessarily solved just yet...
        domino_solve(cube)
        return
    elif (len(cycle) == 3):
        cube.rotate_seq([UP, UP, FRONT, FRONT, UP, UP, RIGHT, RIGHT, UP, UP, FRONT, FRONT, UP, UP, RIGHT, RIGHT])
        # now this should run only once more, if that
        domino_solve(cube)
        return
