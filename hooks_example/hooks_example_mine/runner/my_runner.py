from .hooks import HOOKS, Hook
from  ..utils import build_from_cfg
from .priority import Priority, get_priority
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
    def register_hook(self, hook, priority='NORMAL'):
        """Register a hook into the hook list.

        The hook will be inserted into a priority queue, with the specified
        priority (See :class:`Priority` for details of priorities).
        For hooks with the same priority, they will be triggered in the same
        order as they are registered.

        Args:
            hook (:obj:`Hook`): The hook to be registered.
            priority (int or str or :obj:`Priority`): Hook priority.
                Lower value means higher priority.
        """
        assert isinstance(hook, Hook)
        if hasattr(hook, 'priority'):
            raise ValueError('"priority" is a reserved attribute for hooks')
        priority = get_priority(priority)
        hook.priority = priority
        # insert the hook to a sorted list
        inserted = False
        for i in range(len(self._hooks) - 1, -1, -1):
            if priority >= self._hooks[i].priority:
                self._hooks.insert(i + 1, hook)
                inserted = True
                break
        if not inserted:
            self._hooks.insert(0, hook)

    # def register_hook(self, hook):
    #     # 这里不做优先级判断，直接在头部插入HOOK
    #     # self._hooks.insert(0, hook)
    #     self._hooks.append(hook)
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
    def register_learning_hook(self,learning_config):
        hook = build_from_cfg(learning_config,HOOKS)
        self.register_hook(hook)
    def register_my_hook(self, exercise_config,learning_config):
        self.register_exercise_hook(exercise_config)
        self.register_learning_hook(learning_config)
        # self.register_other_hook(other_config)

    def register_my_hook_auto(self, **params_config):
        for name ,data_config in params_config.items():
            hook = build_from_cfg(data_config, HOOKS)
            self.register_hook(hook,priority=data_config['priority'])

    def run(self):
        print('开始启动我的一天')
        #执行所有hooks实例中的before_run方法
        self.call_hook('before_run')
        # 执行所有hooks实例中的after_run方法
        self.call_hook('after_run')
        print('~~睡觉~~')
