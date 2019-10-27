import pyglet
from pyglet.gl import *
import numpy as np
pyglet.resource.path = ["images"]
pyglet.resource.reindex()

# Grid world function
def drawGridWorld(windowPixels_x, windowPixels_y, Nx, Ny):

  # Compute appropriate corners for our grid world, so that it lies sufficiently inside the window
  leftX = (2.0/8.0) * windowPixels_x
  rightX = (6.0/8.0) * windowPixels_x
  topY = (6.0/8.0) * windowPixels_y
  bottomY = (2.0/8.0) * windowPixels_y

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

def initializeAircraftAndObstacles(windowPixels_x, windowPixels_y, Nx, Ny):
  
  # Compute appropriate corners for our grid world, so that it lies sufficiently inside the window
  leftX = (2.0/8.0) * windowPixels_x
  rightX = (6.0/8.0) * windowPixels_x
  topY = (6.0/8.0) * windowPixels_y
  bottomY = (2.0/8.0) * windowPixels_y

  dx = (rightX - leftX) / Nx
  dy = (topY - bottomY) / Ny
  
  # Place aircraft on screen
  aircraft = pyglet.resource.image("aircraft.png") 
  aircraft.anchor_x = aircraft.width/2
  aircraft.anchor_y = aircraft.height/2
  aircraft_sprite = pyglet.sprite.Sprite(img=aircraft, x=leftX+0.5*dx, y=bottomY+0.5*dy)
  #aircraft_sprite.scale = 0.5
  aircraft_sprite.draw()
  
  # Place obstacle on screen
  obstacle = pyglet.resource.image("asteroid.png") 
  obstacle.anchor_x = obstacle.width/2
  obstacle.anchor_y = obstacle.height/2
  obstacle_sprite = pyglet.sprite.Sprite(img=obstacle, x=rightX-0.5*dx, y=bottomY+0.5*dy)
  #aircraft_sprite.scale = 0.5
  obstacle_sprite.draw()

# main function
windowPixels_x = 800
windowPixels_y = 800
Nx = 5
Ny = 5
game_window = pyglet.window.Window(800,800)

@game_window.event
def on_draw():

  # Clear initial window
  game_window.clear()
  
  # Draw the grid lines in grid world
  drawGridWorld(windowPixels_x, windowPixels_y, Nx, Ny)
  
  # Place aircraft on lower lefthand side of screen (can change later)
  # Place enemy on lower righthand side of screen (can change later)
  initializeAircraftAndObstacles(windowPixels_x, windowPixels_y, Nx, Ny)

  level_label = pyglet.text.Label('Aircraft Collision Avoidance Environment', font_size=24, x = windowPixels_x/2, y = windowPixels_y-100, anchor_x='center')
  level_label.draw()

pyglet.app.run()
