#!/usr/bin/env python3
"""
SQLite 数据库操作工具

提供完整的增删改查 (CRUD) 功能，支持：
- 创建数据库和表
- 插入数据
- 查询数据
- 更新数据
- 删除数据
- 执行自定义 SQL
"""

import sqlite3
import json
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional


class SQLiteDB:
    """SQLite 数据库操作类"""
    
    def __init__(self, db_path: str):
        """
        初始化数据库连接
        
        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
    
    def connect(self) -> "SQLiteDB":
        """连接到数据库"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # 使结果可以通过列名访问
        self.cursor = self.conn.cursor()
        return self
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.commit()
            self.conn.close()
    
    def __enter__(self):
        """上下文管理器入口"""
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.close()
    
    def create_table(self, table_name: str, columns: Dict[str, str]):
        """
        创建表
        
        Args:
            table_name: 表名
            columns: 列定义字典，格式 {'列名': '类型和约束'}
                    例如: {'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                           'name': 'TEXT NOT NULL',
                           'age': 'INTEGER'}
        """
        column_defs = ', '.join([f"{name} {definition}" for name, definition in columns.items()])
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})"
        self.cursor.execute(sql)
        self.conn.commit()
        print(f"✓ 表 '{table_name}' 创建成功")
    
    def insert(self, table_name: str, data: Dict[str, Any]) -> int:
        """
        插入单条数据
        
        Args:
            table_name: 表名
            data: 数据字典，格式 {'列名': 值}
        
        Returns:
            插入数据的行 ID
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, list(data.values()))
        self.conn.commit()
        row_id = self.cursor.lastrowid
        print(f"✓ 插入成功，行 ID: {row_id}")
        return row_id
    
    def insert_many(self, table_name: str, data_list: List[Dict[str, Any]]) -> int:
        """
        批量插入数据
        
        Args:
            table_name: 表名
            data_list: 数据字典列表
        
        Returns:
            插入的行数
        """
        if not data_list:
            print("⚠ 没有数据需要插入")
            return 0
        
        columns = ', '.join(data_list[0].keys())
        placeholders = ', '.join(['?' for _ in data_list[0]])
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        values_list = [list(data.values()) for data in data_list]
        self.cursor.executemany(sql, values_list)
        self.conn.commit()
        count = self.cursor.rowcount
        print(f"✓ 批量插入成功，共 {count} 条记录")
        return count
    
    def query(self, table_name: str, columns: str = "*", 
              where: Optional[str] = None, params: Optional[tuple] = None,
              order_by: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        查询数据
        
        Args:
            table_name: 表名
            columns: 要查询的列，默认 "*"
            where: WHERE 子句（不包含 WHERE 关键字）
            params: WHERE 子句的参数
            order_by: ORDER BY 子句（不包含 ORDER BY 关键字）
            limit: 限制返回的行数
        
        Returns:
            查询结果列表
        """
        sql = f"SELECT {columns} FROM {table_name}"
        
        if where:
            sql += f" WHERE {where}"
        if order_by:
            sql += f" ORDER BY {order_by}"
        if limit:
            sql += f" LIMIT {limit}"
        
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        
        rows = self.cursor.fetchall()
        results = [dict(row) for row in rows]
        print(f"✓ 查询成功，返回 {len(results)} 条记录")
        return results
    
    def update(self, table_name: str, data: Dict[str, Any], 
               where: str, params: Optional[tuple] = None) -> int:
        """
        更新数据
        
        Args:
            table_name: 表名
            data: 要更新的数据字典
            where: WHERE 子句（不包含 WHERE 关键字）
            params: WHERE 子句的参数
        
        Returns:
            受影响的行数
        """
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {where}"
        
        # 合并 SET 和 WHERE 的参数
        all_params = list(data.values())
        if params:
            all_params.extend(params)
        
        self.cursor.execute(sql, all_params)
        self.conn.commit()
        count = self.cursor.rowcount
        print(f"✓ 更新成功，影响 {count} 条记录")
        return count
    
    def delete(self, table_name: str, where: str, params: Optional[tuple] = None) -> int:
        """
        删除数据
        
        Args:
            table_name: 表名
            where: WHERE 子句（不包含 WHERE 关键字）
            params: WHERE 子句的参数
        
        Returns:
            删除的行数
        """
        sql = f"DELETE FROM {table_name} WHERE {where}"
        
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        
        self.conn.commit()
        count = self.cursor.rowcount
        print(f"✓ 删除成功，影响 {count} 条记录")
        return count
    
    def execute_sql(self, sql: str, params: Optional[tuple] = None) -> Any:
        """
        执行自定义 SQL 语句
        
        Args:
            sql: SQL 语句
            params: SQL 参数
        
        Returns:
            查询结果（如果是 SELECT）或受影响的行数
        """
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        
        self.conn.commit()
        
        # 如果是 SELECT 语句，返回结果
        if sql.strip().upper().startswith('SELECT'):
            rows = self.cursor.fetchall()
            results = [dict(row) for row in rows]
            print(f"✓ SQL 执行成功，返回 {len(results)} 条记录")
            return results
        else:
            count = self.cursor.rowcount
            print(f"✓ SQL 执行成功，影响 {count} 条记录")
            return count
    
    def get_tables(self) -> List[str]:
        """获取数据库中所有表名"""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in self.cursor.fetchall()]
        return tables
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """获取表结构信息"""
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        rows = self.cursor.fetchall()
        columns = [dict(row) for row in rows]
        return columns


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='SQLite 数据库操作工具')
    parser.add_argument('db_path', help='数据库文件路径')
    parser.add_argument('operation', choices=['create_table', 'insert', 'query', 'update', 'delete', 'execute', 'list_tables', 'table_info'],
                       help='操作类型')
    parser.add_argument('--table', help='表名')
    parser.add_argument('--columns', help='列定义（JSON 格式）或查询的列名')
    parser.add_argument('--data', help='数据（JSON 格式）')
    parser.add_argument('--where', help='WHERE 子句')
    parser.add_argument('--params', help='SQL 参数（JSON 数组格式）')
    parser.add_argument('--order-by', help='ORDER BY 子句')
    parser.add_argument('--limit', type=int, help='限制返回的行数')
    parser.add_argument('--sql', help='自定义 SQL 语句')
    parser.add_argument('--output', help='输出文件（JSON 格式）')
    
    args = parser.parse_args()
    
    try:
        with SQLiteDB(args.db_path) as db:
            result = None
            
            if args.operation == 'create_table':
                if not args.table or not args.columns:
                    print("错误：create_table 需要 --table 和 --columns 参数")
                    sys.exit(1)
                columns = json.loads(args.columns)
                db.create_table(args.table, columns)
            
            elif args.operation == 'insert':
                if not args.table or not args.data:
                    print("错误：insert 需要 --table 和 --data 参数")
                    sys.exit(1)
                data = json.loads(args.data)
                if isinstance(data, list):
                    db.insert_many(args.table, data)
                else:
                    db.insert(args.table, data)
            
            elif args.operation == 'query':
                if not args.table:
                    print("错误：query 需要 --table 参数")
                    sys.exit(1)
                columns = args.columns or "*"
                params = json.loads(args.params) if args.params else None
                result = db.query(args.table, columns, args.where, 
                                params, args.order_by, args.limit)
                print(json.dumps(result, ensure_ascii=False, indent=2))
            
            elif args.operation == 'update':
                if not args.table or not args.data or not args.where:
                    print("错误：update 需要 --table、--data 和 --where 参数")
                    sys.exit(1)
                data = json.loads(args.data)
                params = json.loads(args.params) if args.params else None
                db.update(args.table, data, args.where, params)
            
            elif args.operation == 'delete':
                if not args.table or not args.where:
                    print("错误：delete 需要 --table 和 --where 参数")
                    sys.exit(1)
                params = json.loads(args.params) if args.params else None
                db.delete(args.table, args.where, params)
            
            elif args.operation == 'execute':
                if not args.sql:
                    print("错误：execute 需要 --sql 参数")
                    sys.exit(1)
                params = json.loads(args.params) if args.params else None
                result = db.execute_sql(args.sql, params)
                if isinstance(result, list):
                    print(json.dumps(result, ensure_ascii=False, indent=2))
            
            elif args.operation == 'list_tables':
                tables = db.get_tables()
                print("数据库中的表：")
                for table in tables:
                    print(f"  - {table}")
                result = tables
            
            elif args.operation == 'table_info':
                if not args.table:
                    print("错误：table_info 需要 --table 参数")
                    sys.exit(1)
                info = db.get_table_info(args.table)
                print(f"表 '{args.table}' 的结构：")
                print(json.dumps(info, ensure_ascii=False, indent=2))
                result = info
            
            # 如果指定了输出文件，保存结果
            if args.output and result is not None:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"✓ 结果已保存到 {args.output}")
    
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误：{e}")
        sys.exit(1)
    except sqlite3.Error as e:
        print(f"数据库错误：{e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误：{e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
