from pyglet.gl import * 

def computeGridCorners(windowPixels_x, windowPixels_y, Nx, Ny):

  # Compute corners of grid world
  leftX = (1.0/4.0) * windowPixels_x
  rightX = (3.0/4.0) * windowPixels_x
  topY = (3.0/4.0) * windowPixels_y
  bottomY = (1.0/4.0) * windowPixels_y

  return leftX, rightX, topY, bottomY

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

