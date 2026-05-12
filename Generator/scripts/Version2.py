import blenderproc as bproc
import os
import numpy as np

bproc.init()

# Path to the assets
#Cones
BigOrangeCone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\bigOrangeCone.blend"
smallFullBlueCone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallFullBlueCone.blend"
smallRedCone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallRedCone.blend"
smallBlueCone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallBlueCone.blend"
smallYellowCone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallYellowCone.blend"

#Distractors
smallSensor_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\smallSensor.blend"

# 1. Base Szene
Straße = bproc.loader.load_blend("D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\NormalAsphalt.blend")
Zaun = bproc.loader.load_blend("D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\RoadBarrierInnit.blend")
Baeume = bproc.loader.load_blend("D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\TreelineInnit.blend")
Tribuene = bproc.loader.load_blend("D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\GroßeTribueneInnit.blend")

# 2. Objekte platzieren
BigOrangeCone = bproc.loader.load_blend(BigOrangeCone_path)
orange_cone = BigOrangeCone[0]
orange_cone.set_location([0, 0, 0])

smallFullBlueCone = bproc.loader.load_blend(smallFullBlueCone_path)
blue_cone = smallFullBlueCone[0]
blue_cone.set_location([-2, 0, 0])

smallRedCone = bproc.loader.load_blend(smallRedCone_path)
red_cone = smallRedCone[0]
red_cone.set_location([2, 0, 0])

smallYellowCone = bproc.loader.load_blend(smallYellowCone_path)
yellow_cone = smallYellowCone[0]
yellow_cone.set_location([1, 0, 0])

smallBlueCone = bproc.loader.load_blend(smallBlueCone_path)
blue_cone2 = smallBlueCone[0]
blue_cone2.set_location([-1, 0, 0])

smallSensor = bproc.loader.load_blend(smallSensor_path)
sensor = smallSensor[0]
sensor.set_location([2, 2, 0])

cube = bproc.object.create_primitive("CUBE")
cube.set_location([0, 2, 1])

# Cone-Objekte explizit in einer Liste sammeln
cone_objects = [orange_cone, blue_cone, red_cone, yellow_cone, blue_cone2]

# 2.1 Category IDs setzen – Cones per Referenz, nicht per Namensstring
for obj in bproc.object.get_all_mesh_objects():
    if obj in cone_objects:  # ✅ sicherer als Namensvergleich
        obj.set_cp("category_id", 1)
        obj.set_cp("supercategory", "cone")
    else:
        obj.set_cp("category_id", 0)

# 3. Licht-Setup
light = bproc.types.Light()
light.set_type("POINT")
light.set_location([4.076, 1, 6])
light.set_energy(1000)


# 4. Kamera
# 4.1 POI setzen 
poi = bproc.object.compute_poi(orange_cone) 
# 4.2 Kamera-Platzieren
bproc.camera.set_resolution(1280, 720)
cam_pose = bproc.math.build_transformation_mat([0.0, -9.0, 1.4700000286102295], [1.483529806137085, 0.0, 0.0])
bproc.camera.add_camera_pose(cam_pose)

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



