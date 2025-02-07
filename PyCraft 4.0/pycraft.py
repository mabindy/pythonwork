from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import random, math, json

# -------------------------------------------
# CHUNK CLASS WITH TEXTURE ATLAS SUPPORT
# -------------------------------------------
block_highlight = Entity(
        model='cube',
        color=color.rgba(255, 255, 255, 0.2),
        scale=1.005,
        enabled=False,
        # Optionally, set a shader that draws only an outline:
        # shader=lit_with_shadows_shader,
        double_sided=True
    )

class Chunk(Entity):
    def __init__(self, origin=(0,0,0), size=5, noise=None, saved_data=None, **kwargs):
        """
        A chunk covers a square area in the X–Z plane.
        Blocks are stored with local X and Z (0 to size-1) and a global Y.
        The chunk’s origin is in world space; the mesh is built in local coordinates.
        If saved_data is provided, it is used for the block dictionary.
        """
        super().__init__(**kwargs)
        self.origin = Vec3(*origin)
        self.size = size
        self.noise = noise if noise is not None else PerlinNoise(octaves=2, seed=random.randint(0,10000))
        self.model = Mesh()
        # Use your texture atlas image:
        self.texture = 'PyCraft/Textures/grassta.png'
        if saved_data is None:
            self.block_dict = {}
            self.generate_terrain()
        else:
            self.block_dict = saved_data
        self.rebuild()
        self.collider = MeshCollider(self)
        self.position = self.origin

    def generate_terrain(self):
        """
        Generate terrain using Perlin noise for the surface, then fill each (x,z) column down to a fixed ground level.
        This ensures that the bottom layer is flat (all at the same y value).
        """
        ground_level = 0    # Set the flat bottom level (you can adjust this as needed)
        scale = 0.02        # Lower frequency produces smoother, larger hills.
        amplitude = 10      
        offset = 4         # This offset should be high enough so that surface_y is always > ground_level.
        
        for x in range(self.size):
            for z in range(self.size):
                world_x = self.origin.x + x
                world_z = self.origin.z + z
                # Compute the surface level using Perlin noise.
                surface_y = int(self.noise([world_x * scale, world_z * scale]) * amplitude) + offset
                # Fill the column from the surface down to the ground level.
                # (Using ground_level - 1 in the range so that ground_level is included.)
                for y in range(surface_y, ground_level - 1, -1):
                    if y == surface_y:
                        block_type = 'grass'
                    elif y >= surface_y - 3:
                        block_type = 'dirt'
                    else:
                        block_type = 'stone'
                    self.block_dict[(x, y, z)] = block_type


    def rebuild(self):
        """
        Rebuild the mesh from self.block_dict.
        Only add faces for sides that are not hidden by a neighbor (within this chunk).
        """
        vertices = []
        triangles = []
        uvs = []
        vertex_index = 0

        directions = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]
        for pos, block_type in self.block_dict.items():
            x, y, z = pos
            for normal in directions:
                nx, ny, nz = normal
                neighbor = (x+nx, y+ny, z+nz)
                # If neighbor exists inside this chunk (in X,Z) skip drawing the face.
                if (0 <= x+nx < self.size) and (0 <= z+nz < self.size):
                    if neighbor in self.block_dict:
                        continue
                self.add_cube_face(vertices, triangles, uvs, float(x), float(y), float(z), normal, vertex_index, block_type)
                vertex_index += 4

        self.update_mesh(vertices, triangles, uvs)
        try:
            if self.collider and hasattr(self.collider, 'eternal'):
                destroy(self.collider)
        except Exception as e:
            print("Failed to destroy collider:", e)
        self.collider = MeshCollider(self)

    def update_mesh(self, vertices, triangles, uvs):
        self.model.vertices = vertices
        self.model.triangles = triangles
        self.model.uvs = uvs
        self.model.normals = []  # Clear old normals.
        self.model.generate()
        self.model.generate_normals()
        self.model.entity = self

    def get_uvs_for_face(self, block_type, normal, atlas_cols=4, atlas_rows=4):
        """
        Compute the UV coordinates for a given block type and face (normal) based on a texture atlas.
        Adjust the tile indices to suit your atlas layout.
        """
        tile_width = 1 / atlas_cols
        tile_height = 1 / atlas_rows

        if block_type == 'grass':
            if normal == (0, 1, 0):      # Top face uses grass texture.
                tile = (1, 0)
            elif normal == (0, -1, 0):   # Bottom face uses dirt texture.
                tile = (2, 0)
            else:                       # Side faces use grass_side.
                tile = (0, 0)
        elif block_type == 'dirt':
            tile = (2, 0)
        elif block_type == 'stone':
            tile = (3, 0)
        else:
            tile = (3, 0)  # Default tile.

        u0 = tile[0] * tile_width
        v0 = tile[1] * tile_height
        u1 = u0 + tile_width
        v1 = v0 + tile_height
        # Return UVs in the order: bottom-left, bottom-right, top-right, top-left.
        return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]

    def add_cube_face(self, vertices, triangles, uvs, x, y, z, normal, index, block_type):
        """
        Adds one face of a cube at local coordinate (x,y,z) in the given normal direction.
        Uses get_uvs_for_face() to compute the proper UV coordinates from the texture atlas.
        Then, based on the face (normal), reorders the UVs to match the vertex order.
        """
        if normal == (1, 0, 0):  # Right face.
            face_vertices = [(x+1, y,   z),
                             (x+1, y,   z+1),
                             (x+1, y+1, z+1),
                             (x+1, y+1, z)]
        elif normal == (-1, 0, 0):  # Left face.
            face_vertices = [(x, y,   z),
                             (x, y+1, z),
                             (x, y+1, z+1),
                             (x, y,   z+1)]
        elif normal == (0, 1, 0):  # Top face.
            face_vertices = [(x, y+1, z),
                             (x+1, y+1, z),
                             (x+1, y+1, z+1),
                             (x, y+1, z+1)]
        elif normal == (0, -1, 0):  # Bottom face.
            face_vertices = [(x, y, z),
                             (x, y, z+1),
                             (x+1, y, z+1),
                             (x+1, y, z)]
        elif normal == (0, 0, 1):  # Front face.
            face_vertices = [(x, y,   z+1),
                             (x, y+1, z+1),
                             (x+1, y+1, z+1),
                             (x+1, y,   z+1)]
        elif normal == (0, 0, -1):  # Back face.
            face_vertices = [(x, y,   z),
                             (x+1, y,   z),
                             (x+1, y+1, z),
                             (x, y+1, z)]
        else:
            face_vertices = []
        
        # Ensure all vertices are floats.
        face_vertices = [(float(vx), float(vy), float(vz)) for vx, vy, vz in face_vertices]
        vertices.extend(face_vertices)
        triangles.extend([index, index+1, index+2, index, index+2, index+3])
        
        # Get default UVs from the atlas.
        default_uvs = self.get_uvs_for_face(block_type, normal)
        
        # Reorder UVs based on face normal and our computed desired ordering.
        if normal == (1, 0, 0):  # Right face: desired order [v1, v0, v3, v2]
            reordered_uvs = [default_uvs[1], default_uvs[0], default_uvs[3], default_uvs[2]]
        elif normal == (-1, 0, 0):  # Left face: desired order [v0, v3, v2, v1]
            reordered_uvs = [default_uvs[0], default_uvs[3], default_uvs[2], default_uvs[1]]
        elif normal == (0, 0, 1):  # Front face: desired order [v0, v3, v2, v1]
            reordered_uvs = [default_uvs[0], default_uvs[3], default_uvs[2], default_uvs[1]]
        elif normal == (0, 0, -1):  # Back face: desired order [v1, v0, v3, v2]
            reordered_uvs = [default_uvs[1], default_uvs[0], default_uvs[3], default_uvs[2]]
        else:
            # Top and bottom faces (and any unspecified normals) use the default order.
            reordered_uvs = default_uvs
        
        uvs.extend(reordered_uvs)


    def remove_block(self, local_pos):
        """
        Remove a block at the given local coordinate (x,y,z). If the block being removed is at
        or near the bottom of its column, extend that column downward. Also, check every column
        in the chunk that is within a horizontal radius (here, radius 2) of the removed block.
        If any of those columns has its lowest block above the removed block’s y, extend them as well.
        """
        if local_pos in self.block_dict:
            removed_y = local_pos[1]
            x, z = local_pos[0], local_pos[2]
            # Remove the block.
            del self.block_dict[local_pos]
            
            # First, for the column where the block was removed:
            column_ys = [y for (xx, y, zz) in self.block_dict.keys() if xx == x and zz == z]
            if not column_ys or removed_y <= min(column_ys):
                self.extend_column(x, z, start_y=removed_y)
            
            # Now extend neighboring columns within a horizontal radius.
            # (You can adjust the radius as needed.)
            horizontal_radius = 2  # includes immediate neighbors and further out if available.
            for nx in range(self.size):
                for nz in range(self.size):
                    # Compute Euclidean distance from the removed block's column.
                    if math.sqrt((nx - x)**2 + (nz - z)**2) <= horizontal_radius:
                        neighbor_ys = [y for (xx, y, zz) in self.block_dict.keys() if xx == nx and zz == nz]
                        if not neighbor_ys or min(neighbor_ys) > removed_y:
                            self.extend_column(nx, nz, start_y=removed_y)
            self.rebuild()
    
    def extend_column(self, x, z, start_y):
        extension_depth = 5
        for new_y in range(start_y - 1, start_y - extension_depth - 1, -1):
            self.block_dict[(x, new_y, z)] = 'stone'

    def place_block(self, local_pos, block_type='grass'):
        if local_pos not in self.block_dict:
            self.block_dict[local_pos] = block_type
            self.rebuild()

