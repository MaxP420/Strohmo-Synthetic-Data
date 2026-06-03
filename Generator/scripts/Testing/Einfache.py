import blenderproc as bproc
import numpy as np

bproc.init()
# Path to the assets
#Cones
BigOrangeCone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\bigOrangeCone.blend"
smallFullBlueCone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallFullBlueCone.blend"
smallRedCone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallRedCone.blend"
smallBlueCone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallBlueCone.blend"
smallYellowCone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallYellowCone.blend"
smallFullBlue_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallFullBlueCone.blend"
#Distractors
smallSensor_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\smallSensor.blend"
#Object laden
BigOrangeCone = bproc.loader.load_blend(BigOrangeCone_path)
orange_cone = BigOrangeCone[0]
orange_cone.set_location([0, 0, -5])

BlueCone = bproc.loader.load_blend(smallFullBlueCone_path)
blue_cone = BlueCone[0]


# Create a point light next to it
light = bproc.types.Light()
light.set_location([2, -2, 0])
light.set_energy(300)

# Set the camera to be in front of the object
cam_pose = bproc.math.build_transformation_mat([2.0716500282287598, -1.9419399499893188, 1.3450347185134888], [1.1093189716339111, 4.011331711240018e-09, 0.8149281740188599])
bproc.camera.add_camera_pose(cam_pose)


# Render the scene
data = bproc.renderer.render()

# Write the rendering into an hdf5 file
bproc.writer.write_hdf5("output/", data)