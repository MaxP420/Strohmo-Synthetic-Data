import blenderproc as bproc
import os
import numpy as np
import random



bproc.init() 

# 1. Base Szene
Straße = bproc.loader.load_blend("D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\NormalAsphalt.blend")
Zaun = bproc.loader.load_blend("D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\RoadBarrierInnit.blend")
Baeume = bproc.loader.load_blend("D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\TreelineInnit.blend")
Tribuene = bproc.loader.load_blend("D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\GroßeTribueneInnit.blend")

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


# 2. Cones Innit
BigOrangeCone = bproc.loader.load_blend(BigOrangeCone_path)
orange_cone = BigOrangeCone[0]

BlueCone = bproc.loader.load_blend(smallFullBlueCone_path)
blue_cone = BlueCone[0]

RedCone = bproc.loader.load_blend(smallRedCone_path)
red_cone = RedCone[0]

YellowCone = bproc.loader.load_blend(smallYellowCone_path)
yellow_cone = YellowCone[0]

# 2.1 Cone Liste erstellen 
cones = [orange_cone, blue_cone, red_cone, yellow_cone]
# 2.2 Coustom Properties setzen 
for obj in bproc.object.get_all_mesh_objects():
    if obj in cones:  # ✅ sicherer als Namensvergleich
        obj.set_cp("category_id", 1)
        obj.set_cp("supercategory", "cone")
    else:
        obj.set_cp("category_id", 0)
# 2.3 Cone platzierungsrahmen bestimmen  
x_min, x_max = -10, 10
y_min, y_max = -10, 10
z_value = 0
dublicates = []
# 2.4 Cones zufällig platzieren
for obj in cones: 
    for i in range(5): 
        dub = obj.duplicate() 
        dub.set_cp("category_id", 1)
        dub.set_cp("supercategory", "cone")

        x = np.random.uniform(x_min, x_max)
        y = np.random.uniform(y_min, y_max)

        dub.set_location([x, y, z_value])
        dublicates.append(dub)

# 3. Licht-Setup
light = bproc.types.Light()
light.set_type("POINT")
light.set_location([4.076, 1, 6])
light.set_energy(1000)

# 4. Kamera
# 4.1 POI random setzen 
#poi = np.random.uniform([-10, -10, 0], [10, 10, 0])  # Random POI innerhalb des Platzierungsrahmens 

# 4.2 Kamera-Platzieren (2-Simple Posen)
for i in range(4):
    poi = np.random.uniform([-10, -10, 0], [10, 10, 0])  # Random POI innerhalb des Platzierungsrahmens 
    # Sample random camera location above objects in a circle around the POI
    location = np.random.uniform([-15, -15, 1], [15, 15, 2])
    # Compute rotation based on vector going from location towards poi
    rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(0,0))
    # Add homog cam pose based on location an rotation
    cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
    bproc.camera.add_camera_pose(cam2world_matrix)

# 5. HDRI
hdri_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\zwartkops_curve_sunset_4k.exr"
bproc.world.set_world_background_hdr_img(hdri_path)


# 6. Aktiviere Normals 
bproc.renderer.enable_normals_output()
bproc.renderer.enable_segmentation_output(map_by=["category_id", "instance", "name"])

#7 Rendern 
data = bproc.renderer.render()



output_dir = "output"

# ✅ COCO-Annotationen mit Bounding Boxes (nur Cones, category_id=1)
bproc.writer.write_coco_annotations(os.path.join(output_dir, "coco_data"),    # ✅ Unterordner coco_data
    instance_segmaps=data["instance_segmaps"],
    instance_attribute_maps=data["instance_attribute_maps"],
    colors=data["colors"],
    color_file_format="JPEG",
)
