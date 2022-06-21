import sys
class HOOK:

    def before_breakfirst(self, runner):
        print('{}:吃早饭之前晨练30分钟'.format(sys._getframe().f_code.co_name))

    def after_breakfirst(self, runner):
        print('{}:吃早饭之前晨练30分钟'.format(sys._getframe().f_code.co_name))

    def before_lunch(self, runner):
        print('{}:吃午饭之前跑上实验'.format(sys._getframe().f_code.co_name))

    def after_lunch(self, runner):
        print('{}:吃完午饭午休30分钟'.format(sys._getframe().f_code.co_name))

    def before_dinner(self, runner):
        print('{}: 没想好做什么'.format(sys._getframe().f_code.co_name))

    def after_dinner(self, runner):
        print('{}: 没想好做什么'.format(sys._getframe().f_code.co_name))

    def after_finish_work(self, runner, are_you_busy=False):
        if are_you_busy:
            print('{}:今天事贼多，还是加班吧'.format(sys._getframe().f_code.co_name))
        else:
            print('{}:今天没啥事，去锻炼30分钟'.format(sys._getframe().f_code.co_name))
class Runner(object):
    '''
    1.Runner 对象初始化
    2.注册各类 Hook 到 Runner 中
    3.调用 Runner 的 resume 或者 load_checkpoint 方法对权重进行加载
    4.运行给定的工作流，此时才真正开启了工作流
    '''
    def __init__(self, ):
        pass
        self._hooks = []

    def register_hook(self, hook):
        # 这里不做优先级判断，直接在头部插入HOOK
        self._hooks.insert(0, hook)

    def call_hook(self, hook_name):
        for hook in self._hooks:
            #geattr获取属性，返回的是一个函数，输入参数调用函数显示结果
            # 相当于hook.before_lunch('para'),参数不一定是self,可以是其它的
            getattr(hook, hook_name)(self)

    def run(self):
        print('开始启动我的一天')
        self.call_hook('before_breakfirst')
        self.call_hook('after_breakfirst')
        self.call_hook('before_lunch')
        self.call_hook('after_lunch')
        self.call_hook('before_dinner')
        self.call_hook('after_dinner')
        self.call_hook('after_finish_work')
        print('~~睡觉~~')

if __name__ == '__main__':
    runner = Runner()
    hook = HOOK()
    #hook是类的一个实例，注册hook就把把实例插入到列表中
    runner.register_hook(hook)
    #调用call_hook,读取列表中的hook实例,通过getattr(hook, hook_name)，
    # 即通过hook实例的hook_name属性获取该属性，是一个函数，然后调用该函数
    runner.run()