#!/usr/bin/python

DOCUMENTATION = '''
---
module: postgres_db
short_description: Add/update databse
'''

EXAMPLES = '''
- name: Add new database
  postgres_db:
    name: "db_test"
    owner: "db_test"
'''

from ansible.module_utils.basic import *

import psycopg2


def postgres_db(data):  
    
    has_changed = False
    
    hostname = data['hostname']
    
    port = data['port']
    
    login_user = data['login_user']
    
    login_password = data['login_password']
    
    name = data['name']
    
    owner = data['owner']
    
    state = data['state']
    
    
    connect_request = "dbname=postgres user={}".format(login_user)
    
    if hostname != "localhost":
      connect_request+" host={}".format(hostname)
    
    if login_password != "":
      connect_request+" password={}".format(login_password)
    
    if port != "5432":
      connect_request+" port={}".format(port)
      
  
    connection = psycopg2.connect(connect_request)
    
    
    cursor = connection.cursor()
        
    cursor.execute("SELECT count(*) FROM pg_database WHERE datname='{}'".format(name))
    
    result = cursor.fetchone()
    
    if result[0]==0:
	
	if state == "present":  
	
	  connection.set_isolation_level(0)
	  
	  cursor.execute("CREATE DATABASE {} OWNER={};".format(name,owner))
	  
	  connection.commit()
	  
	  return True, {"status": "SUCCESS. Database has been created"}
        
        else:
	
	  return False, {"status": "WARNING. Database has not been deleted because it didn't exist."}
    else:   
	
	if state == "present":
	
	  cursor.execute("ALTER DATABASE {} OWNER TO {};".format(name,owner))
	  
	  connection.commit()	                
	  
	  return True, {"status": "SUCCESS. Database has been updated"}
	
	else:
	  
	  connection.set_isolation_level(0)
	  
	  cursor.execute("DROP DATABASE {};".format(name))
	  
	  connection.commit()
	  
	  return False, {"status": "SUCCESS. Database has been dropped."}
    
    cursor.close()
	
    connection.close()
    
def main():
    
    fields ={
        "hostname": {"required": False, "default": "localhost", "type": "str"},
        "port": {"required": False, "default": "5432", "type": "str"},
        "login_user": {"required": False, "default": "postgres", "type": "str"},
        "login_password": {"required": False, "default": "", "type": "str"},
	"name": {"required": True, "type": "str"},
        "owner": {"required": True, "type": "str"},
        "state": {"required": True, "type": "str"}
    }
    
    module = AnsibleModule(argument_spec=fields)
    has_changed, result = postgres_db(module.params)
    module.exit_json(changed=has_changed, meta=result)


if __name__ == '__main__':  
    main()