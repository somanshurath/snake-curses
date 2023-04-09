# Steps to play the game
# 1. Install windows-curses package (in case you don't have it installed). Type: python -m pip install windows-curses (in Windows Powershell)
# 2. Download the python file.
# 3. Go the folder where you downloaded, right click and select "Open in Terminal". Go fullscreen.
# 4. Type: python the-curse-of-the-snake.py (and click enter).


import random
import curses
from curses import textpad

opposite_direction_dict = {
    curses.KEY_UP: curses.KEY_DOWN,
    curses.KEY_DOWN: curses.KEY_UP,
    curses.KEY_RIGHT: curses.KEY_LEFT,
    curses.KEY_LEFT: curses.KEY_RIGHT
}
direction_list = [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_UP]

def create_food(snake, play_area):
    food = None
    while food is None:
        food = [random.randint(play_area[0][0] + 1, play_area[1][0] - 1),
                random.randint(play_area[0][1] + 1, play_area[1][1] - 1)]
        if food in snake:
            food = None
    return food
menu = ['Play', 'Credits', 'Exit']
def print_menu(stdscr, selected_row_idx):
	stdscr.clear()
	h, w = stdscr.getmaxyx()
	for idx, row in enumerate(menu):
		x = w//2 - len(row)//2
		y = h//2 - len(menu)//2 + idx
		if idx == selected_row_idx:
			stdscr.attron(curses.color_pair(1))
			stdscr.addstr(y, x, row)
			stdscr.attroff(curses.color_pair(1))
		else:
			stdscr.addstr(y, x, row)
	stdscr.refresh()
def print_center(stdscr, text):
	stdscr.clear()
	h, w = stdscr.getmaxyx()
	x = w//2 - len(text)//2
	y = h//2
	stdscr.addstr(y, x, text)
	stdscr.refresh()

def main(stdscr):
	curses.curs_set(0)
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
	current_row = 0

	print_center(stdscr,"- The Curse of the Snake -")
	curses.napms(5000)
	print_menu(stdscr, current_row)
	while 1:

		key = stdscr.getch()

		if key == curses.KEY_UP and current_row > 0:
			current_row -= 1
		elif key == curses.KEY_DOWN and current_row < len(menu)-1:
			current_row += 1
		elif key == curses.KEY_ENTER or key in [10, 13]:

			if current_row == 0:
				stdscr.clear()
				curses.curs_set(0)
				stdscr.nodelay(1)
				stdscr.timeout(100)

				sh, sw = stdscr.getmaxyx()
				play_area = [[3, 3], [sh - 3, sw - 3]]
				textpad.rectangle(stdscr, play_area[0][0], play_area[0][1], play_area[1][0], play_area[1][1])

				snake = [[sh // 2, sw // 2 + 1], [sh // 2, sw // 2], [sh // 2, sw // 2 - 1]]
				direction = curses.KEY_RIGHT

				for y, x in snake:
					stdscr.addstr(y, x, '#')

				food2 = create_food(snake, play_area)
				stdscr.addstr(food2[0], food2[1], '*')
				food1 = create_food(snake, play_area)
				stdscr.addstr(food1[0], food1[1], '*')
				food3 = create_food(snake, play_area)
				stdscr.addstr(food3[0], food3[1], '*')

				score = 0
				score_text = "In order to lift the curse, you must reach the score 32.       Score: {}".format(score)
				stdscr.addstr(1, sw // 2 - len(score_text) // 2, score_text)

				while 1:
					key = stdscr.getch()

					if key in direction_list and key != opposite_direction_dict[direction]:
						direction = key

					head = snake[0]
					if direction == curses.KEY_RIGHT:
						new_head = [head[0], head[1] + 1]
					elif direction == curses.KEY_LEFT:
						new_head = [head[0], head[1] - 1]
					elif direction == curses.KEY_DOWN:
						new_head = [head[0] + 1, head[1]]
					elif direction == curses.KEY_UP:
						new_head = [head[0] - 1, head[1]]

					stdscr.addstr(new_head[0], new_head[1], '#')
					snake.insert(0, new_head)

					if snake[0] == food1:
						score += 1
						score_text = "In order to lift the curse, you must reach the score 32.       Score: {}".format(score)
						stdscr.addstr(1, sw // 2 - len(score_text) // 2, score_text)
						food1 = create_food(snake, play_area)
						stdscr.addstr(food1[0], food1[1], '*')
						stdscr.timeout(100 - (len(snake) // 3) % 90)

					elif snake[0] == food2:
						score += 1
						score_text = "In order to lift the curse, you must reach the score 32.       Score: {}".format(score)
						stdscr.addstr(1, sw // 2 - len(score_text) // 2, score_text)
						food2 = create_food(snake, play_area)
						stdscr.addstr(food2[0], food2[1], '*')
						stdscr.timeout(100 - (len(snake) // 3) % 90)

					elif snake[0] == food3:
						score += 1
						score_text = "In order to lift the curse, you must reach the score 32.       Score: {}".format(score)
						stdscr.addstr(1, sw // 2 - len(score_text) // 2, score_text)
						food3 = create_food(snake, play_area)
						stdscr.addstr(food3[0], food3[1], '*')
						stdscr.timeout(100 - (len(snake) // 3) % 90)

					else:
						stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
						snake.pop()

					if score >=32:
						stdscr.clear()
						msg = "Ahh! Praise the Gods! You have skillfully guided the snake to victory and have lifted it from its curse!"
						stdscr.addstr((sh // 2), sw // 2 - len(msg) // 2, msg)
						stdscr.refresh()
						curses.napms(7000)
						stdscr.nodelay(0)
						stdscr.getch()
						break

					if (snake[0][0] in [play_area[0][0], play_area[1][0]] or
							snake[0][1] in [play_area[0][1], play_area[1][1]] or
							snake[0] in snake[1:]):
						stdscr.clear()
						msg = "Game Over! Alas, the curse on the snake shall remain unbroken."
						stdscr.addstr((sh // 2) -1, sw // 2 - len(msg) // 2, msg)
						msg = "Final score: {}".format(score)
						stdscr.addstr((sh // 2), sw // 2 - len(msg) // 2, msg)
						stdscr.refresh()
						curses.napms(7000)
						stdscr.nodelay(0)
						stdscr.getch()
						break


			if current_row == len(menu)-2:
				print_center(stdscr,"Made by Somanshu Rath - April 2023 - Using Python Curses Library")
				curses.napms(5000)

			if current_row == len(menu)-1:
				break

		print_menu(stdscr, current_row)


curses.wrapper(main)
