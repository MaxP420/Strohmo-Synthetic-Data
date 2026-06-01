import blenderproc as bproc
import os
import numpy as np
import random


bproc.init()








def Config():

    Config = {
        #Configuration of Scene / set True or Flase for each category / Give percentage of appearence for each Cne type
        #Cones (Enter the type)
        "BigOrange_cone": True,
        "appearance_percentage_BigOrange_cone": 0.0,

        "blue_cone": True,
        "appearance_percentage_blue_cone": 33.333333,

        "orange_cone": True,
        "appearance_percentage_orange_cone": 33.3333,

        "yellow_cone": True,
        "appearance_percentage_yellow_cone": 33.3333,

        "MinNumber_of_cones": 15,
        "MaxNumber_of_cones": 25,
        "Include_Damaged_Cones": False,
        "appearance_percentage_of_damaged_cones": 5.0,
        "Include_Knocked_Over_Cones": False,
        "appearance_percentage_knocked_over_cones": 0.0,

        #Distractors
        "MinNumber_of_distractor_Types": 2,
        "MaxNumber_of_distractor_Types": 3,
        "MinNumber_of_distractors_of_Type": 5,
        "MaxNumber_of_distractors_of_Type": 6,

        #Lighting 
        "All_lightings": True,
        "Daylight": False,
        "Sunset": False,
        "Nighttime": False,

        #Number of images to generate
        "Number_of_scenes": 1,
        "Number_of_Camera_Poses": 2,
        "YOLO_Annotation": True,
        "Output_path": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\output"
    }
    return Config


def calculate_number_of_cones(Config):
    #Calculate Number of each Cone and Distractors based on the configuration
    Cone_distribution = {
        #All Cones
        "total_cones": random.randint(Config["MinNumber_of_cones"], Config["MaxNumber_of_cones"]),
    
        #Number of normal Cones
        "number_of_orange_cones": int((Config["appearance_percentage_orange_cone"] / 100) * Config["total_cones"]),
        "number_of_blue_cones": int((Config["appearance_percentage_blue_cone"] / 100) * Config["total_cones"]),
        "number_of_yellow_cones": int((Config["appearance_percentage_yellow_cone"] / 100) * Config["total_cones"]),
        "number_of_BigOrange_cones": int((Config["appearance_percentage_BigOrange_cone"] / 100) * Config["total_cones"]),

        #Number of Damaged Cones 
        "number_of_damaged_orange_cones": int((Config["appearance_percentage_of_damaged_cones"] / 100) * Config["number_of_orange_cones"]),
        "number_of_damaged_blue_cones": int((Config["appearance_percentage_of_damaged_cones"] / 100) * Config["number_of_blue_cones"]),
        "number_of_damaged_yellow_cones": int((Config["appearance_percentage_of_damaged_cones"] / 100) * Config["number_of_yellow_cones"]),
        "number_of_damaged_BigOrange_cones": int((Config["appearance_percentage_of_damaged_cones"] / 100) * Config["number_of_BigOrange_cones"]),

        #Number of Knocked Over Cones 
        "number_of_KnockedOver_orange_cones": int((Config["appearance_percentage_of_damaged_cones"] / 100) * Config["number_of_orange_cones"]),
        "number_of_KnockedOver_blue_cones": int((Config["appearance_percentage_of_damaged_cones"] / 100) * Config["number_of_blue_cones"]),
        "number_of_KnockedOver_yellow_cones": int((Config["appearance_percentage_of_damaged_cones"] / 100) * Config["number_of_yellow_cones"]),
        "number_of_KnockedOver_BigOrange_cones": int((Config["appearance_percentage_of_damaged_cones"] / 100) * Config["number_of_BigOrange_cones"]),

        #Distractors Total and per Type. Select Distractors and palce in new list
        "total_distractor_types": random.randint(Config["MinNumber_of_distractor_Types"], Config["MaxNumber_of_distractor_Types"]),
        "total_distractors_per_type": random.randint(Config["MinNumber_of_distractors_of_Type"], Config["MaxNumber_of_distractors_of_Type"]),
        "distractors_in_scene": random.sample(Config["Distractors"], Config["total_distractor_types"])
    }
    return Cone_distribution


