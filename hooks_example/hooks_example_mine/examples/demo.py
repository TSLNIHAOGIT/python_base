from hooks_example.hooks_example_mine.runner import MyRunner
'''
cfg
Out[2]: {'type': 'Rice', 'name': '东北大米', 'taste': 'sweet'}
registry
Out[3]: Registry(name=food, items={'Rice': <class 'hooks_example.regestry_eg.builder.Rice'>, 'Apple': <class 'hooks_example.regestry_eg.builder.Apple'>})

'''
if __name__ == '__main__':
    #类的名称和初始化参数
    params_config = dict(
        exercise_config=dict(type='ExerciseHook',name = 'exercise',priority='NORMAL'),
        learning_config=dict(type='LearningHook', name='learning',priority='HIGHEST'),
        enjoy_config=dict(type='EnjoyHook', name='enjoy', priority='HIGH')
    )

    runner = MyRunner()
    # runner.register_my_hook(**params_config)
    runner.register_my_hook_auto(**params_config)
    runner.run()