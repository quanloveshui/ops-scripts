>>> def f():
...     a = 0
...     while True:
...         b = yield a
...         print b
...         if b == 'q':
...             break
...         print 'send is %s' % b

>>> g=f()   f()不是函数的调用，而是产生生成器对象
>>> g.next()   第一次调用生成器的next方法，将运行到yield位置，此时暂停执行环境，并返回yield后的值
0
>>> g.next()  
第二次调用next方法，上一次调用next,执行到yield a暂停，再次执行恢复环境，给b赋值(注意：这里的b的值并不是a的值，而是通过send方法接受的值)，由于我们没有调用send方法，所以b的值为None,此时输出None，并执行到下一次yield a,所以又输出0
None
send is None
0
>>> g.send(1) 上次程序执行到yield暂停，此时我们send(1)，程序将收到1，并给b赋值为1，此时b=1，并执行到下一次yield a，暂停环境
1
send is 1
0
