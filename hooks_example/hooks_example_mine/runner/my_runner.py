from .hooks import HOOKS, Hook
from  hooks_example.hooks_example_mine.utils import build_from_cfg
class MyRunner(object):
    '''
    1.Runner 对象初始化
    2.注册各类 Hook 到 Runner 中
    3.调用 Runner 的 resume 或者 load_checkpoint 方法对权重进行加载
    4.运行给定的工作流，此时才真正开启了工作流
    '''
    def __init__(self ):
        pass
        self._hooks = []

    def register_hook(self, hook):
        # 这里不做优先级判断，直接在头部插入HOOK
        self._hooks.insert(0, hook)
    def register_hook_from_cfg(self, hook_cfg):
        """Register a hook from its cfg.

        Args:
            hook_cfg (dict): Hook config. It should have at least keys 'type'
              and 'priority' indicating its type and priority.

        Notes:
            The specific hook class to register should not use 'type' and
            'priority' arguments during initialization.
        """
        hook = build_from_cfg(hook_cfg, HOOKS)
        self.register_hook(hook)

    #self就是MyRunner类的实例
    def call_hook(self, hook_name):
        for hook in self._hooks:
            #geattr获取属性，返回的是一个函数，输入参数调用函数显示结果
            getattr(hook, hook_name)(self)


    def register_exercise_hook(self,exercise_config):
        hook = build_from_cfg(exercise_config,HOOKS)
        self.register_hook(hook)

    def register_my_hook(self, exercise_config):
        self.register_exercise_hook(exercise_config)

    def run(self):
        print('开始启动我的一天')
        self.call_hook('before_run')
        self.call_hook('after_run')
        print('~~睡觉~~')
