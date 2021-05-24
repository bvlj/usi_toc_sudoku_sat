from flask import Flask, jsonify, render_template, request
from z3 import And, Int, Or, Solver, sat


def is_valid(*data: str):
    """
    Create SAT condition that ensures
    all the entries in the data array are
    different from one another (supports
    mixed pre-filled and unknown variables)
    """
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
            or_args.append(x[i] == d)
        and_args.append(Or(*or_args))

    return And(*and_args)


def build_sudoku_solver(board):
    """
    Return a solver for a
    given sudoku board
    """
    rows_check = []
    for i in range(0, 9):
        rows_check.append(is_valid(board[i][0], board[i][1], board[i][2],
                                   board[i][3], board[i][4], board[i][5],
                                   board[i][6], board[i][7], board[i][8]))
    columns_check = []
    for i in range(0, 9):
        columns_check.append(is_valid(board[0][i], board[1][i], board[2][i],
                                      board[3][i], board[4][i], board[5][i],
                                      board[6][i], board[7][i],
                                      board[8][i]))
    squares_check = []
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            squares_check.append(is_valid(board[i][j], board[i][j + 1],
                                          board[i][j + 2], board[i + 1][j],
                                          board[i + 1][j + 1],
                                          board[i + 1][j + 2],
                                          board[i + 2][j],
                                          board[i + 2][j + 1],
                                          board[i + 2][j + 2]))

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
                board[i][j] = "x%d%d" % (i, j)
            else:
                # Pre-filled cell
                board[i][j] = str(int(board[i][j]) - 1)

    # Build the solver
    solver = build_sudoku_solver(board)

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
