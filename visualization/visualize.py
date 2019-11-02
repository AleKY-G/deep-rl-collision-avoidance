import pyglet
from pyglet.gl import *
import numpy as np
pyglet.resource.path = ["images"]
pyglet.resource.reindex()
from pyglet.window import key
import pylab

def computeGridCorners(windowPixels_x, windowPixels_y, Nx, Ny):

  # Compute corners of grid world
  leftX = (1.0/4.0) * windowPixels_x
  rightX = (3.0/4.0) * windowPixels_x
  topY = (3.0/4.0) * windowPixels_y
  bottomY = (1.0/4.0) * windowPixels_y

  return leftX, rightX, topY, bottomY, 

# Grid world function
def drawGridWorld(windowPixels_x, windowPixels_y, Nx, Ny):

  # Compute appropriate corners for our grid world, so that it lies sufficiently inside the window
  leftX, rightX, topY, bottomY = computeGridCorners(windowPixels_x, windowPixels_y, Nx, Ny)

  glBegin(GL_LINES)
  
  # Draw all horizontal lines in the grid
  dx = (rightX - leftX) / Nx
  for i in range(Nx+1):
    x = leftX + i * dx
    glVertex2f(x, topY)
    glVertex2f(x, bottomY)

  # Draw all vertical lines in the grid
  dy = (topY - bottomY) / Ny
  for j in range(Ny+1):
    y = bottomY + j * dy
    glVertex2f(leftX, y)
    glVertex2f(rightX, y)

  # Mark the goal with an X
  leftCornerX = rightX - dx
  bottomCornerY = topY - dy
  glVertex2f(leftCornerX, bottomCornerY)
  glVertex2f(rightX, topY)
  glVertex2f(leftCornerX, topY)
  glVertex2f(rightX, bottomCornerY)

  glEnd()

# Create aircraft
def initializeAircraft(windowPixels_x, windowPixels_y, Nx, Ny):
  
  # Compute appropriate corners for our grid world, so that it lies sufficiently inside the window
  leftX, rightX, topY, bottomY = computeGridCorners(windowPixels_x, windowPixels_y, Nx, Ny)
  dx = (rightX - leftX) / Nx
  dy = (topY - bottomY) / Ny
  
  # Create aircraft object
  aircraft = pyglet.resource.image("aircraft.png") 
  aircraft.anchor_x = aircraft.width/2
  aircraft.anchor_y = aircraft.height/2
  aircraft_sprite = pyglet.sprite.Sprite(img=aircraft, x=leftX+0.5*dx, y=bottomY+0.5*dy)
  #aircraft_sprite.scale = 0.5
  
  return aircraft_sprite

# Create obstacles
def initializeObstacle(windowPixels_x, windowPixels_y, Nx, Ny):
  
  # Compute appropriate corners for our grid world, so that it lies sufficiently inside the window
  leftX, rightX, topY, bottomY = computeGridCorners(windowPixels_x, windowPixels_y, Nx, Ny)
  dx = (rightX - leftX) / Nx
  dy = (topY - bottomY) / Ny
  
  # Place obstacle on screen
  obstacle = pyglet.resource.image("asteroid.png") 
  obstacle.anchor_x = obstacle.width/2
  obstacle.anchor_y = obstacle.height/2
  obstacle_sprite = pyglet.sprite.Sprite(img=obstacle, x=rightX-0.5*dx, y=bottomY+0.5*dy)
  #obstacle_sprite.scale = 0.5
  obstacle_sprite.draw()

  return obstacle_sprite

#####################################
# main function
#####################################
windowPixels_x = 800
windowPixels_y = 800
Nx = 5
Ny = 5
game_window = pyglet.window.Window(800,800)
keys = key.KeyStateHandler()
game_window.push_handlers(keys)

# Call function to create aircraft and obstacle sprites
aircraft_sprite = initializeAircraft(windowPixels_x, windowPixels_y, Nx, Ny)
obstacle_sprite = initializeObstacle(windowPixels_x, windowPixels_y, Nx, Ny)

filename = "position.txt"

data = pylab.loadtxt(open(filename), delimiter=' ', usecols=(0,1))
maxMoves = len(data[:,0])
print(maxMoves)
def readPosition(data, moveNumber):
  i = data[moveNumber, 0]
  j = data[moveNumber, 1]

  return i, j

def moveAircraft(windowPixels_x, windowPixels_y, i, j):
  # Compute appropriate corners for our grid world, so that it lies sufficiently inside the window
  leftX, rightX, topY, bottomY = computeGridCorners(windowPixels_x, windowPixels_y, Nx, Ny)
  dx = (rightX - leftX) / Nx
  dy = (topY - bottomY) / Ny
  
  # Compute new x position and y position of aircraft based on index
  x_pos = leftX + 0.5 * dx + i * dx
  y_pos = bottomY + 0.5 * dy + j * dy
  
  # Update aircraft position properties to match new position
  aircraft_sprite.x = x_pos
  aircraft_sprite.y = y_pos
  
moveNumber = 0
# Call update function every cycle to detect key inputs and move accordingly
def update(dt):
  global moveNumber
  i, j = readPosition(data, moveNumber)
  moveAircraft(windowPixels_x, windowPixels_y, i, j)
  print(moveNumber)
  if (keys[key.RIGHT] and moveNumber < maxMoves-1):
    moveNumber = moveNumber + 1 
  if (keys[key.LEFT] and moveNumber > 0):
    moveNumber = moveNumber - 1
 
# Call update function every cycle to detect key inputs and move accordingly
def updateOld(dt):
  if keys[key.LEFT]:
    aircraft_sprite.x = aircraft_sprite.x - 100*dt
    aircraft_sprite.rotation = 180
  if keys[key.RIGHT]:
    aircraft_sprite.x = aircraft_sprite.x + 100*dt
    aircraft_sprite.rotation = 0
  if keys[key.UP]:
    aircraft_sprite.y = aircraft_sprite.y + 100*dt
    aircraft_sprite.rotation = 270
  if keys[key.DOWN]:
    aircraft_sprite.y = aircraft_sprite.y - 100*dt
    aircraft_sprite.rotation = 90

@game_window.event
def on_draw():

  # Clear initial window
  game_window.clear()
  
  # Draw the grid lines in grid world
  drawGridWorld(windowPixels_x, windowPixels_y, Nx, Ny)
  
  # Place aircraft on lower lefthand side of screen (can change later)
  aircraft_sprite.draw()

  # Place enemy on lower righthand side of screen (can change later)
  obstacle_sprite.draw()

  # Create title of the environment (Aircraft Collision Avoidance Environment)
  level_label = pyglet.text.Label('Aircraft Collision Avoidance Environment', font_size=24, x = windowPixels_x/2, y = windowPixels_y-100, anchor_x='center')
  level_label.draw()

# Run update function to update position of airplane every cycle 
pyglet.clock.schedule_interval(update, 1/30.0)
pyglet.app.run()
