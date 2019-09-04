import json
from pathlib import Path
from threading import Lock

# This path will point to this file no matter where it is called from
current_file_path = Path(__file__).resolve().parent.parent


def load_param_json(env_name):
    """
    Loads hyperparameters saved as json file
    :param env_name:
    :return: hyperparameters in dict
    """

    param_path = current_file_path.joinpath('hyperparameters',
                                            env_name + '.json')

    with open(str(param_path), 'r') as f:
        parameters = json.load(f)
    return parameters


class threadDoneCounter:
    def __init__(self, NUM_THREADS):
        self.count_done = 0
        self.num_threads = NUM_THREADS
        self.count_lock = Lock()

    def increment(self):
        self.count_lock.acquire()
        self.count_done += 1
        self.count_lock.release()

    def is_done(self):
        if self.count_done >= self.num_threads:
            return True
        else:
            return False


class dummy:

    def __init__(self):
        self.collection = []
        self.lock = threading.Lock()
        self.timeout = 5

    def add_coll(self, data):
        self.collection.append(data)


if __name__ == '__main__':
    import threading
    import time
    dum = dummy()

    c_t = threadDoneCounter(2)

    def worker(dum, i, c_t):
        while True:
            time.sleep(1)
            result = 'a-' + str(i)
            print(f'Added {result} at time {time.time()-tag}')
            dum.add_coll(result)

            if dum.timeout != None and (time.time() - tag) >= dum.timeout:
                c_t.increment()
                return


    tag = time.time()
    for i in range(2):
        t = threading.Thread(target=worker, args=(dum, i, c_t))
        t.start()

    while True:
        time.sleep(0.5)
        if c_t.is_done():
            print(True)
            break
        else:
            print(False)

    exit(0)
    main_thread = threading.currentThread()

    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()

    print(f'time: {time.time() - tag}')
    print(dum.collection)