import bpy
import numpy as np
import json
from os.path import dirname, join
from mathutils import Vector

fp = bpy.path.abspath(f"//images")

def listify_matrix(matrix):
    matrix_list = []
    for row in matrix:
        print(list(row))
        matrix_list.append(list(row))
    return matrix_list

def generate_transform_matrix(pos, rot, average_position):
    def Rx(theta):
      return np.matrix([[ 1, 0            , 0            ],
                        [ 0, np.cos(theta),-np.sin(theta)],
                        [ 0, np.sin(theta), np.cos(theta)]])
    def Ry(theta):
      return np.matrix([[ np.cos(theta), 0, np.sin(theta)],
                        [ 0            , 1, 0            ],
                        [-np.sin(theta), 0, np.cos(theta)]])
    def Rz(theta):
      return np.matrix([[ np.cos(theta), -np.sin(theta), 0 ],
                        [ np.sin(theta), np.cos(theta) , 0 ],
                        [ 0            , 0             , 1 ]])

    R = Rz(rot[2]) * Ry(rot[1]) * Rx(rot[0])
    xf_rot = np.eye(4)
    xf_rot[:3,:3] = R

    xf_pos = np.eye(4)
    
    #xf_pos[:3,3] = pos - average_position
    xf_pos[:3,3] = pos
    # barbershop_mirros_hd_dense:
    # - camera plane is y+z plane, meaning: constant x-values
    # - cameras look to +x

    # Don't ask me...
    extra_xf = np.matrix([
        [-1, 0, 0, 0],
        [ 0, 0, 1, 0],
        [ 0, 1, 0, 0],
        [ 0, 0, 0, 1]])
    # NerF will cycle forward, so lets cycle backward.
    shift_coords = np.matrix([
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1]])
    xf = shift_coords @ extra_xf @ xf_pos
    assert np.abs(np.linalg.det(xf) - 1.0) < 1e-4
    xf = xf @ xf_rot
    return xf

avg_x = 0.0
avg_y = 0.0
avg_z = 0.0

num_objects = 0;

scene = bpy.context.scene
for ob in scene.objects:
    if ob.type == 'CAMERA':
        avg_x += ob.location[0]
        avg_y += ob.location[1]
        avg_z += ob.location[2]
        num_objects = num_objects + 1
        print(num_objects)

avg_pos = Vector((avg_x / num_objects, avg_y / num_objects, avg_z / num_objects))

out_data = {
    'camera_angle_x': bpy.data.objects['00000.jpeg'].data.angle_x,
    'camera_angle_y': bpy.data.objects['00000.jpeg'].data.angle_y
}
     
out_data['frames'] = []

scene = bpy.context.scene

for ob in scene.objects:
    if ob.type == 'CAMERA':
        print(ob.name)
        xf = generate_transform_matrix(ob.location, ob.rotation_euler, avg_pos)
        frame_data = {
            'file_path': "./images/" + ob.name,
            #'transform_matrix': listify_matrix(xf)
            'rotation' : 0.0,
            'transform_matrix': xf.tolist()
        }
        out_data['frames'].append(frame_data)

with open(fp + '/../' + 'transforms.json', 'w') as out_file:
    json.dump(out_data, out_file, indent=4)
    
print("DONE")