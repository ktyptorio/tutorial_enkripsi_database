
from fastapi import FastAPI
from vault_controller import vault_controller
from db_controller import db_controller

app = FastAPI()

# Endpoint to write data to MariaDB
@app.post('/write')
def write_data(data: dict):

    # Initialize the Vault controller
    vault = vault_controller('transit')

    # Initialize the DB controller
    db = db_controller()
    
    # Encrypt the data using Vault
    encrypted_data = vault.encrypt_data(data['data'], 'my-key-0')
    
    # Write the encrypted data to MariaDB
    db.write_data(encrypted_data, data['table'])

    return 'Data written to MariaDB'

# Endpoint to read all data from MariaDB
@app.get('/read_all')
def read_all_data(table: str):
    
    # Initialize the Vault controller
    vault = vault_controller('transit')

    # Initialize the DB controller
    db = db_controller()

    # Read all data from MariaDB
    data_list = db.read_all_data(table)
    
    # Decrypt the data using Vault
    decrypted_data_list = []
    for data in data_list:
        data = vault.decrypt_data(data, 'my-key-0')
        decrypted_data_list.append(data)
        
    return {'data': decrypted_data_list}

# Endpoint to read data based on ID from MariaDB
@app.get('/read/{id}')
def read_data_by_id(id: int, table: str):

    # Initialize the Vault controller
    vault = vault_controller('transit')

    # Initialize the DB controller
    db = db_controller()

    # Read data from MariaDB by ID
    data = db.read_data_by_id(id, table)
    
    # Decrypt the data using Vault
    decrypted_data = vault.decrypt_data(data, 'my-key-0')

    return {'data': decrypted_data}

# Endpoint to rewrap data in MariaDB
@app.post('/rewrap')
async def rewrap_data(table: str):

    # Initialize the Vault controller
    vault = vault_controller('transit')

    # Initialize the DB controller
    db = db_controller()

    # Get all data from MariaDB
    data_list = db.read_all_data(table)

    # Rewrap the data using Vault
    rewrapped_data_list = []
    id_list = []
    for data in data_list:
        id_list.append(data['id'])
        data = vault.rewrap_data(data, 'my-key-0')
        rewrapped_data_list.append(data)

    # Initialize the DB controller
    db = db_controller()

    # Update the rewrapped data in MariaDB
    for i, data in enumerate(rewrapped_data_list):
        # Initialize the DB controller
        db = db_controller()
        db.update_data(id_list[i], data, 'encrypted_personal_data')

    return 'Data rewrapped in MariaDB'