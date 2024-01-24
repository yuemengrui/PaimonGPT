import numpy as np
from typing import List
from mylogger import logger
from .rdbms import RDBMSDatabase
from info.utils.api_servers.llm_base import servers_embedding_text


class RdbmsSummary:
    """Get rdbms db table summary template.
    summary example:
    table_name(column1(column1 comment),column2(column2 comment),column3(column3 comment) and index keys, and table comment is {table_comment})
    """

    def __init__(self, host, port, username, password, db_name, embedding_model=None):
        self.summary_template = "{table_name}({columns})"

        self.embedding_model = embedding_model

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
        self.tables = list(self.db.get_table_names())

        self.table_info_summaries = {table_name: self.get_table_summary(table_name) for table_name in self.tables}

        self.table_info_embeddings = None
        self.get_table_embedding()

    def get_table_embedding(self):
        if self.embedding_model is not None:
            sentences = [self.get_table_summary(table_name) for table_name in self.tables]
            try:
                embeddings = servers_embedding_text(sentences=sentences, model_name=self.embedding_model).json()[
                    'embeddings']
                self.table_info_embeddings = {self.tables[i]: np.array(embeddings[i]) for i in range(len(embeddings))}
            except Exception as e:
                logger.error({'EXCEPTION': e})

    def get_related_table_summaries(self, query, limit=5, threshold=None):
        if len(self.tables) > 3 and self.table_info_embeddings is not None:
            try:
                query_embedding = np.array(
                    servers_embedding_text(sentences=[query], model_name=self.embedding_model).json()['embeddings'][0])
            except Exception as e:
                logger.error({'EXCEPTION': e})
            else:
                table_scores = []
                for t_name, emb in self.table_info_embeddings.items():
                    cos_sim = query_embedding.dot(emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb))
                    if isinstance(threshold, (int, float)):
                        if cos_sim < threshold:
                            continue

                    table_scores.append([t_name, cos_sim])

                table_scores.sort(key=lambda x: x[1], reverse=True)
                related_tables = [x[0] for x in table_scores[:limit]]

                return '\n'.join([self.table_info_summaries[t] for t in related_tables])

        return self.table_summaries()

    def get_table_summary(self, table_name):
        """Get table summary for table.
        example:
            table_name(column1(column1 comment),column2(column2 comment),column3(column3 comment) and index keys, and table comment: {table_comment})
        """
        return _parse_table_summary(self.db, self.summary_template, table_name)

    def table_summaries(self):
        """Get table summaries."""
        return '\n'.join(list(self.table_info_summaries.values()))

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
