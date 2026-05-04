import blenderproc as bproc
import numpy as np
import cv2

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

#Bounding Box
rgb = data["colors"][0] #first image 
points = bproc.camera.project_points(objs[0].get_bound_box(), frame=0)

xs = points[:, 0]
ys = points[:, 1]

xmin = int(np.min(xs))
ymin = int(np.min(ys))
xmax = int(np.max(xs))
ymax = int(np.max(ys))

img = (rgb * 255).astype(np.uint8)

# OpenCV uses BGR sometimes but rectangle still fine
cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)

# Save
cv2.imwrite("output/bbox_result.png", img)










