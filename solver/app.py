from flask import Flask
from z3 import And, Bool, Int, Or, solve


def is_valid(*data: str):
    x = []
    for i in range(0, 9):
        if data[i].isnumeric():
            x[i] = int(data[i])
        else:
            x[i] = Int(data[i])

    and_args = []
    for d in range(0, 9):
        or_args = []
        for i in range(0, 9):
            or_args.append(Bool(x[i] == d))
        and_args.append(Or(*or_args))

    return And(*and_args)


def solve_sudoku(sudoku):
    rows_check = []
    for i in range(0, 9):
        rows_check.append(is_valid(sudoku[i, 0], sudoku[i, 1], sudoku[i, 2],
                                   sudoku[i, 3], sudoku[i, 4], sudoku[i, 5],
                                   sudoku[i, 6], sudoku[i, 7], sudoku[i, 8]))
    columns_check = []
    for i in range(0, 9):
        columns_check.append(is_valid(sudoku[0, i], sudoku[1, i], sudoku[2, i],
                                      sudoku[3, i], sudoku[4, i], sudoku[5, i],
                                      sudoku[6, i], sudoku[7, i], sudoku[8, i]))
    squares_check = []
    for i in range(0, 9, step=3):
        for j in range(0, 9, step=3):
            squares_check.append(is_valid(sudoku[i, j], sudoku[i, j + 1], sudoku[i, j + 2],
                                          sudoku[i + 1, j], sudoku[i + 1, j + 1], sudoku[i + 1, j + 2],
                                          sudoku[i + 2, j], sudoku[i + 2, j + 1], sudoku[i + 2, j + 2]))

    return solve(And(And(*rows_check), And(*columns_check), And(*squares_check)))


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Oh-h-h...it's T-o-C......."