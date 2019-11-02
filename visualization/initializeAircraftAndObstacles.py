# Import pyglet
import pyglet
pyglet.resource.path = ["images"]
pyglet.resource.reindex()

# Import grid world functions
from gridWorld import computeGridCorners

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

