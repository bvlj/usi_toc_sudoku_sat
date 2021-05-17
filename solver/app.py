from flask import Flask
from flask import request
from flask import render_template
import numpy as np
from z3 import And, Bool, Int, Or, Solver, unsat, unknown
from flask import jsonify

def is_valid(*data: str):
    x = []
    for i in range(0, 9):
        if data[i].isnumeric():
            x.append(int(data[i]))
        else:
            x.append(Int(data[i]))

    and_args = []
    for d in range(0, 9):
        or_args = []
        for i in range(0, 9):
            if type(x[i]) == int:
                or_args.append(Bool(x[i] == d))
            else:
                or_args.append(x[i] == d)
        and_args.append(Or(*or_args))

    return And(*and_args)


def solve_sudoku(sudoku):
    rows_check = []
    for i in range(0, 9):
        print(rows_check)
        rows_check.append(is_valid(sudoku[i][0], sudoku[i][1], sudoku[i][2],
                                   sudoku[i][3], sudoku[i][4], sudoku[i][5],
                                   sudoku[i][6], sudoku[i][7], sudoku[i][8]))
    columns_check = []
    for i in range(0, 9):
        columns_check.append(is_valid(sudoku[0][i], sudoku[1][i], sudoku[2][i],
                                      sudoku[3][i], sudoku[4][i], sudoku[5][i],
                                      sudoku[6][i], sudoku[7][i],
                                      sudoku[8][i]))
    squares_check = []
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            squares_check.append(is_valid(sudoku[i][j], sudoku[i][j + 1],
                                          sudoku[i][j + 2], sudoku[i + 1][j],
                                          sudoku[i + 1][j + 1],
                                          sudoku[i + 1][j + 2],
                                          sudoku[i + 2][j],
                                          sudoku[i + 2][j + 1],
                                          sudoku[i + 2][j + 2]))
    s = Solver()
    s.add(And(And(*rows_check), And(*columns_check), And(*squares_check),
        Bool("k!0" == ))
    r = s.check()
    if r == unsat or r == unknown:
        return {"solution": False}
    else:
        m = s.model()
        ihavethesolution = {}
        for d in m:
            if str(d)[0] != "x":
                continue
            ihavethesolution[str(d)] = str(m[d])
        return {"solution": True, "model": ihavethesolution}


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('base.html')


@app.route('/solve_sudoku', methods=['POST'])
def rossya():
    print("\n\n\n\n\n\n\n\n\n")
    board = [x.split(',') for x in request.args.get('board').split(';')]
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if not board[i][j]:
                board[i][j] = "x%d%d" % (i, j)
    ihavethesolution = solve_sudoku(board)
    return jsonify(ihavethesolution)
