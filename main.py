import pygame
import random
import os
from button import Button

pygame.font.init()
pygame.mixer.init()

# Basic config
WIDTH, HEIGHT = 850, 600
BLACK, WHITE, BLUE, RED, GREY = (0, 0, 0), (255, 255, 255), (0, 0, 255), (255, 0, 0), (128, 128, 128)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PONG')

# Fonts initializing
SCORE_FONT = pygame.font.SysFont('Arial', 55)
WIN_FONT = pygame.font.SysFont('dejavuserif', 60)
ENDGAME_FONT = pygame.font.SysFont('Arial', 30)

# Images and sound initializing
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'bg_image.jpg')), (850, 600))
PADDLE_HIT_SOUND = pygame.mixer.Sound(os.path.join('sounds', 'paddle_hit_sound.mp3'))
BORDER_HIT_SOUND = pygame.mixer.Sound(os.path.join('sounds', 'border_hit_sound.mp3'))
SCORE_SOUND = pygame.mixer.Sound(os.path.join('sounds', 'score_sound.mp3'))
GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join('sounds', 'game_over_sound.mp3'))
MENU_CHOOSING_SOUND = pygame.mixer.Sound(os.path.join('sounds', 'menu_choosing_sound.mp3'))

FPS = 100
VEL_PLAYER = 5
VEL_X_BALL = 4
VEL_Y_BALL = 2
player1_score = 0
player2_score = 0