# -------------------------------------------
# INFINITE WORLD CLASS WITH PERSISTENCE
# -------------------------------------------
class InfiniteWorld:
    def __init__(self, chunk_size=5, view_distance=7):
        """
        The infinite world keeps a dictionary of loaded chunks (by (chunk_x, chunk_z))
        and a dictionary of saved chunk modifications.
        Chunks within view_distance (in chunks) around the player are loaded.
        """
        self.chunk_size = chunk_size
        self.view_distance = view_distance
        self.noise = PerlinNoise(octaves=2, seed=random.randint(0,10000))
        self.loaded_chunks = {}  # Keys: (cx, cz); Values: Chunk instances.
        self.saved_chunks = {}   # Keys: (cx, cz); Values: saved block_dict.
        self.chunk_load_queue = []

    def update(self, player_pos):
        current_cx = math.floor(player_pos.x / self.chunk_size)
        current_cz = math.floor(player_pos.z / self.chunk_size)
        active_coords = set()
        for dx in range(-self.view_distance, self.view_distance+1):
            for dz in range(-self.view_distance, self.view_distance+1):
                active_coords.add((current_cx+dx, current_cz+dz))
        for coord in active_coords:
            if coord not in self.loaded_chunks and coord not in self.chunk_load_queue:
                self.chunk_load_queue.append(coord)
        for key in list(self.loaded_chunks.keys()):
            if key not in active_coords:
                self.saved_chunks[key] = self.loaded_chunks[key].block_dict
                destroy(self.loaded_chunks[key])
                del self.loaded_chunks[key]
        chunks_to_load_per_frame = 1
        for _ in range(chunks_to_load_per_frame):
            if self.chunk_load_queue:
                coord = self.chunk_load_queue.pop(0)
                if coord in active_coords:
                    cx, cz = coord
                    origin = (cx * self.chunk_size, 0, cz * self.chunk_size)
                    saved_data = self.saved_chunks.get(coord)
                    chunk = Chunk(origin=origin, size=self.chunk_size, noise=self.noise, saved_data=saved_data)
                    self.loaded_chunks[coord] = chunk

    def get_chunk_at(self, world_pos):
        cx = math.floor(world_pos.x / self.chunk_size)
        cz = math.floor(world_pos.z / self.chunk_size)
        return self.loaded_chunks.get((cx, cz))

    def remove_block_at(self, world_pos):
        bx = math.floor(world_pos.x)
        by = math.floor(world_pos.y)
        bz = math.floor(world_pos.z)
        chunk = self.get_chunk_at(Vec3(bx,by,bz))
        if chunk:
            local_x = bx - int(chunk.origin.x)
            local_z = bz - int(chunk.origin.z)
            local_pos = (local_x, by, local_z)
            chunk.remove_block(local_pos)
            self.update_neighbor_chunks(chunk, local_x, local_z)
        else:
            print("No chunk found at", world_pos)

    def place_block_at(self, world_pos, block_type='grass'):
        bx = math.floor(world_pos.x)
        by = math.floor(world_pos.y)
        bz = math.floor(world_pos.z)
        chunk = self.get_chunk_at(Vec3(bx,by,bz))
        if chunk:
            local_x = bx - int(chunk.origin.x)
            local_z = bz - int(chunk.origin.z)
            local_pos = (local_x, by, local_z)
            chunk.place_block(local_pos, block_type)
            self.update_neighbor_chunks(chunk, local_x, local_z)
        else:
            print("No chunk found at", world_pos)

    def update_neighbor_chunks(self, chunk, local_x, local_z):
        cx = int(chunk.origin.x // self.chunk_size)
        cz = int(chunk.origin.z // self.chunk_size)
        if local_x == 0:
            neighbor = self.loaded_chunks.get((cx - 1, cz))
            if neighbor: neighbor.rebuild()
        if local_x == self.chunk_size - 1:
            neighbor = self.loaded_chunks.get((cx + 1, cz))
            if neighbor: neighbor.rebuild()
        if local_z == 0:
            neighbor = self.loaded_chunks.get((cx, cz - 1))
            if neighbor: neighbor.rebuild()
        if local_z == self.chunk_size - 1:
            neighbor = self.loaded_chunks.get((cx, cz + 1))
            if neighbor: neighbor.rebuild()
        if local_x == 0 and local_z == 0:
            neighbor = self.loaded_chunks.get((cx - 1, cz - 1))
            if neighbor: neighbor.rebuild()
        if local_x == 0 and local_z == self.chunk_size - 1:
            neighbor = self.loaded_chunks.get((cx - 1, cz + 1))
            if neighbor: neighbor.rebuild()
        if local_x == self.chunk_size - 1 and local_z == 0:
            neighbor = self.loaded_chunks.get((cx + 1, cz - 1))
            if neighbor: neighbor.rebuild()
        if local_x == self.chunk_size - 1 and local_z == self.chunk_size - 1:
            neighbor = self.loaded_chunks.get((cx + 1, cz + 1))
            if neighbor: neighbor.rebuild()
creative = True
class CustomFirstPersonController(Entity):
    def __init__(self, **kwargs):
        self.cursor = Entity(parent=camera.ui, model='quad', texture="PyCraft/Textures/cursor.png", color=color.white, scale=.03)
        super().__init__()
        self.speed = 5
        self.height = 2
        self.camera_pivot = Entity(parent=self, y=self.height)

        camera.parent = self.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 90
        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = 25
        self.gravity_enabled = True
        self.vertical_velocity = 0
        self.grounded = False
        self.jump_speed = 9  # Adjusted jump speed
        self.jumping = False

        self.last_space_press_time = 0
        self.space_press_count = 0
        self.double_press_threshold = 0.3

        self.traverse_target = scene     # by default, it will collide with everything. change this to change the raycasts' traverse targets.
        self.ignore_list = [self, ]
        self.on_destroy = self.on_disable

        for key, value in kwargs.items():
            setattr(self, key ,value)

        # make sure we don't fall through the ground if we start inside it
        if self.gravity:
            ray = raycast(self.world_position+(0,self.height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)
            if ray.hit:
                self.y = ray.world_point.y



    def update(self):
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -90, 90)

        self.direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
            ).normalized()

        feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        if not feet_ray.hit and not head_ray.hit:
            move_amount = self.direction * time.dt * self.speed

            if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = max(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = min(move_amount[2], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = max(move_amount[2], 0)
            self.position += move_amount

        if self.gravity and self.gravity_enabled:
            # Apply gravity
            self.vertical_velocity -= self.gravity * time.dt

            # Calculate potential movement
            delta_y = self.vertical_velocity * time.dt

            # Check for collision in the vertical movement
            direction = Vec3(0, math.copysign(1, delta_y), 0) if delta_y != 0 else Vec3(0,0,0)
            ray = raycast(self.position + Vec3(0, self.height / 2, 0), direction, distance=self.height / 2 + abs(delta_y), traverse_target=self.traverse_target, ignore=self.ignore_list)
            if ray.hit:
                if self.vertical_velocity < 0:
                    # Landing on ground
                    self.y = ray.world_point.y
                    self.vertical_velocity = 0
                    self.grounded = True
                elif self.vertical_velocity > 0:
                    # Hitting ceiling
                    self.y = ray.world_point.y - self.height
                    self.vertical_velocity = 0
            else:
                # No collision, proceed with movement
                self.y += delta_y
                self.grounded = False
        else:
            self.vertical_velocity = 0
            self.grounded = False

            vertical_movement = (held_keys['space'] - held_keys['left control']) * self.speed * time.dt
            self.y += vertical_movement
    def input(self, key):
        if key == 'space' and not creative:
            self.jump()
        if key == 'space' and creative:
            current_time = time.time()
            if current_time - self.last_space_press_time <= self.double_press_threshold:
                # Detected double press
                self.gravity_enabled = not self.gravity_enabled
                print(f"Gravity enabled: {self.gravity_enabled}")
                # Reset the space press count
                self.space_press_count = 0
                self.last_space_press_time = 0
            else:
                # First press, start counting
                self.last_space_press_time = current_time
                self.space_press_count = 1
                # Handle jump if gravity is enabled
                if self.gravity_enabled:
                    self.jump()

    def jump(self):
        if not self.grounded or not self.gravity_enabled:
            return
        self.vertical_velocity = self.jump_speed
        self.grounded = False

    def on_enable(self):
        mouse.locked = True
        self.cursor.enabled = True
        # restore parent and position/rotation from before disablem in case you moved the camera in the meantime.
        if hasattr(self, 'camera_pivot') and hasattr(self, '_original_camera_transform'):
            camera.parent = self.camera_pivot
            camera.transform = self._original_camera_transform

    def on_disable(self):
        mouse.locked = False
        self.cursor.enabled = False
        self._original_camera_transform = camera.transform  # store original position and rotation
        camera.world_parent = scene

    
hand = Entity(model='cube', color=color.hsv(30, 0.4, 0.8), scale=(0.2,0.7,0.2), rotation=(45,0,0), position=(0,0,0), parent=camera)
defrot = hand.rotation
def update_hand_position():
    hand.position = (0.5, -0.5, 1)
# -------------------------------------------
# MAIN SCRIPT
# -------------------------------------------
if __name__ == '__main__':
    app = Ursina()

    # Create a first-person controller.
    player = CustomFirstPersonController()
    player.position = (10, 20, 10)
    player.height = 1.8
    player.camera_pivot.y = 1.8
    mouse.locked = True
    scene.fog_density = (0,75)
    scene.fog_color = color.white
    destroy(player.cursor)
    player.cursor = Entity(parent=camera.ui, model='quad', texture="PyCraft/Textures/cursor.png", color=color.white, scale=.03)
    sky = Sky(texture="sky_default")
    sky.color = color.hsv(0, 0, 0.9)
    update_hand_position()
    infinite_world = InfiniteWorld(chunk_size=5, view_distance=7)

    def input(key):
        if key == 'left mouse down':  # Remove block.
            hand.rotation = defrot
            hand.animate_rotation((110, -30, 0), duration=0.2, curve=curve.in_out_quad)
            invoke(hand.animate_rotation, defrot, duration=0.2, curve=curve.in_out_quad, delay=0.2)
            hit_info = raycast(camera.world_position, camera.forward, distance=10, ignore=[player])
            if hit_info.hit:
                hit_point = hit_info.world_point - hit_info.normal * 0.5
                infinite_world.remove_block_at(hit_point)
        elif key == 'right mouse down':  # Place block.
            hit_info = raycast(camera.world_position, camera.forward, distance=10, ignore=[player])
            if hit_info.hit:
                hit_point = hit_info.world_point + hit_info.normal * 0.5
                infinite_world.place_block_at(hit_point, block_type='grass')
    issprinting = False
    def update():
        global issprinting
        infinite_world.update(player.position)
        ray_info = raycast(camera.world_position, camera.forward, distance=10, ignore=[player])
        if ray_info.hit:
            # Calculate the block position using similar logic as block placement/removal.
            block_pos = Vec3(
                math.floor(ray_info.world_point.x - ray_info.normal.x * 0.5),
                math.floor(ray_info.world_point.y - ray_info.normal.y * 0.5),
                math.floor(ray_info.world_point.z - ray_info.normal.z * 0.5)
            )
            block_highlight.position = block_pos + Vec3(0.5, 0.5, 0.5)
            block_highlight.enabled = True
        else:
            block_highlight.enabled = False
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
    app.run()
