from .hook import HOOKS, Hook

@HOOKS.register_module()
class LearningHook(Hook):

    def __init__(self, **kwargs):
        print('kwargs',kwargs)
        super(LearningHook, self).__init__(**kwargs)

    def before_run(self, runner):
        print('学习前要先锻炼')
        print('runner is:',runner)
    def after_run(self, runner):
        print('学习后要去吃饭')
        print('runner is:',runner)