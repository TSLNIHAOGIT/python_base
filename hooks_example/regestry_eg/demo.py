'''
总逻辑：
1.builder构建全局的注册器类进行注册
2.返回类的实例进行调用
'''

from hooks_example.regestry_eg.builder import build_fruit, build_food
from hooks_example.regestry_eg.lunch import lunch
'''
lunch=dict(
    #注册Rice类
    food=dict(type='Rice', name='东北大米'),
    #注册Apple类
    fruit=dict(type='Apple', name='青苹果')
)
最终返回多个类的实例
'''
class COOKER():
    def __init__(self,food, fruit):
        print('今日饮食清单：{}, {}'.format(food, fruit))
        print(f'food:{food}')
        print(f'fruit:{fruit}')
        #build_food(food)返回的是类的实例，可以调用类的相关属性和方法
        self.food = build_food(food)
        self.fruit = build_fruit(fruit)
    def run(self):
        print('具体饮食计划')
        print('主食吃: {}'.format(self.food.name))
        print('水果吃: {}'.format(self.fruit.name))
if __name__ == '__main__':
    cook = COOKER(**lunch)
    cook.run()