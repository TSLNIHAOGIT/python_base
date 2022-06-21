from hooks_example.hooks_example_mine.runner import MyRunner
'''
hook的设计思想，是做某件事时有个主流程，如1,2,3步骤，那么可以通过hooks实现，在每一步之前之后做或者不做一些事情
但是在没有主流程的情况下，可以自己按照优先级决定运行哪些模块

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
    #type='ExerciseHook'类的名称和初始化参数name = 'exercise'
    '''
      如果配置文件中是一个类里面还有小类，那么用法是进行组合：小类的实例返回给大类，大类里面可以调用小类的方法
    大的逻辑为：
    1.定义一个个需要的类
    2.通过hooks注册机制，以及config参数，来决定掉用某些类的先后顺序，并传入相应的参数
  
    
    '''
    params_config = dict(
        exercise_config=dict(type='ExerciseHook',name = 'exercise',priority='NORMAL'),
        # learning_config=dict(type='LearningHook', name='learning',priority='HIGH'),
        enjoy_config=dict(type='EnjoyHook', name='enjoy', priority='HIGHEST')
    )

    runner = MyRunner()
    # runner.register_my_hook(**params_config)
    runner.register_my_hook_auto(**params_config)
    runner.run()