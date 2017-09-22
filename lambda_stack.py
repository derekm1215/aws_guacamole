
import boto.cloudformation
import sys
import logging
import time
import pymysql

#connect to DB
logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    cx = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

x = cx.cursor()

def handler(event, context):
	"""
	This function adds connections from CloudFormation outputs to Guacamole
	"""
	host = "hostname"
	port = "port"
	conn = boto.cloudformation.connect_to_region('us-west-1')  # or your favorite region

	while True:
		(conn.describe_stacks()[0]).stack_status != 'CREATE_COMPLETE'
		time.sleep(5)
		if (conn.describe_stacks()[0]).stack_status =='CREATE_COMPLETE':
			break

	stacks = conn.describe_stacks()
	stack = stacks[0]     

	for output in stack.outputs:
		if "vnc" in output.key:
			cxn = output.description
			ct = "vnc"
			pt = "5901"
			ip = output.value
		else:
			cxn = output.description
			ct = "ssh"
			pt = "22"
			ip = output.value
		
		item_count = 0
		
		x.execute('''INSERT INTO guacamole_connection (connection_name, protocol) VALUES (%s, %s)''' ,(cxn, ct))
		key = cx.insert_id()
		x.execute('''INSERT INTO guacamole_connection_parameter VALUES (%s, %s, %s)''' ,(key ,host, c))
		x.execute('''INSERT INTO guacamole_connection_parameter VALUES (%s, %s, %s)''' ,(key, port, pt))
		cx.commit()
		x.execute("select * from guacamole_connection")
		for row in x:
			item_count += 1
			logger.info(row)
			#print(row)
	return "Added %d items from RDS guacamole_connection table" %(item_count)
cx.close()





