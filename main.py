import random
import time
import os, psutil

board_size = 8
depth_level = 0
cycles_made = 0
generated = []
start_time = 0
max_mb_use = 512
max_time_allowed_to_run = 30 * 60 * 1000
num_of_previous_states = 0
found_solution = False


def current_milli_time():
    return round(time.time() * 1000)


def copy(arr):
    result = []
    for row in range(len(arr)):
        r = []
        for col in range(len(arr[row])):
            r.append(arr[row][col])

        result.append(r)

    return result


def check_unique(b):
    result = False

    if len(generated) == 0:
        result = True

    for board in generated:
        for row in range(len(b)):
            for col in range(len(b[row])):
                if b[row][col] != board[row][col]:
                    result = True

    if result:
        generated.append(b)


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


def get_num_of_diagonal_conflicts_right(arr):
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


def get_num_of_diagonal_conflicts_left(arr):
    num_of_conflicts = 0

    for row in range(len(arr)):
        r = row
        c = board_size - 1
        while r < len(arr) and c < len(arr[row]):
            if arr[r][c] == 1:
                r2 = r + 1
                c2 = c - 1

                while r2 < len(arr) and c2 >= 0:
                    if arr[r2][c2] == 1:
                        num_of_conflicts += 1
                        break

                    r2 += 1
                    c2 -= 1

            r += 1
            c -= 1

    for col in range(board_size - 2, 0, -1):
        r = 0
        c = col
        while r < len(arr) and c >= 0:
            if arr[r][c] == 1:
                r2 = r + 1
                c2 = c - 1
                while r2 < len(arr) and c2 >= 0:
                    if arr[r2][c2] == 1:
                        num_of_conflicts += 1
                        break

                    r2 += 1
                    c2 -= 1

            r += 1
            c -= 1

    return num_of_conflicts


def get_number_of_conflicts(arr):
    return get_num_of_horizontal_conflicts(arr) \
           + get_num_of_vertical_conflicts(arr) \
           + get_num_of_diagonal_conflicts_right(arr) \
           + get_num_of_diagonal_conflicts_left(arr)


def has_reached_goal(arr):
    return get_number_of_conflicts(arr) == 0


def pretty_print(arr):
    for row in range(len(arr)):
        print(arr[row])


def solve_board(board):
    global found_solution, cycles_made, start_time, depth_level, num_of_previous_states

    generated_states = [board]

    while not found_solution:
        print(f"Entering depth level {depth_level}")
        new_states = []

        for state in generated_states:
            if current_milli_time() - start_time > max_time_allowed_to_run:
                print("Reached max time use. Closing")
                return

            mb_used = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2

            if mb_used > max_mb_use:
                print("Reached max memory use. Closing")
                return

            if has_reached_goal(state):
                found_solution = True
                print(
                    f"Found a solution! Cycles made: {cycles_made}. States in memory: {len(new_states)}. Total states: {len(new_states) + num_of_previous_states}")
                pretty_print(state)
                return

            new_states.extend(generate_states(state))

        num_of_previous_states += len(generated_states)
        generated_states.clear()
        generated_states.extend(new_states)
        depth_level += 1


def generate_states(board):
    global cycles_made
    result = []

    for col in range(len(board[0])):
        for row in range(len(board)):
            if board[row][col] == 1:
                # found a queen in this column
                for r in range(len(board)):
                    if board[r][col] == 0:
                        # found an empty spot
                        board_copy = copy(board)
                        board_copy[r][col] = 1
                        board_copy[row][col] = 0
                        result.append(board_copy)
                        cycles_made += 1

    return result


def main():
    global start_time
    start_time = current_milli_time()
    found_good_initial_state = False

    while not found_good_initial_state:
        board = generate_initial_state()
        found_good_initial_state = not has_reached_goal(board) and get_number_of_conflicts(board) == 1

        if found_good_initial_state:
            print("Initial state:")
            pretty_print(board)
            print(f"Found {get_number_of_conflicts(board)} conflicts")
            print("Is winning position: " + str(has_reached_goal(board)))
            solve_board(board)


if __name__ == '__main__':
    main()
