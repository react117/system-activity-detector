# -*- coding: utf-8 -*-
#
# Author: react117
# Email: avikbhattacharyya.2k@gmail.com

import socket
import threading
import queue
import logging
from datetime import datetime

class NetworkMonitor(threading.Thread):
    # initialize the log settings
    logging.basicConfig(filename='log/' + datetime.now().strftime("%Y%m%d") + '_error.log', format='[%(asctime)s.%(msecs)03d]: %(name)s - %(levelname)s - %(message)s')

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
            except IOError as e:
                self.op_queue.put('Network not available')
                logging.error('There is an error in connection. Error : ' + str(e))
        except socket.error as msg:
            self.op_queue.put('Network not available')
            logging.error('There is an error in socket creation. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])

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
