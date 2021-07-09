from threading import Thread
import time


class Test:
    def __init__(self):
        self.container = dict()
        self.scheduler = dict()
        self.thread = None
        self._run()

    def add(self, topic):
        if topic not in self.container.keys():
            self.container[topic] = dict()
        return self.container[topic]

    def set(self, key=None, value=None, dictionary=None, ex=0):
        if key and value:
            self.container.update({key: value})
            if ex:
                self.scheduler.update({key: {"expert_time": ex, "register_timestamp": time.time()}})
        if dictionary and isinstance(dictionary, dict):
            for k, v in dictionary.items():
                self.container.update({k: v})
                if ex:
                    self.scheduler.update({k: {"expert_time": ex, "register_timestamp": time.time()}})

    def get(self, key):
        return self.container.get(key)

    def get_all(self):
        return self.container

    def pop(self, key):
        temp = self.container.get(key)
        if key in self.container.keys():
            del self.container[key]
        return temp

    def delete(self, key):
        if key not in self.container.keys():
            return 0
        del self.container[key]
        return 1

    def expire(self, key, ex):
        if key not in self.container.keys():
            return 0
        if not isinstance(ex, int) or not isinstance(ex, float):
            return 0
        if ex < 0:
            return 0
        self.scheduler.update({key: {"expert_time": ex, "register_timestamp": time.time()}})
        return 1

    def _timer(self):
        while True:
            time.sleep(0.1)
            delete_list = []
            for key, value in self.scheduler.items():
                if time.time() - value["register_timestamp"] > value["expert_time"]:
                    delete_list.append(key)
            if delete_list:
                for key in delete_list:
                    del self.container[key]
                    del self.scheduler[key]

    def _run(self):
        thread = Thread(target=self._timer)
        thread.start()


class Container:
    def __init__(self):
        self.container = dict()





t = Test()
t.set('name', 'bingo')
t.set('age', 18, ex=3)
print(t.get_all())
time.sleep(4)
print(t.get('name'))
t.set('sexual', 'male', ex=3)
print(t.get('age'))
time.sleep(1)
print(t.get('sexual'))
time.sleep(2.5)
print(t.get('sexual'))
print(t.get('name'))