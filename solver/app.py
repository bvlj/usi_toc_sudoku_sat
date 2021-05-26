import math

from flask import Flask, jsonify, render_template, request
from z3 import And, Int, Or, Solver, sat


def is_valid(max_val: int, *data: str):
    """
    Create SAT condition that ensures
    all the entries in the data array are
    different from one another (supports
    mixed pre-filled and unknown variables)
    """
    x = []
    n = len(data)
    for i in range(0, n):
        if data[i].isnumeric():
            x.append(int(data[i]))
        else:
            x.append(Int(data[i]))

    and_args = []
    for d in range(0, max_val):
        or_args = []
        for i in range(0, n):
            or_args.append(x[i] == d)
        and_args.append(Or(*or_args))

    return And(*and_args)


def build_sudoku_solver(board, n):
    """
    Return a solver for a
    given sudoku board
    """
    rows_check = []
    for i in range(0, n):
        rows_check.append(is_valid(n, *board[i]))

    columns_check = []
    for i in range(0, n):
        args = []
        for j in range(0, n):
            args.append(board[j][i])
        columns_check.append(is_valid(n, *args))

    squares_check = []
    size_box = int(math.sqrt(n))
    for i in range(0, n, size_box):
        for j in range(0, n, size_box):
            args = []
            for q in range(0, size_box):
                for w in range(0, size_box):
                    args.append(board[i + q][j + w])
            squares_check.append(is_valid(n, *args))

    s = Solver()
    s.add(And(And(*rows_check), And(*columns_check), And(*squares_check)))
    return s


app = Flask(__name__)


@app.route("/")
def app_base():
    return render_template("base.html")


@app.route("/solve_sudoku", methods=["POST"])
def app_solve():
    # Read the sudoku board from url arguments
    board = [x.split(",") for x in request.args.get("board").split(";")]
    n = len(board)
    for i in range(0, n):
        for j in range(0, n):
            if not board[i][j]:
                # Make a new unknown variable
                board[i][j] = "x%dy%d" % (i, j)
            else:
                # Pre-filled cell
                board[i][j] = str(int(board[i][j]) - 1)

    # Build the solver
    solver = build_sudoku_solver(board, n)

    if solver.check() == sat:
        solution = {}
        model = solver.model()

        # Build a solution matrix from the SAT model
        for item in model:
            key = str(item)
            value = int(str(model[item])) + 1
            solution[key] = value

        print("Satisfiable", solution)
        return jsonify({"sat": True, "model": solution})
    else:
        print("Unsatisfiable")
        return jsonify({"sat": False})
