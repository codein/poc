import os
import logging
import sqlite3
import pandas as pd

SQL_LOADER_HOME = '~/temp/sql_loader_home'
DB_NAME = 'sql_loader_1.db'
db_path = os.path.expanduser('{0}/{1}'.format(SQL_LOADER_HOME, DB_NAME))

select_command_template = """
select count(*) from {table_name}
"""

select_by_primary_key_command_template = """
select * from {table_name}
where
{primary_key_where_clause}
"""

update_command_template_base = """
update {table_name} set
{set_list}
where
{primary_key_where_clause}
"""

insert_command_template_base = """
INSERT INTO {table_name}
{column_names}
VALUES
{value_names}
"""

def get_logger(name):
    FORMAT = '%(asctime)-15s %(name)s %(filename)s:%(lineno)d - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    logger = logging.getLogger(name)
    return logger

logger = get_logger('l0-base')

def get_db_connection():
    conn = sqlite3.connect(db_path)
    return conn

class SQLite_Upsert_Loader_Class(object):
    """
    Class used to update or insert flat files into a connected
    database by harnessing multiprocessing pools
    """
    def __init__(self, *args, **kwargs):
        super(SQLite_Upsert_Loader_Class, self).__init__()
        self.logger = get_logger('sqlite-upsert-loader-base')
        self.connection = get_db_connection()
        for key, value in kwargs.items():
              setattr(self, key, value)
        self.data_fields = self.df.columns.to_list()
        [self.data_fields.remove(primary_key) for primary_key in self.primary_keys]

    @staticmethod
    def _get_set_list(row_data, fields):
        set_list = []
        for field in fields:
            value = row_data[field]
            if pd.isnull(value):
                setter = '[{0}]={{{0}}}'.format(field)
            else:
                setter = '[{0}]=\'{{{0}}}\''.format(field)
            set_list.append(setter)
        return ', '.join(set_list)

    @staticmethod
    def _get_column_names(fields):
        column_names = ['[{0}]'.format(field) for field in fields]
        return '({0})'.format(', '.join(column_names))

    @staticmethod
    def _get_value_names(row_data, fields):
        column_names = ['{{{0}}}'.format(field) for field in fields]
        value_names = []
        for field in fields:
            value = row_data[field]
            if pd.isnull(value):
                value_name = '{{{0}}}'.format(field)
            else:
                value_name = '\'{{{0}}}\''.format(field)
            value_names.append(value_name)

        return '({0})'.format(', '.join(value_names))

    @staticmethod
    def _get_primary_key_where_clauses(primary_keys):
        clauses = []
        for primary_key in primary_keys:
            clauses.append('[{0}]=\'{{{0}}}\''.format(primary_key))

        return ' and '.join(clauses)


    @staticmethod
    def _execute(cursor, sql_query):
        try:
            cursor.execute(sql_query)
        except Exception as e:
            print(sql_query)

    @staticmethod
    def _replace_nan(row_data, fields):
        data = {}
        for field in fields:
            value = row_data[field]
            if pd.isnull(value):
                data[field] = 'null'
            else:
                data[field] = row_data[field]

        return data


    @staticmethod
    def _update_row(row_data, cursor, table_name, primary_keys, data_fields, execute=True):
        primary_key_where_clause = SQLite_Upsert_Loader_Class._get_primary_key_where_clauses(primary_keys)
        set_list = SQLite_Upsert_Loader_Class._get_set_list(row_data, data_fields)

        update_query_template = update_command_template_base.format(
            table_name=table_name,
            set_list=set_list,
            primary_key_where_clause=primary_key_where_clause)

        row_data = SQLite_Upsert_Loader_Class._replace_nan(row_data, primary_keys + data_fields)
        update_query = update_query_template.format(**row_data)
        if execute:
            SQLite_Upsert_Loader_Class._execute(cursor, update_query)
        return update_query

    @staticmethod
    def _insert_row(row_data, cursor, table_name, primary_keys, data_fields, execute=True):
        primary_key_where_clause = SQLite_Upsert_Loader_Class._get_primary_key_where_clauses(primary_keys)
        column_names = SQLite_Upsert_Loader_Class._get_column_names(primary_keys + data_fields)
        value_names= SQLite_Upsert_Loader_Class._get_value_names(
            row_data,
            primary_keys + data_fields
        )

        insert_query_template = insert_command_template_base.format(
            table_name=table_name,
            column_names=column_names,
            value_names=value_names)

        row_data = SQLite_Upsert_Loader_Class._replace_nan(row_data, primary_keys + data_fields)

        insert_query = insert_query_template.format(**row_data)
        if execute:
            SQLite_Upsert_Loader_Class._execute(cursor, insert_query)
        return insert_query

    @staticmethod
    def insert_or_update(cnxn, row_data, table_name, primary_keys, data_fields, dry_run=True):
        primary_key_where_clause = SQLite_Upsert_Loader_Class._get_primary_key_where_clauses(primary_keys)
        select_query_template = select_by_primary_key_command_template.format(
            table_name=table_name,
            primary_key_where_clause=primary_key_where_clause)
        cursor = cnxn.cursor()
        select_query = select_query_template.format(**row_data)

        SQLite_Upsert_Loader_Class._execute(cursor, select_query)
        select_count = 1
        update_count = 0
        insert_count = 0
        row =  cursor.fetchone()

        query = ''
        execute = not dry_run
        if row:
            query = SQLite_Upsert_Loader_Class._update_row(row_data, cursor, table_name, primary_keys, data_fields, execute=execute )
            update_count += 1
        else:
            query =SQLite_Upsert_Loader_Class._insert_row(row_data, cursor, table_name, primary_keys, data_fields, execute=execute)
            insert_count += 1


        if not dry_run:
            cnxn.commit()

        log = {
            'selects': select_count,
            'updates': update_count,
            'inserts': insert_count,
        }
        return (log, query)

    @staticmethod
    def parallel_insert_or_update_records(df, connection_string, table_name, primary_keys, data_fields, dry_run=True):
        batches = create_batches(df, connection_string, table_name, primary_keys, data_fields, dry_run)
        pool = Pool(5)
        list_batched_transactions = pool.map(get_batched_upsert_transactions, batches)
        pool.close()
        pool.join()

        logs = []
        for batched_transactions in list_batched_transactions:
            log = execute_batched_transactions(batched_transactions)
            logs.append(log)

        logs_df = pd.DataFrame(logs)
        logs_dict = {
            'selects': logs_df.selects.sum(),
            'updates': logs_df.updates.sum(),
            'inserts': logs_df.inserts.sum(),
            'table_name': table_name
        }
        logging.info('{table_name} selects:{selects} inserts:{inserts} updates:{updates}'.format(**logs_dict))


    def execute(self):
        logs = []
        for index,row in self.df.iterrows():
            (log, query) = SQLite_Upsert_Loader_Class.insert_or_update(
                self.connection,
                row,
                self.table_name,
                self.primary_keys,
                self.data_fields,
                dry_run=self.dry_run
            )
            logs.append(log)
        self.connection.close()

        logs_df = pd.DataFrame(logs)
        logs_dict = {
            'selects': logs_df.selects.sum(),
            'updates': logs_df.updates.sum(),
            'inserts': logs_df.inserts.sum(),
            'table_name': self.table_name
        }
        logging.info('{table_name} selects:{selects} inserts:{inserts} updates:{updates}'.format(**logs_dict))

