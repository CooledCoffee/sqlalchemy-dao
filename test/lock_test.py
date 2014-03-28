# -*- coding: utf-8 -*-
from testutil import DbTest
from threading import Thread
import time

class LockTest(DbTest):
    def test_success(self):
        # set up
        def foo():
            with self.mysql.dao.Lock('lock1'):
                time.sleep(0.05)
        class BlockingThread(Thread):
            def run(self):
                foo()
                
        # test
        thread1 = BlockingThread()
        thread2 = BlockingThread()
        begin = time.time()
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        end = time.time()
        self.assertGreater(end - begin, 0.1)
        