def Innit_Base_Scene(Config, Paths): 
    # Base Szene Laden: Tribuene, Zaun, Baeume
    tribuene = bproc.loader.load_blend(Paths["all"]["tribuene"])
    Zaun = bproc.loader.load_blend(Paths["zaun"])
    Baeume = bproc.loader.load_blend(Paths["baeume"])

    # Randomisierungsparameter für Straße, HDRI, Licht (2 Parameter)
    #Street 
    street_path = random.choice(Paths["streets"]["all"])
    Straße = bproc.loader.load_blend(street_path)

    #randomize HDRI and set world background 
    if Config["All_lightings"]:
        hdri = random.choice(Config["HDRIs"])
        bproc.world.set_world_background_hdr_img(hdri)
    elif Config["Daylight"]:
        hdri = random.choice(Config["Daylight_HDRIs"])
        bproc.world.set_world_background_hdr_img(hdri)
    elif Config["Sunset"]:
        hdri = random.choice(Config["Sunset_HDRIs"])
        bproc.world.set_world_background_hdr_img(hdri)
    elif Config["Nighttime"]:
        hdri = random.choice(Config["Nighttime_HDRIs"])
        bproc.world.set_world_background_hdr_img(hdri)

    #Set Lightsource 
    light = bproc.types.Light()
    light.set_type("POINT")
    light.set_location([4.076, 1, 6])
    light.set_energy(1000)


def select_distractors(Config, Paths):
    selected_distractors = random.sample(Paths["distractors"]["all"], Config["total_distractor_types"])
    return selected_distractors


def set_cdproperties(Paths):
    #Load Cones out of sight and set custom properties for annotation
    #Set Supercategory
    supercategory = "cone"
    for cone_path in Paths["cones"]["all"]:
        cone = bproc.loader.load_blend(cone_path)[0]
        cone.set_location([0, 0, -10])  # Move the cone out of sight

        # Set custom properties
        if "yellow_cone" in cone_path:
            cone.set_name("yellow_cone")
            cone.set_cp("category_id", 1)
            cone.set_cp("class_name", "yellow_cone")
            cone.set_cp("cone_color", "yellow")
            cone.set_cp("supercategory", supercategory)

        elif "blue_cone" in cone_path:
            cone.set_name("blue_cone")
            cone.set_cp("category_id", 2)
            cone.set_cp("class_name", "blue_cone")
            cone.set_cp("cone_color", "blue")
            cone.set_cp("supercategory", supercategory)

        elif "orange_cone" in cone_path:
            cone.set_name("orange_cone")
            cone.set_cp("category_id", 3)
            cone.set_cp("class_name", "orange_cone")
            cone.set_cp("cone_color", "orange")
            cone.set_cp("supercategory", supercategory)

        elif "big_orange_cone" in cone_path:
            cone.set_name("big_orange_cone")
            cone.set_cp("category_id", 4)
            cone.set_cp("class_name", "big_orange_cone")
            cone.set_cp("cone_color", "big_orange")
            cone.set_cp("supercategory", supercategory)

    #Load Distractors and set category_id: 0 for all non-cone objects
    for distractor_path in Paths["distractors"]["all"]:
        distractor = bproc.loader.load_blend(distractor_path)[0]
        distractor.set_location([0, 0, -10])  # Move the distractor out of sight
    
    for obj in bproc.object.get_all_mesh_objects():
        if obj.get_cp("category_id") is None:  # If the object doesn't have a category_id, set it to 0 (background)
            obj.set_cp("category_id", 0) #Check if works 
            obj.set_cp("supercategory", "background")


