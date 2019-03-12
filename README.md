# BlenderPhong

A Blender python script to render an 3D model object by Phong Shading from several viewpoints.
We currently support **.obj**, **.stl**, and **.off** files.

This is an output from `airplane.off`:

<img src="https://i.imgur.com/9Vq37vD.png" width="200">

We use [blender-off-addon](https://github.com/alextsui05/blender-off-addon) for off importing support.

## Requirements
 - [Blender](https://www.blender.org/)

## Usage
Because the blender install path is various with different OS,  you should assign the absolute install path for Blender in WIN10

### Run with Blender

```bash
<blender install path> phong.blend --background --python phong.py -- <model file> <output dir>
```

### Single .off 
Win10:

```python
"C:\Program Files\Blender Foundation\Blender\blender.exe" phong.blend --background --python phong.py -- .\\single_off_samples\\airplane_0001.off .\\single_samples_MV
```

Ubuntu:

```python
blender phong.blend --background --python phong.py -- ./single_off_samples/airplane_0001.off ./single_samples_MV
```



### Multiple models

Win10:

```python
"C:\Program Files\Blender Foundation\Blender\blender.exe" phong.blend --background --python phong.py -- dataset.txt .\dataset_samples_MV
```

Ubuntu:

```python
blender phong.blend --background --python phong.py -- dataset.txt ./dataset_samples_MV
```
