from hooks_example.hooks_example_mine.runner import MyRunner
'''
cfg
Out[2]: {'type': 'Rice', 'name': '东北大米', 'taste': 'sweet'}
registry
Out[3]: Registry(name=food, items={'Rice': <class 'hooks_example.regestry_eg.builder.Rice'>, 'Apple': <class 'hooks_example.regestry_eg.builder.Apple'>})

'''
if __name__ == '__main__':
    exercise_config = dict(type='ExerciseHook',name = 'exercise')
    runner = MyRunner()
    runner.register_my_hook(exercise_config)
    runner.run()