def placing_cones(Config, Cone_distribution):
    #Placement bounds
    x_min, x_max = -10, 10
    y_min, y_max = -10, 10
    z_value = 0 

    #Place Cones if set to True in Config with duplicates according to their distribution 
    if Config["blue_cone"]:
        for i in range(Cone_distribution["number_of_blue_cones"]):
            # Duplicate the cone
            blue_cone_duplicate = bproc.object.get_by_name("blue_cone").duplicate()
            blue_cone_duplicate.set_cp("category_id", 2)
            blue_cone_duplicate.set_cp("cone_color", "blue")
            blue_cone_duplicate.set_cp("supercategory", "cone")
            blue_cone_duplicate.set_name("blue_cone")

            # Randomize placement within bounds
            x = np.random.uniform(x_min, x_max)
            y = np.random.uniform(y_min, y_max)
            blue_cone_duplicate.set_location([x, y, z_value])

    if Config["orange_cone"]:
        for i in range(Cone_distribution["number_of_orange_cones"]):
            # Duplicate the cone
            orange_cone_duplicate = bproc.object.get_by_name("orange_cone").duplicate()
            orange_cone_duplicate.set_cp("category_id", 3)
            orange_cone_duplicate.set_cp("cone_color", "orange")
            orange_cone_duplicate.set_cp("supercategory", "cone")
            orange_cone_duplicate.set_name("orange_cone")

            # Randomize placement within bounds
            x = np.random.uniform(x_min, x_max)
            y = np.random.uniform(y_min, y_max)
            orange_cone_duplicate.set_location([x, y, z_value])
    
    if Config["yellow_cone"]:
        for i in range(Cone_distribution["number_of_yellow_cones"]):
            # Duplicate the cone
            yellow_cone_duplicate = bproc.object.get_by_name("yellow_cone").duplicate()
            yellow_cone_duplicate.set_cp("category_id", 1)
            yellow_cone_duplicate.set_cp("cone_color", "yellow")
            yellow_cone_duplicate.set_cp("supercategory", "cone")
            yellow_cone_duplicate.set_name("yellow_cone")

            # Randomize placement within bounds
            x = np.random.uniform(x_min, x_max)
            y = np.random.uniform(y_min, y_max)
            yellow_cone_duplicate.set_location([x, y, z_value])

    if Config["BigOrange_cone"]:
        for i in range(Cone_distribution["number_of_BigOrange_cones"]):
            # Duplicate the cone
            big_orange_cone_duplicate = bproc.object.get_by_name("big_orange_cone").duplicate()
            big_orange_cone_duplicate.set_cp("category_id", 4)
            big_orange_cone_duplicate.set_cp("cone_color", "big_orange")
            big_orange_cone_duplicate.set_cp("supercategory", "cone")
            big_orange_cone_duplicate.set_name("big_orange_cone")

            # Randomize placement within bounds
            x = np.random.uniform(x_min, x_max)
            y = np.random.uniform(y_min, y_max)
            big_orange_cone_duplicate.set_location([x, y, z_value])
    

def placing_distractors(Cone_distribution, selected_distractors):
    #Placement bounds 
    x_min, x_max = -10, 10
    y_min, y_max = -10, 10
    z_value = 0 

    for distractor_obj in selected_distractors:
        for i in range(Cone_distribution["total_distractors_per_type"]):
            # Duplicate distractor
            distractor_duplicate = distractor_obj.dublicate()
            # Randomize placement
            x = np.random.uniform(x_min, x_max)
            y = np.random.uniform(y_min, y_max)
            distractor_duplicate.set_location([x, y, z_value])

    
