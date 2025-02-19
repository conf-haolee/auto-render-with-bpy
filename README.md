# auto-render-with-bpy

使用blender-python 自动渲染模拟出的密封圈下落场景图片

更新计划：
[TO DO](./TODO.md)

## 实例渲染图片展示

- 密集下落场景模拟文件：**fallRingsCircleSimulation.blend**

<div align="center"><img src=https://raw.githubusercontent.com/conf-haolee/Images/master/PicGoImg/202411201637695.png width=400px /></div>

- 自动渲染程序：**auto_render_torus_simulate_fall.py**

<div align="center"><img src=https://raw.githubusercontent.com/conf-haolee/Images/master/PicGoImg/202411201713357.png width=400px /></div>

- 渲染指定数量`labeled bmp`密封圈图片程序：**auto_render_torus_with_overlap.py**

<div align="center"><img src=https://raw.githubusercontent.com/conf-haolee/Images/master/PicGoImg/202411201721298.png width=400px /></div>



## 添加用户界面

<div align="center"><img src= https://raw.githubusercontent.com/conf-haolee/Images/master/PicGoImg/202502191032006.png width=600px /></div>




> 环境配置

`Python 3.11.9`
`blender 4.1`
`bpy-4.1.0-cp311-cp311-win_amd64.whl`

ui界面需要的环境：`pip install pyqt6`
`pip install pyqt6-tools`

官方软件下载
https://download.blender.org/release/Blender4.1/

bpy模块离线下载
https://pypi.tuna.tsinghua.edu.cn/simple/bpy/

pyqt6 入门参考

https://www.byhy.net/py/qt/qt_01/
