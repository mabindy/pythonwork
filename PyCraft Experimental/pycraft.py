from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from ursina import Slider
from perlin_noise import PerlinNoise
from ursina.collider import BoxCollider
from ursina.texture_importer import load_texture
from ursina import InputField
import random
import json
import os
import math
import importlib
import importlib.util
import sys
app = Ursina(borderless=False, title='PyCraft', icon='PyCraft/pycraftlogo.ico')
game_version = '1.4 indev'
world_data = []
debugOpen = False
window.fullscreen = False
seedvalue = None
fov_slider = None
saved_world_name = None
holding_block = False
replacingslot = False
pause_menu_open = False
play_menu_open = False
block_class_mapping = {}
# Define a Voxel class.
# By setting the parent to scene and the model to 'cube' it becomes a 3d button.
class Voxel(Button):
    block_texture='PyCraft/Textures/cobblestone.png'
    block_icon = 'PyCraft/Textures/cobblestoneblock.png'
    block_color = color.hsv(0, 0, .9)
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, 0.9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/cobblestone.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['Voxel'] = Voxel
class IronOreVoxel(Button):
    block_texture='PyCraft/Textures/iron_ore.png'
    block_icon = 'PyCraft/Textures/ironoreblock.png'
    block_color = color.hsv(0, 0, .9)
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, 0.9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/iron_ore.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['IronOreVoxel'] = IronOreVoxel
class CoalOreVoxel(Button):
    block_texture='PyCraft/Textures/coal_ore.png'
    block_icon = 'PyCraft/Textures/coaloreblock.png'
    block_color = color.hsv(0, 0, .9)
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, 0.9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/coal_ore.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['CoalOreVoxel'] = CoalOreVoxel
class OakPlanksVoxel(Button):
    block_texture='PyCraft/Textures/oak_planks.png'
    block_icon = 'PyCraft/Textures/oakplanksblock.png'
    block_color = color.hsv(0, 0, .9)
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/oak_planks.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['OakPlanksVoxel'] = OakPlanksVoxel
class OakLogVoxel(Button):
    block_texture='PyCraft/Textures/oaklog.png'
    block_icon = 'PyCraft/Textures/oaklogblock.png'
    block_color = color.hsv(0, 0, .9)
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/oaklog.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['OakLogVoxel'] = OakLogVoxel
class TreeLeavesVoxel(Button):
    block_texture='PyCraft/Textures/treeleaves.png'
    block_icon = 'PyCraft/Textures/oaklogblock.png'
    block_color = color.hsv(0, 0, .9)
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/treeleaves.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['TreeLeavesVoxel'] = TreeLeavesVoxel
class GlassVoxel(Button):
    block_texture='PyCraft/Textures/glass.png'
    block_icon = 'PyCraft/Textures/glassblock.png'
    block_color = color.hsv(0, 0, .9)
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/glass.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['GlassVoxel'] = GlassVoxel
class GroundVoxel(Button):
    block_texture='PyCraft/Textures/grass_top.png'
    block_icon = 'PyCraft/Textures/grassblock.png'
    block_color = color.hsv(120, 0.75, 0.7)
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(120, 0.75, 0.7)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/grass_top.png',
            color=base_color,
            highlight_color=color.cyan,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['GroundVoxel'] = GroundVoxel
class BrownVoxel(Button):
    block_texture = 'PyCraft/Textures/default_dirt.png'
    block_icon = 'PyCraft/Textures/dirtblock.png'
    block_color = color.hsv(30, 0.5, 0.7)
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(30, 0.5, 0.7)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/default_dirt.png',
            color=base_color,
            highlight_color=color.cyan,
            collider='box',
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['BrownVoxel'] = BrownVoxel
class WhiteWoolVoxel(Button):
    block_texture='PyCraft/Textures/white_wool.png'
    block_icon = 'PyCraft/Textures/whitewoolblock.png'
    block_color = color.hsv(0, 0, .9)
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/white_wool.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['WhiteWoolVoxel'] = WhiteWoolVoxel
class BlackWoolVoxel(Button):
    block_texture='PyCraft/Textures/black_wool.png'
    block_icon = 'PyCraft/Textures/blackwoolblock.png'
    block_color = color.hsv(0, 0, .9)
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/black_wool.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['BlackWoolVoxel'] = BlackWoolVoxel
class RedWoolVoxel(Button):
    block_texture='PyCraft/Textures/red_wool.png'
    block_icon = 'PyCraft/Textures/redwoolblock.png'
    block_color = color.hsv(0, 0, .9)
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, .9)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/red_wool.png',
            color=base_color,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
block_class_mapping['RedWoolVoxel'] = RedWoolVoxel

class DoorVoxel(Button):
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(30, 0.5, 0.7)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            scale = (1,2,0.25),
            origin_y=.5,
            texture='PyCraft/Textures/oak_door.png',
            color=base_color,
            highlight_color=color.cyan,
            collider='box'
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)

class Bedrock(Button):
    block_texture='PyCraft/Textures/bedrocktexture.png'
    block_icon = 'PyCraft/Textures/bedrockblock.png'
    block_color = color.hsv(0, 0, 1)
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, 1)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='PyCraft/Textures/bedrocktexture.png',
            color=base_color,
            highlight_color=color.cyan,
            isblock = True
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
        self.destroyable = False
block_class_mapping['Bedrock'] = Bedrock
worldgenerationvoxels = {
    'surfacevoxel': GroundVoxel,
    'minvoxel': Bedrock,
    'undersurfacevoxel': BrownVoxel,
    'deepvoxel': Voxel,
}


