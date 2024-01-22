from typing import List
from .rdbms import RDBMSDatabase


class RdbmsSummary:
    """Get rdbms db table summary template.
    summary example:
    table_name(column1(column1 comment),column2(column2 comment),column3(column3 comment) and index keys, and table comment is {table_comment})
    """

    def __init__(self, host, port, username, password, db_name):
        self.summary_template = "{table_name}({columns})"

        try:
            self.db = RDBMSDatabase.from_uri_db(host=host, port=port, user=username, pwd=password, db_name=db_name)
        except Exception as e:
            raise f'db connect failure: {e}'

        self.metadata = """user info :{users}, grant info:{grant}, charset:{charset}, collation:{collation}""".format(
            users=self.db.get_users(),
            grant=self.db.get_grants(),
            charset=self.db.get_charset(),
            collation=self.db.get_collation(),
        )
        self.tables = self.db.get_table_names()
        self.table_info_summaries = [
            self.get_table_summary(table_name) for table_name in self.tables
        ]

    def get_table_summary(self, table_name):
        """Get table summary for table.
        example:
            table_name(column1(column1 comment),column2(column2 comment),column3(column3 comment) and index keys, and table comment: {table_comment})
        """
        return _parse_table_summary(self.db, self.summary_template, table_name)

    def table_summaries(self):
        """Get table summaries."""
        return self.table_info_summaries

    def get_table_info_with_json(self):
        tables = []
        for table_name in self.tables:
            columns = []
            for column in self.db._inspector.get_columns(table_name):
                column.update({'type': str(column['type'])})
                columns.append(column)
            tables.append({'table_name': table_name, 'columns': columns})

        return tables


def _parse_db_summary(
        conn: RDBMSDatabase, summary_template: str = "{table_name}({columns})"
) -> List[str]:
    """Get db summary for database.

    Args:
        conn (RDBMSDatabase): database connection
        summary_template (str): summary template
    """
    tables = conn.get_table_names()
    table_info_summaries = [
        _parse_table_summary(conn, summary_template, table_name)
        for table_name in tables
    ]
    return table_info_summaries


def _parse_table_summary(
        conn: RDBMSDatabase, summary_template: str, table_name: str
) -> str:
    """Get table summary for table.

    Args:
        conn (RDBMSDatabase): database connection
        summary_template (str): summary template
        table_name (str): table name

    Examples:
        table_name(column1(column1 comment),column2(column2 comment),column3(column3 comment) and index keys, and table comment: {table_comment})
    """
    columns = []
    for column in conn._inspector.get_columns(table_name):
        if column.get("comment"):
            columns.append(f"{column['name']} ({column.get('comment')})")
        else:
            columns.append(f"{column['name']}")

    column_str = ", ".join(columns)
    index_keys = []
    for index_key in conn._inspector.get_indexes(table_name):
        key_str = ", ".join(index_key["column_names"])
        index_keys.append(f"{index_key['name']}(`{key_str}`) ")
    table_str = summary_template.format(table_name=table_name, columns=column_str)
    if len(index_keys) > 0:
        index_key_str = ", ".join(index_keys)
        table_str += f", and index keys: {index_key_str}"
    try:
        comment = conn._inspector.get_table_comment(table_name)
    except Exception:
        comment = dict(text=None)
    if comment.get("text"):
        table_str += f", and table comment: {comment.get('text')}"
    return table_str
