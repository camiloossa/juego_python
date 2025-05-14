import pygame
import random
import math
import io

from pygame import mixer

pygame.init() # Inicializamos y tenemos todas las herramientas de pygame para iniciar a trabajar

#Crear la pantalla con un tamaño establecido
pantalla = pygame.display.set_mode((800, 600))

# Configuraciones del titutlo y el icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("fondo.jpg")

# Agregar musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# Jugador 
img_jugador = pygame.image.load("cohete.png")
#Posicionamiento del jugador
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# Enemigo 
img_enemigo = []
#Posicionamiento del enemigo
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
  img_enemigo.append(pygame.image.load("enemigo.png"))
  #Posicionamiento del enemigo
  enemigo_x.append(random.randint(0, 736))
  enemigo_y.append(random.randint(50, 100))
  enemigo_x_cambio.append(0.5)
  enemigo_y_cambio.append(50)

# Bala 
bala = []
img_bala = pygame.image.load("bala.png")
#Posicionamiento del bala
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 1
bala_visible = False

# Funcion para transformar la fuente a Object Bytes
def fuente_bytes(fuente):
  # Abre un archivo TTF en modo lectura binaria
  with open(fuente, 'rb') as f:
    # Lee todos los bytes del archivo y los almacena en una variable
    ttf_bytes = f.read()
  # Crea un objeto BytesIO a partir de los bytes del archivo TTF
  return io.BytesIO(ttf_bytes)

# Variable para puntaje
puntaje = 0
fuente_como_bytes = fuente_bytes("freesansbold.ttf")
fuente = pygame.font.Font(fuente_como_bytes, 28)
texto_x = texto_y = 10

# Texto final del juego
fuente_final = pygame.font.Font('freesansbold.ttf', 50)

def texto_final():
  mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
  pantalla.blit(mi_fuente_final, (160, 200))


# Funcion mostrar puntaje
def mostrar_puntaje(x, y):
  texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
  pantalla.blit(texto, (x, y))





# Funcion que pinta al jugador en pantalla y su movimiento
def jugador(x, y):
  pantalla.blit(img_jugador, (x, y))

# Funcion que pinta al enemigo en pantalla y su movimiento
def enemigo(x, y, ene):
  pantalla.blit(img_enemigo[ene], (x, y))

# Funcion dispara bala
def dispara_bala(x, y):
  global bala_visible
  bala_visible = True
  pantalla.blit(img_bala, (x + 16, y + 10))

# Funcion para detectar colisiones
def hay_colision(x1, y1, x2, y2):
  distancia =  math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
  if distancia < 27:
    return True
  else:
    return False



# Loop del juego
se_ejecuta = True
while se_ejecuta:
  # Imagen de fondo de la pantalla
  pantalla.blit(fondo, (0, 0))

  # Iterar eventos
  for evento in pygame.event.get():
    # Evento que sirve para finalizar el programa
    if evento.type == pygame.QUIT:
      se_ejecuta = False 

    # Evento que verifica si se presiono una tecla
    if evento.type == pygame.KEYDOWN:
      if evento.key == pygame.K_LEFT:
        jugador_x_cambio = -1
      if evento.key == pygame.K_RIGHT:
        jugador_x_cambio = 1
      if evento.key == pygame.K_SPACE:
        sonido_bala = mixer.Sound('disparo.mp3')
        if  not bala_visible:
          sonido_bala.play()
          bala_x = jugador_x
          dispara_bala(bala_x, bala_y)
    # Evento que verifica si se solto una flecha
    if evento.type == pygame.KEYUP:
      if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
        jugador_x_cambio = 0   

  # Modificar ubicación del jugador 
  jugador_x += jugador_x_cambio

  # Mantener al jugador dentro de los border
  if jugador_x <= 0:
    jugador_x = 0
  elif jugador_x >= 736:
    jugador_x = 736

  # Modificar ubicación del enemigo 
  for e in range(cantidad_enemigos):

    # Fin del juego
    if enemigo_y[e] > 450:
      for k in range(cantidad_enemigos):
        enemigo_y[k] = 1000
      texto_final()
      break

    enemigo_x[e] += enemigo_x_cambio[e]

    # Mantener al enemigo dentro de los border
    if enemigo_x[e] <= 0:
      enemigo_x_cambio[e] = 0.5
      enemigo_y[e] += enemigo_y_cambio[e]
    elif enemigo_x[e] >= 736:
      enemigo_x_cambio[e] = -0.5
      enemigo_y[e] += enemigo_y_cambio[e]
    
    # Verificación de colision
    colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
    if colision and bala_visible:
      sonido_colision = mixer.Sound('golpe_1.mp3')
      sonido_colision.set_volume(0.3)
      sonido_colision.play()
      bala_y = 500
      bala_visible = False
      puntaje += 1
      enemigo_x[e] = random.randint(0, 736)
      enemigo_y[e] = random.randint(50, 100)
    
    enemigo(enemigo_x[e], enemigo_y[e], e)

  # Movimiento de la bala
  if bala_y <= -64:
    bala_y = 500
    bala_visible = False

  if bala_visible:
    dispara_bala(bala_x, bala_y)
    bala_y -= bala_y_cambio 


  jugador(jugador_x, jugador_y)

  mostrar_puntaje(texto_x, texto_y)
  

  # Actualizar pantalla 
  pygame.display.update()