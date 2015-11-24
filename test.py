#!/usr/bin/env python

__author__ = "Venu Anuganti"
__email__ = "venu@venublog.com"

import sys, os

import logging
import mysql.connector
import time
from threading import Thread

config_mysql1 = { 'user' : 'mysql', 'password' : 'mysql', 'host' : 'mydocker', 'port' : 4001 }
config_mysql2 = { 'user' : 'mysql', 'password' : 'mysql', 'host' : 'mydocker', 'port' : 4002 }
config_mysql3 = { 'user' : 'mysql', 'password' : 'mysql', 'host' : 'mydocker', 'port' : 4003 }
config_mysql4 = { 'user' : 'mysql', 'password' : 'mysql', 'host' : 'mydocker', 'port' : 4004 }
config_mysql5 = { 'user' : 'mysql', 'password' : 'mysql', 'host' : 'mydocker', 'port' : 4005 }

MAX_RECORDS = 5
MAX_SHARDS = 1

sharded_servers=['mysql1', 'mysql2', 'mysql3', 'mysql4']
sharded_master="mysql5"

replica_query="change master to master_host='%s', master_user='mysql', master_password='mysql', master_log_file='mysql-bin.000001', master_log_pos=120 for channel '%s'"

log = logging.getLogger("shardtest")
log.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='[%(asctime)s] %(levelname)-5s %(lineno)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

def __mysql_connect(config):
    try:
        mysqldb =  mysql.connector.connect(**config)
        mysqldb.autocommit = True
        return mysqldb
    except mysql.connector.Error as e:
        logging.error(e)
        return

def print_formatted_results_vertical(cursor, data=None, rowlens=0):
    desc = cursor.description
    max_field_name_len = 0
    for col in range(len(desc)):
        if len(desc[col][0]) > max_field_name_len:
            max_field_name_len = len(desc[col][0])

    if not data:
        data = cursor.fetchall()

    print("-------------------------------------------------------------------")
    count = 0
    for row in data:
        count += 1
        if (count > 1):
            print("\n++++ ROW %d ++++\n" %(count))
        for col in range(len(desc)):
            print("{:<{}s} = {}".format(desc[col][0], max_field_name_len, row[col]))
    print("")
    print("Fetched %d rows from %d columns" %(count, len(desc)))
    print("-------------------------------------------------------------------")

    return "FOO"

def execute(cursor, query, results=False):
    try:
        log.debug("  executing => {}".format(query))
        for result in cursor.execute(query, multi=True):
            if result.with_rows:
                if results:
                    print_formatted_results_vertical(cursor)
            else:
                log.debug("   rows affected: %d" %(result.rowcount))
    except mysql.connector.Error as err:
        log.error(err.msg)


def setup_replication_rewrite(server, cursor):
    log.info("[%s] Setting replication filters to re-write all shard databases to single database" % server)
    query = "CHANGE REPLICATION FILTER REPLICATE_REWRITE_DB = ("
    for shard in range(0,MAX_SHARDS):
        database_name = "shard%d" %(shard+1)
        if shard > 1:
            query += ","
        query += "(%s, shardm)" %(database_name)
    query += ")"
    execute(cursor, query)

def setup_replication(config):
    server =  "%s:%d" %(config['host'], config['port'])
    mysqldb = __mysql_connect(config)
    cursor = mysqldb.cursor()

    execute(cursor, "CREATE DATABASE IF NOT EXISTS shardm")
    #setup_replication_rewrite(server, cursor)

    log.info("[%s] Setting replication for %d servers" % (server, len(sharded_servers)))
    for host in sharded_servers:
        query = "STOP SLAVE; "
        query += replica_query %(host, host)
        execute(cursor, query)
    execute(cursor, "start slave")
    log.info(" [%s] Replication enabled for all %d servers" % (server, len(sharded_servers)))
    execute(cursor, "SHOW SLAVE STATUS", results=True)
    cursor.close()
    mysqldb.close()

def load_test_data(config):
    server =  "%s:%d" %(config['host'], config['port'])
    log.info(" [%s] Creating schema" % server)
    mysqldb = __mysql_connect(config)
    mysqldb.autocommit = True
    cursor = mysqldb.cursor()
    for shard in range(0, MAX_SHARDS):
        db = "shard%d" %(shard+1)
        query = "CREATE DATABASE IF NOT EXISTS %s; use %s; DROP TABLE IF EXISTS test; CREATE TABLE IF NOT EXISTS test(id int not null auto_increment primary key, name varchar(12))" %(db, db)
        execute(cursor, query);

    log.info(" [%s] Loading %d records into test tables" %(server, MAX_RECORDS))
    for shard in range(0, MAX_SHARDS):
        db = "shard%d" %(shard+1)
        cursor.execute("USE %s" % db)
        for id in range(0, MAX_RECORDS):
            str = "'row data %d'" %(id+1)
            insert_query = "INSERT INTO test(name) values(%s)"
            cursor.execute(insert_query % str)

    cursor.close()
    mysqldb.close()
    log.info(" [%s] Done loading data" % server)

def validate_data(config):
    server =  "%s:%d" %(config['host'], config['port'])
    mysqldb = __mysql_connect(config)
    cursor = mysqldb.cursor()
    count = 0
    expected = 1 * MAX_RECORDS * (len(sharded_servers))
    cursor.execute("SELECT count(*) as count FROM shardm.test")
    data = cursor.fetchall()
    count = data[0][0]
    cursor.close()
    mysqldb.close()
    log.info(" Total records from merged shard: {} (expected: {})".format(count, expected))
    assert count == expected
        
def main(argv):
    setup_replication(config_mysql5)

    threads = []

    threads.append(Thread(target=load_test_data, args=[config_mysql1]))
    threads.append(Thread(target=load_test_data, args=[config_mysql2]))
    threads.append(Thread(target=load_test_data, args=[config_mysql3]))
    threads.append(Thread(target=load_test_data, args=[config_mysql4]))

    # start 
    log.info("Launching all threads...")
    for t in threads:
        t.start()

    # wait 
    log.info("Waiting for all threads to finish...")
    for t in threads:
        t.join()

    # check
    log.info("Load done by all threads, validating the data after sleeping for 8 secs...")
    time.sleep(8)
    validate_data(config_mysql5)

if __name__ == "__main__":
    main(sys.argv[1:])
