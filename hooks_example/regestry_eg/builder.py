'''
调用注册类，然后进行注册
目前 Registry 类一共有 4 种用法，方便不同场景下注册。
'''
from hooks_example.regestry_eg.Registry import Registry, build_from_cfg
# 0. 先构建一个全局的 FRUIT、FOOD注册器类
FRUIT = Registry('fruit')
# Registry(name=food, items={})
FOOD = Registry('food')
CATS = Registry('cat')


def build(cfg, registry, default_args=None):
    '''返回类的一个实例'''
    return build_from_cfg(cfg, registry, default_args)


def build_fruit(cfg):
    return build(cfg, FRUIT)

#用装饰注册过的FOOD这里直接拿来使用，如果是默认值，可能就找不到
def build_food(cfg):
    return build(cfg, FOOD)

# 通过装饰器方式作用在想要加入注册器的具体类中
#===============================================================
# 1. 不需要传入任何参数，此时默认实例化的配置字符串是 str (类名)
#注册之后FOOD显示：Registry(name=food, items={'Rice': <class '__main__.Rice'>})
@FOOD.register_module()
class Rice():
    def __init__(self, name,taste):
        self.name = name
        self.taste = taste
class Rice1(Rice):
    def __init__(self):
        super(Rice1,self).__init__()
        self.r1='你好'

class Rice2(Rice):
    def __init__(self):
        super(Rice2,self).__init__()
        self.r2 = '我好'

@FOOD.register_module()
class Apple():
    def __init__(self, name):
        self.name = name

#通过get方法输入类名，返回类本身: food_cls=FOOD.get('Rice')
# 类实例话：food_instance=food_cls('my_name')
#调用实例属性：food_instance.name


@FRUIT.register_module()
class Apple():
    def __init__(self, name):
        self.name = name

# 2.传入指定 str，实例化时候只需要传入对应相同 str 即可
@CATS.register_module(name='Siamese')
class SiameseCat:
    pass
#返回类本身：cat_cls=CATS.get('Siamese')
# 类实例化:cat_instance=cat_cls()

# 3.如果出现同名 Registry Key，可以选择报错或者强制覆盖
# 如果指定了 force=True，那么不会报错
# 此时 Registry 的 Key 中，Siamese2Cat 类会覆盖 SiameseCat 类
# 否则会报错
@CATS.register_module(name='Siamese',force=True)
class Siamese2Cat:
    pass
# 类实例化:CATS.get('Siamese')(**args)

#注册多次之后
# CATS：Registry(name=cat, items={'Siamese': <class '__main__.Siamese2Cat'>, 'Munchkin': <class '__main__.Munchkin'>})
# 4. 可以直接注册类
class Munchkin:
    pass
CATS.register_module(Munchkin)

# 类实例化:CATS.get('Munchkin')(**args)

if __name__ == '__main__':
    pass