import threading
import time
import json
import os

class PyInMemStore:
    def __init__(self):
        self.data={}
        self.lock = threading.Lock()

    def setup(self):
        while True:
            time.sleep(1)
            if os.path.exists("data.json"):
                if os.path.getsize("data.json") == 0:
                    with open("data.json", 'w') as json_file:
                        json.dump({}, json_file)
                with open("data.json", "r") as json_file:
                    self.data = json.load(json_file)
                for item in list(self.data.keys()):
                    if self.data[item][1]!=1000000000000:
                        if self.data[item][1]-time.time()<=0:
                            del self.data[item]
                        else:
                            self.Expire(item[0],self.data[item][1]-time.time())
                with open("data.json", "w") as json_file:
                    json.dump(self.data, json_file)
            else:
                with open("data.json", 'w') as json_file:
                    json.dump({}, json_file)

    def Set(self,key,value):
        with self.lock:
            self.data[key]=[value,1000000000000]
            with open("data.json", "w") as json_file:
                json.dump(self.data, json_file)

    def Get(self,key):
        with self.lock:
            with open("data.json", "w") as json_file:
                json.dump(self.data, json_file)
            try: 
                if self.data[key][1]-time.time() <= 0:
                    del self.data[key]
                with open("data.json", "w") as json_file:
                    json.dump(self.data, json_file)
                return [True,self.data[key][0]]
            except:
                return [False,None]

        
    def Delete(self,key):
        with self.lock:
            try:
                if self.data[key][1]-time.time() <= 0:
                    del self.data[key]
                with open("data.json", "w") as json_file:
                    json.dump(self.data, json_file)
                del self.data[key]
                with open("data.json", "w") as json_file:
                    json.dump(self.data, json_file)
                return True
            except:
                return False
    
    def Expire(self,key,timeout_seconds):
        expiration_time = time.time() + timeout_seconds
        with self.lock:
            try:
                if self.data[key][1]-time.time() <= 0:
                    del self.data[key]
                    with open("data.json", "w") as json_file:
                        json.dump(self.data, json_file)
                self.data[key][1]=expiration_time
                with open("data.json", "w") as json_file:
                    json.dump(self.data, json_file)
                threading.Thread(target=self.expire_del, args=(key, expiration_time)).start()
                return True
            except:
                return False


    def expire_del(self, key, expiration_time):
        time.sleep(expiration_time - time.time())
        with self.lock:
            if key in self.data and self.data[key][1] == expiration_time:
                del self.data[key]
                with open("data.json", "w") as json_file:
                    json.dump(self.data, json_file)

    def Ttl(self,key):
        with self.lock:
            try:
                if self.data[key][1]-time.time() <= 0:
                    del self.data[key]
                    with open("data.json", "w") as json_file:
                        json.dump(self.data, json_file)
                if self.data[key][1] == 1000000000000:
                    return [True,1000000000000]
                return [True,self.data[key][1]-time.time()]
            except:
                return [False]
    def Keys(self):
        with self.lock:
            return self.data


def user_input(store):
    while True:
        command = input("Enter a command and then press enter(commands/set/get/delete/exit/expire/keys/ttl): ").lower()

        if command == 'exit':
            break
        if command == 'commands':            
            commands = ['exis','commands','set','get','ttl','delete','expire','keys']
            for item in commands:
                print(item)
            
        if command == 'set':
            key = input("Enter the key: ")
            value = input("Enter the value: ")
            store.Set(key, value)
            print(f"Key '{key}' set to value '{value}'")

        elif command == 'get':
            key = input("Enter the key: ")
            value = store.Get(key)
            if value[0]:
                print(f"Value for key '{key}': {value[1]}")
            else:
                print(value[1])
        
        elif command == 'delete':
            key = input("Enter the key: ")
            if store.Delete(key):
                print(f"'{key}' key deleted ")
            else:
                print(f"'{key}' key dose not exist")

        elif command == 'expire':
            key = input('Enter key name for Expire: ')
            expire = int(input('Enter timeout: '))
            if store.Expire(key,expire):
                print(f"'{key}' key timeout {expire} ")
            else:
                print(f"{key} key dose not exist")

        elif command == 'ttl':
            key = input('Enter key name for ttl: ')
            if store.Ttl(key)[0]:
                ttl=int(store.Ttl(key)[1])
                if ttl == 1000000000000:
                    print(-1)
                else:
                    print(ttl)
            else:
                print(-2)

        elif command == 'keys':
            key = store.Keys()
            for item in key:
                print(item)
        
        else:
            print(f"command '{command}' dose not exist")
        
store=PyInMemStore()

setup_thread = threading.Thread(target=store.setup)
setup_thread.start()
# store.setup()
input_thread = threading.Thread(target=user_input, args=(store,))
input_thread.start()
# setup_thread = threading.Thread(target=store.setup())
# setup_thread.start()
# while True:
#     store.setup()