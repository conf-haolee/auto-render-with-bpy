import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

mu = 0  # 均值
sigma = 15  # 标准差

# 生成正态分布随机数
samples_normal = np.random.normal(mu, sigma, 10000)

# 绘制正态分布的概率密度函数图形
x_normal = np.linspace(0, 100, 500)  # x轴范围
y_normal = norm.pdf(x_normal, mu, sigma)  # 计算概率密度函数值

# 绘制直方图: 箱子数 概率密度 透明度
plt.hist(samples_normal, bins=50, density=True, alpha=0.5, label='Generated Samples')
plt.plot(x_normal, y_normal, color='red', label='PDF')
plt.xlabel('x')
plt.ylabel('Probability Density')
plt.title('Normal Distribution')
plt.legend()
plt.show()
