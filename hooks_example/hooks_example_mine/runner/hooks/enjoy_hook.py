from .hook import HOOKS, Hook

@HOOKS.register_module()
class EnjoyHook(Hook):

    def __init__(self, **kwargs):
        print('kwargs',kwargs)
        super(EnjoyHook, self).__init__(**kwargs)

    def before_run(self, runner):
        print('3.1享受之前要先学习')
        # print('runner is:',runner)
    def after_run(self, runner):
        print('3.2享受之后要开启新的一天')
        # print('runner is:',runner)