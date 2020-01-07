#!/usr/bin/python3
from random import randint

DEPTH_LIMIT = 2
VERY_LARGE = 2000000

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
# A "slot" is a space for a mark, 'X' or 'O' or '.'
# winning condition traid
WINNING_CON = [
	[1, 2, 3],
	[4, 5, 6],
	[7, 8, 9],
	[1, 4, 7],
	[2, 5, 8],
	[3, 6, 9],
	[1, 5, 9],
	[3, 5, 7] 
]

# the potentially-winning-triads at each position
DO_SLOT_WINNING_CON = [
	[WINNING_CON[0], WINNING_CON[3], WINNING_CON[6]],
	[WINNING_CON[0], WINNING_CON[4]],
	[WINNING_CON[0], WINNING_CON[5], WINNING_CON[7]],
	[WINNING_CON[1], WINNING_CON[3]],
	[WINNING_CON[1], WINNING_CON[4], WINNING_CON[6], WINNING_CON[7]],
	[WINNING_CON[1], WINNING_CON[5]],
	[WINNING_CON[2], WINNING_CON[3], WINNING_CON[7]],
	[WINNING_CON[2], WINNING_CON[4]],
	[WINNING_CON[2], WINNING_CON[5], WINNING_CON[6]]
]

# corner in the sub-boards
CORNER_INDEXES = [1, 3, 7, 9]

# CORNERS = np.zeros((10, 10), dtype="int8")
CORNERS = newBoard()
for i in range(1,10):
    for j in CORNER_INDEXES:
        CORNERS[i][j] = 1

# a middle position in a sub-board.
# MIDDLES = np.zeros((10, 10), dtype="int8")
MIDDLES = newBoard()
for i in range(1,10):
	MIDDLES[i][5] = 1

# A single move's heuristic value. 
# Gives smaller, possibly negative values to 'X' (-1) player
# Gives larger, possibly positive values to 'O' (1) player.
#
#  Actually returns an array of length 2, ret[0] is heuristic value,
# ret[1] = true if someoe won, false if someone lost.
#
def heuristic(board, last_slot, slot, depth):

	win = False  
	score = 0

	slot_in_array = slot - 1

	for triad in DO_SLOT_WINNING_CON[slot_in_array]:

		triad_sum = board[last_slot][triad[0]]+ board[last_slot][triad[1]] + board[last_slot][triad[2]]

		if triad_sum == -3 or triad_sum == 3:
			score = board[last_slot][triad[0]] * VERY_LARGE - depth
			win = True
		if triad_sum == 2:
			score += 3000  
		if triad_sum == -2:
			score -= 3000  
		if triad_sum == 1 or triad_sum == -1:
			if board[last_slot][triad[0]] != 0 or board[last_slot][triad[1]] != 0 or board[last_slot][triad[2]] != 0:
				if triad_sum == 1:
					score -= triad_sum * 1000
				if triad_sum == -1:
					score +=  triad_sum * 1000  
		if triad_sum == 0:  
			score += board[last_slot][slot]

		if win: 
			break

	if not win:
		bonus = 7 * MIDDLES[last_slot][slot] +  2 * CORNERS[last_slot][slot]
		score += board[last_slot][slot] * bonus

	return [score, win]



# Alpha-Beta minimaxing.
def alphabeta(board, last_slot, player, next_player, alpha, beta, depth, score_so_far, last_move_won):

	if last_move_won or depth >= DEPTH_LIMIT:
		return score_so_far


	for slot in range(1,10):
		if board[last_slot][slot] == 0:
			board[last_slot][slot] = player
			rets = heuristic(board, last_slot, slot, depth)
			val = alphabeta(board, slot, next_player, player, alpha, beta, depth + 1, score_so_far + rets[0], rets[1])
			board[last_slot][slot] = 0

			if player == PLAYER1:
				# Maximizing player, we play
				if val > alpha: 
					alpha = val
			if player == PLAYER2:
				# Minimizing player, opponent plays
				if val < beta: 
					beta = val

			if beta <= alpha:
				break

	score = beta
	if player == PLAYER1:
		score = alpha

	return score



# Figure out the our next move, based on the current board and the last "slot" (last_slot argument),
# Returns a single numerical value
def our_move(board, last_slot):


	my_moves = []
	best_val = -VERY_LARGE*10 - DEPTH_LIMIT

	for slot in range(1,10):

		if board[last_slot][slot] == 0:
			board[last_slot][slot] = 1
			rets = heuristic(board, last_slot, slot, 0)
			val = alphabeta(board, slot, -1, 1, -(VERY_LARGE+DEPTH_LIMIT)-1, VERY_LARGE+DEPTH_LIMIT+1, 1, rets[0], rets[1])
			board[last_slot][slot] = 0
			if val > best_val:
				best_val = val
				my_moves = [[last_slot,slot]]
			elif val == best_val:
				my_moves.append([last_slot,slot])

	recommend = my_moves[0][1]
	if len(my_moves) > 1:
		x = randint(1,2000)
		x = x % len(my_moves)
		recommend = my_moves[x][1]

	return recommend

	# if __name__ == "__main__":
		# our_move(board,last_slot)