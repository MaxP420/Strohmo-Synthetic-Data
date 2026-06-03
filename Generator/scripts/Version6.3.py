import blenderproc as bproc
import os
import bpy
import numpy as np
import random


bproc.init()


#Paths
# Path to the assets
#Cones
yellow_striped_cone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallYellowCone.blend" #NOT FSF striped yellow cone
blue_striped_cone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallBlueCone.blend" #NOT FSF striped blue cone
#FSF
orange_cone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallRedCone.blend" #FSF full orange cone
yellow_cone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallFullYellowCone.blend" #FSF Full Yellow
blue_cone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\smallFullBlueCone.blend" #FSF full blue cone 
BigOrangeCone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\bigOrangeCone.blend" #NOT FSF big orange cone
#FSF damaged/imperfect
blue_cone_damaged_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\Damaged Cones\\blue_cone_damaged.blend"
yellow_cone_damaged_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\Damaged Cones\\smallFullYellowConeDamaged.blend"
orange_cone_damaged_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\Damaged Cones\\smallRedConeDamaged.blend"
#FSF Knocked OverCone ? 
blue_knocked_over_cone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\BlueKnockedOverCone.blend"
yellow_knocked_over_cone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\YellowKnockedOverCone.blend"
orange_knocked_over_cone_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Cones\\RedKnockedOverCone.blend"
Cones = [BigOrangeCone_path, blue_cone_path, orange_cone_path, blue_striped_cone_path, yellow_striped_cone_path, yellow_cone_path, blue_cone_damaged_path, yellow_cone_damaged_path, orange_cone_damaged_path, blue_knocked_over_cone_path, yellow_knocked_over_cone_path, orange_knocked_over_cone_path]

#Base Scene Objects
Zaun_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\RoadBarrierInnit.blend"
Baeume_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\TreelineInnit.blend"
Tribuene_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\GroßeTribueneInnit.blend"

#Straßentypen Normal
PlainAspahlt_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\Ground Textures\\NormalAsphalt.blend"
floorPattern_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\Ground Textures\\FloorPattern.blend"
plaster_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\Ground Textures\\Plaster.blend"
groundGrey_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\Ground Textures\\GroundGrey.blend"

#Straßentypen Nass
PlainAsphalt_wet_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\Ground Textures\\NormalAsphaltWet.blend"
floorPattern_wet_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\Ground Textures\\FloorPatternWet.blend"
plaster_wet_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\Ground Textures\\PlasterWet.blend"
groundGrey_wet_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\Ground Textures\\GroundGreyWet.blend"

Streets = [PlainAspahlt_path, floorPattern_path, plaster_path, groundGrey_path]
WetStreets = [PlainAsphalt_wet_path, floorPattern_wet_path, plaster_wet_path, groundGrey_wet_path]
#Distractors
smallSensor_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\smallSensor.blend"
redPropaneTank_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\RedPropaneTank.blend"
constructionLight_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\ConstructionLight.blend"
fireExtinguisher_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\FireExtinguisher.blend"
cardboardBox_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\CardboardBox.blend"
barrelStove_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\BarrelStove.blend"
barell_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\Barrel.blend"
redJerryCan_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\RedJerryCan.blend"
Chair_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\Chair.blend"
TrashCan_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\distractors\\TrashCan.blend"

Distractors = [smallSensor_path, redPropaneTank_path, constructionLight_path, fireExtinguisher_path, cardboardBox_path, barrelStove_path, barell_path, redJerryCan_path, Chair_path, TrashCan_path]

#HDRIs
#Daylight 
driving_school_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\Daylight\\driving_school_4k.exr"
mallParkingLot_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\Daylight\\mall_parking_lot_4k.exr"
racetrack_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\zwartkops_curve_sunset_4k.exr"
#Sunset
belfast_sunset_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\Sunset\\belfast_sunset_4k.exr"
bambanani_sunset_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\Sunset\\bambanani_sunset_4k.exr"
#Sunrise
spruit_sunrise_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\Sunrise\\spruit_sunrise_4k.exr"
#Nighttime
sandsloot_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\Nighttime\\sandsloot_4k.exr"
#Cloudy (For Bad Weather)
shudu_lake = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\Cloudy\\shudu_lake_4k.exr"
airfield = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\hdri\\Cloudy\\hanger_exterior_cloudy_4k.exr"


