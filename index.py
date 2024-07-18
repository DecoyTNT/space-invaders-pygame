import pygame
from bullet import Bullet
from enemy import Enemy
from player import Player
from pygame import mixer
import random
import math
import io
import traceback

def start():
    # Inicializar Pygame
    pygame.init()
    # Definir evento de cambio de dirección
    CHANGE_DIRECTION_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(CHANGE_DIRECTION_EVENT, 500)  # 1000 milisegundos = 1 segundos
    
    # Titulo e Icono
    pygame.display.set_caption("Space Invaders")
    icon = pygame.image.load("assets/ovni.png")
    pygame.display.set_icon(icon)
    
    # Música de fondo
    mixer.music.load("assets/musica_fondo.mp3")
    mixer.music.set_volume(0.1)
    mixer.music.play(-1)
    
    # Sonido de disparo y colisión
    shoot_sound = mixer.Sound("assets/disparo.mp3")
    shoot_sound.set_volume(0.1)
    collision_sound = mixer.Sound("assets/golpe.mp3")
    
    # Fondo
    bg_image = pygame.image.load("assets/Fondo.jpg")

    # Tamaño de la pantalla
    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))
    
    is_executed = True
    
    player = Player(width // 2 - 32, height - 10 - 64, "assets/cohete.png", screen)
    bullets = []
    enemies = []
    
    score = 0
    is_game_over = False
    
    for i in range(10):
        enemies.append(Enemy(random.randint(0, width-64), random.randint(0, 200), screen))
    
    while is_executed:
        # RGB - Red, Green and Blue
        # screen.fill((102, 178, 255))
        
        # Fondo
        screen.blit(bg_image, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_executed = False
            
            if event.type == pygame.KEYDOWN:
                # Movimiento de nave
                if event.key == pygame.K_LEFT:
                    if not is_game_over:
                        player.move('left')
                if event.key == pygame.K_RIGHT:
                    if not is_game_over:
                        player.move('right')
                # Disparo
                if event.key == pygame.K_SPACE:                    
                    if not is_game_over:
                        if len(bullets) < 10:
                            bullet = Bullet(player.position_x + 16, player.position_y - 10, "assets/bala.png", screen)
                            bullet.shoot()
                            shoot_sound.play()
                            bullets.append(bullet)
                # Reiniciar juego
                if event.key == pygame.K_RETURN:
                    if is_game_over:
                        is_game_over = False
                        player.position_x = width // 2 - 32
                        player.position_y = height - 10 - 64
                        score = 0
                        for enemy in enemies:
                            enemies.remove(enemy)
                        for i in range(10):
                            enemies.append(Enemy(random.randint(0, width-64), random.randint(0, 200), screen))
            # Cambio de dirección de los enemigos
            if event.type == CHANGE_DIRECTION_EVENT:
                for enemy in enemies:
                    enemy.change_speed()
            
            # Detener el movimiento
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.stop_move()
            
            
        player.update()
        player.make_player()
        
        for bullet in bullets:
            bullet.move()
            if bullet.position_y < 0:
                bullets.remove(bullet)
            for enemy in enemies:
                collision = is_collision(enemy, bullet)
                if collision:
                    collision_sound.play()
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    new_enemy = Enemy(random.randint(0, width-64), random.randint(0, 200), screen)
                    new_enemy.change_speed()
                    enemies.append(new_enemy)
                    score += 1
                    break
        
        for enemy in enemies:
            enemy.move()
            enemy.update()
            enemy.make_enemy()
            collision = is_collision(enemy, player)
            if collision:
                enemy.position_y = 2000
                is_game_over = True
                break
            if enemy.position_y > height - 64:                
                is_game_over = True
                enemy.position_y = 2000
                break
        
        if is_game_over:
            final_text(screen)
            player.position_y = 2000
            for enemy in enemies:
                enemies.remove(enemy)
        
        show_score(score, screen)
        
        pygame.display.update()


def is_collision(obj1, obj2):
    distance = math.sqrt((math.pow(obj1.position_x - obj2.position_x, 2)) + (math.pow(obj1.position_y - obj2.position_y, 2)))
    if distance < 27:        
        return True
    return False

def show_score(score, screen):
    font_in_bytes = font_bytes('assets/FreeSansBold.ttf')
    font = pygame.font.Font(font_in_bytes, 32)
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, (10, 10))

def final_text(screen):
    font_in_bytes = font_bytes('assets/FreeSansBold.ttf')
    font = pygame.font.Font(font_in_bytes, 64)
    font2 = pygame.font.Font(font_in_bytes, 32)
    text = font.render("Game Over", True, (255, 255, 255))
    text2 = font2.render("Presiona Enter para empezar de nuevo", True, (255, 255, 255))
    screen.blit(text, (220, 250))
    screen.blit(text2, (100, 350))
    
def font_bytes(font):
    # Abre el archivo ttf en modo lectura binaria
    with open(font, 'rb') as f:
        # Lee todos los bytes del archivo y los guarda en la variable ttf_bytes
        ttf_bytes = f.read()
    # Retorna los bytes del archivo ttf
    return io.BytesIO(ttf_bytes)

def main():
    try:
        print("Juego iniciado correctamente")
        start()
    except Exception as e:
        print("Ocurrió un error:")
        traceback.print_exc()
    finally:
        input("Presiona Enter para cerrar...")

if __name__ == "__main__":
    main()