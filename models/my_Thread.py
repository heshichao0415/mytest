import threading
import time

#定义线程要执行的函数
def writing():
    print("我在写字的哦")
    time.sleep(2)     #沉睡2秒，方便我们看到执行的过程

#定义线程要执行的函数
def drawing():
    print("我在画画的哦")
    time.sleep(2)     #沉睡2秒，方便我们看到执行的过程

def main():
    t1 = threading.Thread(target=writing)     #创建线程1
    t2 = threading.Thread(target=drawing)     #创建线程2
    t1.start()
    t2.start()
    time.sleep(1)    #沉睡1秒，方便我们看到执行的过程

# def main():
#     writing()
#     drawing()

if __name__ == '__main__':
    main()
    main()
    main()
