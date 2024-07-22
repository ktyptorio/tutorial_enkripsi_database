import hvac
import sys

class transit_engine_key:
    def __init__(self, secret_engine):
        self.secret_engine = secret_engine
        self.client = hvac.Client(url='http://localhost:8200', token='12345678')
    
    def create_engine_key(self):
        if self.client.sys.list_mounted_secrets_engines()['data'].get(self.secret_engine+'/') is None:
            self.client.sys.enable_secrets_engine(backend_type='transit', path=self.secret_engine)
            print("Transit engine created")
        else:
            print("Transit engine already enabled")

    def create_key(self, key_name):
        engine = self.secret_engine
        self.client.write('{}/keys/{}'.format(engine, key_name))
        print("Key {} created".format(key_name))
    

def main(*args, **kwargs):
    secret_path = args[2]
    engine = transit_engine_key(secret_path.split('/')[0])

    if args[1] == 'create_engine':
        engine.create_engine_key()
    elif args[1] == 'create_key':
        key_name = secret_path.split('/')[-1]
        engine.create_key(key_name)
    else:
        print("Invalid command")

if __name__ == '__main__':
    main(*sys.argv)
