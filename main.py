import random

board_size = 3


def copy(arr):
    result = []
    for row in range(len(arr)):
        r = []
        for col in range(len(arr[row])):
            r.append(arr[row][col])

        result.append(r)

    return result


def generate_initial_state():
    arr = []
    for row in range(board_size):
        nested = []
        for col in range(board_size):
            nested.append(0)

        arr.append(nested)

    for column in range(board_size):
        row = random.randrange(0, board_size)
        arr[row][column] = 1

    return arr


def have_this_conflict_pair_already(arr, row1, col1, row2, col2):
    return f"{row1},{col1};{row2},{col2}" in arr or f"{row2},{col2};{row1},{col1}" in arr


def get_num_of_horizontal_conflicts(arr):
    num_of_conflicts = 0

    for row in range(len(arr)):
        for col in range(len(arr[row])):
            if arr[row][col] == 1 and col < len(arr[row]) - 1:
                for c in range(col + 1, len(arr[row])):
                    if arr[row][c] == 1:
                        num_of_conflicts += 1
                        break

    return num_of_conflicts


def get_num_of_vertical_conflicts(arr):
    num_of_conflicts = 0

    for col in range(len(arr[0])):
        for row in range(len(arr)):
            if arr[row][col] == 1 and row < len(arr) - 1:
                for r in range(row + 1, len(arr)):
                    if arr[r][col] == 1:
                        num_of_conflicts += 1
                        break

    return num_of_conflicts


def get_num_of_diagonal_conflicts(arr):
    num_of_conflicts = 0

    for row in range(len(arr)):
        r = row
        c = 0
        while r < len(arr) and c < len(arr[row]):
            if arr[r][c] == 1:
                r2 = r + 1
                c2 = c + 1

                while r2 < len(arr) and c2 < len(arr[row]):
                    if arr[r2][c2] == 1:
                        num_of_conflicts += 1
                        break

                    r2 += 1
                    c2 += 1

            r += 1
            c += 1

    for col in range(1, len(arr[0])):
        r = 0
        c = col
        while r < len(arr) and c < len(arr[0]):
            if arr[r][c] == 1:
                r2 = r + 1
                c2 = c + 1
                while r2 < len(arr) and c2 < len(arr[0]):
                    if arr[r2][c2] == 1:
                        num_of_conflicts += 1
                        break

                    r2 += 1
                    c2 += 1

            r += 1
            c += 1

    return num_of_conflicts


def has_reached_goal(arr):
    num_of_conflicts = 0


def pretty_print(arr):
    for row in range(len(arr)):
        print(arr[row])


if __name__ == '__main__':
    board = generate_initial_state()
    print("Initial state:")
    pretty_print(board)
    print(get_num_of_horizontal_conflicts(board))
    print(get_num_of_vertical_conflicts(board))
    print(get_num_of_diagonal_conflicts(board))
