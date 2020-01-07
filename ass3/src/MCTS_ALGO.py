#!/usr/bin/python3
import math
import random
from random import randint
import time
import multiprocessing

PLAYER1 = 1
PLAYER2 = -1
DRAW = -2
UNTOUCHED = -3
IN_PROGRESS = 0
MAX_SAFE_INTEGER = 1000000
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

class TreeNode(object):
	"""A node in the MCTS tree. Each node keeps track of its own value Q,
	prior probability P, and its visit-count-adjusted prior score u. subboard: next step board to go
	"""

	def __init__(self, parent, player, board, subboard):
		self._parent = parent
		#current player
		self._player = player
		self._children = {}  # a map from action to TreeNode
		self._visitCount = 0
		self._winScore = 0
		self._boardState = copyBoard(board)
		# which board we're going to play on next
		self._currBoard = subboard

	def updateAttribute(self, children, visitCount, winScore):
		self._children = children
		self._visitCount = visitCount
		self._winScore = winScore

	def checkStatus(self):
		win = IN_PROGRESS
		slot_in_array = self._currBoard - 1
		# if self._parent is None:
		for i in range(1, 10):
			for triad in DO_SLOT_WINNING_CON[slot_in_array]:
				triad_sum = self._boardState[i][triad[0]]+ self._boardState[i][triad[1]] + self._boardState[i][triad[2]]
				# opponent win
				if triad_sum == -3: 
					win = PLAYER2
				elif triad_sum == 3:
					win = PLAYER1

				if win == PLAYER2 or win == PLAYER1: 
					break
		# else:
		# 	last_board = self._parent._currBoard
		# 	for triad in DO_SLOT_WINNING_CON[slot_in_array]:
		# 		triad_sum = self._boardState[last_board][triad[0]]+ self._boardState[last_board][triad[1]] + self._boardState[last_board][triad[2]]
		# 		# opponent win
		# 		if triad_sum == -3: 
		# 			win = PLAYER2
		# 		elif triad_sum == 3:
		# 			win = PLAYER1

		# 		if win == PLAYER2 or win == PLAYER1: 
		# 			break
		return win

	def find_selection_leaf(self):
		node = self
		while len(node._children) != 0:
			node = bestNodeWithUCB1(node)
		return node
	
	def togglePlayer(self):
		if self._player == PLAYER1:
			self._player = PLAYER2
		else:
			self._player = PLAYER1

# =========================== draw board =================================
s = [".","O","X"]

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

def newBoard():
	c = []
	for i in range(10):
		column = []
		for j in range(10):
			column.append(0)
		c.append(column)
	return c

def copyBoard(boardStatus):
	copy = newBoard()
	for row in range(1,10):
		for column in range(1,10):
			copy[row][column] = boardStatus[row][column]
	return copy

# ==================================== UCB CALCULATION ===========================================
def UCB1(totalVisit, nodeWinScore, nodeVisit):
	if nodeVisit == 0:
		return MAX_SAFE_INTEGER
	value = (nodeWinScore / nodeVisit) + 1.41 * math.sqrt(math.log(totalVisit) / nodeVisit)
	return value


# return the promising node
def bestNodeWithUCB1(node: TreeNode):
	parentVisit = node._visitCount
	# a map from child to UCB1
	childUCB1 = {}

	for child in node._children:
		child_info = node._children[child]
		ucb1 = UCB1(parentVisit, child_info._winScore, child_info._visitCount)
		childUCB1[child] = ucb1

	index = max(childUCB1, key=lambda i: childUCB1[i])
	return node._children[index]
# ==================================================================================
def togglePlayer(player):
	if player == PLAYER1:
		player = PLAYER2
	else:
		player = PLAYER1
	return player

def posibleNextState(node):
	possiState = {}
	currBoard = node._currBoard
	for slot in range(1,10):
		board = copyBoard(node._boardState)
		if board[currBoard][slot] == 0:
			player = togglePlayer(node._player)
			board[currBoard][slot] = player
			new_node = TreeNode(node, player, board, slot)
			possiState[slot] = new_node
	return possiState

# =========================== EXPAND =============================
def expandNode(node):
	possibleStates = posibleNextState(node)
	for action in possibleStates:
		node._children[action] = possibleStates[action]

# ========================== SIMULATION =============================
def randomPlay(node: TreeNode):
	available_slot = []
	board = node._boardState
	currBoard = node._currBoard
	for i in range(1, 10):
		if board[currBoard][i] == 0:
			available_slot.append(i)
	
	total_avail_slot = len(available_slot)
	if total_avail_slot == 0:
		return DRAW
	ran = randint(0, 1000) % total_avail_slot
	n = available_slot[ran]
	node.togglePlayer()
	node._boardState[currBoard][n] = node._player
	node._currBoard = n

	return UNTOUCHED