Daylight_HDRIs = [driving_school_path, mallParkingLot_path, racetrack_path]
Sunset_HDRIs = [belfast_sunset_path, bambanani_sunset_path]
Sunrise_HDRIs = [spruit_sunrise_path]
Nighttime_HDRIs = [sandsloot_path]
Cloudy_HDRIs = [shudu_lake, airfield]
HDRIs = Daylight_HDRIs + Sunset_HDRIs + Sunrise_HDRIs + Nighttime_HDRIs + Cloudy_HDRIs






#Configuration of Scene / set True or Flase for each category / Give percentage of appearence for each Cne type
#Cones (Enter the type)
BigOrange_cone = True
appearance_percentage_BigOrange_cone = 0.0

blue_cone = True
appearance_percentage_blue_cone = 33.333333

orange_cone = True
appearance_percentage_orange_cone = 33.3333

yellow_cone = True
appearance_percentage_yellow_cone = 33.3333

MinNumber_of_cones = 10
MaxNumber_of_cones = 15
Include_Damaged_Cones = False
appearance_percentage_of_damaged_cones = 10.0 #in percent
Include_Knocked_Over_Cones = False 
appearance_percentage_of_knocked_over_cones = 10.0 #in percent 

#Distractors
MinNumber_of_distractor_Types = 2
MaxNumber_of_distractor_Types = 3
MinNumber_of_distractors_of_Type = 2
MaxNumber_of_distractors_of_Type = 3

#Lighting 
All_lightings = False
BadWeather = False
Daylight = True
Sunset = False
Sunrise = False
Nighttime = False

#Artefakte
MotionBlur = False
Distortion = False

#Number of images to generate
Number_of_scenes = 1
Number_of_Camera_Poses = 4
YOLO_Annotation = True
#Set Camera Resolution x,y 
CameraResX = 640
CameraResY = 640
Output_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\output"










bproc.utility.reset_keyframes()
#Funktion Body of Loop

#Calculate Number of each Cone and Distractors based on the configuration
#All Cones
total_cones = random.randint(MinNumber_of_cones, MaxNumber_of_cones)
#Number of normal Cones
number_of_orange_cones = int((appearance_percentage_orange_cone / 100) * total_cones)
number_of_blue_cones = int((appearance_percentage_blue_cone / 100) * total_cones)
number_of_yellow_cones = int((appearance_percentage_yellow_cone / 100) * total_cones)
number_of_BigOrange_cones = int((appearance_percentage_BigOrange_cone / 100) * total_cones)
#Number of Damaged Cones 
number_of_damaged_orange_cones = int((appearance_percentage_of_damaged_cones / 100) * number_of_orange_cones)
number_of_damaged_blue_cones = int((appearance_percentage_of_damaged_cones / 100) * number_of_blue_cones)
number_of_damaged_yellow_cones = int((appearance_percentage_of_damaged_cones / 100) * number_of_yellow_cones)
number_of_damaged_BigOrange_cones = int((appearance_percentage_of_damaged_cones / 100) * number_of_BigOrange_cones)
#Number of Knocked Over Cones 
number_of_KnockedOver_orange_cones = 5 #int(round((appearance_percentage_of_knocked_over_cones/100)*total_cones * (appearance_percentage_orange_cone/100)))
number_of_KnockedOver_blue_cones = 5 #int(round((appearance_percentage_of_knocked_over_cones/100)*total_cones * (appearance_percentage_blue_cone/100)))
number_of_KnockedOver_yellow_cones = 5 #int(round((appearance_percentage_of_knocked_over_cones/100)*total_cones * (appearance_percentage_yellow_cone/100)))
number_of_KnockedOver_BigOrange_cones = 0 #int(round((appearance_percentage_of_knocked_over_cones/100)*total_cones * (appearance_percentage_BigOrange_cone/100)))
#Distractors Total and per Type. Select Distractors and palce in new list
total_distractor_types = random.randint(MinNumber_of_distractor_Types, MaxNumber_of_distractor_Types)
total_distractors_per_type = random.randint(MinNumber_of_distractors_of_Type, MaxNumber_of_distractors_of_Type)
distractors_in_scene = random.sample(Distractors, total_distractor_types)













