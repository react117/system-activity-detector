# -*- coding: utf-8 -*-
#
# Author: react117
# Email: avikbhattacharyya.2k@gmail.com

import socket
import threading
import queue

class NetworkMonitor(threading.Thread):
    def __init__(self, host_address='www.google.com', port=80, interval=2):
        self.host_address = host_address
        self.port = port
        self.interval = interval
        self.op_queue = queue.Queue()

    def check_connection(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                host_ip = socket.gethostbyname(self.host_address)
                s.connect((host_ip, self.port))
                self.op_queue.put('Network available')
            except:
                self.op_queue.put('Network not available')
        except socket.error as msg:
            self.op_queue.put('Network not available')
            # print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])

        print(self.op_queue.get())
        s.close()
        thread = threading.Timer(self.interval, self.check_connection)
        self.thread_process(thread)

    def thread_process(self, thread, daemon=''):
        if daemon:
            thread.daemon = True

        thread.start()
        thread.join()


nm = NetworkMonitor()
nm.check_connection()
