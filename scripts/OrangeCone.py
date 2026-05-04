import blenderproc as bproc
import numpy as np


bproc.init()

#Object laden
objs = bproc.loader.load_blend("D:/Strohmo/Synthetic Data/Strohmo-Synthetic-Data/assets/Cones/bigOrangeCone.blend")
objs[0].set_location([0,0,0])

# Create a point light next to it
light = bproc.types.Light()
light.set_location([2, -2, 0])
light.set_energy(300)

# Set the camera to be in front of the object
cam_pose = bproc.math.build_transformation_mat([3, 0, 2], [1.0471975803375244, 0.0, 1.5707963705062866])
bproc.camera.add_camera_pose(cam_pose)

# Render the scene
data = bproc.renderer.render()

# Render the scene
data = bproc.renderer.render()

# Write the rendering into an hdf5 file
bproc.writer.write_hdf5("output/", data)