#Innit Base Scene 
# Base Szene Laden: Tribuene, Zaun, Baeume
Tribuene = bproc.loader.load_blend(Tribuene_path)
Zaun = bproc.loader.load_blend(Zaun_path)
Baeume = bproc.loader.load_blend(Baeume_path)

# Randomisierungsparameter für Straße, HDRI, Licht (2 Parameter)
#Street
#randomize HDRI and set world background + Street 
if All_lightings:
    random_lighing_condition = random.choice(["Daylight_HDRIs", "Sunset_HDRIs", "Sunrise_HDRIs", "Nighttime_HDRIs", "Cloudy_HDRIs"])
    if random_lighing_condition == "Daylight_HDRIs":
        Daylight = True 
    elif random_lighing_condition == "Sunset_HDRIs":
        Sunset = True 
    elif random_lighing_condition == "Sunrise_HDRIs":
        Sunrise = True 
    elif random_lighing_condition == "Nighttime_HDRIs":
        Nighttime = True 
    elif random_lighing_condition == "Cloudy_HDRIs":
        BadWeather = True

if Daylight:
    hdri = random.choice(Daylight_HDRIs)
    bproc.world.set_world_background_hdr_img(hdri)
    #Set Lighsource for Daylight
    light = bproc.types.Light()
    light.set_type("POINT")
    light.set_location([4.076, 1, 6])
    light.set_energy(1000)

elif Sunset:
    hdri = random.choice(Sunset_HDRIs)
    bproc.world.set_world_background_hdr_img(hdri)
    #Set Lightsource for Sunset
    light = bproc.types.Light()
    light.set_type("POINT")
    light.set_location([6.0, -3.0, 1.8])
    light.set_energy(500)
    # deeper orange/red
    light.set_color([1.0, 0.42, 0.22])

elif Sunrise:
    hdri = random.choice(Sunrise_HDRIs)
    bproc.world.set_world_background_hdr_img(hdri)
    #Set Lightsource for Sunrise
    light = bproc.types.Light()
    light.set_type("POINT")
    light.set_location([-6.0, -2.0, 2.5])
    light.set_energy(350)
    # warm orange
    light.set_color([1.0, 0.58, 0.32])

elif Nighttime:
    hdri = random.choice(Nighttime_HDRIs)
    bproc.world.set_world_background_hdr_img(hdri)
    #Set Lighsource for Nighttime
    light = bproc.types.Light()
    light.set_type("POINT")
    light.set_location([2.0, -1.0, 8.0])
    light.set_energy(35)
    # cold blue
    light.set_color([0.55, 0.65, 1.0])

elif BadWeather: 
    hdri = random.choice(Cloudy_HDRIs)
    bproc.world.set_world_background_hdr_img(hdri)

if BadWeather:
    street_path = random.choice(WetStreets)
else:
    street_path = random.choice(Streets)

Straße = bproc.loader.load_blend(street_path)
#Lighting 
#Set Lightsource 
# light = bproc.types.Light()
# light.set_type("POINT")
# light.set_location([4.076, 1, 6])
# light.set_energy(1000)












#List Objects and apply Categories 
# Distractor List Definitions
distractors_all = [
    {
        "path": smallSensor_path,
        "name": "small_sensor"
    },
    {
        "path": redPropaneTank_path,
        "name": "red_propane_tank"
    },
    {
        "path": constructionLight_path,
        "name": "construction_light"
    },
    {
        "path": fireExtinguisher_path,
        "name": "fire_extinguisher"
    },
    {
        "path": cardboardBox_path,
        "name": "cardboard_box"
    },
    {
        "path": barrelStove_path,
        "name": "barrel_stove"
    },
    {
        "path": barell_path,
        "name": "barrel"
    },
    {
        "path": redJerryCan_path,
        "name": "red_jerry_can"
    },
    {
        "path": Chair_path,
        "name": "chair"
    },
    {
        "path": TrashCan_path,
        "name": "trash_can"
    },
]

