import trimesh
import amulet
from amulet.api.block import Block
from math import sqrt
from scipy.spatial import cKDTree
import numpy as np

WOOL_PALETTE = {
    "minecraft:white_wool": (234, 236, 237),
    "minecraft:orange_wool": (241, 118, 20),
    "minecraft:magenta_wool": (191, 75, 201),
    "minecraft:light_blue_wool": (58, 175, 217),
    "minecraft:yellow_wool": (249, 198, 39),
    "minecraft:lime_wool": (112, 185, 25),
    "minecraft:pink_wool": (237, 141, 172),
    "minecraft:gray_wool": (62, 68, 71),
    "minecraft:light_gray_wool": (142, 142, 134),
    "minecraft:cyan_wool": (21, 137, 145),
    "minecraft:purple_wool": (121, 42, 172),
    "minecraft:blue_wool": (53, 57, 157),
    "minecraft:brown_wool": (114, 71, 40),
    "minecraft:green_wool": (84, 109, 27),
    "minecraft:red_wool": (161, 39, 34),
    "minecraft:black_wool": (20, 21, 25),
}
CONCRETE_PALETTE = {
    "minecraft:white_concrete": (207, 213, 214),
    "minecraft:orange_concrete": (224, 97, 0),
    "minecraft:magenta_concrete": (170, 47, 156),
    "minecraft:light_blue_concrete": (36, 137, 199),
    "minecraft:yellow_concrete": (241, 175, 21),
    "minecraft:lime_concrete": (94, 168, 24),
    "minecraft:pink_concrete": (214, 101, 143),
    "minecraft:gray_concrete": (54, 57, 61),
    "minecraft:light_gray_concrete": (125, 125, 115),
    "minecraft:cyan_concrete": (21, 119, 136),
    "minecraft:purple_concrete": (100, 32, 156),
    "minecraft:blue_concrete": (44, 46, 143),
    "minecraft:brown_concrete": (96, 59, 31),
    "minecraft:green_concrete": (73, 91, 36),
    "minecraft:red_concrete": (142, 32, 32),
    "minecraft:black_concrete": (8, 10, 15),
}
TERRACOTTA_PALETTE = {
    "minecraft:white_terracotta": (209, 178, 161),
    "minecraft:orange_terracotta": (161, 83, 37),
    "minecraft:magenta_terracotta": (150, 88, 109),
    "minecraft:light_blue_terracotta": (113, 108, 137),
    "minecraft:yellow_terracotta": (186, 133, 35),
    "minecraft:lime_terracotta": (103, 117, 53),
    "minecraft:pink_terracotta": (160, 77, 78),
    "minecraft:gray_terracotta": (57, 42, 35),
    "minecraft:light_gray_terracotta": (135, 107, 98),
    "minecraft:cyan_terracotta": (86, 91, 91),
    "minecraft:purple_terracotta": (118, 70, 86),
    "minecraft:blue_terracotta": (74, 59, 91),
    "minecraft:brown_terracotta": (77, 51, 36),
    "minecraft:green_terracotta": (76, 82, 42),
    "minecraft:red_terracotta": (143, 61, 46),
    "minecraft:black_terracotta": (37, 23, 16),
}
GLASS_PALETTE = {
    "minecraft:white_stained_glass": (255, 255, 255),
    "minecraft:orange_stained_glass": (216, 127, 51),
    "minecraft:magenta_stained_glass": (178, 76, 216),
    "minecraft:light_blue_stained_glass": (102, 153, 216),
    "minecraft:yellow_stained_glass": (229, 229, 51),
    "minecraft:lime_stained_glass": (127, 204, 25),
    "minecraft:pink_stained_glass": (242, 127, 165),
    "minecraft:gray_stained_glass": (76, 76, 76),
    "minecraft:light_gray_stained_glass": (153, 153, 153),
    "minecraft:cyan_stained_glass": (76, 127, 153),
    "minecraft:purple_stained_glass": (127, 63, 178),
    "minecraft:blue_stained_glass": (51, 76, 178),
    "minecraft:brown_stained_glass": (102, 76, 51),
    "minecraft:green_stained_glass": (102, 127, 51),
    "minecraft:red_stained_glass": (153, 51, 51),
    "minecraft:black_stained_glass": (25, 25, 25),
}
START_POS = (0, -60, 0)  # Insertion start point, world coordinates (x, y, z)
ROTATE_ANGLE = (0, 0, 0)  # Rotation angle (x, y, z), in degrees
PITCH = 1.0  # Voxel size, smaller is finer (note MC block size limit)
GAME_VERSION = ("java", (1, 20, 1))  # Minecraft version

# Find the closest block in the palette based on color
def find_closest_block_with_glass(color, palette, glass_palette=GLASS_PALETTE):
    r, g, b, a = color
    min_distance = float('inf')
    closest_block = None
    if a < 200:
        for block_name, (br, bg, bb) in glass_palette.items():
            distance = sqrt((r-br)**2 + (g-bg)**2 + (b-bb)**2)
            if distance < min_distance:
                min_distance = distance
                closest_block = block_name
    else:
        for block_name, (br, bg, bb) in palette.items():
            distance = sqrt((r-br)**2 + (g-bg)**2 + (b-bb)**2)
            if distance < min_distance:
                min_distance = distance
                closest_block = block_name
    return closest_block
def find_closest_block_without_glass(color, palette):
    r, g, b, a = color
    min_distance = float('inf')
    closest_block = None
    for block_name, (br, bg, bb) in palette.items():
        distance = sqrt((r-br)**2 + (g-bg)**2 + (b-bb)**2)
        if distance < min_distance:
            min_distance = distance
            closest_block = block_name
    return closest_block
