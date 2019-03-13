# BlenderPhong
First, thanks for the work of weitang, this code is revised from https://github.com/WeiTang114/BlenderPhong.

---
中文博客地址：
https://blog.csdn.net/jorg_zhao/article/details/86309774
https://blog.csdn.net/jorg_zhao/article/details/88345324
---

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
The followings are examples, you should change the absolute blender install path in win10.

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
