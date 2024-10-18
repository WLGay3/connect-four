import numpy as np
import pygame
import re
import sys
import math
import time

board_color = '#005511'
black = '#000000'
window_color = '#cccccc'
SQUARESIZE = 100
radius = SQUARESIZE/2 - 5

player1_color = '#ff0000'
player2_color = '#ffff00'

def create_board():
	board = np.zeros((6,7), dtype=int)
	return board
play_again = True
game_over = False
player1 = True
row = 5
column = 6
turn = 0


width = column* SQUARESIZE
height = (row+2)*SQUARESIZE

size = (width, height)

board = create_board()
pygame.init()
t0 = time.time()
font = pygame.font.SysFont(None, 48)

sysfont = pygame.font.get_default_font()
font1 = pygame.font.SysFont('comicsansms', 72)
img1 = font1.render("Player " + str(turn+1) + " wins!", True, '#0000ff')



def drop_piece(selection,row, board, turn):
	for x in board:
			if board[row, selection] == 0:
				board[row, selection] = turn +1
				row = 5
				break
			elif row == 0 or selection > len(board):
				print("Try another spot")
				row = 5
			else:
				row -=1


def check_win_state(board, turn):
	if turn == 0:
		win = '1111'
		win_diag = '1 1 1 1'
	else:
		win = '2222'
		win_diag = '2 2 2 2'
	check_row = np.array2string(board, separator="")
	check_col = np.array2string(board.T, separator="")
	check_diagonal = ""
	for k in range(-2,3):
		check_diagonal += re.sub('( \[|\[|\])', ' ', str(np.array2string(np.diag(board, k=k))))
		check_diagonal += re.sub('( \[|\[|\])', ' ', str(np.array2string(np.diag(np.fliplr(board), k=k))))


	if(win in check_row):
		return True
	elif(win in check_col):
		return True
	elif(win_diag in check_diagonal):
		return True

#pygame code



def draw_board(board):
	for c in range(column):
		for r in range(row+1):
			pygame.draw.rect(screen, board_color, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
			if board[r][c] == 0:
				pygame.draw.circle(screen, black,(c*SQUARESIZE + SQUARESIZE/2, r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2), radius, 0)
			elif board [r][c] == 1:
				pygame.draw.circle(screen, player1_color,(c*SQUARESIZE + SQUARESIZE/2, r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2), radius, 0)
			elif board [r][c] == 2:
				pygame.draw.circle(screen, player2_color,(c*SQUARESIZE + SQUARESIZE/2, r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2), radius, 0)

	pygame.display.update()


screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()


while not game_over:
	#player_piece(turn)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, black, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			
			if turn == 0:
				pygame.draw.circle(screen, player1_color, (posx, SQUARESIZE/2), radius, 0)
			else:
				pygame.draw.circle(screen, player2_color, (posx, SQUARESIZE/2), radius, 0)
	

		if event.type == pygame.MOUSEBUTTONDOWN:
			if turn == 0:
				posx = event.pos[0]
				selection = math.floor(posx/SQUARESIZE)
			else:
				posx = event.pos[0]
				selection = math.floor(posx/SQUARESIZE)
			
			drop_piece(selection, row, board, turn)
			if check_win_state(board, turn):
				pygame.draw.rect(screen, black, (0,0, width, SQUARESIZE))
				screen.blit(img1,(40,10))
				game_over = True

			turn += 1
			turn = turn % 2
			player1 = not player1
			draw_board(board)
		pygame.display.update()

pygame.time.wait(3000)