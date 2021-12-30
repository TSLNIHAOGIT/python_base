import inspect
class Registry(object):
    #初始化name是什么组件,组件里面是一个dict,保存name跟它的具体类
    def __init__(self, name):
        self._name = name
        self._module_dict = dict()

    def __repr__(self):
        format_str = self.__class__.__name__ + '(name={}, items={})'.format(
            self._name, list(self._module_dict.keys()))
        return format_str

    @property
    def name(self):
        return self._name

    @property
    def module_dict(self):
        return self._module_dict

    def get(self, key):
        return self._module_dict.get(key, None)

    #把组件类与类名注册到注册表中,方便从config文件构建类
    def _register_module(self, module_class):
        """Register a module.

        Args:
            module (:obj:`nn.Module`): Module to be registered.
        """
        if not inspect.isclass(module_class):
            raise TypeError('module must be a class, but got {}'.format(
                type(module_class)))
        module_name = module_class.__name__
        if module_name in self._module_dict:
            raise KeyError('{} is already registered in {}'.format(
                module_name, self.name))
        self._module_dict[module_name] = module_class

    def register_module(self, cls):
        '''

        :param cls: 代表类本身
        :return:
        '''
        self._register_module(cls)
        return cls

BACKBONES = Registry('backbone')

@BACKBONES.register_module
class ResNet():
    def __init__(self):
        pass
    def my_log(self):
        print('my resnet')
    pass
if __name__ == '__main__':

    pass