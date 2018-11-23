import numpy as np

class MP:
    """
    Enum to hold some of the Model Parameters
    """

    """ 
    Global Parameters
    """

    # Discretisation step
    DXY = 0.01

    # Room geometry
    ROOM_LENGTH = 4
    ROOM_WIDTH = 3
    ROOM_HEIGHT = 2.3

    # Number of lamps
    N_LAMPS = 3

    # Parameters
    LAMP_EFFICIENCY = 0.8
    LAMP_RADII = [0.1, 0.2, 0.1]

    POWER_SCALING_FACTOR = 1
    LAMP_POW = [50, 120, 50]
    LAMP_POW = np.array(LAMP_POW) * POWER_SCALING_FACTOR

    # Albedo
    ALBEDO = 0.75
    BOUNCES = 6

    # Plot parameters
    N_LEVELS = 100

    """
    Light Quality Subsystem
    """

    # Initial lamp location guess (design variables: [x1, y1, x2, y2, x3, y3])
    INITIAL_GUESS_LAMP_LOCS = np.array([1, 1, 2, 2, 3, 2.5])
    # INITIAL_GUESS_LAMP_LOCS_3D = np.array([1, 1, 1, 4, 4, 1, 6, 6, 1.5])

    # Linear Constraint Matrix
    CONSTRAINT_MAT = [[1, 0, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0, 1]]

    # Lamp 1: Bed: Bound Constraints (x1, y1)
    G1 = [LAMP_RADII[0], 2.3 - LAMP_RADII[0]]
    G2 = [LAMP_RADII[0], 1.5 - LAMP_RADII[0]]

    # Lamp 2: Floor: Bound Constraints (x2, y2)
    G3 = [0.4 + LAMP_RADII[1], 2.3 - LAMP_RADII[1]]
    G4 = [0.9 + LAMP_RADII[1], 3 - LAMP_RADII[1]]

    # Lamp 3: Desk: Bound Constraints (x3, y3)
    G5 = [2.3 + LAMP_RADII[2], 4 - LAMP_RADII[2]]
    G6 = [1.9 + LAMP_RADII[2], 3 - LAMP_RADII[2]]

    CONSTRAINTS = [G1, G2, G3, G4, G5, G6]

    # Linear Constraint Bounds
    LOWER_BOUND = [constraint[0] for constraint in CONSTRAINTS]
    UPPER_BOUND = [constraint[1] for constraint in CONSTRAINTS]

    """
    Cost Subsystem
    """

    # Cost
    CABLE_COST = 4
    LAMP_COST = 10
    WORK_COST = 60
    ENERGY_COST = 0.12
    AVG_HOURS_PER_YEAR = float(1500 / 1000)