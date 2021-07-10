import pygame
import numpy
import time

pygame.init()

# Numero de casillas
n_cellsX = 60
n_cellsY = 60

HEIGHT = 600
WIDTH = 600
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

dim_CW = WIDTH / n_cellsX
dim_CH = HEIGHT / n_cellsY


# creamos una matriz
cells_state = numpy.zeros((n_cellsX, n_cellsY))
print(cells_state)

# Ejemplo: forma palo
cells_state[5, 6] = 1
cells_state[5, 5] = 1
cells_state[5, 4] = 1

run = True

pause = False

while run:
  # Hacemos la copia del estado anterior del juego
  newCells_state = numpy.copy(cells_state)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        run = False
    # Si la tecla pulsada es espacio negaremos el valor anterior de pause 
    # De esta forma si pause = False luego sera True y cuando volvamos a pulsar sera false
    if event.type == pygame.KEYDOWN:
     if event.key == pygame.K_SPACE:
        pause = not pause
    mouse = pygame.mouse.get_pressed()

    # Si el botón pulsado del raton es el izquierdo entonces se crea una nueva célula
    if mouse[0]:
        pos_x, pos_y = pygame.mouse.get_pos()
        cellX = int(pos_x / dim_CW) # Calculamos la casilla que estamos pulsando
        cellY = int(pos_y / dim_CH)
        newCells_state[cellX, cellY] = 1
    # Si el botón pulsado del raton es el derecho entonces la célula muere
    if mouse[2]:
        pos_x, pos_y = pygame.mouse.get_pos()
        cellX = int(pos_x / dim_CW)
        cellY = int(pos_y / dim_CH)
        newCells_state[cellX, cellY] = 0

  screen.fill([0, 0, 0])
  
  time.sleep(0.08)

  # Creamos un bucle for que recorra tanto el eje y como el x de la cuadrícula
  for y in range(0, n_cellsX):
    for x in range(0, n_cellsY):
      # Mientras el juego no este pausado las reglas de este funcionaran
      if not pause:
          # estado de las celulas vecinas
          # Utilizamos el operado % para que cuando un celula se salga del rango de la matriz vuelva al principio
          neigh_cs = cells_state[(x - 1) % n_cellsX, (y - 1) % n_cellsY] + \
                  cells_state[x % n_cellsX, (y - 1) % n_cellsY] + \
                  cells_state[(x + 1) % n_cellsX, (y - 1) % n_cellsY] + \
                  cells_state[(x - 1) % n_cellsX, y % n_cellsY] + \
                  cells_state[(x + 1) % n_cellsX, y % n_cellsY] + \
                  cells_state[(x - 1) % n_cellsX, (y + 1) % n_cellsY] + \
                  cells_state[x % n_cellsX, (y + 1) % n_cellsY] + \
                  cells_state[(x + 1) % n_cellsX, (y + 1) % n_cellsY]

          # ----------REGLAS DEL JUEGO-----------------        
          if cells_state[x, y] == 0 and neigh_cs == 3:
            newCells_state[x, y] = 1
          
          elif cells_state[x, y] == 1 and (neigh_cs == 2 or neigh_cs == 3):
            newCells_state[x, y] = 1
          
          elif cells_state[x, y] == 1 and (neigh_cs < 2 or neigh_cs > 3):
            newCells_state[x, y] = 0
      # Creamos la cuadrícula      
      grid = [(x * dim_CW, y * dim_CH),
              ((x + 1) * dim_CW, y * dim_CH),
              ((x + 1) * dim_CW, (y + 1) * dim_CH),
              (x * dim_CW, (y + 1) * dim_CH)]
      # Con polygon uniremos todos los puntos que hemos indicado en la lista grid        
      if newCells_state[x, y] == 0: 
         pygame.draw.polygon(screen, [128, 128, 128], grid, 1)
      else:
        pygame.draw.polygon(screen, [255, 255, 255], grid, 0)
  
  cells_state = newCells_state
  pygame.display.update()
