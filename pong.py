import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255,105,180)
GREEN = (0, 255, 0)

WIDTH = 800
HEIGHT = 600

# Set winning score (first player to reach this score wins)
WINNING_SCORE = 5

pygame.init()
game_font = pygame.font.SysFont('Ubuntu', 40)
winner_font = pygame.font.SysFont('Ubuntu', 60)

delay = 30

paddle_speed = 10
paddle_width = 10
paddle_height = 100

# Player 1 paddle
p1_x_pos = 10
p1_y_pos = HEIGHT / 2 - paddle_height / 2 
# Player 2 paddle
p2_x_pos = WIDTH - paddle_width - 10
p2_y_pos = HEIGHT / 2 - paddle_height / 2 

# Scores
p1_score = 0
p2_score = 0

p1_up = False
p1_down = False
p2_up = False
p2_down = False
ball_x_pos = WIDTH / 2
ball_y_pos = HEIGHT / 2
ball_width = 8
ball_x_vel = -10
ball_y_vel = 0

# Game state
game_over = False
winner = ""

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# drawing objects
def draw_objects():
    pygame.draw.rect(screen, WHITE, (int(p1_x_pos), int(p1_y_pos), paddle_width, paddle_height))
    pygame.draw.rect(screen, WHITE, (int(p2_x_pos), int(p2_y_pos), paddle_width, paddle_height))
    pygame.draw.circle(screen, PINK, (ball_x_pos, ball_y_pos), ball_width)
    score = game_font.render(f"{str(p1_score)} - {str(p2_score)}", False, WHITE)
    screen.blit(score, (WIDTH / 2 - score.get_width() / 2, 30))
    
    # Display winner message if game is over
    if game_over:
        winner_text = winner_font.render(f"{winner} WINS!", False, GREEN)
        restart_text = game_font.render("Press R to restart or ESC to quit", False, WHITE)
        screen.blit(winner_text, (WIDTH / 2 - winner_text.get_width() / 2, HEIGHT / 2 - 50))
        screen.blit(restart_text, (WIDTH / 2 - restart_text.get_width() / 2, HEIGHT / 2 + 50))

def apply_player_movement():
    global p1_y_pos
    global p2_y_pos

    # Only allow movement if game is not over
    if not game_over:
        if p1_up:
            p1_y_pos = max(p1_y_pos - paddle_speed, 0)
        elif p1_down:
            p1_y_pos = min(p1_y_pos + paddle_speed, HEIGHT - paddle_height)
        if p2_up:
            p2_y_pos = max(p2_y_pos - paddle_speed, 0)
        elif p2_down:
            p2_y_pos = min(p2_y_pos + paddle_speed, HEIGHT - paddle_height)

def apply_ball_movement():
    global ball_x_pos
    global ball_y_pos
    global ball_x_vel
    global ball_y_vel
    global p1_score
    global p2_score
    global game_over
    global winner

    # Only move ball if game is not over
    if not game_over:
        # Left paddle collision
        if (ball_x_pos + ball_x_vel <= p1_x_pos + paddle_width) and (ball_y_pos >= p1_y_pos) and (ball_y_pos <= p1_y_pos + paddle_height) and (ball_x_vel < 0):
            ball_x_vel = -ball_x_vel
            ball_y_vel = (p1_y_pos + paddle_height / 2 - ball_y_pos) / 15
            ball_y_vel = -ball_y_vel
        elif ball_x_pos + ball_x_vel < 0:
            p2_score += 1
            ball_x_pos = WIDTH / 2
            ball_y_pos = HEIGHT / 2
            ball_x_vel = 10
            ball_y_vel = 0
            
            # Check for winner
            if p2_score >= WINNING_SCORE:
                game_over = True
                winner = "PLAYER 2"

        # Right paddle collision
        if (ball_x_pos + ball_x_vel >= p2_x_pos - ball_width) and (ball_y_pos >= p2_y_pos) and (ball_y_pos <= p2_y_pos + paddle_height) and (ball_x_vel > 0):
            ball_x_vel = -ball_x_vel
            ball_y_vel = (p2_y_pos + paddle_height / 2 - ball_y_pos) / 15
            ball_y_vel = -ball_y_vel
        elif ball_x_pos + ball_x_vel > WIDTH:
            p1_score += 1
            ball_x_pos = WIDTH / 2
            ball_y_pos = HEIGHT / 2
            ball_x_vel = -10
            ball_y_vel = 0
            
            # Check for winner
            if p1_score >= WINNING_SCORE:
                game_over = True
                winner = "PLAYER 1"
                
        if ball_y_pos + ball_y_vel > HEIGHT - ball_width or ball_y_pos + ball_y_vel < ball_width:
            ball_y_vel = -ball_y_vel

        ball_x_pos += ball_x_vel
        ball_y_pos += ball_y_vel

def reset_game():
    global p1_score, p2_score, ball_x_pos, ball_y_pos, ball_x_vel, ball_y_vel, game_over, winner
    p1_score = 0
    p2_score = 0
    ball_x_pos = WIDTH / 2
    ball_y_pos = HEIGHT / 2
    ball_x_vel = -10
    ball_y_vel = 0
    game_over = False
    winner = ""

pygame.display.set_caption("Pink Pong")
screen.fill(BLACK)
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w:
                p1_up = True
            if event.key == pygame.K_s:
                p1_down = True
            if event.key == pygame.K_UP:
                p2_up = True
            if event.key == pygame.K_DOWN:
                p2_down = True
            # Reset the game if R is pressed and game is over
            if event.key == pygame.K_r and game_over:
                reset_game()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                p1_up = False
            if event.key == pygame.K_s:
                p1_down = False
            if event.key == pygame.K_UP:
                p2_up = False
            if event.key == pygame.K_DOWN:
                p2_down = False

    screen.fill(BLACK)
    apply_player_movement()
    apply_ball_movement()
    draw_objects()
    pygame.display.flip()
    pygame.time.wait(delay)