
import threading
import time

from src.main.SearchDirectory.search_file_system import read_dir


class RunLookup(object):

    def __init__(self):

        thread = threading.Thread(target=self.run, args=())
        # thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        read_dir()
        time.sleep(self.interval)