def find_closest_block_only_glass(color, palette, glass_palette=GLASS_PALETTE):
    r, g, b, a = color
    min_distance = float('inf')
    closest_block = None
    for block_name, (br, bg, bb) in glass_palette.items():
        distance = sqrt((r-br)**2 + (g-bg)**2 + (b-bb)**2)
        if distance < min_distance:
            min_distance = distance
            closest_block = block_name
    return closest_block

# Get the color of a voxel
def get_voxel_color(point, colors, tree):
    _, index = tree.query(point)
    voxel_color = colors[index]
    return voxel_color

# Get the palette based on the selected blocks
def get_palette(wool=True, concrete=True, terracotta=True):
    palette = {}
    if wool:
        palette.update(WOOL_PALETTE)
    if concrete:
        palette.update(CONCRETE_PALETTE)
    if terracotta:
        palette.update(TERRACOTTA_PALETTE)
    return palette

# Get the block function based on the selected blocks
def get_block_function(wool=True, concrete=True, terracotta=True, glass=True):
    if wool or concrete or terracotta:
        if glass:
            return find_closest_block_with_glass
        else:
            return find_closest_block_without_glass
    else:
        return find_closest_block_only_glass

# Load the model
def load_model(obj_file):
    print(f"Loading model from {obj_file}...")
    mesh = trimesh.load(obj_file)
    print(f'Type of mesh: {type(mesh)}')
    if type(mesh) == trimesh.Scene:
        meshes = list(mesh.geometry.values())
    elif type(mesh) == trimesh.Trimesh:
        meshes = [mesh]
    else:
        raise TypeError(f"Unsupported mesh type: {type(mesh)}")
    print(f"Model loaded, {len(meshes)} meshes in total")
    return meshes

# Voxelize the model
def voxelize_model(mesh, pitch=PITCH):
    print("Voxelizing model...")
    print(f'Type of visual: {type(mesh.visual)}')
    if type(mesh.visual) == trimesh.visual.TextureVisuals:
        mesh.visual = mesh.visual.to_color() # Convert to ColorVisuals
        #mesh.visual = trimesh.visual.ColorVisuals(mesh=mesh) # Convert to ColorVisuals
    colors = mesh.visual.vertex_colors  # Get vertex colors
    vertices = mesh.vertices
    tree = cKDTree(vertices)  # Build a KDTree for fast color lookup
    voxels = mesh.voxelized(pitch=pitch)
    points = voxels.points  # Voxel coordinates
    print(f"Voxelization completed, {len(points)} blocks in total")
    return points, colors, tree

# Calculate rotation matrix
def calculate_rotation_matrix(rotate_angle=ROTATE_ANGLE, pitch=PITCH):
    # Convert degrees to radians for rotation
    rx, ry, rz = map(lambda x: x * 3.1415926 / 180, rotate_angle)
    # Rotation matrix for x-axis
    rx_matrix = [
        [1, 0, 0],
        [0, np.cos(rx), -np.sin(rx)],
        [0, np.sin(rx), np.cos(rx)]
    ]
    # Rotation matrix for y-axis
    ry_matrix = [
        [np.cos(ry), 0, np.sin(ry)],
        [0, 1, 0],
        [-np.sin(ry), 0, np.cos(ry)]
    ]
    # Rotation matrix for z-axis
    rz_matrix = [
        [np.cos(rz), -np.sin(rz), 0],
        [np.sin(rz), np.cos(rz), 0],
        [0, 0, 1]
    ]
    # Combine rotation matrices
    rotation_matrix = np.dot(rz_matrix, np.dot(ry_matrix, rx_matrix))
    return rotation_matrix / pitch

# Insert blocks
def insert_blocks(points, colors, tree, world, palette, start_pos=START_POS, rotate_angle=ROTATE_ANGLE, pitch=PITCH, game_version=GAME_VERSION):
    dimension = world.dimensions[0]
    rotation_matrix = calculate_rotation_matrix(rotate_angle, pitch)
    for point in points:
        # Calculate real world coordinates
        world_x, world_y, world_z = np.dot(rotation_matrix, point) + start_pos
        world_x, world_y, world_z = map(int, (world_x, world_y, world_z))

        # Get voxel color
        voxel_color = get_voxel_color(point, colors, tree)
        # Find closest block
        closest_block = find_closest_block(voxel_color, palette)

        # Place block
        block = Block.from_string_blockstate(closest_block)
        #block = Block("minecraft", "stone")
        world.set_version_block(
            world_x,  # x location
            world_y,  # y location
            world_z,  # z location
            dimension,
            game_version,
            block,
        )
    print(f"Successfully placed {len(points)} blocks")

# Main function
def model_to_minecraft(obj_file, world_path, start_pos=START_POS, rotate_angle=ROTATE_ANGLE, pitch=PITCH, game_version=GAME_VERSION, wool=True, concrete=True, terracotta=True, glass=True):
    global find_closest_block
    find_closest_block = get_block_function(wool, concrete, terracotta, glass)
    palette = get_palette(wool, concrete, terracotta)

    meshes = load_model(obj_file)

    print("Connecting to Minecraft world...")
    world = amulet.load_level(world_path)

    for mesh in meshes:
        points, colors, tree = voxelize_model(mesh, pitch)
        insert_blocks(points, colors, tree, world, palette, start_pos, rotate_angle, pitch, game_version)
    
        print("Saving world...")
        world.save()
    world.close()
    print("All done! Enjoy your Minecraft model!")
    print('-'*20)