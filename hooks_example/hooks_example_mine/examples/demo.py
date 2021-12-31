from hooks_example.hooks_example_mine.runner import MyRunner
'''
hook的设计思想，是做某件事时有个主流程，如1,2,3步骤，那么可以通过hooks实现，在每一步之前之后做或者不做一些事情
#train_epoch之前要做些操作
self.call_hook('before_train_epoch')
time.sleep(2)  # Prevent possible deadlock during epoch transition

#整个for循环是train_epoch操作
for i, data_batch in enumerate(self.data_loader):
    self._inner_iter = i
    #train_iter之前要做的事
    self.call_hook('before_train_iter')
    #train_iter
    self.run_iter(data_batch, train_mode=True, **kwargs)
    #train_iter之后要做的事
    self.call_hook('after_train_iter')
    self._iter += 1
# train_epoch之后要做些操作
self.call_hook('after_train_epoch')
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