def Camera_Pose_Sampling(Config):
    for i in range(Config["Number_of_Camera_Poses"]):
        #bproc.camera.set_resolution(1280, 720)
        poi = np.random.uniform([-10, -10, 0], [10, 10, 0])  # Random POI innerhalb des Platzierungsrahmens 
        # Sample random camera location above objects in a circle around the POI
        location = np.random.uniform([-15, -15, 1], [15, 15, 2])
        # Compute rotation based on vector going from location towards poi
        rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(0,0))
        # Add homog cam pose based on location an rotation
        cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
        bproc.camera.add_camera_pose(cam2world_matrix)


def Rendering():
      # 6. Aktiviere Normals 
    bproc.renderer.enable_normals_output()
    bproc.renderer.enable_segmentation_output(map_by=["category_id", "instance", "name"])

    #7 Rendern 
    data = bproc.renderer.render()
    bproc.writer.write_hdf5("output/", data)

    output_dir = "output"

    # ✅ COCO-Annotationen mit Bounding Boxes für Jede Cone ein entsprechendes Label
    bproc.writer.write_coco_annotations(os.path.join(output_dir, "coco_data"),    # ✅ Unterordner coco_data
        instance_segmaps=data["instance_segmaps"],
        instance_attribute_maps=data["instance_attribute_maps"],
        colors=data["colors"],
        color_file_format="JPEG",
    )

def get_paths():
    Paths = {
        "cones": {
            "yellow_striped": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallYellowCone.blend",
            "blue_striped": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallBlueCone.blend",
            "big_orange_cone": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\bigOrangeCone.blend",
            "orange_cone": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallRedCone.blend",
            "yellow_cone": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallFullYellowCone.blend",
            "blue_cone": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallFullBlueCone.blend",
            "all": [
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\bigOrangeCone.blend",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallFullBlueCone.blend",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallRedCone.blend",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallBlueCone.blend",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallYellowCone.blend",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallFullYellowCone.blend"
            ]
        },

        "environment": {
            "zaun": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\RoadBarrierInnit.blend",
            "baeume": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\TreelineInnit.blend",
            "tribuene": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\GroßeTribueneInnit.blend",
        },

        "streets": {
            "plain_asphalt": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\NormalAsphalt.blend",
            "floor_pattern": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\Ground Textures\\FloorPattern.blend",
            "plaster": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\Ground Textures\\Plaster.blend",
            "ground_grey": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\Ground Textures\\GroundGrey.blend",
            "all": [
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\NormalAsphalt.blend",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\Ground Textures\\FloorPattern.blend",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\Ground Textures\\Plaster.blend",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\Ground Textures\\GroundGrey.blend"
            ]
        },

        "distractors": {
            "small_sensor": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\smallSensor.blend",
            "red_propane": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\RedPropaneTank.blend",
            "construction_light": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\ConstructionLight.blend",
            "fire_extinguisher": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\FireExtinguisher.blend",
            "cardboard_box": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\CardboardBox.blend",
            "barrel_stove": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\BarrelStove.blend",
            "barrel": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\Barrel.blend",
            "red_jerrycan": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\RedJerryCan.blend",
            "chair": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\Chair.blend",
            "trashcan": "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\TrashCan.blend",
            "all": [
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\smallSensor.blend",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\RedPropaneTank.blend",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\ConstructionLight.blend",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\FireExtinguisher.blend",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\CardboardBox.blend",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\BarrelStove.blend",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\Barrel.blend",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\RedJerryCan.blend",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\Chair.blend",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\TrashCan.blend"
            ]
        },

        "hdris": {
            "Sunrise": [


            ],
            "daylight": [
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\Daylight\\driving_school_4k.exr",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\Daylight\\mall_parking_lot_4k.exr",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\zwartkops_curve_sunset_4k.exr"
            ],
            "sunset": [


            ],
            "night": [
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\Nighttime\\sandsloot_4k.exr"
            ],
            "all": [
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\Daylight\\driving_school_4k.exr",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\Daylight\\mall_parking_lot_4k.exr",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\zwartkops_curve_sunset_4k.exr",
                "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\Nighttime\\sandsloot_4k.exr"
            ]
        }
    }

    return Paths 
    
