from flask import Flask, request

import redis

from arcus import *
from arcus_mc_node import *

import sys, traceback

app = Flask(__name__)
app.secret_key = 'W0asf38r9sdsdjoq!@$89WX/,?RT'


mySQL_config = {"user": "root",
                "password": "1234",
                "database": "test_db",
                "host": "172.17.0.2" # Target MySQL ip-address
                }


from mysql.connector.pooling import MySQLConnectionPool
mysql_pool = MySQLConnectionPool(pool_name=None, pool_size=4, pool_reset_session=True, **mySQL_config)

last_insert_key = None;

client = Arcus(ArcusLocator(ArcusMCNodeAllocator(ArcusTranscoder())))
client.connect("172.17.0.4:2181", "guddnjs91-cloud") # Target Arcus ip-address

redis_host = "172.17.0.7" # Target nBase-ARC ip-address
redis_port = 6000


@app.route('/mysql_select')
def mysql_select():
    connection = mysql_pool.get_connection()

    try:
        result = None;
        cursor = connection.cursor()
        key = request.args['key']

        query = "SELECT * FROM `test_table` WHERE `key`='%s'" % (key)
        queryResult = cursor.execute(query)
        result_data = cursor.fetchone()

        if result_data is not None and cursor.rowcount == 1:
            result = "Found value : " + result_data[1]
        else:
            result = "Not Found"
    except Exception as e:
        result = e.msg
        print("*" * 20)
        traceback.print_exc(file=sys.stdout)
        print("#" * 20)
    finally:
        if connection is not None:
            connection.close()

    return result


@app.route('/mysql_insert')
def mysql_insert():
    result = None;

    try:
        connection = mysql_pool.get_connection()
        cursor = connection.cursor()
        key = request.args['key']
        value = request.args['value']

        query = "INSERT INTO  `test_table` (`key`, `value`) VALUES ('%s', '%s')" % (key, value)
        queryResult = cursor.execute(query)
        connection.commit()
        result_data = cursor.fetchone()

        result = key + " inserted"
    except Exception as e:
        result = e.msg
        print("*" * 20)
        traceback.print_exc(file=sys.stdout)
        print("#" * 20)
    finally:
        if connection is not None:
            connection.close()

    return result


@app.route('/arcus_set')
def arcus_select():
    result = None;

    try:
        key = request.args['key']
        value = request.args['value']

        ret = client.set(key, value, 3600) # Expiration Time : 1 hour

        result = key + " set " + str(ret)
    except Exception as e:
        result = str(e)
        print("*" * 20)
        traceback.print_exc(file=sys.stdout)
        print("#" * 20)
    finally:
        pass

    return result


@app.route('/arcus_get')
def arcus_insert():
    result = None;

    try:
        key = request.args['key']
        ret = client.get(key)
        print(str(ret))
        result = ret.get_result()
    except Exception as e:
        result = str(e)
        print("*" * 20)
        traceback.print_exc(file=sys.stdout)
        print("#" * 20)
    finally:
        pass

    print("#### " + str(result));

    if result is None:
        result = "Not Found"

    return result

redis_pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=0)


@app.route('/nbase_arc_set')
def nbase_arc_set():
    result = None

    try:
        key = request.args['key']
        value = request.args['value']

        r = redis.Redis(connection_pool=redis_pool)
        ret = r.set(key, value)
        print(str(ret))
        result = str(ret)
    except Exception as e:
        result = str(e)
        print("*" * 20)
        traceback.print_exc(file=sys.stdout)
        print("#" * 20)
    finally:
        pass

    print("#### " + str(result));
    return result


@app.route("/nbase_arc_get")
def nbase_arc_get():
    result = None;

    try:
        key = request.args['key']

        r = redis.Redis(connection_pool=redis_pool)
        ret = r.get(key)
        print(str(ret))

        result = str(ret)
    except Exception as e:
        result = str(e)
        print("*" * 20)
        traceback.print_exc(file=sys.stdout)
        print("#" * 20)
    finally:
        pass

    print("#### " + str(result));
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
