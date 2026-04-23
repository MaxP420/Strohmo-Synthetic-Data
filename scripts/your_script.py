import blenderproc as bproc
import os

bproc.init()

# -------------------
# OBJECTS
# -------------------
cube = bproc.object.create_primitive("CUBE")
cube.set_location([0, 0, 1])

plane = bproc.object.create_primitive("PLANE")
plane.set_scale([5, 5, 1])

# -------------------
# LIGHT
# -------------------
light = bproc.types.Light()
light.set_type("POINT")
light.set_location([2, -2, 3])
light.set_energy(1500)

# -------------------
# CAMERA (WICHTIG FIX)
# -------------------
cam_pose = bproc.math.build_transformation_mat([0, -4, 1.5], [1.2, 0, 0])
bproc.camera.add_camera_pose(cam_pose)

# -------------------
# RENDER
# -------------------
data = bproc.renderer.render()

# -------------------
# OUTPUT
# -------------------
os.makedirs("output", exist_ok=True)
bproc.writer.write_hdf5("output", data)

print("Done")