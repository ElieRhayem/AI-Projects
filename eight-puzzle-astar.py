# Rodolph EL Khoury - 222199
# Elie Rhayem - 222555

import numpy as np
from queue import PriorityQueue
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import itertools

class EightPuzzle:
    def __init__(self, initial_state):
        self.state = np.array(initial_state)
        self.blank_pos = np.argwhere(self.state == 0)[0]

    def move(self, direction):
        row, col = self.blank_pos
        if direction == 'up' and row > 0:
            self._swap((row, col), (row - 1, col))
        elif direction == 'down' and row < 2:
            self._swap((row, col), (row + 1, col))
        elif direction == 'left' and col > 0:
            self._swap((row, col), (row, col - 1))
        elif direction == 'right' and col < 2:
            self._swap((row, col), (row, col + 1))

    def _swap(self, pos1, pos2):
        self.state[tuple(pos1)], self.state[tuple(pos2)] = self.state[tuple(pos2)], self.state[tuple(pos1)]
        self.blank_pos = pos2

    def is_solved(self):
        return np.array_equal(self.state, np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]]))

    def copy(self):
        return EightPuzzle(self.state.copy())

    def legal_moves(self):
        row, col = self.blank_pos
        moves = []
        if row > 0:
            moves.append('up')
        if row < 2:
            moves.append('down')
        if col > 0:
            moves.append('left')
        if col < 2:
            moves.append('right')
        return moves

    def result(self, move):
        new_puzzle = self.copy()
        new_puzzle.move(move)
        return new_puzzle

    def __eq__(self, other):
        return np.array_equal(self.state, other.state)

    def __hash__(self):
        return hash(self.state.tobytes())

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.state]) + '\n'
    
def update_display(puzzle, ax):
    ax.clear()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)

    for i in range(3):
        for j in range(3):
            value = puzzle.state[2 - i][j]
            label = '' if value == 0 else str(value)
            ax.text(j + 0.5, i + 0.5, label, ha='center', va='center', fontsize=45, fontweight='bold',
                    bbox=dict(facecolor='lightgray' if value == 0 else 'white', 
                              edgecolor='black', boxstyle='round,pad=0.6', linewidth=2))

    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.1)
    plt.draw()

def on_click(event, puzzle, ax, solution_moves, step_counter):
    if step_counter[0] < len(solution_moves):
        move = solution_moves[step_counter[0]]
        puzzle.move(move)
        update_display(puzzle, ax)
        step_counter[0] += 1

def manual_animation_with_button(puzzle_initial_state, solution_moves):
    fig, ax = plt.subplots(figsize=(5, 5))

    ax_next = plt.axes([0.8, 0.02, 0.15, 0.07])
    next_btn = Button(ax_next, 'Next')

    puzzle = EightPuzzle(puzzle_initial_state.copy())

    step_counter = [0]

    next_btn.on_clicked(lambda event: on_click(event, puzzle, ax, solution_moves, step_counter))

    update_display(puzzle, ax)
    plt.show()

def is_solvable(puzzle_state):
    puzzle_flat = [tile for row in puzzle_state for tile in row if tile != 0]

    inversions = 0
    for i in range(len(puzzle_flat)):
        for j in range(i + 1, len(puzzle_flat)):
            if puzzle_flat[i] > puzzle_flat[j]:
                inversions += 1

    blank_row = next(row for row in range(3) if 0 in puzzle_state[row])
    return inversions % 2 == 0

def manhattan_distance(puzzle):
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    distance = 0
    for i in range(3):
        for j in range(3):
            if puzzle.state[i, j] != 0:
                goal_pos = np.argwhere(goal_state == puzzle.state[i, j])[0]
                distance += abs(i - goal_pos[0]) + abs(j - goal_pos[1])
    return distance

def misplaced_tiles(puzzle):
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    return np.sum(puzzle.state != goal_state) - 1

def euclidean_distance(puzzle):
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    distance = 0.0
    for i in range(3):
        for j in range(3):
            if puzzle.state[i, j] != 0:
                goal_pos = np.argwhere(goal_state == puzzle.state[i, j])[0]
                distance += np.sqrt((i - goal_pos[0]) ** 2 + (j - goal_pos[1]) ** 2)
    return distance

def no_heuristic(puzzle):
    return 0

def a_star_solve(puzzle, heuristic):
    frontier = PriorityQueue()
    counter = itertools.count()
    frontier.put((0, next(counter), puzzle.copy(), []))
    explored = set()
    explored_nodes = 0

    while not frontier.empty():
        f, _, current_puzzle, moves = frontier.get()

        if current_puzzle.is_solved():
            return moves, explored_nodes

        current_state_tuple = tuple(current_puzzle.state.flatten())
        if current_state_tuple not in explored:
            explored.add(current_state_tuple)
            explored_nodes += 1

            for move in current_puzzle.legal_moves():
                new_puzzle = current_puzzle.result(move)
                new_moves = moves + [move]
                g = len(new_moves)
                h = heuristic(new_puzzle)
                f_new = g + h
                frontier.put((f_new, next(counter), new_puzzle, new_moves))

    return [], explored_nodes

def run_experiments(initial_state, heuristics):
    results = []

    for heuristic_name, heuristic_function in heuristics.items():
        puzzle = EightPuzzle(initial_state)
        solution_moves, explored_nodes = a_star_solve(puzzle, heuristic_function)
        
        results.append({
            "heuristic": heuristic_name,
            "moves": len(solution_moves),
            "explored_nodes": explored_nodes,
            "solution": solution_moves
        })

    return results

if __name__ == "__main__":
    heuristics = {
        "Manhattan Distance": manhattan_distance,
        "Misplaced Tiles": misplaced_tiles,
        "Euclidean Distance": euclidean_distance,
        "Uniform Cost Search (UCS)": no_heuristic
    }

    initial_configs = [
        [[8, 0, 6], [5, 4, 7], [2, 3, 1]],
        [[1, 2, 3], [4, 5, 6], [8, 7, 0]],
        [[8, 7, 6], [5, 4, 3], [2, 1, 0]],
    ]

    for config_num, initial_state in enumerate(initial_configs):
        print(f"\n=== Experiment with Initial Configuration {config_num + 1} ===")
        if is_solvable(initial_state):
            for heuristic_name, heuristic_func in heuristics.items():
                print(f"\nUsing Heuristic: {heuristic_name}")
                experiment_results = run_experiments(initial_state, {heuristic_name: heuristic_func})

                for result in experiment_results:
                    print(f"Heuristic: {result['heuristic']}")
                    print(f"Moves required: {result['moves']}")
                    print(f"Explored Nodes: {result['explored_nodes']}")
                    print(f"Solution Path: {result['solution']}")
                    manual_animation_with_button(initial_state, result["solution"])
        else:
            print("Not solvable\n")
