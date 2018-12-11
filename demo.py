# -*-coding:utf-8-*-
import random


a = [[1, 2], [3, 4]]
b = [1, 2, 3, 4]
c = max(max(a, key=lambda x: max(x)))
print(random.sample(b, 2))