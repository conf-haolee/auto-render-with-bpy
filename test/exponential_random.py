import numpy as np
import matplotlib.pyplot as plt

def generate_exponential_random_numbers(size=1000, scale=2):
    """
    生成符合指数概率分布的随机数，使得靠近 1 的数值指数变多
    :param size: 生成的随机数个数
    :param scale: 控制指数分布的衰减速率 (λ = 1/scale)
    :return: np.array 随机数
    """
    exp_samples = np.random.exponential(scale=scale, size=size)  # 生成指数分布数据
    exp_samples = 3 * (1 - exp_samples / 50) # 归一化到 (0, 1)
    return exp_samples  # 翻转，使得靠近 1 的数值更多

# 生成 100 个符合要求的随机数
random_numbers = generate_exponential_random_numbers(size=1000)
for i in range(20):
    print(random_numbers[i])

# 绘制直方图
plt.hist(random_numbers, bins=30, density=True, alpha=0.7, color='blue')
plt.xlabel("Random Value")
plt.ylabel("Density")
plt.title("Exponentially Distributed Random Numbers (Closer to 1)")
plt.show()
