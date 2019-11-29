import socket
import time
import threading

#创建socket (AF_INET:IPv4, AF_INET6:IPv6) (SOCK_STREAM:面向流的TCP协议)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#绑定本机IP和任意端口(>1024)
s.bind(('127.0.0.1', 10021))
#监听，等待连接的最大数目为1
s.listen(1)
print('Server is running...')

#TCP服务器端处理逻辑
def TCP(sock, addr):
    # 接受连接请求
    print('Accept new connection from %s:%s.' %addr)
    while True:
        # 接受其数据
        data = sock.recv(1024)
        print(data.decode('utf-8'))
        time.sleep(1)
        # 如果数据为空或者'quit'，则退出
        if not data or data.decode() == 'quit':
            break
        # 发送变成大写后的数据,需先解码,再按utf-8编码,  encode()其实就是encode('utf-8')
        sock.send(data.decode('utf-8').upper().encode())

    #关闭连接
    sock.close()
    print('Connection from %s:%s closed.' % addr)

while True:
    # 接收一个新连接
    sock, addr = s.accept()
    TCP(sock, addr)
