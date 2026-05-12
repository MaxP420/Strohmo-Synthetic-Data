import blenderproc as bproc
import os

bproc.init()

# Path to the assets
BigOrangeCone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\bigOrangeCone.blend"
smallFullBlueCone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallFullBlueCone.blend"
smallRedCone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallRedCone.blend"
smallBlueCone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallBlueCone.blend"
smallYellowCone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallYellowCone.blend"

smallSensor_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\smallSensor.blend"

# 1. Base Szene: Straße + Zaun + Bäume + Tribüne + HDRI 

Straße = bproc.loader.load_blend("D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\NormalAsphalt.blend")
Straße = Straße[0]  
Straße.set_cp("category_id", 0)
Straße.set_cp("class_name", "background")
Zaun = bproc.loader.load_blend("D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\RoadBarrierInnit.blend")
Zaun = Zaun[0]  
Zaun.set_cp("category_id", 0)
Zaun.set_cp("class_name", "background")
Baeume = bproc.loader.load_blend("D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\TreelineInnit.blend")
Baeume = Baeume[0]  
Baeume.set_cp("category_id", 0)
Baeume.set_cp("class_name", "background")
Tribuene = bproc.loader.load_blend("D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\GroßeTribueneInnit.blend")
Tribuene = Tribuene[0]  
Tribuene.set_cp("category_id", 0)
Tribuene.set_cp("class_name", "background")


#2. Objekte platzieren
# 2.1 Cones Platzieren Test 
BigOrangeCone = bproc.loader.load_blend(BigOrangeCone_path)
cone_obj = BigOrangeCone[0]                 # einzelnes MeshObject
cone_obj.set_location([0, 0, 0])
cone_obj.set_cp("category_id", 1)
cone_obj.set_cp("class_name", "cone")

smallFullBlueCone = bproc.loader.load_blend(smallFullBlueCone_path)
blue_cone = smallFullBlueCone[0]
blue_cone.set_location([-2, 0, 0])
blue_cone.set_cp("category_id", 1)
blue_cone.set_cp("class_name", "cone")

smallRedCone = bproc.loader.load_blend(smallRedCone_path)
red_cone = smallRedCone[0]
red_cone.set_location([2, 0, 0])
red_cone.set_cp("category_id", 1)
red_cone.set_cp("class_name", "cone")

smallYellowCone = bproc.loader.load_blend(smallYellowCone_path)
yellow_cone = smallYellowCone[0]
yellow_cone.set_location([1, 0, 0])
yellow_cone.set_cp("category_id", 1)
yellow_cone.set_cp("class_name", "cone")

smallBlueCone = bproc.loader.load_blend(smallBlueCone_path)
blue_cone = smallBlueCone[0]
blue_cone.set_location([-1, 0, 0])
blue_cone.set_cp("category_id", 1)
blue_cone.set_cp("class_name", "cone")

# 2.2 Distractor platzieren 
smallSensor = bproc.loader.load_blend(smallSensor_path)
sensor = smallSensor[0]
sensor.set_location([2, 2, 0])
sensor.set_cp("category_id", 0)
sensor.set_cp("class_name", "distractor")

cube = bproc.object.create_primitive("CUBE")  
cube_obj = cube
cube_obj.set_location([0, 2, 1])
cube_obj.set_cp("category_id", 0)
cube_obj.set_cp("class_name", "distractor")


#3. Licht-Setup 
light = bproc.types.Light()
light.set_type("POINT")
light.set_location([4.076, 1, 6])
light.set_energy(1000)

#4. Kamera-Platzieren
bproc.camera.set_resolution(1280, 720)
cam_pose = bproc.math.build_transformation_mat([0.0, -9.0, 1.4700000286102295], [1.483529806137085, 0.0, 0.0])
bproc.camera.add_camera_pose(cam_pose)

#5. HDRI hinzufügen 
hdri_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\zwartkops_curve_sunset_4k.exr"
bproc.world.set_world_background_hdr_img(hdri_path)

#6 COCO Annotaions hinzufügen 
# activate normal rendering
bproc.renderer.enable_normals_output()
bproc.renderer.enable_segmentation_output(map_by=["category_id", "instance", "name"])


#6. Rendern 
data = bproc.renderer.render()
bproc.writer.write_hdf5("output/", data)

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
# Write data to coco file
bproc.writer.write_coco_annotations(
                                    output_dir = output_dir,
                                    instance_segmaps=data["instance_segmaps"],
                                    instance_attribute_maps=data["instance_attribute_maps"],
                                    colors=data["colors"],
                                    color_file_format="JPEG",
                                    supercategory = "cone")
