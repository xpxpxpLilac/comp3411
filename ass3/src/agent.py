#!/usr/bin/python3

import socket
import sys
# import numpy as np
import algo as ALGO
#import MCTS as MCTS
import MCTS_ALGO as MCTS
##### QUESTION ######
# Briefly describe how your program works
# algorithms and data structures employed
# All the algorithm is in file algo.py
# The algorithm we used is alpha-beta minimax pruning with a heuristic function
# For board representation, we used a 2D array to conclude the gameboard
# valid positions are from index 1-9 in rows and columns
# because it is easy to update the board corresponding to real raw board.
# We save all the winning conditions in general in WINNING_CON, for example, in a subboard
# if position 1, 2, 3 are captured by a player, this player wins the game, so WINNING_CON[0] = [1, 2, 3]
# And then we store winning condition for each position in a 9 * 9 board.
# For example, at position 1 in a subboard, the winning condition should be either [1,2,3] or [1,4,6] or [1,5,9]
# This is exactly what we store in DO_SLOT_WINNING_CON[0](for index in this array should be position-1)
# We also save central positions in MIDDLES and corner positions in CORNERS in advance, which are prepared for heuristic
# For heuristic function, we first find available slots, 
# and check each slots with DO_SLOT_WINNING_CON to see whether it can lead to a winning
# if YES, we give it a prettyb high score and change game status to WIN to true
# if not, we check if it is two same symbols, if it is ours, we give positive mark, if not we give negative mark 
# then if it is a block(2 oppoent's 1 ours, vice versa), we give postive for oppoent blocked, and negative mark for us blocked
# then if it is one symbol from each player, we just give small reward 
# explain any design decisions you made along the way. 


# board representation:
#   0 - Empty
#   1 - We played here
#   -1 - They played here

PLAYER1 = 1
PLAYER2 = -1
def newBoard():
	c = []
	for i in range(10):
		column = []
		for j in range(10):
			column.append(0)
		c.append(column)
	return c
boards = newBoard()
s = [".","O","X"]
curr = 0 # this is the current board to play in

# print a row
# This is just ported from game.c
def print_board_row(board, a, b, c, i, j, k):
    print(" "+s[board[a][i]]+" "+s[board[a][j]]+" "+s[board[a][k]]+" | " \
             +s[board[b][i]]+" "+s[board[b][j]]+" "+s[board[b][k]]+" | " \
             +s[board[c][i]]+" "+s[board[c][j]]+" "+s[board[c][k]])

# Print the entire board
# This is just ported from game.c
def print_board(board):
    print_board_row(board, 1,2,3,1,2,3)
    print_board_row(board, 1,2,3,4,5,6)
    print_board_row(board, 1,2,3,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 4,5,6,1,2,3)
    print_board_row(board, 4,5,6,4,5,6)
    print_board_row(board, 4,5,6,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 7,8,9,1,2,3)
    print_board_row(board, 7,8,9,4,5,6)
    print_board_row(board, 7,8,9,7,8,9)
    print()

# choose a move to play
def play(last_slot):
    print_board(boards)
    print("Last move is " + str(last_slot))
#    n = ALGO.our_move(boards, last_slot)
    n = MCTS.MCTS(boards, last_slot)
    print('our move is '+ str(n))
    # print("playing", n)
    place(curr, n, PLAYER1)
    return n

# place a move in the global boards
def place(board, num, player):
    global curr
    curr = num
    boards[board][num] = player

# read what the server sent us and
# only parses the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    if command == "second_move":
        print("====================== WE ARE PLAYING O ======================")
        place(int(args[0]), int(args[1]), PLAYER2)
        return play(curr)
    elif command == "third_move":
        print("====================== WE ARE PLAYING O ======================")
        # place the move that was generated for us
        place(int(args[0]), int(args[1]), PLAYER1)
        # place their last move
        place(curr, int(args[2]), PLAYER2)
        return play(curr)
    elif command == "next_move":
        place(curr, int(args[0]), PLAYER2)
        return play(curr)
    elif command == "win":
        print("Yay!! We win!! :)")
        return -1
    elif command == "loss":
        print("We lost :(")
        return -1
    elif command == "draw":
        print("It's a tie game :|")
        return -1
    return 0

# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()