# Cone List Definitions with custom properties and innit objects
BigOrangeCone = bproc.loader.load_blend(BigOrangeCone_path)
BigOrange_cone = BigOrangeCone[0]
BigOrange_cone.set_location([0,0,-5])

BlueCone = bproc.loader.load_blend(blue_cone_path)
blue_cone = BlueCone[0]
blue_cone.set_location([0,0,-5])

OrangeCone = bproc.loader.load_blend(orange_cone_path)
orange_cone = OrangeCone[0]
orange_cone.set_location([0,0,-5])

YellowCone = bproc.loader.load_blend(yellow_cone_path)
yellow_cone = YellowCone[0]
yellow_cone.set_location([0,0,-5])

BlueDamagedCone = bproc.loader.load_blend(blue_cone_damaged_path)
blue_damaged_cone = BlueDamagedCone[0]
blue_damaged_cone.set_location([0,0,-5])

OrangeDamagedCone = bproc.loader.load_blend(orange_cone_damaged_path)
orange_damaged_cone = OrangeDamagedCone[0]
orange_damaged_cone.set_location([0,0,-5])

YellowDamagedCone = bproc.loader.load_blend(yellow_cone_damaged_path)
yellow_damaged_cone = YellowDamagedCone[0]
yellow_damaged_cone.set_location([0,0,-5])

BlueKnockedOverCone = bproc.loader.load_blend(blue_knocked_over_cone_path)
blue_knocked_over_cone = BlueKnockedOverCone[0]
blue_knocked_over_cone.set_location([0,0,-5])

OrangeKnockedOverCone = bproc.loader.load_blend(orange_knocked_over_cone_path)
orange_knocked_over_cone = OrangeKnockedOverCone[0]
orange_knocked_over_cone.set_location([0,0,-5])

YellowKnockedOverCone = bproc.loader.load_blend(yellow_knocked_over_cone_path)
yellow_knocked_over_cone = YellowKnockedOverCone[0]
yellow_knocked_over_cone.set_location([0,0,-5])

cones = [
    {
        "obj": BigOrange_cone,
        "name": "big_orange_cone",
        "category_id": 1,
        "cone_color": "orange",
        "supercategory": "cone"
    },
    {
        "obj": blue_cone,
        "name": "blue_cone",
        "category_id": 2,
        "cone_color": "blue",
        "supercategory": "cone"
    },
    {
        "obj": orange_cone,
        "name": "orange_cone",
        "category_id": 3,
        "cone_color": "orange",
        "supercategory": "cone"
    },
    {
        "obj": yellow_cone,
        "name": "yellow_cone",
        "category_id": 4,
        "cone_color": "yellow",
        "supercategory": "cone"
    },
    {
        "obj": blue_damaged_cone,
        "name": "blue_cone_damaged",
        "category_id": 5,
        "cone_color": "blue",
        "supercategory": "cone"
    },
    {
        "obj": orange_damaged_cone,
        "name": "orange_cone_damaged",
        "category_id": 6,
        "cone_color": "orange",
        "supercategory": "cone"
    },
    {
        "obj": yellow_damaged_cone,
        "name": "yellow_cone_damaged",
        "category_id": 7,
        "cone_color": "yellow",
        "supercategory": "cone"
    },
    {
        "obj": blue_knocked_over_cone,
        "name": "blue_cone_knocked_over",
        "category_id": 8,
        "cone_color": "blue",
        "supercategory": "cone"
    },
    {
        "obj": orange_knocked_over_cone,
        "name": "orange_cone_knocked_over",
        "category_id": 9,
        "cone_color": "orange",
        "supercategory": "cone"
    },
    {
        "obj": yellow_knocked_over_cone,
        "name": "yellow_cone_knocked_over",
        "category_id": 10,
        "cone_color": "yellow",
        "supercategory": "cone"
    }
]
# Load enabled cones and set custom properties
for cone in cones:
    cone["obj"].set_name(cone["name"])
    cone["obj"].set_cp("category_id", cone["category_id"])
    cone["obj"].set_cp("cone_color", cone["cone_color"])
    cone["obj"].set_cp("supercategory", cone["supercategory"])