inventory_opened = False
inventory_blocks_pg1 = [
    {'voxel_class': Voxel, 'texture': Voxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Cobblestone'},
    {'voxel_class': BrownVoxel, 'texture': BrownVoxel.block_icon, 'color': color.hsv(30, 0.5, 0.7), 'name': 'Dirt'},
    {'voxel_class': GroundVoxel, 'texture': GroundVoxel.block_icon, 'color': color.hsv(120, 0.75, 0.7), 'name': 'Grass'},
    {'voxel_class': OakPlanksVoxel, 'texture': OakPlanksVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Oak Planks'},
    {'voxel_class': GlassVoxel, 'texture': GlassVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Glass'},
    {'voxel_class': IronOreVoxel, 'texture': IronOreVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Iron Ore'},
    {'voxel_class': CoalOreVoxel, 'texture': CoalOreVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Coal Ore'},
    {'voxel_class': Bedrock, 'texture': Bedrock.block_icon, 'color': color.hsv(0,0,1), 'name': 'Bedrock'},
    {'voxel_class': Voxel, 'texture': Voxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Cobblestone'},
    {'voxel_class': Voxel, 'texture': Voxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Cobblestone'},
    {'voxel_class': BrownVoxel, 'texture': BrownVoxel.block_icon, 'color': color.hsv(30, 0.5, 0.7), 'name': 'Dirt'},
    {'voxel_class': GroundVoxel, 'texture': GroundVoxel.block_icon, 'color': color.hsv(120, 0.75, 0.7), 'name': 'Grass'},
    {'voxel_class': OakPlanksVoxel, 'texture': OakPlanksVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Oak Planks'},
    {'voxel_class': GlassVoxel, 'texture': GlassVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Glass'},
    {'voxel_class': IronOreVoxel, 'texture': IronOreVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Iron Ore'},
    {'voxel_class': CoalOreVoxel, 'texture': CoalOreVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Coal Ore'},
    {'voxel_class': Bedrock, 'texture': Bedrock.block_icon, 'color': color.hsv(0,0,1), 'name': 'Bedrock'},
    {'voxel_class': Voxel, 'texture': Voxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Cobblestone'},
    {'voxel_class': Voxel, 'texture': Voxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Cobblestone'},
    {'voxel_class': BrownVoxel, 'texture': BrownVoxel.block_icon, 'color': color.hsv(30, 0.5, 0.7), 'name': 'Dirt'},
    {'voxel_class': GroundVoxel, 'texture': GroundVoxel.block_icon, 'color': color.hsv(120, 0.75, 0.7), 'name': 'Grass'},
    {'voxel_class': OakPlanksVoxel, 'texture': OakPlanksVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Oak Planks'},
    {'voxel_class': GlassVoxel, 'texture': GlassVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Glass'},
    {'voxel_class': IronOreVoxel, 'texture': IronOreVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Iron Ore'},
    {'voxel_class': CoalOreVoxel, 'texture': CoalOreVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Coal Ore'},
    {'voxel_class': Bedrock, 'texture': Bedrock.block_icon, 'color': color.hsv(0,0,1), 'name': 'Bedrock'},
    {'voxel_class': Voxel, 'texture': Voxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Cobblestone'},

]
inventory_blocks_pg2 = [
    {'voxel_class': WhiteWoolVoxel, 'texture': WhiteWoolVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'White Wool'},
    {'voxel_class': BlackWoolVoxel, 'texture': BlackWoolVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Black Wool'},
    {'voxel_class': RedWoolVoxel, 'texture': RedWoolVoxel.block_icon, 'color': color.hsv(0,0,0.9), 'name': 'Red Wool'},

]

pages = {
    1: inventory_blocks_pg1,
    2: inventory_blocks_pg2,
}
currentpagedata = {
    'page': inventory_blocks_pg1,
    'pagenumber': '1',
    'pagelabel': 'Base Blocks',
    }
pagelabels = {
    '1': 'Base Blocks',
    '2': 'Wools',
}


game_api = {
    'inventory_blocks_pg1': inventory_blocks_pg1,
    'inventory_blocks_pg2': inventory_blocks_pg2,
    'block_class_mapping': block_class_mapping,
    'pages': pages,
    'pagelabels': pagelabels,
    'worldgenerationvoxels': worldgenerationvoxels,

}


def load_mod_states(mods_folder='Documents/PyCraft/mods'):
    config_path = os.path.join(mods_folder, 'mods_config.json')
    mod_states = {}

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            mod_states = json.load(f)
    
    current_mod_files = [f for f in os.listdir(mods_folder) if f.endswith('.py') and f != 'mods_config.json']
    current_mod_names = [f[:-3] for f in current_mod_files]

    updated_mod_states = {}
    for mod_name in current_mod_names:
        if mod_name in mod_states:
            updated_mod_states[mod_name] = mod_states[mod_name]
        else:
            updated_mod_states[mod_name] = False

    mod_states = updated_mod_states

    with open(config_path, 'w') as f:
        json.dump(mod_states, f)

    return mod_states

def save_mod_states(mod_states, mods_folder='Documents/PyCraft/mods'):
    config_path = os.path.join(mods_folder, 'mods_config.json')
    with open(config_path, 'w') as f:
        json.dump(mod_states, f)

world_mods = []
def load_mods(mod_states, mods_folder='Documents/PyCraft/mods', game_api=None):
    global world_mods
    for filename in os.listdir(mods_folder):
        if filename.endswith('.py'):
            mod_name = filename[:-3]
            if mod_states.get(mod_name, False):
                file_path = os.path.join(mods_folder, filename)
                spec = importlib.util.spec_from_file_location(mod_name, file_path)
                mod = importlib.util.module_from_spec(spec)
                sys.modules[mod_name] = mod
                try:
                    spec.loader.exec_module(mod)
                except Exception as e:
                    print(f"Failed to load mod '{mod_name}': {e}")
                    continue

                if hasattr(mod, 'initialize') and hasattr(mod, 'deinitialize') and callable(mod.initialize) and callable(mod.deinitialize):
                    try:
                        mod.initialize(game_api)
                        world_mods.append(mod_name)
                    except Exception as e:
                        print(f"Error initializing mod '{mod_name}': {e}")
                else:
                    if not hasattr(mod, 'initialize'):
                        print(f"Mod {mod_name} does not have an 'initialize' function.")
                    if not hasattr(mod, 'deinitialize'):
                        print(f"Mod {mod_name} does not have a 'deinitialize' function.")

mods_folder = 'Documents\PyCraft\mods'

mod_states = load_mod_states(mods_folder)



def generate_world(worldseed):
    global worlddimensions, min_y, seedvalue, worldver, inventory_blocks_pg1, inventory_blocks_pg2
    load_mods(mod_states, mods_folder, game_api)
    clear_world()
    worldver = game_version
    try:
        worldseed = int(worldseed)
    except:
        print('Invalid seed. Generating random seed')
        worldseed = random.randint(1,1000000)
    noise = PerlinNoise (octaves=3, seed=worldseed)
    seedvalue = worldseed
    min_y = -10
    worlddimensions = 10 #World dimensions are twice this number 
    for z in range(-worlddimensions,worlddimensions):
        for x in range(-worlddimensions,worlddimensions):
            surface_y = noise([x * .02,z * .02])
            surface_y = math.floor(surface_y*7.5)
            for y in range(min_y, surface_y + 1):
                position = (x, y, z)
                if y == surface_y:
                    voxel = worldgenerationvoxels['surfacevoxel'](position=position)
                    block_type = (type(voxel).__name__)
                    treegenerator = random.randint(0,50)
                    if treegenerator == 5:
                        voxel = OakLogVoxel(position=(x,y+1,z))
                        voxel = OakLogVoxel(position=(x,y+2,z))
                        voxel = OakLogVoxel(position=(x,y+3,z))
                        voxel = TreeLeavesVoxel(position=(x,y+3,z+1))
                        voxel = TreeLeavesVoxel(position=(x+1,y+3,z+1))
                        voxel = TreeLeavesVoxel(position=(x-1,y+3,z+1))
                        voxel = TreeLeavesVoxel(position=(x,y+3,z-1))
                        voxel = TreeLeavesVoxel(position=(x+1,y+3,z-1))
                        voxel = TreeLeavesVoxel(position=(x-1,y+3,z-1))
                        voxel = TreeLeavesVoxel(position=(x+1,y+3,z))
                        voxel = TreeLeavesVoxel(position=(x-1,y+3,z))
                        voxel = TreeLeavesVoxel(position=(x,y+4,z+1))
                        voxel = TreeLeavesVoxel(position=(x+1,y+4,z+1))
                        voxel = TreeLeavesVoxel(position=(x-1,y+4,z+1))
                        voxel = TreeLeavesVoxel(position=(x,y+4,z-1))
                        voxel = TreeLeavesVoxel(position=(x+1,y+4,z-1))
                        voxel = TreeLeavesVoxel(position=(x-1,y+4,z-1))
                        voxel = TreeLeavesVoxel(position=(x+1,y+4,z))
                        voxel = TreeLeavesVoxel(position=(x-1,y+4,z))
                        voxel = TreeLeavesVoxel(position=(x,y+5,z))
                elif y == min_y:
                    voxel = worldgenerationvoxels['minvoxel'](position=position)
                    block_type = (type(voxel).__name__)
                elif y > surface_y - 3:
                    voxel = worldgenerationvoxels['undersurfacevoxel'](position=position)
                    block_type = (type(voxel).__name__)
                else:
                    oregenerator = random.randint(0,20)
                    if oregenerator == 5 and y < surface_y - 10:
                        voxel = IronOreVoxel(position=position)
                        block_type = 'IronOreVoxel'
                    elif oregenerator == 15:
                        voxel = CoalOreVoxel(position=position)
                        block_type = 'CoalOreVoxel'
                    else:
                        voxel = worldgenerationvoxels['deepvoxel'](position=position)
                        block_type = (type(voxel).__name__)
                world_data.append({'position': [x, y, z], 'block_type': block_type})
    build_barriers(worlddimensions, min_y)
    player.position = Vec3(*[0,0,0])
    destroy_play_menu()
    build_hotbar()
    mouse.locked = True

def build_barriers(dimensions, miny):
    global worlddimensions, min_y
    worlddimensions = dimensions
    min_y = miny
    wall_thickness = 1
    wall_height = 200
    voxel_size = 1

    min_xz = -dimensions
    max_xz = dimensions - 1
    terrain_min_xz = min_xz - voxel_size / 2
    terrain_max_xz = max_xz + voxel_size / 2
    terrain_width_xz = terrain_max_xz - terrain_min_xz

    north_wall = Entity(
        model = 'cube',
        scale = (terrain_width_xz, wall_height, wall_thickness),
        position = (
            (terrain_min_xz + terrain_max_xz) / 2,
            wall_height / 2 + miny,
            terrain_max_xz + wall_thickness / 2,
        ),
        collider = 'box',
        visible = False,
        destroyable = False,
        wall = True
    )
    south_wall = Entity(
        model = 'cube',
        scale = (terrain_width_xz, wall_height, wall_thickness),
        position = (
            (terrain_min_xz + terrain_max_xz) / 2,
            wall_height / 2 + miny,
            terrain_min_xz - wall_thickness / 2,
        ),
        collider = 'box',
        visible = False,
        destroyable = False,
        wall = True
    )
    east_wall = Entity(
        model = 'cube',
        scale = (wall_thickness, wall_height, terrain_width_xz),
        position=(
            terrain_max_xz + wall_thickness / 2,
            wall_height / 2 + miny,
            (terrain_min_xz + terrain_max_xz) / 2
        ),
        collider = 'box',
        visible = False,
        destroyable = False,
        wall = True
    )
    west_wall = Entity(
        model = 'cube',
        scale = (wall_thickness, wall_height, terrain_width_xz),
        position=(
            terrain_min_xz + wall_thickness / 2 - 1,
            wall_height / 2 + miny,
            (terrain_min_xz + terrain_max_xz) / 2
        ),
        collider = 'box',
        visible = False,
        destroyable = False,
        wall = True
    )


hotbar = Entity(
    parent=camera.ui,
    model='quad',
    texture = 'PyCraft/Textures/hotbar.png',
    scale=(0.5, 0.055),
    position=(0,-0.45,1),
    visible=True  
    )

def build_hotbar():
    global hotbar, selector, slot1, slot2, slot3, slot4, slot5, slot6, slot7, slot8, slot9, slotselected
    hotbar = Entity(
    parent=camera.ui,
    model='quad',
    texture = 'PyCraft/Textures/hotbar.png',
    scale=(0.5, 0.055),
    position=(0,-0.45,1),
    visible=True  
    )
    
    selector = Button( 
                    color=color.rgb(0, 0, 0), 
                    position=(-0.225, -0.45, 0), 
                    scale=(0.045, 0.045),
                    currentslot = 'slot1',
                    visible=True
                    )
    slot1 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture='PyCraft/Textures/cobblestoneblock.png',
                    position=(-0.225, -0.45, -1), 
                    scale=(0.045, 0.045),
                    hand_color = color.hsv(0, 0, .9),
                    on_click = lambda: equip_block(slot1) if holding_block else swap_block(slot1),
                    equipped=Voxel 
                    )
    slot2 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture='PyCraft/Textures/dirtblock.png',
                    position=(-0.168, -0.45, -1), 
                    scale=(0.045, 0.045),
                    hand_color = color.hsv(30, 0.5, 0.7),
                    on_click = lambda: equip_block(slot2) if holding_block else swap_block(slot2),
                    equipped=BrownVoxel
                    )
    slot3 = Button( 
                    color=color.hsv(0, 0, 0.9),
                    position=(-0.114, -0.45, -1), 
                    scale=(0.045, 0.045),
                    hand_color = color.hsv(30, 0.4, 0.8),
                    on_click = lambda: equip_block(slot3) if holding_block else swap_block(slot3),
                    visible=False,
                    equipped=False
                    )
    slot4 = Button( 
                    color=color.hsv(0, 0, 1),
                    position=(-0.057, -0.45, -1), 
                    scale=(0.045, 0.045),
                    hand_color = color.hsv(0,0,.9),
                    on_click = lambda: equip_block(slot4) if holding_block else swap_block(slot4),
                    equipped='gun'
                    )
    slot5 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture='PyCraft/Textures/oakplanksblock.png',
                    position=(0, -0.45, -1), 
                    scale=(0.045, 0.045),
                    hand_color = color.hsv(0,0,.9),
                    on_click = lambda: equip_block(slot5) if holding_block else swap_block(slot5),
                    equipped=OakPlanksVoxel
                    )
    slot6 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture='PyCraft/Textures/glassblock.png',
                    position=(0.055, -0.45, -1), 
                    scale=(0.045, 0.045),
                    hand_color = color.hsv(0,0,.9),
                    on_click = lambda: equip_block(slot6) if holding_block else swap_block(slot6),
                    equipped=GlassVoxel
                    )
    slot7 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture='PyCraft/Textures/dirtblock.png',
                    position=(-0.168, -0.45, -1), 
                    scale=(0.045, 0.045),
                    equipped='open',
                    visible=False
                    )
    slot8 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture='PyCraft/Textures/dirtblock.png',
                    position=(-0.168, -0.45, -1), 
                    scale=(0.045, 0.045), 
                    equipped='open',
                    visible=False
                    )
    slot9 = Button( 
                    color=color.hsv(0, 0, .9),
                    texture='PyCraft/Textures/dirtblock.png',
                    position=(-0.168, -0.45, -1), 
                    scale=(0.045, 0.045), 
                    equipped='open',
                    visible=False
                    )
    slotselected = slot1

hand = Entity(model='cube',texture='PyCraft/Textures/cobblestone.png', color=color.hsv(0,0,0.9), scale=(0.5,0.5,0.5), rotation=(0,0,0), position=(0,0,0), parent=camera)

def update_hand_position():
    if selected == 'ak':
        hand.position = (0.5, -0.5, 2)
    else:
        hand.position = (0.5, -0.5, 1)

def clear_world():
    for entity in scene.entities[:]:
        if isinstance(entity, Button) and entity != player and hasattr(entity, 'isblock') and not hasattr(entity, 'wall'):
            destroy(entity)

def rebuild_world_from_data():

    for block in world_data:
        position = block['position']
        block_type = block['block_type']
        x, y, z = position
        position = Vec3(x,y,z)

        block_class = block_class_mapping.get(block_type)
        if block_class:
            block_class(position=position)


        

def save_world(filename=r'C:\Users\mberr954\Documents\PyCraft\Worlds\world_save.json'):
    global worlddimensions, min_y, saved_world_name
    saved_world_name = filename[43:]
    print(saved_world_name)
    save_data = {
        'world_data': world_data,
        'player_position': [player.position.x, player.position.y, player.position.z],
        'world_size': [worlddimensions, min_y],
        'world_version': game_version,
    }
    if world_mods != []:
        save_data['world_mods'] = world_mods
    if seedvalue != None:
        save_data['world_seed'] = seedvalue
    with open(filename, 'w') as f:
        json.dump(save_data, f)

def load_world(filename):
    global world_data, worlddimensions, worldver, seedvalue, saved_world_name, inventory_blocks_pg1, inventory_blocks_pg2
    saved_world_name = filename[43:]
    with open(filename, 'r') as f:
        save_data = json.load(f)
    world_data = save_data['world_data']
    player_position = save_data.get('player_position', [0,0,0])
    worldver = save_data.get('world_version', 'Unknown')
    seedvalue = save_data.get('world_seed', 'Unknown')
    neededmods = save_data.get('world_mods', None)
    missingmods = []
    if neededmods:
        for mod in neededmods:
            if not mod in mod_states or not mod_states[mod]:
                missingmods.append(mod)
    if missingmods != []:
        print(f"World '{filename}' requires mods: {missingmods}")
        return
    try:
        worldproperties = save_data['world_size']
    except:
        print(f'ERROR: World {filename} is corrupt')
        return
    load_mods(mod_states, mods_folder, game_api)
    destroy_play_menu()
    build_barriers(worldproperties[0], worldproperties[1])
    clear_world()
    rebuild_world_from_data()
    build_hotbar()
    player.position = Vec3(*player_position)
    mouse.locked = True


settings_opened = False
def toggle_mouse_lock():
    global settings_opened, pause_menu_open
    if mouse.locked:
        mouse.locked = False
        mouse.visible = True
        pause_menu.visible = True
        build_pause_menu()
        pause_menu_open = True
    else:
        mouse.locked = True
        mouse.visible = False
        pause_menu.visible = False
        if settings_opened:
            close_settings()
        destroy_pause_menu()
        pause_menu_open = False
pause_menu = Entity(
    parent=camera.ui,
    model='quad',
    scale=(2, 2, 1),
    color=color.rgba(0,0,0, 0.5),  
    visible=False  
)
def toggle_fullscreen():
    window.fullscreen = not window.fullscreen
    fullscreen_button.text = 'Fullscreen: Disabled' if not window.fullscreen else 'Fullscreen: Enabled'

def open_settings():
    global settings_label, back_button, fullscreen_button, settings_opened, fov_slider
    settings_opened = True
    destroy_pause_menu()
    settings_label = Text(
        parent=pause_menu,  
        text='Settings',   
        origin=(0, 0),      
        scale=2,            
        color=color.white,   
        position=(0, 0.1),            
    )   
    fullscreen_button = Button(
        parent=pause_menu,
        text='Fullscreen: Disabled' if not window.fullscreen else 'Fullscreen: Enabled',
        color=color.gray,
        scale=(0.15, 0.02),  # Size of the button
        position=(0, 0),  # Position on the screen
        on_click = lambda: toggle_fullscreen()
    )
    fov_slider = Slider(
        min=60, max=120, default=camera.fov,
        parent=pause_menu,
        text='FOV',
        color=color.gray,
        step=1,
        position = (-0.099, 0.05),
        scale = (0.4, 0.5),
        dynamic=True,
    )

    def set_fov():
        camera.fov = fov_slider.value
        print(camera.fov)

    fov_slider.on_value_changed = set_fov

    back_button = Button(
        parent=pause_menu,
        text='Back',
        color=color.gray,
        scale=(0.15, 0.02),  # Size of the button
        position=(0, -0.1),  # Position on the screen
        on_click = lambda: close_settings()
    )

def close_settings():
    global settings_opened
    destroy(back_button)
    destroy(settings_label)
    destroy(fullscreen_button)
    destroy(fov_slider)
    build_pause_menu()
    settings_opened = False

def destroy_pause_menu():
    global save_field_open, confirm_save_button
    if save_field_open:
        destroy(save_name_field)
        destroy(confirm_save_button)
        save_field_open = False
    destroy(resume_button)
    destroy(quit_button)
    destroy(settings_button)
    destroy(pause_label)
    destroy(save_button)
    destroy(load_button)
    destroy(gen_button)

def build_pause_menu():
    global resume_button, quit_button, pause_label, settings_button, save_button, load_button, gen_button, save_field_open, confirm_save_button, saved_world_name
    save_field_open = False
    resume_button = Button(
        parent=pause_menu,
        text='Resume',
        color=color.gray,
        scale=(0.15, 0.02),  # Size of the button
        position=(0, 0),  # Position on the screen
        on_click = lambda: toggle_mouse_lock()
    )
    if saved_world_name != None:
        save_button = Button(
        parent=pause_menu,
        text='Save World',
        color=color.gray,
        scale=(0.15, 0.02),
        position=(0, -0.1),  
        on_click = lambda: save_world(f'C:\\Users\\mberr954\\Documents\\PyCraft\\Worlds\\{saved_world_name}')
        )
    else:
        save_button = Button(
            parent=pause_menu,
            text='Save World',
            color=color.gray,
            scale=(0.15, 0.02),
            position=(0, -0.1),  
            on_click = lambda: toggle_save_field()
        )
        def toggle_save_field():
            global save_field_open, save_name_field,confirm_save_button
            if save_field_open:
                destroy(save_name_field)
                destroy(confirm_save_button)
                save_field_open = False
            else:
                save_name_field = InputField(
                    parent=pause_menu,
                    default_value='World Name',
                    scale=(0.15, 0.02), 
                    position=(0.15, -0.1)
                    )
                confirm_save_button = Button(
                    parent=pause_menu,
                    text='Confirm',
                    color=color.gray,
                    scale=(0.15, 0.02),
                    position=(0.3, -0.1),  
                    on_click = lambda: save_world(f'C:\\Users\\mberr954\\Documents\\PyCraft\\Worlds\\{save_name_field.text}.json')
                )
                save_field_open = True

    load_button = Button(
        parent=pause_menu,
        text='Load World',
        color=color.gray,
        scale=(0.15, 0.02), 
        position=(0, -0.2),  
        on_click = lambda: load_world()
    )

    gen_button = Button(
        parent=pause_menu,
        text='Back to Menu',
        color=color.gray,
        scale=(0.15, 0.02), 
        position=(0, -0.25),  
        on_click = lambda: leavetomenu()
    )

    quit_button = Button(
        parent=pause_menu,
        text='Quit',
        color=color.gray,
        scale=(0.15, 0.02), 
        position=(0, -0.15),  
        on_click = application.quit
    )
    settings_button = Button(
        parent=pause_menu,
        text='Settings',
        color=color.gray,
        scale=(0.15, 0.02), 
        position=(0, -0.05),  
        on_click = lambda: open_settings()
    )
    pause_label = Text(
    parent=pause_menu,  
    text='Paused',   
    origin=(0, 0),      
    scale=2,            
    color=color.white,   
    position=(0, 0.1),            
    )   

def leavetomenu():
    destroy_pause_menu()
    build_main_menu()

def build_main_menu():
    global mainbackground,titletext,play_button,menu_quit_button,main_menu_open, mod_menu_button
    if play_menu_open:
        destroy_play_menu()
    main_menu_open = True
    mainbackground = Entity(
    parent=camera.ui,
    model='quad',
    texture = 'PyCraft/Textures/menubackground.jpg',
    scale=(2, 2, -1),  
    visible=True  
    )
    titletext = Entity(
    parent=camera.ui,
    model='quad',
    texture = 'PyCraft/Textures/titlelogo.png',
    scale=(0.5, 0.2),
    position=(0,0.25),
    visible=True  
    )
    play_button = Button(
        parent=camera.ui,
        text='Play',
        color=color.gray,
        scale=(0.25, 0.04),
        position=(0, 0),  
        on_click = lambda: open_play_menu()
    )
    mod_menu_button = Button(
        parent=camera.ui,
        text='Mods',
        color=color.gray,
        scale=(0.25, 0.04),
        position=(0, -0.1),  
        on_click = lambda: open_mod_menu()
    )
    menu_quit_button = Button(
        parent=camera.ui,
        text='Quit',
        color=color.gray,
        scale=(0.25, 0.04),
        position=(0, -0.2),  
        on_click = application.quit
    )

def destroy_main_menu():
    destroy(titletext)
    destroy(play_button)
    destroy(menu_quit_button)
    destroy(mod_menu_button)

def open_mod_menu():
    global mod_buttons, back_to_main_menu_button, mod_states, mod_labels
    destroy_main_menu()
    mod_labels = []
    mod_buttons = []
    mods_folder = 'Documents/PyCraft/mods'
    mod_states = load_mod_states(mods_folder)

    for i, mod_name in enumerate(mod_states.keys()):
        mod_label = Text(
            parent = camera.ui,
            text = mod_name,
            position = (-0.1, 0.4 - i * 0.05),
            scale = 1.5,
            color = color.white
        )
        mod_labels.append(mod_label)

        mod_button = Button(
            parent = camera.ui,
            text = 'Enabled' if mod_states[mod_name] else 'Disabled',
            color=color.green if mod_states[mod_name] else color.red,
            scale = (0.15, 0.04),
            position = (0.22, 0.383 - i * 0.05),
            on_click = lambda m=mod_name: toggle_mod_state(m)
        )
        mod_buttons.append(mod_button)
    back_to_main_menu_button = Button(
        parent = camera.ui,
        text = 'Back',
        color = color.gray,
        scale = (0.25, 0.04),
        position = (0, -0.4),
        on_click = lambda: back_to_main_menu()
    )

def toggle_mod_state(mod_name):
    global mod_states
    mods_folder = 'Documents/PyCraft/mods'
    mod_states[mod_name] = not mod_states[mod_name]
    save_mod_states(mod_states, mods_folder)

    for i, name in enumerate(mod_states.keys()):
        if name == mod_name:
            mod_buttons[i].text = 'Enabled' if mod_states[mod_name] else 'Disabled'
            mod_buttons[i].color = color.green if mod_states[mod_name] else color.red
            break

def back_to_main_menu():
    for label in mod_labels:
        destroy(label)
    for button in mod_buttons:
        destroy(button)
    destroy(back_to_main_menu_button)
    destroy(mainbackground)
    build_main_menu()
def open_play_menu():
    global file_buttons, createworld_button, worldseedinput, play_menu_open, returntomenu_button
    destroy_main_menu()
    play_menu_open = True
    folder_path = r'C:\Users\mberr954\Documents\PyCraft\Worlds'
    files = os.listdir(folder_path)
    scroll_container = Entity(parent=camera.ui, position = (0,0.3), scale=(1,1), visible=True)
    scroll_offset = 0

    file_buttons = []
    for i, file_name in enumerate(files):
        worldfilebutton = Button(
            parent=scroll_container,
            text=file_name,
            color=color.gray,
            scale=(0.25,0.05),
            position=(0, -i * 0.06),
            on_click = lambda file_name=file_name: load_world(f'C:\\Users\\mberr954\\Documents\\PyCraft\\Worlds\\{file_name}')
        )
        file_buttons.append(worldfilebutton)
    createworld_button = Button(
        parent=camera.ui,
        text='Create World',
        color=color.gray,
        scale=(0.25, 0.04),
        position=(0, -0.15),  
        on_click = lambda: generate_world(worldseedinput.text)
    )
    worldseedinput = InputField(
        default_value='Seed',
        scale=(0.2, 0.05), 
        position=(0, -0.2)
        )
    def limit_text():
        if len(worldseedinput.text) > 5:
            worldseedinput.text = worldseedinput.text[:7]
    worldseedinput.on_value_changed = limit_text
    returntomenu_button = Button(
        parent=camera.ui,
        text='Back',
        color=color.gray,
        scale=(0.25, 0.04),
        position=(-0.3, -0.15),  
        on_click = lambda: build_main_menu()
    )

def destroy_play_menu():
    global file_buttons, main_menu_open
    destroy(mainbackground)
    destroy(createworld_button)
    destroy(worldseedinput)
    destroy(returntomenu_button)
    for i in file_buttons:
        destroy(i)
    file_buttons = []
    play_menu_open = False
    main_menu_open = False

def toggle_inventory():
    global inventory_opened
    if inventory_opened:
        close_inventory()
    else:
        open_inventory(currentpagedata['page'], currentpagedata['pagenumber'], currentpagedata['pagelabel'])

def open_inventory(pg, pgn, pgl):
    global inventory_opened, inventory_panel, block_buttons, page_number, next_arrow, previous_arrow, page_label
    inventory_opened = True
    mouse.locked = False
    mouse.visible = True


    inventory_panel = Entity(
        parent=camera.ui,
        model='quad',
        texture = 'PyCraft/Textures/inventory.png',
        scale=(0.4,0.25),
        color=color.hsv(0,0,0.9),
        position = (0,0,1)
    )

    block_buttons = []
    num_columns = 9
    num_rows = math.ceil(len(pg) / num_columns)
    button_scale = (0.1,0.18)
    spacing = 0.108

    row_y_positions = [0.265, 0.175, 0.085]

    for index,block in enumerate(pg):
        col = index % num_columns
        row = index // num_columns

        position = Vec3(
            -0.43 + col * spacing,
            row_y_positions[row] - row * spacing,
            -1
        )

        block_button = Button(
            parent=inventory_panel,
            model='quad',
            texture=block['texture'],
            scale=button_scale,
            position=position,
            color=color.white,
            on_click=lambda b=block: hold_block(b)
        )
        block_buttons.append(block_button)

    page_number = Text(
    parent=inventory_panel,  
    text=pgn,   
    origin=(0, 0),      
    scale=(3,5),            
    color=color.black,   
    position=(0, -0.39, -1),            
    )
    page_label = Text(
    parent=inventory_panel,  
    text=pgl,
    origin=(0, 0),      
    scale=(2,4),            
    color=color.black,   
    position=(0.3, 0.42, -1),            
    )
    next_arrow = Button(
            parent=inventory_panel,
            texture='PyCraft/Textures/nextarrow.png',
            color=color.gray,
            scale=(0.09, 0.15),
            position=(0.429, -0.375, -1),
            on_click = lambda: next_inventory_page()
        )
    previous_arrow = Button(
            parent=inventory_panel,
            texture='PyCraft/Textures/backarrow.png',
            color=color.gray,
            scale=(0.09, 0.15),
            position=(-0.429, -0.375, -1),
            on_click = lambda: previous_inventory_page()
        )
def next_inventory_page():
    global page_number, currentpagedata, page_label
    if int(page_number.text) + 1 in pages:
        clear_inventory_page()
        build_new_page(pages.get(int(page_number.text) + 1))
        currentpagedata['page'] = pages.get(int(page_number.text) + 1)
        page_number.text = str(int(page_number.text) + 1)
        page_label.text = pagelabels[page_number.text]
        currentpagedata['pagenumber'] = page_number.text
        currentpagedata['pagelabel'] = pagelabels[page_number.text]
def previous_inventory_page():
    global page_number, currentpagedata, page_label
    if int(page_number.text) - 1 in pages:
        clear_inventory_page()
        build_new_page(pages.get(int(page_number.text) - 1))
        currentpagedata['page'] = pages.get(int(page_number.text) - 1)
        page_number.text = str(int(page_number.text) - 1)
        page_label.text = pagelabels[page_number.text]
        currentpagedata['pagenumber'] = page_number.text
        currentpagedata['pagelabel'] = pagelabels[page_number.text]
def hold_block(block):
    global selectedvoxel,selected,hand,defrot,holding_block,block_drag,block_held
    if holding_block:
        destroy(block_drag)
    holding_block = True
    block_drag = Entity(
            parent=camera.ui,
            model='quad',
            texture=block['texture'],
            blockcolor = block['color'],
            scale=(0.05,0.05),
            color=color.white,
        )
    block_held = block['voxel_class']
def equip_block(slot):
    global selectedvoxel,selected,hand,defrot,holding_block,block_drag,block_held,slot1,slot2,slot3,slot4,slot5,slot6,slot7,slot8,slot9, replacingslot
    if holding_block and not replacingslot:
        slot.texture=block_drag.texture
        slot.equipped=block_held
        slot.hand_color=block_drag.blockcolor
        slot.visible = True
        destroy(block_drag)
        holding_block = False
        if slot == slotselected:
            update_equipped_slot(slot)
    if holding_block and replacingslot:
        replacingslot.texture = slot.texture
        replacingslot.equipped = slot.equipped
        replacingslot.hand_color = slot.hand_color
        replacingslot.visible = slot.visible
        slot.texture=block_drag.texture
        slot.equipped=block_held
        slot.hand_color=block_drag.blockcolor
        slot.visible = True
        destroy(block_drag)
        if slot == slotselected or replacingslot == slotselected:
            update_equipped_slot(slotselected)
        replacingslot = False
        holding_block = False

def swap_block(slot):
    global selectedvoxel,selected,hand,defrot,holding_block,block_drag,block_held,slot1,slot2,slot3,slot4,slot5,slot6,slot7,slot8,slot9, replacingslot

    block_drag = Entity(
        parent=camera.ui,
        model='quad',
        texture=slot.texture,
        blockcolor = slot.hand_color,
        scale=(0.05,0.05),
        color=color.white,
    )
    replacingslot = slot
    slot.visible = False
    block_held = slot.equipped
    holding_block = True
    slot.equipped = None
    if slot == slotselected:
        update_equipped_slot(slot)
def close_inventory():
    global inventory_opened, inventory_panel, block_buttons, holding_block
    inventory_opened = False
    mouse.locked = True
    mouse.visible = False
    if holding_block:
        holding_block = False
        destroy(block_drag)
    destroy(inventory_panel)
    for btn in block_buttons:
        destroy(btn)
    block_buttons = []

def clear_inventory_page():
    global block_buttons
    for btn in block_buttons:
        destroy(btn)
    block_buttons = []
def build_new_page(pg):
    global block_buttons
    block_buttons = []
    num_columns = 9
    num_rows = math.ceil(len(pg) / num_columns)
    button_scale = (0.1,0.18)
    spacing = 0.108

    row_y_positions = [0.265, 0.175, 0.085]

    for index,block in enumerate(pg):
        col = index % num_columns
        row = index // num_columns

        position = Vec3(
            -0.43 + col * spacing,
            row_y_positions[row] - row * spacing,
            -1
        )

        block_button = Button(
            parent=inventory_panel,
            model='quad',
            texture=block['texture'],
            scale=button_scale,
            position=position,
            color=color.white,
            on_click=lambda b=block: hold_block(b)
        )
        block_buttons.append(block_button)
def update_equipped_slot(s):
    global selectedvoxel, selector, hand, defrot, selected, slotselected
    if s.equipped and s.equipped != 'gun':
        selectedvoxel = s.equipped
        block_texture = selectedvoxel.block_texture
        selected = 'block'
    elif s.equipped == 'gun':
        selectedvoxel = None
        selected = 'ak'
    else:
        selectedvoxel = None
        block_texture = None
        selected = 'openhand'
    slotselected = s
    destroy(hand)
    if selectedvoxel:
        hand = Entity(model='cube',texture=block_texture, color=s.hand_color, scale=(0.5,0.5,0.5), rotation=(0,0,0), position=(0,0,0), parent=camera)
    elif not selectedvoxel and selected == 'ak':
        hand = Entity(model="PyCraft/Textures/ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180), parent=camera)
    else:
        hand = Entity(model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0), parent=camera)
    defrot = hand.rotation
    destroy(selector)
    selector = Button( 
        color=color.rgb(0, 0, 0), 
        position=(s.position.x, s.position.y, 0), 
        scale=(0.045, 0.045),
        visible=True
        )
    
build_main_menu()
defrot = (0,0,0)



selectedvoxel = Voxel
selected = ''
def input(key):
    global selectedvoxel, selector, hand, defrot, selected, world_data, blockcopied, slotselected
    if key == 'escape' and not main_menu_open and not inventory_opened:
            toggle_mouse_lock()
    if key == 'e' and not main_menu_open and not pause_menu_open:
        toggle_inventory()
        return
    if mouse.locked:
        if (key == 'left mouse down' and mouse.hovered_entity and mouse.hovered_entity != player) or (key == 'left mouse down' and selected == 'ak'):
            if hasattr(mouse.hovered_entity, 'destroyable') and not mouse.hovered_entity.destroyable:

                pass
            else:
                if selected == 'ak':
                    hand.animate_rotation((160, 0, 180), duration=0.1, curve=curve.in_out_expo)
                        
                    invoke(hand.animate_rotation, defrot, duration=0.1, curve=curve.in_out_expo, delay=0.1)
                else:
                    position = mouse.hovered_entity.position
                    destroy(mouse.hovered_entity)

                    for block in world_data:
                        if block['position'] == [position.x, position.y, position.z]:
                            world_data.remove(block)
                            break

                    hand.rotation = defrot

                    hand.animate_rotation((110, -30, 0), duration=0.2, curve=curve.in_out_quad)
                        
                    invoke(hand.animate_rotation, defrot, duration=0.2, curve=curve.in_out_quad, delay=0.2)
        
        if key == 'middle mouse down' and mouse.hovered_entity:
            global blockcopied
            voxcolor = mouse.hovered_entity.color
            blockcopied = mouse.hovered_entity.__class__.__name__
            blocktexture =mouse.hovered_entity.texture
            blockicon = mouse.hovered_entity.block_icon
            if hasattr(mouse.hovered_entity, 'destroyable'):
                class CopiedVoxel(Button):
                    block_texture = blocktexture
                    block_color = voxcolor
                    def __init__(self, position=(0,0,0)):
                        base_color = color.rgb(voxcolor.r, voxcolor.g, voxcolor.b)
                        super().__init__(parent=scene,
                        position=position,
                        model='cube',
                        origin_y=.5,
                        texture=blocktexture,
                        block_icon=blockicon,
                        color=color.rgb(voxcolor.r, voxcolor.g, voxcolor.b),
                        highlight_color=color.cyan,
                        )
                        r = min(base_color.r + 0.1, 1.0)
                        g = min(base_color.g + 0.1, 1.0)
                        b = min(base_color.b + 0.1, 1.0)
                        self.highlight_color = color.rgb(r, g, b)
                        self.destroyable = False
            else:
                class CopiedVoxel(Button):
                    block_texture = blocktexture
                    def __init__(self, position=(0,0,0)):
                        base_color = color.rgb(voxcolor.r, voxcolor.g, voxcolor.b)
                        super().__init__(parent=scene,
                        position=position,
                        model='cube',
                        origin_y=.5,
                        texture=blocktexture,
                        block_icon=blockicon,
                        color=base_color,
                        highlight_color=color.cyan,
                        )
                        r = min(base_color.r + 0.1, 1.0)
                        g = min(base_color.g + 0.1, 1.0)
                        b = min(base_color.b + 0.1, 1.0)
                        self.highlight_color = color.rgb(r, g, b)
            slotselected.hand_color = voxcolor
            slotselected.texture = blockicon
            slotselected.equipped = CopiedVoxel
            slotselected.visible = True
            selectedvoxel = CopiedVoxel
            selected = 'copiedblock'
            defrot = (0,0,0)
            destroy(hand)
            hand = Entity(model='cube',texture=blocktexture, color=color.rgb(voxcolor.r, voxcolor.g, voxcolor.b), scale=(0.5,0.5,0.5), rotation=(0,0,0), position=(0,0,0), parent=camera)
        if key == 'right mouse down':
            hit_info = raycast(camera.world_position, camera.forward, distance=5, ignore=(player,))
            if hit_info.hit and selectedvoxel and not hasattr(hit_info.entity, 'wall'):
                new_position = hit_info.entity.position + hit_info.normal
                selectedvoxel(position=new_position)
                block_type = selectedvoxel.__name__
                if block_type == 'CopiedVoxel':
                    block_type = blockcopied
                world_data.append({'position': [new_position.x, new_position.y, new_position.z], 'block_type': block_type})
                hand.rotation = defrot

                hand.animate_rotation((110, -30, 0), duration=0.2, curve=curve.in_out_quad)
                        
                invoke(hand.animate_rotation, defrot, duration=0.2, curve=curve.in_out_quad, delay=0.2)
        if key == 'f3':
            global debugOpen, worldversion, seedlabel, modslist
            loaded_mods = [i for i in mod_states if mod_states[i]]
            if debugOpen:
                destroy(worldversion)
                destroy(seedlabel)
                destroy(modslist)
                debugOpen = False
            else:
                worldversion = Text(
                parent=camera.ui,  
                text=f'World Version: {worldver}',   
                origin=(0, 0),      
                scale=1,            
                color=color.white,   
                position=(-0.75, 0.47),            
                )
                seedlabel = Text(
                parent=camera.ui,  
                text=f'Seed: {seedvalue}',   
                origin=(0, 0),      
                scale=1,            
                color=color.white,   
                position=(-0.75, 0.43),            
                )
                modslist = Text(
                parent=camera.ui,  
                text=f'Mods: {loaded_mods}',   
                origin=(0, 0),      
                scale=1,            
                color=color.white,   
                position=(-0.5, 0.39),            
                )
                debugOpen = True
        if key == '1':
            if slot1.equipped and slot1.equipped != 'gun':
                selectedvoxel = slot1.equipped
                block_texture = selectedvoxel.block_texture
                selected = 'block'
            elif slot1.equipped == 'gun':
                selectedvoxel = None
                selected = 'ak'
            else:
                selectedvoxel = None
                block_texture = None
                selected = 'openhand'
            slotselected = slot1
            destroy(hand)
            if selectedvoxel:
                hand = Entity(model='cube',texture=block_texture, color=slot1.hand_color, scale=(0.5,0.5,0.5), rotation=(0,0,0), position=(0,0,0), parent=camera)
            elif not selectedvoxel and selected == 'ak':
                hand = Entity(model="PyCraft/Textures/ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180), parent=camera)
            else:
                hand = Entity(model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0), parent=camera)
            defrot = hand.rotation
            destroy(selector)
            selector = Button( 
                color=color.rgb(0, 0, 0), 
                position=(slot1.position.x, slot1.position.y, 0), 
                scale=(0.045, 0.045),
                visible=True
                )
        if key == '2':
            if slot2.equipped and slot2.equipped != 'gun':
                selectedvoxel = slot2.equipped
                block_texture = selectedvoxel.block_texture
                selected = 'block'
            elif slot2.equipped == 'gun':
                selectedvoxel = None
                selected = 'ak'
            else:
                selectedvoxel = None
                block_texture = None
                selected = 'openhand'
            slotselected = slot2
            destroy(hand)
            if selectedvoxel:
                hand = Entity(model='cube',texture=block_texture, color=slot2.hand_color, scale=(0.5,0.5,0.5), rotation=(0,0,0), position=(0,0,0), parent=camera)
            elif not selectedvoxel and selected == 'ak':
                hand = Entity(model="PyCraft/Textures/ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180), parent=camera)
            else:
                hand = Entity(model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0), parent=camera)
            defrot = hand.rotation
            destroy(selector)
            selector = Button( 
                color=color.rgb(0, 0, 0), 
                position=(slot2.position.x, slot2.position.y, 0), 
                scale=(0.045, 0.045),
                visible=True
                )
        if key == '3':
            if slot3.equipped and slot3.equipped != 'gun':
                selectedvoxel = slot3.equipped
                block_texture = selectedvoxel.block_texture
                selected = 'block'
            elif slot3.equipped == 'gun':
                selectedvoxel = None
                selected = 'ak'
            else:
                selectedvoxel = None
                block_texture = None
                selected = 'openhand'
            slotselected = slot3
            destroy(hand)
            if selectedvoxel:
                hand = Entity(model='cube',texture=block_texture, color=slot3.hand_color, scale=(0.5,0.5,0.5), rotation=(0,0,0), position=(0,0,0), parent=camera)
            elif not selectedvoxel and selected == 'ak':
                hand = Entity(model="PyCraft/Textures/ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180), parent=camera)
            else:
                hand = Entity(model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0), parent=camera)
            destroy(selector)
            defrot = hand.rotation
            selector = Button( 
                color=color.rgb(0, 0, 0), 
                position=(slot3.position.x, slot3.position.y, 0), 
                scale=(0.045, 0.045),
                visible=True
                )
        if key == '4':
            if slot4.equipped and slot4.equipped != 'gun':
                selectedvoxel = slot4.equipped
                block_texture = selectedvoxel.block_texture
                selected = 'block'
            elif slot4.equipped == 'gun':
                selectedvoxel = None
                selected = 'ak'
            else:
                selectedvoxel = None
                block_texture = None
                selected = 'openhand'
            destroy(hand)
            destroy(selector)
            slotselected = slot4
            if selectedvoxel:
                hand = Entity(model='cube',texture=block_texture, color=slot4.hand_color, scale=(0.5,0.5,0.5), rotation=(0,0,0), position=(0,0,0), parent=camera)
            elif not selectedvoxel and selected == 'ak':
                hand = Entity(model="PyCraft/Textures/ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180), parent=camera)
            else:
                hand = Entity(model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0), parent=camera)
            defrot = hand.rotation
            selector = Button( 
                color=color.rgb(0, 0, 0), 
                position=(slot4.position.x, slot4.position.y, 0), 
                scale=(0.045, 0.045),
                visible=True
                )
        if key == '5':
            if slot5.equipped and slot5.equipped != 'gun':
                selectedvoxel = slot5.equipped
                block_texture = selectedvoxel.block_texture
                selected = 'block'
            elif slot5.equipped == 'gun':
                selectedvoxel = None
                selected = 'ak'
            else:
                selectedvoxel = None
                block_texture = None
                selected = 'openhand'
            destroy(hand)
            slotselected = slot5
            if selectedvoxel:       
                hand = Entity(model='cube',texture=block_texture, color=slot5.hand_color, scale=(0.5,0.5,0.5), rotation=(0,0,0), position=(0,0,0), parent=camera)
            elif not selectedvoxel and selected == 'ak':
                hand = Entity(model="PyCraft/Textures/ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180), parent=camera)
            else:
                hand = Entity(model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0), parent=camera)
            defrot = hand.rotation
            destroy(selector)
            selector = Button( 
                color=color.rgb(0, 0, 0), 
                position=(slot5.position.x, slot5.position.y, 0), 
                scale=(0.045, 0.045),
                visible=True
                )
        if key == '6':
            if slot6.equipped and slot6.equipped != 'gun':
                selectedvoxel = slot6.equipped
                block_texture = selectedvoxel.block_texture
                selected = 'block'
            elif slot6.equipped == 'gun':
                selectedvoxel = None
                selected = 'ak'
            else:
                selectedvoxel = None
                block_texture = None
                selected = 'openhand'
            destroy(hand)
            slotselected = slot6
            if selectedvoxel:
                hand = Entity(model='cube',texture=block_texture, color=slot6.hand_color, scale=(0.5,0.5,0.5), rotation=(0,0,0), position=(0,0,0), parent=camera)
            elif not selectedvoxel and selected == 'ak':
                hand = Entity(model="PyCraft/Textures/ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180), parent=camera)
            else:
                hand = Entity(model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0), parent=camera)
            defrot = hand.rotation
            destroy(selector)
            selector = Button( 
                color=color.rgb(0, 0, 0), 
                position=(slot6.position.x, slot6.position.y, 0), 
                scale=(0.045, 0.045),
                visible=True
                )


issprinting = False
iscrouching = False
def update():
    global fov_slider, issprinting, iscrouching
    update_hand_position(   )
    if holding_block:
        block_drag.position = Vec3(mouse.x, mouse.y, -1.1)
    if held_keys['shift']:
        player.speed = 10
        if not issprinting:
            camera.animate('fov', camera.fov + 10, duration = 0.05, curve=curve.linear)
            issprinting = True
    else:
        player.speed = 5
        if issprinting:
            camera.animate('fov', camera.fov - 10, duration=0.05, curve=curve.linear)
            issprinting = False
    player.enabled = mouse.locked
player = FirstPersonController()
player.height = 1.8
player.camera_pivot.y = 1.8
mouse.locked = False
Sky()
app.run()