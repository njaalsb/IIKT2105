import time 

intervall = 100
prevmillis = 0
currmillis = 0

def timer():
    currmillis = time.time()
    if currmillis - prevmillis >= intervall:
        prevmillis = time.time()