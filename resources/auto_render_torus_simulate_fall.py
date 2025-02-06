"""
    模拟环体下落过程，自动渲染环体下落时的图片
    v2 更新: 
        1. 添加 环体随机形变
        2. 物体重命名
    time: 2024/11/11
    auther: haolee
"""
import bpy
from datetime import datetime
import math
import random

# 清除默认场景中的所有对象
# bpy.ops.object.delete(use_global=False, confirm=False) #del 
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# step1 新建一个环体 并设置属性
bpy.ops.mesh.primitive_torus_add(
    align='WORLD', 
    location=(0, 0, 10),                        # 位置 XYZ
    rotation=(0, math.radians(90), 0),          # 旋转 XYZ  
    major_radius=0.5,                           # 圆环体内圆半径
    minor_radius=0.2,                           #环半径
    # major_segments=1000,            # 设置主环段数
    # minor_segments=100,             # 辅环段数
    # abso_major_rad=10,              #  通过外圆半径内圆半径定义环体  外圆半径
    # abso_minor_rad=5                #  内圆半径
    )
bpy.context.object.name = "torus"

bpy.ops.object.shade_smooth()       #平滑着色
# 为环体添加修改器， [0]-简易形变
#bpy.context.space_data.context = 'MODIFIER'
bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
bpy.context.object.modifiers[0].deform_axis = 'X'
select_torus = bpy.context.object                         # 记录当前环体
bpy.context.object.modifiers[0].angle = math.radians(10)  # rad(10)
# 设置橡胶圈材质
for material in bpy.data.materials:            # 首先清除所有材质
    bpy.data.materials.remove(material)
 # create material 
bpy.ops.material.new()
rubberRing_material = bpy.data.materials[-1]   # 获取最新创建的材质
#  nodes[0] -- nodes["原理化BSDF"]
# HSV 设置基础色 (色相 饱和度 明度 alpha) 通过调整明度可调整密封圈灰度值
rubberRing_material.node_tree.nodes[0].inputs[0].default_value = (0.1, 0.1, 0.1, 1)  
# 设置材质金属度 范围[0.1]
rubberRing_material.node_tree.nodes[0].inputs[1].default_value = 0.0942623  
# apply light_material  应用材质
bpy.context.active_object.data.materials.append(rubberRing_material)

# step2 新建一个平面背光 
bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(-3, 0, 6), rotation=(3.14159, -1.5708, 0), scale=(2.4, 4.0, 1.0))
bpy.context.object.name = "backlight_face"
bpy.context.object.scale[0] = 2.4
bpy.context.object.scale[1] = 4
# 新建一个发光材质
#bpy.context.space_data.context = 'MATERIAL'
bpy.ops.material.new()
light_material = bpy.data.materials[-1]
light_material.node_tree.nodes[0].inputs[27].default_value = 50     # 设置平面的自发光强度  亮度低会影响渲染背景不够白
# 应用自发光的材质
bpy.context.active_object.data.materials.append(light_material)

# step3 新建摄像机
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(6, 0, 6), rotation=(1.5708, 0, 1.5708), scale=(1, 1, 1))
bpy.context.object.name = "camera"
bpy.context.object.data.lens = 80                   #摄像机焦距

# step4 新建一个平面为其设置粒子系统，模拟环体下落过程
bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 8), scale=(1, 1, 1))
bpy.context.object.name = "particle_face"
bpy.context.object.scale[0] = -0.26                             # 缩放 X
bpy.context.object.scale[1] = -0.8                              # 缩放 Y
bpy.context.object.scale[2] = -2.6                              # 缩放 Z
# set particle system 粒子系统设置
for particle in bpy.data.particles:
    bpy.data.particles.remove(particle)
bpy.ops.object.particle_system_add()
bpy.data.particles[-1].count = 100                               # 环体下落数量
bpy.data.particles[-1].frame_start = 10                         # 发射起始帧
bpy.data.particles[-1].frame_end = 20                           # 发射结束
bpy.data.particles[-1].lifetime = 20                            # 生命周期

bpy.data.particles[-1].render_type = 'OBJECT'                   # 设置粒子系统渲染为 物体
bpy.data.particles[-1].instance_object = bpy.data.objects[3]    # 选择渲染的实例物体 环体
bpy.data.particles[-1].use_rotations = True                     # 旋转开启，
bpy.data.particles[-1].rotation_factor_random = 0.8             # 旋转开启，设置随机值范围[0,1]
bpy.data.particles[-1].use_rotation_instance = True             # 设置物体旋转  开启
bpy.data.particles[-1].particle_size = 0.5                      # 渲染物体的缩放设置
bpy.data.particles[-1].distribution = 'RAND'                    # 随机分布
bpy.data.particles[-1].use_scale_instance = False               # 物体缩放
#rand = random.randint(0,100)                                    # 生成一个随机数
#bpy.context.object.particle_systems[-1].seed = rand             # 设置一个随机种子

# step5 渲染格式设置
scene = bpy.context.scene
scene.render.resolution_x = 4096                     # 输出图片的分辨率 X*Y  4k 4096*2048
scene.render.resolution_y = 2048
scene.render.image_settings.file_format = 'BMP'     # 保存格式为BMP
scene.render.fps = 6                                # 设置渲染fps = 6
scene.frame_start = 1                               # 起始帧
scene.frame_end = 30                                # 结束帧
scene.render.image_settings.color_mode = 'BW'       # 输入：黑白图片渲染

for renderTimes in range(1,3):
    rand_deform = random.randint(-60,60)                            # 生成随机形变值
    select_torus.modifiers[0].angle = math.radians(rand_deform)     # rad(10)
    
    rand = random.randint(0,100)                                    # 生成一个随机数
    bpy.context.object.particle_systems[-1].seed = rand             # 设置一个随机种子
    scene.camera = bpy.data.objects['camera']
    for frame_i in range(1,30):
        bpy.context.scene.frame_set(frame_i)            # 切换到第30帧
        bpy.ops.render.render() 
        if frame_i is 20:                               #  保存第20帧图像
            currentTime = datetime.now().strftime("%Y%m%d %H%M")
            save_bmp = "D:/GXNU/blenderToBmp/BmpData/" + currentTime + "_Render" + "/" + currentTime + "_" + str(renderTimes) + ".bmp"
            bpy.data.images["Render Result"].save_render(save_bmp)              # 保存渲染图片