player1 = pygame.Rect(20, HEIGHT // 2 - 40, 20, 120)
player2 = pygame.Rect(WIDTH - 40, HEIGHT // 2 - 40, 20, 120)

ball_base_position = [WIDTH // 2, 100]
ball = pygame.Rect(ball_base_position[0], ball_base_position[1], 20, 20)
ball_x_direction = random.choice(['left', 'right'])
ball_y_direction = 'down'
hit_count = 0  # Counting times ball hit the paddle, increasing ball's VEL by 1 every 5 hits

# Setting flags to start the appropriate game at the player's will
two_players = False
one_player_easy = False
one_player_medium = False
one_player_hard = False


def player1_movement(keys_pressed):
	"""Left player movement"""
	if keys_pressed[pygame.K_w] and player1.y - VEL_PLAYER > 0:
		player1.y -= VEL_PLAYER
	elif keys_pressed[pygame.K_s] and player1.y + VEL_PLAYER + player1.height < HEIGHT:
		player1.y += VEL_PLAYER


def player2_movement(keys_pressed):
	"""Right player movement"""
	if keys_pressed[pygame.K_UP] and player2.y - VEL_PLAYER > 0:
		player2.y -= VEL_PLAYER
	elif keys_pressed[pygame.K_DOWN] and player2.y + VEL_PLAYER + player2.height < HEIGHT:
		player2.y += VEL_PLAYER


def ball_player_collision(player, direction):
	"""Shortcut to function that changes ball's direction after hitting player's paddle"""
	global ball_x_direction, ball_y_direction, VEL_Y_BALL, VEL_X_BALL, hit_count

	if ball.colliderect(player):
		PADDLE_HIT_SOUND.play()
		ball_x_direction = direction
		hit_count += 1
		# Increasing ball's speed every 10 hits
		if hit_count == 1:
			VEL_X_BALL = 8
		elif hit_count == 11:
			VEL_X_BALL += 1
			hit_count = 2

		if ball.y <= player.y + 10:  # Hitting top corner of paddle (+10px)
			ball_y_direction = 'up'
			VEL_Y_BALL = 4
		elif player.y + 10 < ball.y < player.y + 30:  # Lower than top corner of paddle
			ball_y_direction = 'up'
			VEL_Y_BALL = 3
		elif player.y + 30 <= ball.y < player.y + 45:  # Even higher than center of paddle
			ball_y_direction = 'up'
			VEL_Y_BALL = 2
		elif player.y + 45 <= ball.y < player.y + 55:  # Little higher than center of paddle
			ball_y_direction = 'up'
			VEL_Y_BALL = 1
		elif player.y + 55 <= ball.y <= player.y + 65:  # Center of paddle
			ball_y_direction = None
			VEL_Y_BALL = 0
		elif player.y + 65 < ball.y <= player.y + 75:  # Little lower than center of paddle
			ball_y_direction = 'down'
			VEL_Y_BALL = 1
		elif player.y + 75 < ball.y <= player.y + 100:  # Even Lower than center of paddle
			ball_y_direction = 'down'
			VEL_Y_BALL = 2
		elif player.y + 100 < ball.y < player.y + 120:  # Higher than bottom corner of paddle
			ball_y_direction = 'down'
			VEL_Y_BALL = 3
		elif ball.y >= player.y + 120:  # Bottom corner of paddle
			ball_y_direction = 'down'
			VEL_Y_BALL = 4


def ball_movement():
	"""Function that takes care of ball movement after collisions etc."""
	global ball_x_direction, ball_y_direction, VEL_Y_BALL, VEL_X_BALL

	ball_player_collision(player1, 'right')
	ball_player_collision(player2, 'left')

	# Ball's collision with floor or roof
	if ball.y <= 0:
		BORDER_HIT_SOUND.play()
		ball_y_direction = 'down'
	elif ball.y >= HEIGHT - ball.height:
		BORDER_HIT_SOUND.play()
		ball_y_direction = 'up'

	# Giving appropriate X,Y velocity for the ball depending on direction it is going
	if ball_x_direction == 'right':
		ball.x += VEL_X_BALL
		if ball_y_direction == 'up':
			ball.y -= VEL_Y_BALL
		elif ball_y_direction in ('down', None):
			ball.y += VEL_Y_BALL
	elif ball_x_direction == 'left':
		ball.x -= VEL_X_BALL
		if ball_y_direction == 'up':
			ball.y -= VEL_Y_BALL
		elif ball_y_direction in ('down', None):
			ball.y += VEL_Y_BALL


def easy_bot_movement():
	"""Next three functions takes care of AI bot movement (three different difficulties)"""
	bot = player2
	if ball.y <= bot.y + 40 and bot.y - 1.5 >= 0:
		bot.y -= 1.8
	elif ball.y > bot.y and bot.y + 1.5 <= HEIGHT - bot.height:
		bot.y += 1.8


def medium_bot_movement():
	bot = player2
	if ball.y <= bot.y + 40 and bot.y - 2.7 >= 0:
		bot.y -= 2.7
	elif ball.y > bot.y and bot.y + 2.7 <= HEIGHT - bot.height:
		bot.y += 2.7


def hard_bot_movement():
	bot = player2
	if ball.y <= bot.y + 40 and bot.y - 3.3 >= 0:
		bot.y -= 3.3
	elif ball.y > bot.y and bot.y + 3.3 <= HEIGHT - bot.height:
		bot.y += 3.3


def display_score():
	"""Function that displays score of both players on the screen"""
	global player1_score, player2_score, ball_x_direction, ball_y_direction, VEL_X_BALL, VEL_Y_BALL, hit_count

	WIN.blit(SCORE_FONT.render(str(player1_score), True, WHITE), (WIDTH * 1/4 - 10, 20))
	WIN.blit(SCORE_FONT.render(str(player2_score), True, WHITE), (WIDTH * 3/4, 20))
	if ball.x > WIDTH:
		# Resetting ball's x, y velocities and position, hit_count and increasing player's score after successful goal
		SCORE_SOUND.play()
		player1_score += 1
		ball.x = WIDTH // 2 - ball.width
		ball.y = 50
		VEL_X_BALL = 3
		VEL_Y_BALL = 2
		hit_count = 0
		ball_x_direction = random.choice(['left', 'right'])   # Sending ball back to scorer after score
		ball_y_direction = 'down'
	if ball.x < 0 - ball.width:
		SCORE_SOUND.play()
		player2_score += 1
		ball.x = WIDTH // 2 - ball.width
		ball.y = 50
		VEL_X_BALL = 3
		VEL_Y_BALL = 2
		hit_count = 0
		ball_x_direction = random.choice(['left', 'right'])  # Sending ball back to scorer after score
		ball_y_direction = 'down'


def starting_window():
	"""Function that displays menu before game"""
	global two_players, one_player_easy, one_player_medium, one_player_hard
	flag = 'basic_menu'  # Flag to go back to choosing play/exit options after pressing 'return' button

	# Basic starting window buttons
	play_button = Button(WIDTH // 2 - 150, HEIGHT // 2 - 160, 340, 100, BLACK, GREY, "PLAY THE GAME", 'arial', 50)
	exit_button = Button(WIDTH // 2 - 150, HEIGHT // 2 - 55, 340, 100, BLACK, GREY, "EXIT", 'arial', 50)

	# Buttons after clicking 'play the game' button
	one_player_button = Button(WIDTH // 2 - 150, HEIGHT // 2 - 160, 340, 100, BLACK, GREY, "ONE PLAYER", 'arial', 50)
	two_players_button = Button(WIDTH // 2 - 150, HEIGHT // 2 - 55, 340, 100, BLACK, GREY, "TWO PLAYERS", 'arial', 50)

	# Choosing difficulty of bot after clicking 'one player' button
	easy = Button(WIDTH // 2 - 150, HEIGHT // 2 - 225, 340, 100, BLACK, GREY, "EASY", 'arial', 50)
	medium = Button(WIDTH // 2 - 150, HEIGHT // 2 - 120, 340, 100, BLACK, GREY, "MEDIUM", 'arial', 50)
	hard = Button(WIDTH // 2 - 150, HEIGHT // 2 - 15, 340, 100, BLACK, GREY, "HARD", 'arial', 50)

	return_button = Button(WIDTH - 265, HEIGHT - 85, 250, 70, BLACK, GREY, "RETURN", 'arial', 45)

	while flag == 'basic_menu':
		two_players = False   # Resetting variables after game's restart
		one_player_easy = False
		one_player_medium = False
		one_player_hard = False

		WIN.blit(BACKGROUND_IMAGE, (0, 0))
		play_button.draw(WIN)
		exit_button.draw(WIN)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				MENU_CHOOSING_SOUND.play()
				exit()
			elif play_button.is_clicked(event):
				MENU_CHOOSING_SOUND.play()
				flag = 'players_choosing_menu'

				while flag == 'players_choosing_menu':
					WIN.blit(BACKGROUND_IMAGE, (0, 0))
					one_player_button.draw(WIN)
					two_players_button.draw(WIN)

					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							exit()
						elif event.type == pygame.MOUSEBUTTONDOWN:
							if one_player_button.is_clicked(event):
								MENU_CHOOSING_SOUND.play()
								flag = 'one_player_menu'

								while flag == 'one_player_menu':
									WIN.blit(BACKGROUND_IMAGE, (0, 0))
									easy.draw(WIN)
									medium.draw(WIN)
									hard.draw(WIN)
									return_button.draw(WIN)
									for event in pygame.event.get():
										if event.type == pygame.QUIT:
											exit()
										elif event.type == pygame.MOUSEBUTTONDOWN:
											# Choosing difficulty after pressing 'one player' button
											if easy.is_clicked(event):
												MENU_CHOOSING_SOUND.play()
												one_player_easy = True
												main()
											elif medium.is_clicked(event):
												MENU_CHOOSING_SOUND.play()
												one_player_medium = True
												main()
											elif hard.is_clicked(event):
												MENU_CHOOSING_SOUND.play()
												one_player_hard = True
												main()
											elif return_button.is_clicked(event):
												MENU_CHOOSING_SOUND.play()
												flag = 'basic_menu'  # Going back to play/exit buttons
										pygame.display.update()
							elif two_players_button.is_clicked(event):  # Playing 1 vs 1 after 'two players' button
								MENU_CHOOSING_SOUND.play()
								two_players = True
								main()
					pygame.display.update()

			if exit_button.is_clicked(event):
				exit()

		pygame.display.update()


def endgame_window(winner):
	"""Function that displays winner text and ending menu on screen after 10 points"""
	global VEL_X_BALL, VEL_Y_BALL, ball_y_direction, player1_score, player2_score

	GAME_OVER_SOUND.play()

	play_again_button = Button(WIDTH // 2 - 150, HEIGHT // 2 - 50, 340, 100, BLACK, GREY, "PLAY AGAIN", 'arial', 50)
	exit_button = Button(WIDTH // 2 - 150, HEIGHT // 2 + 55, 340, 100, BLACK, GREY, "EXIT", 'arial', 50)

	if winner == player1:
		win_text = WIN_FONT.render('BLUE PLAYER WINS!', True, WHITE)
	else:
		win_text = WIN_FONT.render('RED PLAYER WINS!', True, WHITE)
	while True:
		WIN.blit(BACKGROUND_IMAGE, (0, 0))
		WIN.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 180))
		play_again_button.draw(WIN)
		exit_button.draw(WIN)

		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			elif play_again_button.is_clicked(event):  # Pressing 'play again' button, restarting the game
				# Resetting all variables, getting objects back into their base positions
				VEL_X_BALL = 4
				VEL_Y_BALL = 2
				player1_score = 0
				player2_score = 0
				ball.y = 100
				ball_y_direction = 'down'
				player1.y, player2.y = HEIGHT // 2 - 40, HEIGHT // 2 - 40
				starting_window()
			elif exit_button.is_clicked(event):  # Quitting the game after pressing 'exit' button
				exit()


def draw_window():
	"""Function that puts stuff in window and updates it"""
	WIN.blit(BACKGROUND_IMAGE, (0, 0))
	display_score()
	pygame.draw.rect(WIN, BLUE, player1, border_radius=15)  # Displaying first player as rectangle on screen
	pygame.draw.rect(WIN, RED, player2, border_radius=15)  # Displaying second player as rectangle on screen
	pygame.draw.rect(WIN, WHITE, ball, border_radius=15)  # Displaying ball on the field

	for i in range(0, HEIGHT + 50, 51):   # Displaying dashed line as central border
		pygame.draw.line(WIN, WHITE, (WIDTH//2, i - 20), (WIDTH // 2, i + 12))

	pygame.display.update()


def main():
	"""Main game function"""
	global two_players, one_player_easy, one_player_medium, one_player_hard

	draw_window()
	pygame.time.delay(1500)  # Freezing the game for 1.5s after first start of the game
	run = True
	clock = pygame.time.Clock()

	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

		if two_players:  # Starting player vs player game if player chose 'Two players' game
			keys_pressed = pygame.key.get_pressed()
			player1_movement(keys_pressed)
			player2_movement(keys_pressed)
			ball_movement()
			draw_window()
			if player1_score == 10:   # Displaying endgame window if one of the players scores 10 goals
				endgame_window(player1)
				starting_window()
			elif player2_score == 10:
				endgame_window(player2)
				starting_window()

		elif one_player_easy:  # Starting one player game vs EASY bot
			keys_pressed = pygame.key.get_pressed()
			player1_movement(keys_pressed)
			easy_bot_movement()
			ball_movement()
			draw_window()
			if player1_score == 10:  # player1 == PLAYER, player2 == BOT, endgame window displaying
				endgame_window(player1)
				starting_window()
			elif player2_score == 10:
				endgame_window(player2)
				starting_window()

		elif one_player_medium:  # Starting one player game vs MEDIUM bot
			keys_pressed = pygame.key.get_pressed()
			player1_movement(keys_pressed)
			medium_bot_movement()
			ball_movement()
			draw_window()
			if player1_score == 10:
				endgame_window(player1)
				starting_window()
			elif player2_score == 10:
				endgame_window(player2)
				starting_window()

		elif one_player_hard:  # Starting one player game vs HARD bot
			keys_pressed = pygame.key.get_pressed()
			player1_movement(keys_pressed)
			hard_bot_movement()
			ball_movement()
			draw_window()
			if player1_score == 10:
				endgame_window(player1)
				starting_window()
			elif player2_score == 10:
				endgame_window(player2)
				starting_window()


if __name__ == '__main__':
	starting_window()

