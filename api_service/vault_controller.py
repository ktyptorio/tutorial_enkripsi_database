import base64
import hvac

class vault_controller:
    def __init__(self, transit):
        self.transit = transit
        self.client = hvac.Client(
            url='http://vault:8200',
            token='12345678',
        )
    
    def base64ify(self, bytes_or_str):
        if isinstance(bytes_or_str, str):
            input_bytes = bytes_or_str.encode('utf8')
        elif isinstance(bytes_or_str, list):
            input_bytes = "".join(bytes_or_str).encode('utf8')
        else:
            input_bytes = bytes_or_str

        output_bytes = base64.urlsafe_b64encode(input_bytes)
        return output_bytes.decode('ascii')
    
    def encrypt_data(self, data, key_name):
        '''
        data: dict
        key_name: str

        return: dict

        Encrypts data using the transit engine

        Example:
        data = {'name': 'John Doe', 'age': 30}
        key_name = 'my_key'
        encrypted_data = encrypt_data(data, key_name)

        encrypted_data = {'name': 'vault:v1:...', 'age': 'vault:v1:...'}
        '''
        batch_data = []
        for key, value in data.items():
            if isinstance(value, int):
                value = str(value)
                
            data[key] = self.base64ify(value)
            batch_data.append({'plaintext': data[key]})

        encrypted_data = self.client.secrets.transit.encrypt_data(
            name=key_name, 
            batch_input=batch_data
        )

        encrypted_data_list = []
        for i in encrypted_data['data']['batch_results']:
            encrypted_data_list.append(i['ciphertext'])

        return dict(zip(data.keys(), encrypted_data_list))
    
    def decrypt_data(self, data, key_name):
        '''
        data: dict
        key_name: str

        return: dict

        Decrypts data using the transit engine

        Example:
        data = {'name': 'vault:v1:...', 'age': 'vault:v1:...'}
        key_name = 'my_key'
        decrypted_data = decrypt_data(data, key_name)

        decrypted_data = {'name': 'John Doe', 'age': '30'}
        '''
        batch_data = []
        for key, value in data.items():
            batch_data.append({'ciphertext': value})

        decrypted_data = self.client.secrets.transit.decrypt_data(
            name=key_name,
            batch_input=batch_data[1:]
        )

        decrypted_data_list = []

        for i in decrypted_data['data']['batch_results']:
            plaintext = base64.b64decode(i['plaintext']).decode('utf-8')
            decrypted_data_list.append(plaintext)

        return dict(zip(list(data.keys())[1:], decrypted_data_list))
    
    def rewrap_data(self, data, key_name):
        '''
        data: dict
        key_name: str

        return: dict

        Rewraps data using the transit engine

        Example:
        data = {'name': 'vault:v1:...', 'age': 'vault:v1:...'}
        key_name = 'my_key'
        rewrapped_data = rewrap_data(data, key_name)

        rewrapped_data = {'name': 'vault:v2:...', 'age': 'vault:v2:...'}

        Note: The ciphertexts are different from the original ciphertexts
        '''
        batch_data = []
        for key, value in data.items():
            batch_data.append({'ciphertext': value})

        rewrapped_data = self.client.secrets.transit.rewrap_data(
            name=key_name,
            batch_input=batch_data[1:],
            ciphertext=""
        )

        rewrapped_data_list = []
        
        for i in rewrapped_data['data']['batch_results']:
            ciphertext = i['ciphertext']
            rewrapped_data_list.append(ciphertext)

        return dict(zip(list(data.keys())[1:], rewrapped_data_list))
