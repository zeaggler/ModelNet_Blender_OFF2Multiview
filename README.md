# BlenderPhong

A Blender python script to render an 3D model object by Phong Shading from several viewpoints.
We currently support **.obj**, **.stl**, and **.off** files.

This is an output from `airplane.off`:

<img src="https://img-blog.csdnimg.cn/20190312104505313.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2pvcmdfemhhbw==,size_16,color_FFFFFF,t_70" width="800">

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

```bash
"C:\Program Files\Blender Foundation\Blender\blender.exe" phong.blend --background --python phong.py -- .\\single_off_samples\\airplane_0001.off .\\single_samples_MV
```

Ubuntu:

```bash
blender phong.blend --background --python phong.py -- ./single_off_samples/airplane_0001.off ./single_samples_MV
```



### Multiple models

Win10:

```bash
"C:\Program Files\Blender Foundation\Blender\blender.exe" phong.blend --background --python phong.py -- dataset.txt .\dataset_samples_MV
```

Ubuntu:

```bash
blender phong.blend --background --python phong.py -- dataset.txt ./dataset_samples_MV
```
