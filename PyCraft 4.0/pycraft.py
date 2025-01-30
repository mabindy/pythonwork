from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import random
class MeshTerrain(Entity):
    def __init__(self, size=16):
        super().__init__()
        self.model = Mesh()
        self.texture = 'PyCraft/Textures/default_dirt.png'  # Use a texture atlas
        self.block_dict = {}  # Store block positions
        self.size = size  # Chunk size
        self.noise = PerlinNoise(octaves=2, seed=random.randint(0, 10000))
        self.generate_terrain()

    def generate_terrain(self):
        """Generates terrain with underground layers."""
        vertices = []
        triangles = []
        uv = []
        index = 0

        for x in range(self.size):
            for z in range(self.size):
                # Generate surface height using Perlin Noise
                surface_y = int(self.noise([x * 0.1, z * 0.1]) * 7) + 10  # Raise height a bit

                # Create layers below surface
                for y in range(surface_y, surface_y - 5, -1):  # 10 blocks deep underground
                    if y == surface_y:
                        block_type = 'grass'
                    elif y > surface_y - 3:
                        block_type = 'dirt'  # Top 3 layers are dirt
                    elif y > surface_y - 6:
                        block_type = 'stone'  # Below that is stone
                    else:
                        block_type = 'deep_stone'  # Bottom layers (deep stone or bedrock)

                    self.block_dict[(x, y, z)] = block_type

                    # Only add visible faces
                    for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                        neighbor_pos = (x + dx, y + dy, z + dz)
                        if neighbor_pos not in self.block_dict:
                            self.add_cube_face(vertices, triangles, uv, float(x), float(y), float(z), (dx, dy, dz), index)
                            index += 4

        self.model.vertices = vertices
        self.model.triangles = triangles
        self.model.uvs = uv
        self.model.generate()
        self.model.generate_normals()
        self.collider = MeshCollider(self)
        self.model.entity = self
        self.model.texture = self.texture

    def remove_block(self):
        """Destroys the block the player is looking at."""
        hit_info = raycast(camera.position, camera.forward, distance=5, ignore=[self])

        if hit_info.hit:
            block_position = (floor(hit_info.world_point.x), floor(hit_info.world_point.y), floor(hit_info.world_point.z))
            print(f"Raycast hit block at {block_position}")  # Debug print

            if block_position in self.block_dict:
                print(f"Removing block at {block_position}")  # Debug print
                del self.block_dict[block_position]  # Remove block
                self.rebuild_mesh()  # Update terrain



    def place_block(self, block_type='stone'):
        print("placing")
        """Places a block at the position the player is looking at."""
        hit_info = raycast(camera.position, camera.forward, distance=5, ignore=[self])

        if hit_info.hit:
            place_position = (
                floor(hit_info.world_point.x + hit_info.normal.x),
                floor(hit_info.world_point.y + hit_info.normal.y),
                floor(hit_info.world_point.z + hit_info.normal.z),
            )

            if place_position not in self.block_dict:
                self.block_dict[place_position] = block_type  # Add block
                self.rebuild_mesh()  # Update terrain


    def rebuild_mesh(self):
        """Rebuilds the terrain mesh after block removal or placement."""
        self.model.vertices = []  # Clear old vertices
        self.model.triangles = []  # Clear old triangles
        self.model.uvs = []  # Clear old UVs
        vertices = []
        triangles = []
        uv = []
        index = 0

        for pos, block_type in self.block_dict.items():
            x, y, z = pos

            # Only add visible faces
            for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                neighbor_pos = (x + dx, y + dy, z + dz)
                if neighbor_pos not in self.block_dict:
                    self.add_cube_face(vertices, triangles, uv, float(x), float(y), float(z), (dx, dy, dz), index)
                    index += 4

        self.model.vertices = vertices
        self.model.triangles = triangles
        self.model.uvs = uv
        self.model.generate()
        self.model.generate_normals()


    def add_cube_face(self, vertices, triangles, uv, x, y, z, normal, index):
        """Adds a cube face in the given direction with corrected face orientation."""
        if normal == (1, 0, 0):
            face_vertices = [(x+1, y, z), (x+1, y, z+1), (x+1, y+1, z+1), (x+1, y+1, z)]
        elif normal == (-1, 0, 0):
            face_vertices = [(x, y, z), (x, y+1, z), (x, y+1, z+1), (x, y, z+1)]
        elif normal == (0, 1, 0):
            face_vertices = [(x, y+1, z), (x+1, y+1, z), (x+1, y+1, z+1), (x, y+1, z+1)]
        elif normal == (0, -1, 0):
            face_vertices = [(x, y, z), (x, y, z+1), (x+1, y, z+1), (x+1, y, z)]
        elif normal == (0, 0, 1):
            face_vertices = [(x, y, z+1), (x, y+1, z+1), (x+1, y+1, z+1), (x+1, y, z+1)]
        elif normal == (0, 0, -1):
            face_vertices = [(x, y, z), (x+1, y, z), (x+1, y+1, z), (x, y+1, z)]
        
        # Convert all vertices to float to prevent integer-related errors
        face_vertices = [(float(vx), float(vy), float(vz)) for vx, vy, vz in face_vertices]
        
        vertices.extend(face_vertices)
        triangles.extend([index, index+1, index+2, index, index+2, index+3])
        uv.extend([(0, 0), (1, 0), (1, 1), (0, 1)])



app = Ursina()
player = FirstPersonController()
player.position = (5, 50, 5)
player.height = 1.8
player.camera_pivot.y = 1.8
mouse.locked = True
sky = Sky(texture="sky_default")
sky.color = color.hsv(0, 0, 0.9)
terrain = MeshTerrain(size=16)
def input(key):
    if key == 'left mouse down':  # Break block
        terrain.remove_block()
    elif key == 'right mouse down':  # Place block
        terrain.place_block('stone')

app.run()