def simulationRollout(node: TreeNode, opponent, timeout):
	tempNode = TreeNode(node._parent, node._player, node._boardState, node._currBoard)
	boardStatus = node.checkStatus()
	if boardStatus == opponent:
		tempNode._parent._winScore = - MAX_SAFE_INTEGER
		return boardStatus
	while boardStatus == IN_PROGRESS and time.time() < timeout:
		touch = randomPlay(tempNode)
		# print_board(tempNode._boardState)
		# print("===================================")
		if touch == DRAW:
			return touch
		boardStatus = tempNode.checkStatus()
	return boardStatus

# ========================== BACKPROPAGATION =================================
def backpropagation(node: TreeNode, playoutResult):
	tempNode = node
	while tempNode is not None:
		tempNode._visitCount += 1
		if tempNode._player == playoutResult:
			tempNode._winScore += 10
		# if playoutResult == togglePlayer(tempNode._player):
			# tempNode._winScore -= MAX_SAFE_INTEGER
		tempNode = tempNode._parent

# ========================== MCTS ===============================
def getRandomChildNode(children):
	key = random.choice(list(children.keys()))
	return children[key]

def getChildWithMaxScore(children):
	dict_ratio = {}
	for action in children:
		print("===================================")
		print("action is "+ str(action))
		print("win score " + str(children[action]._winScore))
		print("visit is "+ str(children[action]._visitCount)+"\n")
		ratio = children[action]._winScore / children[action]._visitCount
		dict_ratio[action] = ratio

	return max(dict_ratio, key=lambda i: dict_ratio[i])

def MCTS(board, slot):
	print("********************8 NEW ROUND *********************************")
	opponent = PLAYER2
	tree_board = copyBoard(board)
	tree = TreeNode(None, opponent, tree_board, slot)
	i = 0
	timeout = time.time() + 5   # 10s from now
	while time.time() < timeout:
	# while i<15:
		# print("((((((((((((((((((((( selection phase ))))))))))))))))))))))")
		promisingNode = tree.find_selection_leaf()
		# print_board(promisingNode._boardState)
		if promisingNode.checkStatus() == IN_PROGRESS:
			# print("im here======================")
			# print("&&&&&&&&&&&&&&&&&&&&&  expand phase &&&&&&&&&&&&&&&&&&&&&&&&&&&&")
			expandNode(promisingNode)
		nodeToExplore = promisingNode
		if len(nodeToExplore._children) > 0:
			# print("^^^^^^^^^^^^^^^^^ random child ^^^^^^^^^^^^^^^^^^^^^")
			nodeToExplore = getRandomChildNode(promisingNode._children)
		# print_board(nodeToExplore._boardState)
		# i += 1
		# print("!!!!!!!!!!!!!!!!!!! rollout !!!!!!!!!!!!!!!!!!!!!!")
		playoutResult = simulationRollout(nodeToExplore, opponent, timeout)
		# print("++++++++++++++++++ back++++++++++++++++++++++")
		backpropagation(nodeToExplore, playoutResult)
	
	# print("==================== ALMOST ++++++++++++++++++++")
	# for child in tree._children:
	# 	print_board(tree._children[child]._boardState)
	winnerAction = getChildWithMaxScore(tree._children)
	return winnerAction
# ============================ MAIN FUNCTION =================================
if __name__ == "__main__":
	board1 = newBoard()
	board1[1][3] = -1
	board1[1][5] = -1
	board1[1][8] = 1

	board1[2][2] = 1
	board1[2][4] = -1

	board1[3][1] = -1
	board1[3][9] = 1

	board1[4][5] = 1
	board1[4][7] = -1
	board1[4][8] = -1

	board1[5][3] = 1
	board1[5][4] = 1
	board1[5][5] = -1
	board1[5][6] = -1

	board1[6][1] = 1

	board1[7][1] = 1
	board1[8][9] = -1
	
	board1[9][2] = -1
	board1[9][4] = 1
	# board1[1][4] = -1

	DIGIT = MCTS(board1, 8)
	print(DIGIT)
	# tree = TreeNode(None, PLAYER1, board1, 4)
	# randomPlay(tree)
	# print_board(tree._boardState)
	# randomPlay(tree)
	# print_board(tree._boardState)
	# simulationRollout(tree, PLAYER2)
	# tree._visitCount = 1
	# # board2 = newBoard()
	# # board2[1][1] = 1
	# # board2[1][2] = -1
	# # node1 = TreeNode(tree, PLAYER2, board2, 2)
	# now = tree.find_selection_leaf()
	# # print_board(now._boardState)
	# expandNode(now)

	# for child in now._children:
	# 	now._children[child]._visitCount = 3
	# 	now._children[child]._winScore = 100
	# now._children[3]._visitCount = 1
	# now = tree.find_selection_leaf()
	# print_board(now._boardState)
	# start = time.time()
	# timeout = time.time() + 10   # 10s from now
	# while time.time() < timeout:
	# 	while True:
	# 		pass
	# p = multiprocessing.Process(target=wait)
	# p.start()

	# # Wait for 10 seconds or until process finishes
	# p.join(10)

	# # If thread is still active
	# if p.is_alive():
	# 	print("running... let's kill it...")

	# 	# Terminate
	# 	p.terminate()
	# 	p.join()
	

	