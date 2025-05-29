import numpy as np
import GrenzVel
from scipy.interpolate import splprep

# Create dummy path
x = np.linspace(0, 1, 10)
y = np.sin(x * 2 * np.pi)
z = np.cos(x * 2 * np.pi)
tckp, _ = splprep([x, y, z], s=0)

# Dummy points: Yellow, Green, Cyan, Magenta (each [x,y,z])
Points = np.array([
    [0.0, 0.0, 0.0],
    [0.2, 0.1, 0.1],
    [0.4, 0.2, 0.2],
    [0.6, 0.3, 0.3],
])

# Call compiled function
out = GrenzVel.GrenzVel(
    tckp,
    Points,
    maxVel=2.0,
    ProzentMaxVel=0.8,
    maxAcc=1.0,
    ProzentMaxAcc=0.9,
    Schiebe=20,
    SwitchSchiebe=1,
    debug=0
)

print("GrenzVel returned:", type(out), len(out))
