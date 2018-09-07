from utils import POOL
import pymysql

# 将pymysql的数据库连接功能、查增改功能封装为函数（可选）


def create_conn():
    conn = POOL.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    return conn, cursor


def close_conn(conn, cursor):
    conn.close()
    cursor.close()
    return True


def inquiry(sql, args, num='one'):
    '''
    通过pymysql查询
    num='one':查询单条
    num='all'：查询所有
    '''
    conn, cursor = create_conn()
    if num == 'one':
        cursor.execute(sql, args)
        result = cursor.fetchone()
    elif num == 'all':
        cursor.execute(sql)  # 使用execute()防止sql注入
        result = cursor.fetchall()
    close_conn(conn, cursor)
    return result


def insert(sql, args):
    '''
    通过pymysql插入
    '''
    conn, cursor = create_conn()
    result = cursor.execute(sql, args)
    conn.commit()
    close_conn(conn, cursor)
    return result


# CREATE TABLE user(
#     id int primary key AUTO_INCREMENT,
#     name char(32) NOT NULL,
#     age int(3) NOT NULL DEFAULT 0,
#     sex boolean DEFAULT true);
