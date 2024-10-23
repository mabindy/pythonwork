from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from ursina import Slider
from perlin_noise import PerlinNoise
from ursina.collider import BoxCollider
from ursina.texture_importer import load_texture
import random

app = Ursina(borderless=False, title='PyCraft', icon='pycraftlogo.ico')

window.fullscreen = False

fov_slider = None


# Define a Voxel class.
# By setting the parent to scene and the model to 'cube' it becomes a 3d button.
class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, random.uniform(.9, 1.0))
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='pycrafttextures/cobblestone.png',
            color=base_color,
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)

class OreVoxel(Button):
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, random.uniform(.9, 1.0))
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='pycrafttextures/iron_ore.png',
            color=base_color,
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)


class GroundVoxel(Button):
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(120, 0.75, 0.7)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='pycrafttextures/grass_top.png',
            color=base_color,
            highlight_color=color.cyan,
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)

class BrownVoxel(Button):
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(30, 0.5, 0.7)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='pycrafttextures/default_dirt.png',
            color=base_color,
            highlight_color=color.cyan,
            collider='box'
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
class Bedrock(Button):
    def __init__(self, position=(0,0,0)):
        base_color = color.hsv(0, 0, 1)
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='pycrafttextures/bedrocktexture.png',
            color=base_color,
            highlight_color=color.cyan,
        )
        r = min(base_color.r + 0.1, 1.0)
        g = min(base_color.g + 0.1, 1.0)
        b = min(base_color.b + 0.1, 1.0)
        self.highlight_color = color.rgb(r, g, b)
        self.destroyable = False



noise = PerlinNoise (octaves=3, seed=random.randint(1,1000000))
min_y = -5
worlddimensions = 15 #World dimensions are twice this number 
for z in range(-worlddimensions,worlddimensions):
    for x in range(-worlddimensions,worlddimensions):
        surface_y = noise([x * .02,z * .02])
        surface_y = math.floor(surface_y*7.5)
        for y in range(min_y, surface_y + 1):
            position = (x, y, z)
            if y == surface_y:
                voxel = GroundVoxel(position=position)
            elif y == min_y:
                voxel = Bedrock(position=position)
            elif y > surface_y - 3:
                voxel = BrownVoxel(position=position)
            else:
                oregenerator = random.randint(0,10)
                if oregenerator == 5:
                    voxel = OreVoxel(position=position)
                else:
                    voxel = Voxel(position=position)
wall_thickness = 1
wall_height = 200
voxel_size = 1

min_xz = -worlddimensions
max_xz = worlddimensions - 1
terrain_min_xz = min_xz - voxel_size / 2
terrain_max_xz = max_xz + voxel_size / 2
terrain_width_xz = terrain_max_xz - terrain_min_xz

north_wall = Entity(
    model = 'cube',
    scale = (terrain_width_xz, wall_height, wall_thickness),
    position = (
        (terrain_min_xz + terrain_max_xz) / 2,
        wall_height / 2 + min_y,
        terrain_max_xz + wall_thickness / 2,
    ),
    collider = 'box',
    visible = False,
    destroyable = False,
)
south_wall = Entity(
    model = 'cube',
    scale = (terrain_width_xz, wall_height, wall_thickness),
    position = (
        (terrain_min_xz + terrain_max_xz) / 2,
        wall_height / 2 + min_y,
        terrain_min_xz - wall_thickness / 2,
    ),
    collider = 'box',
    visible = False,
    destroyable = False,
)
east_wall = Entity(
    model = 'cube',
    scale = (wall_thickness, wall_height, terrain_width_xz),
    position=(
        terrain_max_xz + wall_thickness / 2,
        wall_height / 2 + min_y,
        (terrain_min_xz + terrain_max_xz) / 2
    ),
    collider = 'box',
    visible = False,
    destroyable = False,
)
west_wall = Entity(
    model = 'cube',
    scale = (wall_thickness, wall_height, terrain_width_xz),
    position=(
        terrain_min_xz + wall_thickness / 2,
        wall_height / 2 + min_y,
        (terrain_min_xz + terrain_max_xz) / 2
    ),
    collider = 'box',
    visible = False,
    destroyable = False,
)

hotbar = Button( 
                color=color.rgba(255,255,255,0.8), 
                position=(0, -0.4,0.1), 
                scale=(0.6, 0.07), 
                )

regvoxel = Button( 
                color=color.rgb(0.502, 0.502, 0.502), 
                position=(-0.26, -0.4,0), 
                scale=(0.08, 0.07), 
                )
brovoxel = Button( 
                color=color.rgb(0.545, 0.271, 0.075), 
                position=(-0.15, -0.4, 0), 
                scale=(0.08, 0.07), 
                )
selector = Button( 
                color=color.rgb(0.0, 0.502, 0.0), 
                position=(-0.26, -0.4,0.1), 
                scale=(0.09, 0.08), 
                )

hand = Entity(model='cube',texture='white_cube', color=color.hsv(0, 0, random.uniform(.9, 1.0)), scale=(0.5,0.5,0.5), position=(0,0,0), parent=camera)

def update_hand_position():
    if selected == 'ak':
        hand.position = (0.5, -0.5, 2)
    else:
        hand.position = (0.5, -0.5, 1)


settings_opened = False
def toggle_mouse_lock():
    global settings_opened
    if mouse.locked:
        mouse.locked = False
        mouse.visible = True
        pause_menu.visible = True
        build_pause_menu()
    else:
        mouse.locked = True
        mouse.visible = False
        pause_menu.visible = False
        if settings_opened:
            close_settings()
        destroy_pause_menu()
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
    destroy(resume_button)
    destroy(quit_button)
    destroy(settings_button)
    destroy(pause_label)

