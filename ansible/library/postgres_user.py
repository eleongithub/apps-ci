#!/usr/bin/python

DOCUMENTATION = '''
---
module: postgres_user
short_description: Add/update User
'''

EXAMPLES = '''
- name: Add a new user
  postgres_user:
    user: "db_test"
    password: "db_test"
    roles: "CREATEROLE CREATEUSER"
'''

from ansible.module_utils.basic import *

import psycopg2


def postgres_user(data):  
    
    has_changed = False
    
    hostname = data['hostname']
    
    port = data['port']
    
    login_user = data['login_user']
    
    login_password = data['login_password']
    
    user = data['user']
    
    password = data['password']
    
    roles = data['roles']
    
    state = data['state']
    
    connect_request = "dbname=postgres user={}".format(login_user)
    
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
        
    cursor.execute("SELECT count(*) FROM pg_user WHERE usename='{}'".format(user))
    
    result = cursor.fetchone()
    
    if result[0]==0:
      
        if state == "present":
	  
	  if password != "":
	    
	    cursor.execute("CREATE USER {} LOGIN password '{}' {};".format(user,password, roles))
	  
	  else:
	    
	    cursor.execute("CREATE USER {} {};".format(user, roles))
	  
	  connection.commit()
        	                
	  return True, {"status": "SUCCESS. User have been created"}
      
	else:
	  
	  return False, {"status": "WARNING. User hasn't been deleted because he didn't exist."}
        
    else:
      
	if state == "present":
	  
	  cursor.execute("ALTER ROLE {}  {};".format(user, roles))
        
	  if password != "":
	  
	    cursor.execute("ALTER ROLE  {} WITH PASSWORD  '{}';".format(user, password))
        
	  connection.commit()
        	                
	  return True, {"status": "SUCCESS. User has been updated"}
 
	else:
	  
	  # Drop all schemas belong to user
	  cursor.execute("SELECT schema_name FROM information_schema.schemata where schema_owner='{}'".format(user))
	  
	  rows = cursor.fetchall()
	  
	  for row in rows:
   
	     cursor.execute("DROP SCHEMA {} CASCADE".format(row[0]))
	   
	     connection.commit()
	  
	  
	  # Drop all database belong to user
	  cursor.execute("SELECT d.datname FROM pg_database d JOIN pg_user u ON (d.datdba = u.usesysid) WHERE u.usename='{}'".format(user))
	  
	  rows = cursor.fetchall()
	  
	  connection.set_isolation_level(0)
	  
	  for row in rows:
	    
	      cursor.execute("DROP DATABASE {};".format(row[0]))
	  
	      connection.commit()
	  	   
	  cursor.execute("DROP USER {}".format(user))
	  
	  connection.commit()
	  
	  return True, {"status": "SUCCESS. User has been dropped and its database have been dropped also."}   
	  
    cursor.close()
	
    connection.close()
    
def main():
    
    fields ={
        "hostname": {"required": False, "default": "localhost", "type": "str"},
        "port": {"required": False, "default": "5432", "type": "str"},
        "login_user": {"required": False, "default": "postgres", "type": "str"},
        "login_password": {"required": False, "default": "", "type": "str"},
	"user": {"required": True, "type": "str"},
        "password": {"required": False, "default": "", "type": "str"},
        "roles": {"required": False, "default": "", "type": "str"},
        "state": {"required": True, "type": "str"}
    }
    
    module = AnsibleModule(argument_spec=fields)
    has_changed, result = postgres_user(module.params)
    module.exit_json(changed=has_changed, meta=result)


if __name__ == '__main__':  
    main()