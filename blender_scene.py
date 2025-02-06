import bpy
from datetime import datetime
import math
import random
import numpy as np

class BlenderScene:

    def __init__(self, max_torus_num = 2, render_pic_num = 2, max_deform = 10, outer_radius = 0, inner_radius = 0, save_image_folder_path = ""):
        '''
            参数列表：
            max_torus_num = 2                       # 创建的环体数量
            render_pic_num = 10                # 渲染的图片数量
            max_deform = 60                     # 设置最大形变值
            outer_radius = 0
        '''
        self._max_torus_num = max_torus_num
        self._render_pic_num = render_pic_num
        self._max_deform = max_deform
        self._outer_radius = outer_radius
        self.inner_radius = inner_radius
        self._save_image_folder_path = save_image_folder_path
    
    # python 的getter 和 setter方法
    # 设置环体数量
    @property 
    def max_torus_num(self):
        return self._max_torus_num
    @max_torus_num.setter
    def max_torus_num(self, max_torus_num):
        self._max_torus_num = max_torus_num
    # 设置渲染图片数量
    @property
    def render_pic_num(self):
        return self._render_pic_num
    @render_pic_num.setter
    def render_pic_num(self, render_pic_num):
        self._render_pic_num = render_pic_num
    # 设置最大形变值
    @property
    def max_deform(self):
        return self._max_deform
    @max_deform.setter
    def max_deform(self, max_deform):
        self._max_deform = max_deform
    # 设置外径
    @property
    def outer_radius(self):
        return self._outer_radius
    @outer_radius.setter
    def outer_radius(self, outer_radius):
        self._outer_radius = outer_radius
    # 设置内径
    @property
    def inner_radius(self):
        return self._inner_radius
    @outer_radius.setter
    def inner_radius(self, inner_radius):
        self._inner_radius = inner_radius

    # 设置保存图片的文件夹路径
    @property
    def save_image_folder_path(self):
        return self._save_image_folder_path
    @save_image_folder_path.setter
    def save_image_folder_path(self, save_image_folder_path):
        self._save_image_folder_path = save_image_folder_path

    # 运行渲染
    def blender_render(self):
        # 清除默认场景中的所有对象
        for torus_num_i in range(1,(self._max_torus_num + 1)):
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete()

            # 计算环体的半径  1 / 375 是一个计算的标定系数
            calc_major_radius = (self._outer_radius + self._inner_radius) / 375
            calc_minor_radius = (self._outer_radius - self._inner_radius) / 375

            select_torus = []                       # 存储每个环体对象的列表
            # step1 新建环体  遍历每个环体并设置属性
            for torus_index in range(0, torus_num_i):
                bpy.ops.mesh.primitive_torus_add(
                align='WORLD', 
                location=(0, -0.8, 6.8),            # 位置 XYZ
                rotation=(0, math.radians(90), 0),        # 旋转 XYZ  
                major_radius= calc_major_radius,               # 圆环体内圆半径  major_radius + minor_radius= 圆环外径; major_radius - minor_radius= 圆环内径
                minor_radius= calc_minor_radius,               #环半径
                )
                bpy.context.object.name = "torus_" + str(torus_index)       # 重命名环体
                bpy.ops.object.shade_smooth()       #平滑着色

                # 为环体添加修改器， [0]-简易形变
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
            #   新建一个发光材质
            bpy.ops.material.new()
            light_material = bpy.data.materials[-1]
            light_material.node_tree.nodes[0].inputs[27].default_value = 50     # 设置平面的自发光强度  亮度低会影响渲染背景不够白
            #   应用自发光的材质
            bpy.context.active_object.data.materials.append(light_material)

            # step3 新建摄像机
            bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(6, 0, 6), rotation=(1.5708, 0, 1.5708), scale=(1, 1, 1))
            bpy.context.object.name = "camera"
            bpy.context.object.data.lens = 80                   #摄像机焦距


            # step5 渲染格式设置
            scene = bpy.context.scene
            scene.render.resolution_x = 512                     # 输出图片的分辨率 X*Y  4k 4096*2048
            scene.render.resolution_y = 512
            scene.render.image_settings.file_format = 'BMP'     # 保存格式为BMP
            scene.render.image_settings.color_mode = 'BW'       # 输入：黑白图片渲染

            for renderTimes in range(1,self._render_pic_num + 1):
                for torus_index in range(0,torus_num_i):  
                    rand_move_x = 0
                    # 模拟随机位置 在整个相机视野 生成随机位置 
                    rand_y = random.randint(-100,100) / 100                 
                    rand_z = random.randint(500,700) / 100
                    select_torus[torus_index].location[0] = 0
                    select_torus[torus_index].location[1] = rand_y
                    select_torus[torus_index].location[2] = rand_z
                    # 模拟随机形变  check： 随机形变改成高斯概率 形变
                    mu = 0  # 均值
                    sigma = self._max_deform / 3  # 标准差 3 sigma 概率分布达到 0.9974
                    # 生成正态分布随机数
                    normal_distribution = np.random.normal(mu, sigma, 1)
                    # rand_deform = random.randint((-1 * self._max_deform),self._max_deform)                  # 生成随机形变值
                    select_torus[torus_index].modifiers[0].angle = math.radians(normal_distribution[0])     # 应用形变
                    # 模拟随机旋转
                    rand_rotation_x = random.randint(0,360)                         # 生成随机旋转值 X
                    rand_rotation_y = random.randint(0,360)                         # 生成随机旋转值 Y
                    rand_rotation_z = random.randint(0,360)                         # 生成随机旋转值 Z 
                    select_torus[torus_index].rotation_euler[0] = math.radians(rand_rotation_x)  # 应用旋转
                    select_torus[torus_index].rotation_euler[1] = math.radians(rand_rotation_y)
                    select_torus[torus_index].rotation_euler[2] = math.radians(rand_rotation_z)
                scene.camera = bpy.data.objects['camera']
                bpy.ops.render.render() 
                current_data = datetime.now().strftime("%Y%m%d %H%M")
                current_time = datetime.now().strftime("%Y%m%d %H%M%S")
                # self.save_image_folder_path
                # save_bmp = "D:/workspace/" + currentTime + "_Render" + "/" + currentTime + "_" + str(renderTimes) + ".bmp"
                save_bmp = self._save_image_folder_path + "/" + current_data + "_Render" + "/" + "num_" + str(torus_num_i) + "/" + current_time + "_" + str(renderTimes) + ".bmp"
                bpy.data.images["Render Result"].save_render(save_bmp)              # 保存渲染图片
        

    