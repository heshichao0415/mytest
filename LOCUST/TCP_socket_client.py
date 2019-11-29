import socket

#创建一个socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#建立连接
s.connect(('127.0.0.1', 10021))
while True:
    data = input('请输入要发送的数据')
    if data == 'quit':
        break

    # 发送编码后的数据
    s.send(data.encode())        #直观看到发送的数据请求
    # 打印接收到的大写数据
    print(s.recv(1024).decode('utf-8'))

#放弃连接
s.send(b'quit')
s.close()