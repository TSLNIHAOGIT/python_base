def simple_coroutine(): # ➊
 print('-> coroutine started')
 x = yield # ➋
 print('-> coroutine received:', x)

my_coro = simple_coroutine()
my_coro #