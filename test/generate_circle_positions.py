import numpy as np
import matplotlib.pyplot as plt

def generate_circle_positions(radius, xlim=(-10, 10), ylim=(-10, 10)):
    """
    生成两个相交或相切的圆的圆心坐标，并确保它们不会超出边界
    """
    # 确保第一个圆心不会靠近边界，以便第二个圆仍在范围内
    x1_min, x1_max = xlim[0] + radius, xlim[1] - radius
    y1_min, y1_max = ylim[0] + radius, ylim[1] - radius
    
    while True:
        # 随机生成第一个圆心坐标
        x1 = np.random.uniform(x1_min, x1_max)
        y1 = np.random.uniform(y1_min, y1_max)

        # 生成圆心距离 d，确保 0 < d ≤ 2r
        d = np.random.uniform(0.1, 2 * radius)  

        # 生成随机角度 θ
        theta = np.random.uniform(0, 2 * np.pi)

        # 计算第二个圆心坐标
        x2 = x1 + d * np.cos(theta)
        y2 = y1 + d * np.sin(theta)

        # 确保第二个圆心仍然在范围内
        if (xlim[0] + radius <= x2 <= xlim[1] - radius) and (ylim[0] + radius <= y2 <= ylim[1] - radius):
            return (x1, y1), (x2, y2)

def plot_circles(center1, center2, radius, xlim=(-10, 10), ylim=(-10, 10)):
    """
    绘制两个相交或相切的圆
    """
    fig, ax = plt.subplots()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')

    # 绘制圆
    circle1 = plt.Circle(center1, radius, color='blue', fill=False, linewidth=2)
    circle2 = plt.Circle(center2, radius, color='red', fill=False, linewidth=2)
    ax.add_patch(circle1)
    ax.add_patch(circle2)

    # 绘制圆心
    ax.plot(*center1, 'bo', label="Center 1")
    ax.plot(*center2, 'ro', label="Center 2")

    # 显示
    plt.legend()
    plt.grid(True)
    plt.show()

# 设定半径
r = 3
center1, center2 = generate_circle_positions(r, xlim=(-10, 10), ylim=(-10, 10))
plot_circles(center1, center2, r, xlim=(-10, 10), ylim=(-10, 10))
