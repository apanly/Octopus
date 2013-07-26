import socket
import base64,hashlib,sys,threading,struct,logging,logging.config
import zmq

from JobsProject.server import LOG_SERVER
  

def InitWebSocketServer(host = "localhost", port = 12345, backlog = 100):  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clients = []
    try:  
        sock.bind((host,port)) 
        sock.listen(backlog)  
    except:  
        print("Server does not start, please check the port")  
        sys.exit()  
    logger.info("accepting ...")
    while True:  
        connection,address = sock.accept()  
	logger.info("handshake")
        if(handshake(connection) != False): 
	    clients.append(connection)
	    logger.info("do ...")
            #DoRemoteCommand(connection)
            t = threading.Thread(target=DoRemoteCommand,args=(connection,clients,))  
            t.start()  
    logger.info("do")
  
  
def handshake(client):  
    headers = {}  
    shake = client.recv(1024)  
      
    if not len(shake):  
        return False  
      
    header, data = shake.split('\r\n\r\n', 1)  
    for line in header.split("\r\n")[1:]:  
        key, value = line.split(": ", 1)  
        headers[key] = value  
      
    if(headers.has_key("Sec-WebSocket-Key") == False):  
        print("this socket is not websocket,close")  
        client.close()  
        return False  
      
    szOrigin = headers["Origin"]  
    szKey = base64.b64encode(hashlib.sha1(headers["Sec-WebSocket-Key"] + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').digest())  
    szHost = headers["Host"]  
      
    our_handshake = "HTTP/1.1 101 Switching Protocols\r\n" \
                    "Upgrade:websocket\r\n"\
                    "Connection: Upgrade\r\n"\
                    "Sec-WebSocket-Accept:"+ szKey + "\r\n" \
                    "WebSocket-Origin:" + szOrigin + "\r\n" \
                    "WebSocket-Location: ws://" + szHost + "/WebManagerSocket\r\n" \
                    "WebSocket-Protocol:WebManagerSocket\r\n\r\n"  
                      
    client.send(our_handshake)  
    return True  
  

def RecvData(nNum,client):  
    try:  
        pData = client.recv(nNum)  
        if not len(pData):  
            return False  
    except:  
        return False  
    else:  
        code_length = ord(pData[1]) & 127  
        if code_length == 126:  
            masks = pData[4:8]  
            data = pData[8:]  
        elif code_length == 127:  
            masks = pData[10:14]  
            data = pData[14:]  
        else:  
            masks = pData[2:6]  
            data = pData[6:]  
          
        raw_str = ""  
        i = 0  
        for d in data:  
            raw_str += chr(ord(d) ^ ord(masks[i%4]))  
            i += 1  
              
        return raw_str  
          
          
def SendData(pData,client,clients):  
    if(pData == False):  
        return False  
    else:  
        pData = str(pData)  
          
    token = "\x81"  
    length = len(pData)  
    if length < 126:  
        token += struct.pack("B", length)  
    elif length <= 0xFFFF:  
        token += struct.pack("!BH", 126, length)  
    else:  
        token += struct.pack("!BQ", 127, length)  
    pData = '%s%s' % (token,pData)  
    #print pData
    for client in clients:
        try:
		      client.send(pData)  
        except:
            pass
      
    return True  
  
  
def DoRemoteCommand(connection,clients):  
    while 1:  
        #szBuf = RecvData(8196,connection)  
        szBuf = receiver.recv()
        if(szBuf == False):  
            break
        print szBuf
        SendData(szBuf,connection,clients)  


if __name__ == "__main__":
	logging.config.fileConfig("JobsProject/log4p.conf")
	logger = logging.getLogger("main")
	context = zmq.Context()
	receiver = context.socket(zmq.PULL)
	receiver.bind(LOG_SERVER)
	InitWebSocketServer()
	receiver.close()
	context.term()


__all__ = []
