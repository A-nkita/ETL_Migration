import json  # Make sure this line is added

def get_config_db(filename):
    try:
        with open(filename, 'r') as fp:
            cred = json.load(fp)
        print(f"Loaded config: {cred}")  # Debugging line to check what was loaded
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

    if all(k in cred for k in ['mysql_host', 'mysql_user', 'mysql_password', 'mysql_database', 'mysql_port',
                               'mssql_host', 'mssql_database', 'mssql_port']):
        return (cred['mysql_host'],
                cred['mysql_user'],
                cred['mysql_password'],
                cred['mysql_database'],
                cred['mysql_port'],
                cred['mssql_host'],
                cred['mssql_database'],
                cred.get('mssql_port', 1433))
    else:
        print("Config is missing required keys")
        return None
