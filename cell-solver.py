#!/usr/bin/python3
from dataclasses import dataclass

X_SIZE = 7
Y_SIZE = 12


@dataclass(order=True)
class OuterState:
    visited: frozenset
    found_words: tuple

    def getTopLeft(self):
        for x in range(X_SIZE):
            for y in range(Y_SIZE):
                if (x, y) not in self.visited:
                    return (x, y)


def getWord(squares, board):
    return "".join(
        [
            board[y][x]
            for (x, y) in sorted(squares, key=lambda coords: (coords[1], coords[0]))
        ]
    )


def getValidNeighbors(square, visited):
    x, y = square
    return filter(
        lambda new_square: isInbounds(new_square) and new_square not in visited,
        [
            (delta_x + x, delta_y + y)
            for (delta_x, delta_y) in ((-1, 0), (0, -1), (0, 1), (1, 0))
        ],
    )


def isInbounds(square):
    x, y = square
    return x >= 0 and x < X_SIZE and y >= 0 and y < Y_SIZE


def pretty_print(grid):
    for row in grid:
        print(" ".join(row))


def solve(board, words):
    words = frozenset(
        filter(
            lambda word: len(word) >= 4 and len(word) <= 8,
            [word.upper() for word in words],
        )
    )
    print("Words: ", len(words), "Board: ")
    pretty_print(board)

    # Start with the initial state as the one outer_candidate:
    # Nothing visited, nothing found
    # 1. Pop an outer_candidate from the queue
    # 2. Check the outer candidate
    #    - if all squares are visited, return the found words as the solution
    # 3. Create initial inner candidate: Find the top-leftmost open square and create
    # an inner_candidate there
    # 4. Do the inner loop on inner candidates. Inner loop:
    #   a) if 4-8 letters, check against the dictionary.
    #      If match, create an outer candidate from the inner candidate
    # 	b) if <8 letters, add each of its neighbors that is not already visited
    # 5.  If there are outer candidates remaining, go to 1. If we've run out, we failed

    outer_queue = [OuterState(set(), [])]
    outer_candidate_counter = 0
    inner_candidate_counter = 0
    while len(outer_queue) > 0:
        current_outer = outer_queue.pop()
        outer_candidate_counter += 1
        # if outer_candidate_counter % 1 ==0:
        # 	print("outer candidate: ", outer_candidate_counter, "inner candidate: ", inner_candidate_counter)
        # 	print("outer_tried:", len(outer_tried))
        # 	print("Squares visited: ", len(current_outer.visited), " words so far:", current_outer.found_words)
        if len(current_outer.visited) == X_SIZE * Y_SIZE:
            return current_outer.found_words
        starting_square = current_outer.getTopLeft()
        first_inner = frozenset({starting_square})
        inner_tried = set({first_inner})
        inner_queue = [first_inner]
        while len(inner_queue) > 0:
            inner_candidate_counter += 1
            current_inner = inner_queue.pop()
            # if inner_candidate_counter % 100000 == 0:
            # 	print("inner_candidate:", inner_candidate_counter, "inner_queue:", len(inner_queue), "inner_tried: ", len(inner_tried))
            word = getWord(current_inner, board)
            if word in words:
                # print("Found word: ", word)
                new_outer = OuterState(
                    current_outer.visited.union(current_inner),
                    current_outer.found_words + [word],
                )
                outer_queue.append(new_outer)
            if len(current_inner) < 8:
                for square in current_inner:
                    for neighbor in getValidNeighbors(square, current_outer.visited):
                        new_inner = current_inner.union(set({neighbor}))
                        if new_inner not in inner_tried:
                            inner_queue.append(new_inner)
                            inner_tried.add(new_inner)
    return None


def main():
    board = [list(row.strip()) for row in open("board1.txt")]
    words = [row.strip() for row in open("words.txt")]
    result = solve(board, words)
    if result is None:
        print("Failed to find a solution")
    else:
        print("Found a solution using words: ", result)


if __name__ == "__main__":
    main()
