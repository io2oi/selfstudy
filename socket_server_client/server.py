'''
The original example of multi threaded socket is from
https://webnautes.tistory.com/1381
'''
import socket
import pickle
from _thread import *

def mock_db(query_key):
    '''
    This function has a role of DBMS.
    '''
    dic = {
        '1-1-A-T_HP:000001': [3,10,1,10000],
        '1-1-A-T_HP:000002': [3,2000, 0,100000]
    }
    res = dic.get(query_key,False)
    return res
    
def threaded(client_socket, addr):
    '''
    supporting multi clients by thread
    '''
    print('Connected by :', addr[0], ':', addr[1]) 
    # 클라이언트가 접속을 끊을 때 까지 반복합니다. 
    while True: 
        try:
            # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
            data = client_socket.recv(1024)
            if not data: 
                print('Disconnected by ' + addr[0],':',addr[1])
                break
            print('Received from ' + addr[0],':',addr[1] , data.decode())
            #client_socket.send(data) 
            print(f"return value: {mock_db(data.decode())}")
            rt_val = mock_db(data.decode())
            client_socket.send(pickle.dumps(rt_val))
        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0],':',addr[1])
            break
    client_socket.close() 

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 9999

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT)) 
    server_socket.listen() 

    print('server start')

    # 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.
    # 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다. 
    while True: 
        print('wait')
        client_socket, addr = server_socket.accept() 
        start_new_thread(threaded, (client_socket, addr)) 

    server_socket.close() 