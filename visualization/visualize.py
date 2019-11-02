import pyglet
from pyglet.gl import *
import numpy as np
pyglet.resource.path = ["images"]
pyglet.resource.reindex()
from pyglet.window import key
import pylab
from gridWorld import *
from initializeAircraftAndObstacles import *

#####################################
# main function
#####################################
# User can decide if they want to use keys to scroll through aircraft actions, or just let the GUI scroll through automatically
key_inputs_FLAG = 1

# Initialize the game window with pixels and grid points specified
windowPixels_x = 800
windowPixels_y = 800
Nx = 5
Ny = 5
game_window = pyglet.window.Window(windowPixels_x, windowPixels_y)

# Allow for key inputs
keys = key.KeyStateHandler()
game_window.push_handlers(keys)

# Call function to create aircraft and obstacle sprites
aircraft_sprite = initializeAircraft(windowPixels_x, windowPixels_y, Nx, Ny)
obstacle_sprite = initializeObstacle(windowPixels_x, windowPixels_y, Nx, Ny)

# Open file containing position data for aircraft
filename = "position.txt"
data = pylab.loadtxt(open(filename), delimiter=' ', usecols=(0,1))
maxMoves = len(data[:,0])
moveNumber = 0

# Read the (i,j) position of the aircraft at a specific points in the episode
def readPosition(data, moveNumber):
  i = data[moveNumber, 0]
  j = data[moveNumber, 1]

  return i, j

# Move the aircraft to the correct pixel location based on the current (i,j) read from file
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
  
# Call update function every cycle to detect key inputs and move accordingly
def update(dt):
  global moveNumber
  i, j = readPosition(data, moveNumber)
  moveAircraft(windowPixels_x, windowPixels_y, i, j)
  if (key_inputs_FLAG == 0):
    if (moveNumber < maxMoves - 1):
      moveNumber = moveNumber + 1
  else: 
    if (keys[key.RIGHT] and moveNumber < maxMoves-1):
      moveNumber = moveNumber + 1 
    if (keys[key.LEFT] and moveNumber > 0):
      moveNumber = moveNumber - 1
 
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
