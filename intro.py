import pgzrun
import random
from sprite import Sprite

# Screen Size
WIDTH = 1000
HEIGHT = 600
NUM_FUEL = 3

# Limit number os enemies
LIMIT_ENEMIES = 8

# Enemies Speed
SPEED_METEOR_GRAY = 3
SPEED_METEOR_BROWN = 2.5

# Game state
game_state = "menu"  # Options: "menu", "play" ou "sound"
game_over = False  # Control end of game
count_fuel = 0
stop = False
sound_on = True
sounds.space_ambience.play()

# Buttons of Start Menu
buttons = [
    {"text": "Iniciar", "x": WIDTH // 2, "y": 250, "action": "start"},
    {"text": "Som: Ligado", "x": WIDTH // 2, "y": 320, "action": "sound"},
    {"text": "Sair", "x": WIDTH // 2, "y": 390, "action": "quit"},
]

# List of meteors
meteor_list = []

# Nave
player = None

fuel = None
show_fuel = True
# List of Fuels
empty_fuels = None

def draw_sprites():
    # Fuels
    for i in range(0, len(empty_fuels)):
        empty_fuels[i].sprite.x = WIDTH - 50*(i+1)
        empty_fuels[i].sprite.y = 20
        empty_fuels[i].draw()

    # Meteors
    for m in meteor_list:
        m.draw()

def spawn_fuel():
    global fuel, show_fuel
    # Put fuel in top of screen
    fuel = Sprite(Actor("fuel", (random.randint(50, WIDTH - 50), -500)), speed_x=1.5, speed_y=1.5)
    show_fuel = True

def spawn_enemies():
    global meteor_list
    # Create new meteor
    x_position = random.randint(50, WIDTH - 50)  # Random Position
    speed_enemy = SPEED_METEOR_BROWN if len(meteor_list) % 2 == 0 else SPEED_METEOR_GRAY
    image = 'meteor_slow' if len(meteor_list) % 2 == 0 else 'meteor_fast'

    # New sprite
    new_object = Sprite(Actor(image, (x_position, 20)), speed_x=speed_enemy, speed_y=speed_enemy)
    # Enemies list
    if len(meteor_list) < LIMIT_ENEMIES:
        meteor_list.append(new_object)


# Schedule object create
clock.schedule_interval(spawn_fuel, 30.0) # Fuel
clock.schedule_interval(spawn_enemies, 5.0) # Meteor

# Restart the game
def reset_game():
    global player, game_over, stop, count_fuel
    global meteor_list, fuel, empty_fuels

    count_fuel = 0

    # Itens
    meteor_list = []
    empty_fuels = list([Sprite(Actor('empty_fuel', (-100, -100))) for _ in range(0, NUM_FUEL)])
    fuel = None

    player = Actor('player')
    player = Sprite(Actor('player', (WIDTH // 2, HEIGHT - player.height // 2)), speed_x=3.5, speed_y=3.5)
    player.sprite.pos = (WIDTH // 2, HEIGHT - player.sprite.height // 2)
    player.sprite.image = "player"
    game_over = stop = False

def exit_game():
    exit()

def trigger_game_over():
    global game_over
    game_over = True

def update_meteoros():
    if meteor_list is not None:
        for m in meteor_list:
            # Update position
            m.sprite.x += m.speed_x
            m.sprite.y += m.speed_y

            # Check colision and invert the direction
            if m.sprite.left < 0 or m.sprite.right > WIDTH:
                m.speed_x = -m.speed_x
            if m.sprite.top < 0 or m.sprite.bottom > HEIGHT:
                m.speed_y = -m.speed_y

            # Rotate the meteors
            if m.sprite.angle == 360:
                m.sprite.angle = 0
            m.sprite.angle = m.sprite.angle+1

def update_player():
    global player

    if keyboard.left:
        player.sprite.x -= player.speed_x
        player.sprite.image = 'player_left'
    elif keyboard.right:
        player.sprite.x += player.speed_x
        player.sprite.image = 'player_right'
    elif keyboard.up:
        player.sprite.y -= player.speed_y
        player.sprite.image = 'player_up'
    elif keyboard.down:
        player.sprite.y += player.speed_y
        player.sprite.image = 'player_down'
    else:
        player.sprite.image = 'player'

    # Keeps the sprite on screen
    player.sprite.x = max(player.sprite.width / 2, min(WIDTH - (player.sprite.width / 2), player.sprite.x))
    player.sprite.y = max(player.sprite.height / 2, min(HEIGHT - (player.sprite.height / 2), player.sprite.y))

def update():
    global speed_slow, speed_slow
    global game_over, game_concluded
    global stop

    if not game_over:
        if game_state == "play" and not stop:

            # Update meteors position
            update_meteoros()

            # Update nave position
            update_player()

            # Update fuel position
            if fuel is not None:
                fuel.sprite.y += fuel.speed_x  # Move down

            # Detect collision between player and meteor
            for meteor in meteor_list:
                if player.sprite.colliderect(meteor.sprite):
                    sounds.crash.play()
                    player.sprite.image = "crash"  # Muda o sprite
                    stop = True
                    clock.schedule_unique(trigger_game_over, 1.0)

            # Detect if nave catch the fuel
            if fuel is not None and player.sprite.colliderect(fuel.sprite):
                global empty_fuels, show_fuel, count_fuel
                for f in empty_fuels:
                    if show_fuel and f.sprite.image != 'fuel':
                        f.sprite.image = 'fuel'
                        sounds.fuel.play()
                        show_fuel = False
                        count_fuel += 1


def draw_menu():
    # Draw initial menu
    screen.draw.text("MENU", center=(WIDTH // 2, 150), fontsize=50, color="white")

    for button in buttons:
        screen.draw.filled_rect(Rect((button["x"] - 100, button["y"] - 20), (200, 40)), "blue")
        screen.draw.text(button["text"], center=(button["x"], button["y"]), fontsize=30, color="white")


def on_mouse_down(pos):
    # Detect mouse click
    global game_state
    global sound_on

    if game_over and (WIDTH // 2 - 75 <= pos[0] <= WIDTH // 2 + 75 and HEIGHT // 2 <= pos[1] <= HEIGHT // 2 + 50):
        reset_game()
    else:
        if game_state == "menu":
            for button in buttons:
                bx, by = button["x"], button["y"]
                if Rect((bx - 100, by - 20), (200, 40)).collidepoint(pos):
                    if button["action"] == "start":
                        game_state = "play"
                    elif button["action"] == "sound":
                        sound_on = not sound_on
                        if sound_on:
                            sounds.space_ambience.play()
                            buttons[1]["text"] = "Som: Ligado"
                        else:
                            sounds.space_ambience.stop()
                            buttons[1]["text"] = "Som: Desligado"
                    elif button["action"] == "quit":
                        exit()

def draw():
    screen.clear()
    screen.blit("background", (0, 0))  # Desenha a imagem no fundo

    if game_over:
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=50, color="red")
        if count_fuel < NUM_FUEL:
            screen.draw.filled_rect(Rect((WIDTH // 2 - 75, HEIGHT // 2), (150, 50)), "white")  # Fundo do botão
            screen.draw.text("Reiniciar", center=(WIDTH // 2, HEIGHT // 2 + 25), fontsize=30, color="black")
    elif count_fuel >= NUM_FUEL:
        screen.draw.text("Parabéns!!!", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=50, color="red")
        clock.schedule_unique(exit_game, 1.0)
    else:
        if game_state == "menu":
            draw_menu()
        elif game_state == "play":
            draw_sprites()
            player.draw()
            if fuel is not None and show_fuel:
                fuel.draw()

reset_game()
pgzrun.go()