def build_pause_menu():
    global resume_button, quit_button, pause_label, settings_button
    resume_button = Button(
        parent=pause_menu,
        text='Resume',
        color=color.gray,
        scale=(0.15, 0.02),  # Size of the button
        position=(0, 0),  # Position on the screen
        on_click = lambda: toggle_mouse_lock()
    )

    quit_button = Button(
        parent=pause_menu,
        text='Quit',
        color=color.gray,
        scale=(0.15, 0.02), 
        position=(0, -0.1),  
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



defrot = (0,0,0)


selectedvoxel = Voxel
selected = ''
def input(key):
    global selectedvoxel
    global selector
    global regvoxel
    global brovoxel
    global hand
    global defrot
    global selected
    if key == 'escape':
            toggle_mouse_lock()
        
    if mouse.locked:
        if key == 'right mouse down':
            hit_info = raycast(camera.world_position, camera.forward, distance=5, ignore=(player,))
            if hit_info.hit and selectedvoxel:
                selectedvoxel(position=hit_info.entity.position + hit_info.normal)
                
                hand.rotation = defrot

                hand.animate_rotation((110, -30, 0), duration=0.2, curve=curve.in_out_quad)
                        
                invoke(hand.animate_rotation, defrot, duration=0.2, curve=curve.in_out_quad, delay=0.2)
                
        if (key == 'left mouse down' and mouse.hovered_entity and mouse.hovered_entity != player) or (key == 'left mouse down' and selected == 'ak'):
            if hasattr(mouse.hovered_entity, 'destroyable') and not mouse.hovered_entity.destroyable:

                pass
            else:
                if selected == 'ak':
                    hand.animate_rotation((160, 0, 180), duration=0.1, curve=curve.in_out_expo)
                        
                    invoke(hand.animate_rotation, defrot, duration=0.1, curve=curve.in_out_expo, delay=0.1)
                else:
                    destroy(mouse.hovered_entity)
                
                    hand.rotation = defrot

                    hand.animate_rotation((110, -30, 0), duration=0.2, curve=curve.in_out_quad)
                        
                    invoke(hand.animate_rotation, defrot, duration=0.2, curve=curve.in_out_quad, delay=0.2)
        
        if key == 'middle mouse down' and mouse.hovered_entity:
            voxcolor = mouse.hovered_entity.color
            blocktexture =mouse.hovered_entity.texture
            if hasattr(mouse.hovered_entity, 'destroyable'):
                class CopiedVoxel(Button):
                    def __init__(self, position=(0,0,0)):
                        base_color = color.rgb(voxcolor.r, voxcolor.g, voxcolor.b)
                        super().__init__(parent=scene,
                        position=position,
                        model='cube',
                        origin_y=.5,
                        texture=blocktexture,
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
                    def __init__(self, position=(0,0,0)):
                        base_color = color.rgb(voxcolor.r, voxcolor.g, voxcolor.b)
                        super().__init__(parent=scene,
                        position=position,
                        model='cube',
                        origin_y=.5,
                        texture=blocktexture,
                        color=base_color,
                        highlight_color=color.cyan,
                        )
                        r = min(base_color.r + 0.1, 1.0)
                        g = min(base_color.g + 0.1, 1.0)
                        b = min(base_color.b + 0.1, 1.0)
                        self.highlight_color = color.rgb(r, g, b)
            selectedvoxel = CopiedVoxel
            selected = 'copiedblock'
            defrot = (0,0,0)
            destroy(selector)
            destroy(hand)
            hand = Entity(model='cube',texture=blocktexture, color=color.rgb(voxcolor.r, voxcolor.g, voxcolor.b), scale=(0.5,0.5,0.5), rotation=(0,0,0), position=(0,0,0), parent=camera)
        if key == '1':
            selectedvoxel = Voxel
            selected = 'basic'
            destroy(hand)
            hand = Entity(model='cube',texture='pycrafttextures/cobblestone.png', color=color.hsv(0, 0, random.uniform(.9, 1.0)), scale=(0.5,0.5,0.5), rotation=(0,0,0), position=(0,0,0), parent=camera)
            defrot = hand.rotation
            destroy(selector)
            selector = Button( 
                    color=color.rgb(0.0, 0.502, 0.0), 
                    position=(regvoxel.position.x, regvoxel.position.y, 0.1), 
                    scale=(0.09, 0.08), 
                    )
        if key == '2':
            selectedvoxel = BrownVoxel
            selected = 'dirt'
            destroy(hand)
            hand = Entity(model='cube',texture='pycrafttextures/default_dirt.png', color=color.hsv(30, 0.5, 0.7), scale=(0.5,0.5,0.5), rotation=(0,0,0), position=(0,0,0), parent=camera)
            defrot = hand.rotation
            destroy(selector)
            selector = Button( 
                    color=color.rgb(0.0, 0.502, 0.0), 
                    position=(brovoxel.position.x, brovoxel.position.y, 0.1), 
                    scale=(0.09, 0.08), 
                    )
        if key == '3':
            selectedvoxel = None
            selected = 'openhand'
            destroy(hand)
            destroy(selector)
            hand = Entity(model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0), parent=camera)
            defrot = hand.rotation
        if key == '4':
            selectedvoxel = None
            destroy(hand)
            destroy(selector)
            selected = 'ak'
            hand = Entity(model="ak.obj", scale=(0.5,0.5,0.5), position=(0,0,0), rotation=(180,0,180), parent=camera)
            defrot = hand.rotation
issprinting = False
iscrouching = False
def update():
    global fov_slider, issprinting, iscrouching
    update_hand_position(   )

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
Sky()

app.run()