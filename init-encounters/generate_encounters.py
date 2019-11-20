import numpy as np
import random

def select_action(x, y):

    if ((0 < x < Nx-1) & (0 < y < Ny-1)):
        actions = ["L","R","U","D"]
        output = random.choice(actions)
        return output
    elif ((x == 0) & (y == 0)):
        actions = ["R","D"]
        output = random.choice(actions)
        return output
    elif ((x == 0) & (y == Ny-1)):
        actions = ["R","U"]
        output = random.choice(actions)
        return output
    elif ((x == Nx-1) & (y == 0)):
        actions = ["L","D"]
        output = random.choice(actions)
        return output
    elif ((x == Nx-1) & (y == Ny-1)):
        actions = ["L","U"]
        output = random.choice(actions)
        return output
    elif x == 0:
        actions = ["R","U","D"]
        output = random.choice(actions)
        return output
    elif x == Nx-1:
        actions = ["L","U","D"]
        output = random.choice(actions)
        return output
    elif y == 0:
        actions = ["L","R","D"]
        output = random.choice(actions)
        return output
    elif y == Ny-1:
        actions = ["L","R","U"]
        output = random.choice(actions)
        return output

def createEncounter(Nx, Ny, filename, nsteps_per_encounter):

    # Place intruder in random position
    x = random.randint(0, Nx-1)
    y = random.randint(0, Ny-1)

    # Open file and write first coordinates to file
    intruder_encounter_file = open(filename, "a")
    intruder_encounter_file.write(str(x) + " " + str(y) + "\n")

    # Perform steps of the encounter and save each step to a file
    for i in range(0, nsteps_per_encounter):
        # Select an appropriate action based on current location in grid
        output = select_action(x, y)
        # Update coordinates according to chosen action
        if output == "L":
            x = x - 1
        elif output == "R":
            x = x + 1
        elif output == "U":
            y = y - 1
        elif output == "D":
            y = y + 1
        # Output chosen action to file
        intruder_encounter_file.write(str(output) + "\n")
  
    # Close the file with intruder actions
    intruder_encounter_file.close()
    
# MAIN FUNCTION
    
# Define grid size and number of steps in an encounter
Nx = 10
Ny = 10
nsteps_per_encounter = 100

# Number of encounters we wish to generate
n_encounter = 1000

# Generate all of the encounters
for i in range(0,n_encounter):
    filename = "validation-encounters/validation_encounter." + str(i) + ".txt"
    createEncounter(Nx, Ny, filename, nsteps_per_encounter)
    print("Validation Encounter " + str(i) + " generated")




