#!/usr/bin/python

DOCUMENTATION = '''
---
module: postgres_schema
short_description: Add Schema to database
'''

EXAMPLES = '''
- name: Create a schema to database
  postgres_schema:
    database: "db_test"
    schema: "db_test_schema"
    user: "db_test"
'''

from ansible.module_utils.basic import *

import psycopg2


def postgres_schema(data):  
    
    has_changed = False
    
    hostname = data['hostname']
    
    port = data['port']
    
    login_user = data['login_user']
    
    login_password = data['login_password']
    
    db_name = data['database']
    
    schema = data['schema']
    
    user = data['user']
     
    state = data['state']
     
    connect_request = "dbname={} user={}".format(db_name,login_user)
    
    if hostname != "localhost":
      connect_request+" host={}".format(hostname)
    
    if login_password != "":
      connect_request+" password={}".format(login_password)
    
    if port != "5432":
      connect_request+" port={}".format(port)
      
    # Connect to the database
    connection = psycopg2.connect(connect_request)
    
    # Open a cursor to perform database operations
    cursor = connection.cursor()
    
    cursor.execute("SELECT count(*) FROM pg_catalog.pg_namespace WHERE nspname='{}'".format(schema))
    
    result = cursor.fetchone()
    
    if result[0]==0:
      
	if state == "present":
        
	  cursor.execute("CREATE SCHEMA {} AUTHORIZATION {}".format(schema, user))
        
	  connection.commit()
            
	  return True, {"status": "SUCCESS"}
	
	else:
	
	  return False, {"status": "WARNING. schema hasn't been deleted because it didn't exist."}
        
    else:
      
	if state == "present":
        
	  cursor.execute("ALTER SCHEMA {} OWNER TO {}".format(schema, user))
        
	  connection.commit()
            
	  return True, {"status": "SUCCESS"}
	
	else:
	
	  cursor.execute("DROP SCHEMA {} CASCADE".format(schema))
	  
	  connection.commit()
	  
	  return True, {"status": "SUCCESS. schema has been deleted."}
	 
    
    cursor.close()
	
    connection.close()
    
def main():
    
    fields ={
        "hostname": {"required": False, "default": "localhost", "type": "str"},
        "port": {"required": False, "default": "5432", "type": "str"},
        "login_user": {"required": False, "default": "postgres", "type": "str"},
        "login_password": {"required": False, "default": "", "type": "str"},
        "database": {"required": True, "type": "str"},
        "schema": {"required": True, "type": "str"},
        "user": {"required": True, "type": "str"},
        "state": {"required": True, "type": "str"}
    }
    
    module = AnsibleModule(argument_spec=fields)
    has_changed, result = postgres_schema(module.params)
    module.exit_json(changed=has_changed, meta=result)


if __name__ == '__main__':  
    main()