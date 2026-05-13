import blenderproc as bproc
import os
import numpy as np
import random
import paths

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
#blue_damaged_cone_path = 
#yellow_damaged_cone_path = 
#orange_damaged_cone_path = 

Cones = [BigOrangeCone_path, blue_cone_path, orange_cone_path, blue_striped_cone_path, yellow_striped_cone_path, yellow_cone_path]

#Base Scene Objects
Zaun_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\RoadBarrierInnit.blend"
Baeume_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\TreelineInnit.blend"
Tribuene_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\GroßeTribueneInnit.blend"

#Straßentypen 
PlainAspahlt_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\NormalAsphalt.blend"
floorPattern_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\FloorPattern.blend"
plaster_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\Plaster.blend"
groundGrey_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\Environment Elements\\GroundGrey.blend"

Streets = [PlainAspahlt_path, floorPattern_path, plaster_path, groundGrey_path]

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
driving_school_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\HDRIs\\driving_school_4k.hdr"
mallParkingLot_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\HDRIs\\mall_parking_lot_4k.hdr"
#Sunset
#Nighttime
sandsloot_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\assets\\HDRIs\\sandsloot_4k.hdr"

Daylight_HDRIs = [driving_school_path, mallParkingLot_path]
Sunset_HDRIs = []
Nighttime_HDRIs = [sandsloot_path]
HDRIs = Daylight_HDRIs + Sunset_HDRIs + Nighttime_HDRIs





#Configuration of Scene / set True or Flase for each category / Give percentage of appearence for each Cne type
#Cones (Enter the type)
BigOrange_cone = True
appearance_percentage_BigOrange_cone = 0.0

blue_cone = True
appearance_percentage_blue_cone = 60.0

orange_cone = True
appearance_percentage_orange_cone = 20.0

yellow_cone = True
appearance_percentage_yellow_cone = 20.0

MinNumber_of_cones = 4
MaxNumber_of_cones = 10
Include_Damaged_Cones = False
appearance_percentage_of_damaged_cones = 5.0 
Include_Knocked_Over_Cones = False 

#Distractors
MinNumber_of_distractor_Types = 1
MaxNumber_of_distractor_Types = 3
MinNumber_of_distractors_of_Type = 1
MaxNumber_of_distractors_of_Type = 3

#Lighting 
All_lightings = True
Daylight = True
Sunset = True
Nighttime = True


#Number of images to generate
Number_of_scenes = 2
Number_of_Camera_Poses = 3
YOLO_Annotation = True
Output_path = "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\output"








#Object selection and initialization of base scene 
# Base Szene Laden: Tribuene, Zaun, Baeume
Tribuene = bproc.loader.load_blend(Tribuene_path)
Zaun = bproc.loader.load_blend(Zaun_path)
Baeume = bproc.loader.load_blend(Baeume_path)

# Randomisierungsparameter für Straße, HDRI, Licht (2 Parameter)
#Street 
street_path = random.choice(Streets)
Straße = bproc.loader.load_blend(street_path)

#randomize HDRI and set world background 
if All_lightings:
    hdri = random.choice(HDRIs)
    bproc.world.set_world_background_hdri(hdri)
elif Daylight:
    hdri = random.choice(Daylight_HDRIs)
    bproc.world.set_world_background_hdri(hdri)
elif Sunset:
    hdri = random.choice(Sunset_HDRIs)
    bproc.world.set_world_background_hdri(hdri)
elif Nighttime:
    hdri = random.choice(Nighttime_HDRIs)
    bproc.world.set_world_background_hdri(hdri)

# Put Cones in new Scene List, calculate amount, and initialize objects under the map
cones_in_scene = []
if BigOrange_cone:
    cones_in_scene.append(BigOrangeCone_path)
    BigOrangeCone = bproc.loader.load_blend(BigOrangeCone_path)
    orange_cone = BigOrangeCone[0]
    orange_cone.set_location([0,0,-5]) #Initialice location under the map to avoid appearing
if blue_cone:
    cones_in_scene.append(blue_cone_path)
if orange_cone:
    cones_in_scene.append(orange_cone_path)
if yellow_cone:
    cones_in_scene.append(yellow_cone_path)

# Choose x random distractors and put in new Scene list
distractors_in_scene = random.sample(Distractors, random.randint(MinNumber_of_distractor_Types, MaxNumber_of_distractor_Types)) # Zufällige Auswahl von Distraktoren basierend auf der angegebenen Anzahl
















