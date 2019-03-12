'''**********************************************************************************
THANKS for the work from WeiTang114 (Github:https://github.com/WeiTang114/BlenderPhong)
The original Blender python script has been rewritten.
Allows one to input path of single .off file or dataset.txt

      The python script is written in Win10

##################################################
Usage:
######### input single .off file path ############
Win10:
    "C:\\Program Files\\Blender Foundation\\Blender\\blender.exe" phong.blend --background --python phong.py -- .\\single_off_samples\\airplane_0001.off .\\single_samples_MV
Ubuntu:
    blender phong.blend --background --python phong.py -- ./single_off_samples/airplane_0001.off ./single_samples_MV
######### input dataset.txt file path ############
Win10:
    "C:\\Program Files\\Blender Foundation\\Blender\\blender.exe" phong.blend --background --python phong.py -- dataset.txt .\\dataset_samples_MV
Ubuntu:
    blender phong.blend --background --python phong.py -- dataset.txt ./dataset_samples_MV
##################################################

Parameters needs to be changed:
1. line 48&49 output image size 'w' and 'h'
2. line 164 xx.split('\\') -> '\\' for win10, '/' for ubuntu
3. command: the path of blender.exe should be changed as needed
**********************************************************************************'''

import bpy
import os.path
import math
import sys

C = bpy.context
D = bpy.data
scene = D.scenes['Scene']

# cameras: a list of camera positions
# a camera position is defined by two parameters: (theta, phi),
# where we fix the "r" of (r, theta, phi) in spherical coordinate system.

# 5 orientations: front, right, back, left, top
# cameras = [(60, 0), (60, 90), (60, 180), (60, 270),(0, 0)]

# multiview  with inter-deg elevation
fixed_view = 60
inter = 30
cameras = [(fixed_view, i) for i in range(0, 360, inter)] # output 12(360/30=12) multiview images

render_setting = scene.render

# output image size = (W, H)
w = 224
h = 224
render_setting.resolution_x = w*2
render_setting.resolution_y = h*2


'''****************************************************************'''
def main():
    argv = sys.argv
    argv = argv[argv.index('--') + 1:]

    if len(argv) != 2:
        print('phong.py args: <3d mesh path> <image dir>')
        exit(-1)

    model_path = argv[0]    # input: path of single .off or dataset.txt
    image_dir = argv[1]     	# input: path to save multiview images

    # blender has no native support for off files
    install_off_addon()
    init_camera()
    fix_camera_to_origin()

    '''*************************************************'''
    if model_path.split('.')[-1] == 'off':
        print('model path is ********', model_path) # model_path:'./airplane.off'
        do_model(model_path, image_dir)
    elif model_path.split('.')[-1] == 'txt':
        with open(model_path) as f:
            models = f.read().splitlines()
        for model in models:
            print('model path is ********', model) # model_path:'F:\DATA3D\ModelNet10\monitor\train\monitor_0003.off'
            do_model(model, image_dir)
    else:
        print('......Please input correct parameters......')
        exit(-1)
'''****************************************************************'''


def install_off_addon():
    try:
        bpy.ops.wm.addon_install(
            overwrite=False,
            filepath=os.path.dirname(__file__) +
            '/blender-off-addon/import_off.py'
        )
        bpy.ops.wm.addon_enable(module='import_off')
    except Exception:
        print("""Import blender-off-addon failed.
              Did you pull the blender-off-addon submodule?
              $ git submodule update --recursive --remote
              """)
        exit(-1)


def init_camera():
    cam = D.objects['Camera']
    # select the camera object
    scene.objects.active = cam
    cam.select = True

    # set the rendering mode to orthogonal and scale
    C.object.data.type = 'ORTHO'
    C.object.data.ortho_scale = 2.


def fix_camera_to_origin():
    origin_name = 'Origin'

    # create origin
    try:
        origin = D.objects[origin_name]
    except KeyError:
        bpy.ops.object.empty_add(type='SPHERE')
        D.objects['Empty'].name = origin_name
        origin = D.objects[origin_name]

    origin.location = (0, 0, 0)

    cam = D.objects['Camera']
    scene.objects.active = cam
    cam.select = True

    if 'Track To' not in cam.constraints:
        bpy.ops.object.constraint_add(type='TRACK_TO')

    cam.constraints['Track To'].target = origin
    cam.constraints['Track To'].track_axis = 'TRACK_NEGATIVE_Z'
    cam.constraints['Track To'].up_axis = 'UP_Y'


def do_model(model_path, image_dir):
    # model_path= 'F:\\DATA3D\ModelNet10_MV\\bathtub\\train\\bathtub_0003.off'
    # image_dir = 'F:\\DATA3D\\ModelNet10_MV_32_train\\'
    name = load_model(model_path) # -> name = 'bathtub_0003'
    center_model(name)
    normalize_model(name)

    image_subdir = os.path.join(image_dir, name.split('_')[0], name) # path: image_dir\\bathtub\\bathtub_0003
    for i, c in enumerate(cameras):
        move_camera(c)
        render()
        save(image_subdir, '%s_%d' % (name, i))

    delete_model(name)


def load_model(model_path):
    # single .off: model_path='./airplane.off'
    # dataset.txt: model_path= 'F:\\DATA3D\ModelNet10_MV\\bathtub\\train\\bathtub_0003.off'
    d = os.path.dirname(model_path) # invalide for .off file
    ext = model_path.split('.')[-1] # ext: 'off'

    # Attention!  win10: ..path.split('\\')  linux: ..path.split('/')
    _model_path_tmp = model_path.split('\\')[-1] # _model_path_tmp: 'bathtub_0003.off'
    name = os.path.basename(_model_path_tmp).split('.')[0] # bathtub_0003
    # handle weird object naming by Blender for stl files
    if ext == 'stl':
        name = name.title().replace('_', ' ')

    if name not in D.objects:
        print('loading :' + name)
        if ext == 'stl':
            bpy.ops.import_mesh.stl(filepath=model_path, directory=d,
                                    filter_glob='*.stl')
        elif ext == 'off':
            bpy.ops.import_mesh.off(filepath=model_path, filter_glob='*.off')
        elif ext == 'obj':
            bpy.ops.import_scene.obj(filepath=model_path, filter_glob='*.obj')
        else:
            print('Currently .{} file type is not supported.'.format(ext))
            exit(-1)
    return name # name='airplane' -> 'bathtub_0003'


def delete_model(name):
    for ob in scene.objects:
        if ob.type == 'MESH' and ob.name.startswith(name):
            ob.select = True
        else:
            ob.select = False
    bpy.ops.object.delete()


def center_model(name):
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
    D.objects[name].location = (0, 0, 0)


def normalize_model(name):
    obj = D.objects[name]
    dim = obj.dimensions
    print('original dim:' + str(dim))
    if max(dim) > 0:
        dim = dim / max(dim)
    obj.dimensions = dim

    print('new dim:' + str(dim))


def move_camera(coord):
    def deg2rad(deg):
        return deg * math.pi / 180.

    r = 3.
    theta, phi = deg2rad(coord[0]), deg2rad(coord[1])
    loc_x = r * math.sin(theta) * math.cos(phi)
    loc_y = r * math.sin(theta) * math.sin(phi)
    loc_z = r * math.cos(theta)

    D.objects['Camera'].location = (loc_x, loc_y, loc_z)


def render():
    bpy.ops.render.render()


def save(image_dir, name):
    path = os.path.join(image_dir, name + '.png')
    D.images['Render Result'].save_render(filepath=path)
    print('save to ' + path)


if __name__ == '__main__':
    main()
