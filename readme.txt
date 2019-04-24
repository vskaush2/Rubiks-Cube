Requirements:
 - Python
 - NumPy

If you do not have python, shame on you!
If you do not have NumPy, run the following command in your favorite terminal:
`pip install numpy`


HOW TO RUN

tl;dr:
In this directory (in a terminal) run:

`python main.py`

----

This will run the program. First, it will generate a scramble. Then, it will
print out all of the generated algorithms to get from subgroup to subgroup.
If you'd like to test it on a real cube, you'll have to provide it with a
scramble. In that case, replace the lines that look like this

<code>
for i in range(24):
    cube.rotate(randint(0, 5), randint(0, 1))
</code>

in `main.py` with the following line:

<code>
cube.rotate_seq([YOUR SCRAMBLE HERE])
</code>

Your scramble should look something like this (for reference):

[DOWN, UP, LEFT, RIGHT, -FRONT, -6, BACK]

Note that negative commands mean prime, and -6 means UP prime. (UP is
represented as 0 in the code, so -0 wouldn't distinguish it from 0. Thus, -6 was
chosen as a representation).
