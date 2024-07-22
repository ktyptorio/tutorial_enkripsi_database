import pymysql

class db_controller:

    def __init__(self):
        self.connection = pymysql.connect(host='mariadb',
                                          user='root',
                                          password='secret',
                                          db='my_database',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)
        
    def write_data(self, data = {}, table = 'personal_data'):
        '''
        data: dict
        table: str

        return: None

        Writes data to the database

        Example:
        data = {'name': 'John Doe', 'age': 30}
        table = 'my_table'
        write_data(data, table)

        Data written to the database
        '''
        columns = []
        values = []
        for key, value in data.items():
            columns.append(key)
            values.append(value)
        columns = ', '.join(columns)
        values = ', '.join(map(lambda x: "'{}'".format(x), values))
        
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO `{}` ({}) VALUES ({})".format(table, columns, values)
                cursor.execute(sql)
                self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()
        finally:
            self.connection.close()

    def update_data(self, id, data = {}, table = 'personal_data'):
        '''
        id: int
        data: dict
        table: str

        return: None

        Updates data in the database

        Example:
        id = 1
        data = {'name': 'John Doe', 'age': 30}
        table = 'my_table'
        update_data(id, data, table)

        Data updated in the database
        '''
        values = []
        for key, value in data.items():
            values.append("{} = '{}'".format(key, value))
        values = ', '.join(values)
        
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE `{}` SET {} WHERE id = {}".format(table, values, id)
                cursor.execute(sql)
                self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()
        finally:
            self.connection.close()
    
    def read_all_data(self, table = 'personal_data'):
        '''
        table: str

        return: dict

        Reads all data from the database

        Example:
        table = 'my_table'
        data = read_all_data(table)

        data = {'name': 'John Doe', 'age': 30}
        '''
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM `{}`".format(table)
                cursor.execute(sql)
                result = cursor.fetchall()
                
                return result
        finally:
            self.connection.close()

    def read_data_by_id(self, id, table = 'personal_data'):
        '''
        id: int
        table: str

        return: dict

        Reads data from the database by id

        Example:
        id = 1
        table = 'my_table'
        data = read_data_by_id(id, table)

        data = {'name': 'John Doe', 'age': 30}
        '''
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM `{}` WHERE id = {}".format(table, id)
                cursor.execute(sql)
                result = cursor.fetchall()

                return result[0]
        finally:
            self.connection.close()
