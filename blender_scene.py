
import bpy
from datetime import datetime
import math
import random

class BlenderScene:


    def __init__(self):
        pass
        print("构造函数")
    pass
    
    def build_scene():
        '''
    参数设置列表
'''
max_torus_num = 5                       # 创建的环体数量
render_pic_num = 10000                # 渲染的图片数量
max_deform = 60                     # 设置最大形变值

for torus_num_i in range(1,(max_torus_num-1)):
    # 清除默认场景中的所有对象
    # bpy.ops.object.delete(use_global=False, confirm=False) #del 
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    select_torus = []                       # 存储每个环体对象的列表
    # step1 新建环体 并设置属性
    for torus_index in range(0, torus_num_i):
        bpy.ops.mesh.primitive_torus_add(
            align='WORLD', 
            location=(0, -0.8, 6.8),                    # 位置 XYZ
            rotation=(0, math.radians(90), 0),          # 旋转 XYZ  
            major_radius=0.5,                 # 圆环体内圆半径
            minor_radius=0.2,                 #环半径
            # major_segments=1000,            # 设置主环段数
            # minor_segments=100,             # 辅环段数
            # abso_major_rad=10,              #  通过外圆半径内圆半径定义环体  外圆半径
            # abso_minor_rad=5                #  内圆半径
            )
        bpy.context.object.scale[0] = 0.5       # 缩放X 
        bpy.context.object.scale[1] = 0.5       # 缩放Y 
        bpy.context.object.scale[2] = 0.5       # 缩放Z
        bpy.context.object.name = "torus_" + str(torus_index)       # 重命名环体    
        bpy.ops.object.shade_smooth()       #平滑着色
        
        # 为环体添加修改器， [0]-简易形变
        #bpy.context.space_data.context = 'MODIFIER'
        bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
        bpy.context.object.modifiers[0].deform_axis = 'X'
        bpy.context.object.modifiers[0].angle = math.radians(0)  # rad(10)
        select_torus.append(bpy.context.object)                        # 记录当前环体
        if torus_index == 0:
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

    # step4 渲染格式设置
    scene = bpy.context.scene
    scene.render.resolution_x = 512                     # 输出图片的分辨率 X*Y  4k 4096*2048
    scene.render.resolution_y = 512
    scene.render.image_settings.file_format = 'BMP'     # 保存格式为BMP
    #scene.render.fps = 6                                # 设置渲染fps = 6
    #scene.frame_start = 1                               # 起始帧
    #scene.frame_end = 30                                # 结束帧
    scene.render.image_settings.color_mode = 'BW'       # 输入：黑白图片渲染

    for renderTimes in range(1,render_pic_num + 1):
        
        for torus_index in range(0,torus_num_i):  
            rand_move_x = 0
            rand_y = random.randint(-100,100) / 100                 # 在整个相机视野 生成随机位置
            rand_z = random.randint(500,700) / 100
            select_torus[torus_index].location[0] = 0
            select_torus[torus_index].location[1] = rand_y
            select_torus[torus_index].location[2] = rand_z
            
            rand_deform = random.randint((-1 * max_deform),max_deform)                            # 生成随机形变值
            select_torus[torus_index].modifiers[0].angle = math.radians(rand_deform)     # 应用形变
            
            rand_rotation_x = random.randint(0,360)                         # 生成随机旋转值 X
            rand_rotation_y = random.randint(0,360)                         # 生成随机旋转值 Y
            rand_rotation_z = random.randint(0,360)                         # 生成随机旋转值 Z 
            select_torus[torus_index].rotation_euler[0] = math.radians(rand_rotation_x)  # 应用旋转
            select_torus[torus_index].rotation_euler[1] = math.radians(rand_rotation_y)
            select_torus[torus_index].rotation_euler[2] = math.radians(rand_rotation_z)
        # s
        scene.camera = bpy.data.objects['camera']                       # 设置相机
        bpy.ops.render.render()                                         # 开始渲染图片
        currentTime = datetime.now().strftime("%Y%m%d %H%M")
        save_bmp = "E:/workspace/haolee/blender_bmp/03 render_bmp/circle_" + str(torus_num_i) + "/"  + currentTime + "_" + str(renderTimes) + ".bmp"
        bpy.data.images["Render Result"].save_render(save_bmp)          # 保存渲染图片

