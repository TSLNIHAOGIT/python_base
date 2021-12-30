from .hook import HOOKS, Hook

@HOOKS.register_module()
class ExerciseHook(Hook):

    def __init__(self, **kwargs):
        super(ExerciseHook, self).__init__(**kwargs)

    def before_run(self, runner):
        print('锻炼前要休息好')
        print('runner is:',runner)
    def after_run(self, runner):
        print('锻炼后要放松身体')
        print('runner is:',runner)