# Load selected distractors and set custom properties (category_id: 0)
distractors_in_scene_objs = []
selected_distractor_defs = random.sample(distractors_all, total_distractor_types)
for distractor_def in selected_distractor_defs:
    loaded_distractor = bproc.loader.load_blend(distractor_def["path"])
    loaded_obj = loaded_distractor[0]
    loaded_obj.set_location([0,0,-5])
    distractors_in_scene_objs.append(loaded_obj)

#Alle anderen Objekte außer Cones kategorisieren
for obj in bproc.object.get_all_mesh_objects():
    if obj not in [cone["obj"] for cone in cones]:
        obj.set_cp("category_id", 0)
        obj.set_cp("supercategory", "background")











# Placement Algorithm: Place cones according to calculated numbers
# Define mapping between cone names and their calculated counts
cone_count_map = {
    "big_orange_cone": number_of_BigOrange_cones,
    "blue_cone": number_of_blue_cones,
    "orange_cone": number_of_orange_cones,
    "yellow_cone": number_of_yellow_cones,
    "blue_cone_damaged": number_of_damaged_blue_cones,
    "orange_cone_damaged": number_of_damaged_orange_cones,
    "yellow_cone_damaged": number_of_damaged_yellow_cones,
    "blue_cone_knocked_over": number_of_KnockedOver_blue_cones,
    "orange_cone_knocked_over": number_of_KnockedOver_orange_cones,
    "yellow_cone_knocked_over": number_of_KnockedOver_yellow_cones
}

# Placement bounds
x_min, x_max = -10, 10
y_min, y_max = -10, 10
z_value = 0
z_Knocked = 0.106
 

# Place cones with duplicates according to their calculated counts
placed_cones = []
for cone in cones:
    cone_name = cone["name"]

    if cone_name == "blue_cone_knocked_over" or cone_name == "orange_cone_knocked_over" or cone_name == "yellow_cone_knocked_over" and not Include_Knocked_Over_Cones:
        continue
    if cone_name == "blue_cone_damaged" or cone_name == "orange_cone_damaged" or cone_name == "yellow_cone_damaged" and not Include_Damaged_Cones:
        continue
    count = cone_count_map.get(cone_name, 0)
    
    for i in range(count):
        # Duplicate the cone
        cone_duplicate = cone["obj"].duplicate()
        cone_duplicate.set_cp("category_id", cone["category_id"])
        cone_duplicate.set_cp("cone_color", cone["cone_color"])
        cone_duplicate.set_cp("supercategory", cone["supercategory"])
        cone_duplicate.set_name(cone['name'])
        
        #Calculate Random x and y within bounds 
        x = np.random.uniform(x_min, x_max)
        y = np.random.uniform(y_min, y_max)
        #Place Knocked Over Cones with a different height and random z rotation
        if cone_name == "blue_cone_knocked_over" or cone_name == "orange_cone_knocked_over" or cone_name == "yellow_cone_knocked_over":
            cone_duplicate.set_rotation_euler([1.8812272548675537, 4.155973343245023e-10, np.random.uniform(0, 2 * np.pi)])
            cone_duplicate.set_location([x, y, z_Knocked])
        else:
            cone_duplicate.set_location([x, y, z_value])
            cone_duplicate.set_rotation_euler([0, 0, np.random.uniform(0, 2 * np.pi)])

        placed_cones.append(cone_duplicate)

# Place distractors with duplicates according to total_distractors_per_type
placed_distractors = []
for distractor_obj in distractors_in_scene_objs:
    for i in range(total_distractors_per_type):
        # Duplicate the distractor
        distractor_duplicate = distractor_obj.duplicate()
        
        # Randomize placement within bounds
        x = np.random.uniform(x_min, x_max)
        y = np.random.uniform(y_min, y_max)
        distractor_duplicate.set_location([x, y, z_value])
        
        placed_distractors.append(distractor_duplicate)













