def set_cdproperties(ConesinScene):
    Paths = get_paths()
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
        if obj not in ConesinScene:  # If the object doesn't have a category_id, set it to 0 (background)
            obj.set_cp("category_id", 0) #Check if works 
            obj.set_cp("supercategory", "background")



def placing_cones():
    Config = get_Config()
    Cone_distribution = calculate_number_of_cones()
    ConesinScene = []


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
            ConesinScene.append(blue_cone_duplicate)


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
            ConesinScene.append(orange_cone_duplicate)
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
            ConesinScene.append(yellow_cone_duplicate)
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
            ConesinScene.append(big_orange_cone_duplicate)
            # Randomize placement within bounds
            x = np.random.uniform(x_min, x_max)
            y = np.random.uniform(y_min, y_max)
            big_orange_cone_duplicate.set_location([x, y, z_value])

    return ConesinScene