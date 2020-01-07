#!/usr/bin/python3
import numpy as np
import math
import random
from random import randint
import time
import multiprocessing

PLAYER1 = 1
PLAYER2 = -1
IN_PROGRESS = 0
DRAW = -2
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
		self._boardState = board
		# which board we're going to play on next
		self._currBoard = subboard

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

############################# UCB1 SECTION HELP FUNCTION ###############################
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

############################ NODE EXPANSION SECTION HELP FUNCTION ##########################

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

########################### SIMULATION ROLLOUT SECTION HELP FUNCTION ##################
# last_sub_board where we put to get board -parent's currBoard
# last_slot where it put -action curr node's currBoard
# def checkStatus(board, last_slot):

# 	win = IN_PROGRESS
# 	slot_in_array = last_slot - 1
# 	for i in range(1, 9):
# 		for triad in DO_SLOT_WINNING_CON[slot_in_array]:
# 			triad_sum = board[i][triad[0]]+ board[i][triad[1]] + board[i][triad[2]]
# 			# opponent win
# 			if triad_sum == -3: 
# 				win = PLAYER2
# 			elif triad_sum == 3:
# 				win = PLAYER1

# 			if win == PLAYER2: 
# 				break
# 	return win

def randomPlay(node: TreeNode):
	available_slot = []
	board = copyBoard(node._boardState)
	# print("======= NOW IS "+ str(node._player)+ "'s TURN")
	# print_board(board)
	currBoard = node._currBoard
	for i in range(1, 10):
		if board[currBoard][i] == 0:

			# for triad in DO_SLOT_WINNING_CON[i-1]:
			# 	triad_sum = board[currBoard][triad[0]]+ board[currBoard][triad[1]] + board[currBoard][triad[2]]
			# 	# opponent win
			# 	if triad_sum == -2 or triad_sum == 2: 
			# 		return i
			available_slot.append(i)
	
	total_avail_slot = len(available_slot)
	if total_avail_slot == 0:
		return DRAW
	ran = randint(0, 1000) % total_avail_slot
	return available_slot[ran]

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

# def trial(node):
# 	c = copyBoard(node._boardState)
# 	tempNode = TreeNode(None, node._player, c, node._currBoard)
# 	tempNode._boardState[2][2] = 1



############################# MCTS HELP FUNCTION ##########################
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

##############################  MCTS MAIN 4 STEPS ####################################

def selectPromisingNode(rootNode):
	node = rootNode
	while len(node._children) != 0:
		node = bestNodeWithUCB1(node)
	return node

def expandNode(node):
	possibleStates = posibleNextState(node)
	for action in possibleStates:
		node._children[action] = possibleStates[action]
	
def simulateRollout(node: TreeNode, opponent, timeout):
	tempBoard = copyBoard(node._boardState)
	tempNode = TreeNode(None, node._player, tempBoard, node._currBoard)
	boardStatus = tempNode.checkStatus()
	if boardStatus == opponent:
		# print(node._boardState)
		node._parent._winScore = - MAX_SAFE_INTEGER
		return boardStatus 
	next_node = tempNode
	while boardStatus == IN_PROGRESS and time.time() < timeout:
		player = togglePlayer(next_node._player)
		slot = randomPlay(next_node)
		if slot == DRAW:
			return slot
		board = copyBoard(next_node._boardState)
		board[next_node._currBoard][slot] = player
		currNode = next_node
		next_node = TreeNode(currNode, player, board, slot)
		boardStatus = next_node.checkStatus()
	return boardStatus

def backpropagation(node: TreeNode, playoutResult):
	tempNode = node
	while tempNode is not None:
		tempNode._visitCount += 1
		if tempNode._player == playoutResult:
			tempNode._winScore += 10
		# if playoutResult == togglePlayer(tempNode._player):
			# tempNode._winScore -= MAX_SAFE_INTEGER
		tempNode = tempNode._parent



def MCTS(board, slot):
	opponent = PLAYER2
	tree_board = copyBoard(board)
	tree = TreeNode(None, PLAYER1, tree_board, slot)

	timeout = time.time() + 10   # 10s from now
	while time.time() < timeout:
		# print("another round ==888888888888888888888888888888888888888888888")
		promisingNode = selectPromisingNode(tree)
		if promisingNode.checkStatus() == IN_PROGRESS:
			expandNode(promisingNode)
		nodeToExplore = promisingNode
		if len(nodeToExplore._children) > 0:
			nodeToExplore = getRandomChildNode(promisingNode._children)
		playoutResult = simulateRollout(nodeToExplore, opponent, timeout)
		backpropagation(nodeToExplore, playoutResult)

	print("im jerere =================================================================")
	print("tree has "+ str(len(tree._children)))
	for action in tree._children:
		print("===================================")
		print("action is "+ str(action))
		print("win score " + str(tree._children[action]._winScore))
		print("visit is "+ str(tree._children[action]._visitCount)+"\n")

	winnerAction = getChildWithMaxScore(tree._children)
	return winnerAction

# if __name__ == "__main__":
# 	board = [
# 		[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
# 		[1, -1, -1, -1, 0, 0, 0, 0, 0, 0],
# 		[2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# 		[9, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# 	]
	# c = newBoard()
	# print_board(c)
	# c = copyBoard(board)
	# print(c)
	# tree = TreeNode(None, PLAYER1, board, 1)
	# trial(tree)
	# print(tree._boardState)
# 	node = TreeNode(tree, PLAYER2, board, 1)
# 	# DIGIT = MCTS(board, 3)
# 	result = node.checkStatus()
# 	print(result)