#Add Lens Distortion
#Set Random K1 and K2 Values
# Kameraprofile (simuliert verschiedene Dashcam-Typen)
camera_profiles = [
    {"name": "Weitwinkel",   "k1": -0.28, "k2":  0.10},
    {"name": "Standard",     "k1": -0.15, "k2":  0.05},
    {"name": "Leicht verz.", "k1": -0.05, "k2":  0.01},
    {"name": "Kein Effekt",  "k1":  0.00, "k2":  0.00},
]

#Kamera platzieren 
#POI Random setzen 
#Set Resolution

for i in range(Number_of_Camera_Poses):
    if Distortion:
        profile = random.choice(camera_profiles)
        # Kameramatrix (Brennweite + Hauptpunkt)
        orig_res_x, orig_res_y = CameraResX, CameraResY
        cam_K = np.array([[349.554, 0.0, 336.84], [0.0, 349.554, 189.185], [0.0, 0.0, 1.0]])
        p1, p2 = 0.000311976, -9.62967e-5
        bproc.camera.set_intrinsics_from_K_matrix(cam_K, orig_res_x, orig_res_y, bpy.context.scene.camera.data.clip_start, bpy.context.scene.camera.data.clip_end)
        mapping_coords = bproc.camera.set_lens_distortion(profile["k1"], profile["k2"], 0.0, p1, p2)

    else:
        bproc.camera.set_resolution(CameraResX,CameraResY)
    
    poi = np.random.uniform([-10, -10, 0], [10, 10, 0])  # Random POI innerhalb des Platzierungsrahmens 
    # Sample random camera location above objects in a circle around the POI
    location = np.random.uniform([-15, -15, 1], [15, 15, 2])
    # Compute rotation based on vector going from location towards poi
    rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(0,0))
    # Add homog cam pose based on location an rotation
    cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
    bproc.camera.add_camera_pose(cam2world_matrix)











#Rendern
# 6. Aktiviere Normals 
bproc.renderer.enable_normals_output()
bproc.renderer.enable_distance_output(activate_antialiasing=True)

if MotionBlur:
    bproc.renderer.enable_motion_blur(
    motion_blur_length=0.3,
    rolling_shutter_type="TOP",
    rolling_shutter_length=0.03
    )
    bproc.renderer.enable_depth_output(activate_antialiasing=False)


#7 Rendern 

bproc.renderer.enable_segmentation_output(map_by=["category_id", "instance", "name"])
data = bproc.renderer.render()
bproc.writer.write_hdf5("output/", data)


if Distortion:
    #Post process the data and apply the lens distortion
    # post process the data and apply the lens distortion
    for key in ['colors', 'distance', 'normals']:
        # use_interpolation should be false, for everything except colors
        use_interpolation = key == "colors"
        data[key] = bproc.postprocessing.apply_lens_distortion(data[key], mapping_coords, orig_res_x, orig_res_y,
                                                            use_interpolation=use_interpolation)



# Ergebnis speichern
bproc.writer.write_hdf5("output/", data)






















output_dir = "output"

# ✅ COCO-Annotationen mit Bounding Boxes für Jede Cone ein entsprechendes Label
bproc.writer.write_coco_annotations(os.path.join(output_dir, "coco_data"),    # ✅ Unterordner coco_data
    instance_segmaps=data["instance_segmaps"],
    instance_attribute_maps=data["instance_attribute_maps"],
    colors=data["colors"],
    color_file_format="JPEG",
)

# Print distractor placement summary
print("Distractors placed in this scene:")
if placed_distractors:
    distractor_counts = {}
    for distractor in placed_distractors:
        name = distractor.get_name()
        distractor_counts[name] = distractor_counts.get(name, 0) + 1

    for name, count in distractor_counts.items():
        print(f" - {name}: {count}")
    print(f"Total distractors placed: {len(placed_distractors)}")
else:
    print(" - None")

print("Selected distractor types:")
for distractor_def in selected_distractor_defs:
    print(f" - {distractor_def['name']}")
#print which HDRI was selected
print(f"Selected HDRI: {hdri}")



















