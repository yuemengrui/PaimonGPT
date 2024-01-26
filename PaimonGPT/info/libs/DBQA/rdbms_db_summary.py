import numpy as np
from typing import List
from copy import deepcopy
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

        self.tables = list(self.db.get_table_names())

        self.table_info_summaries = [self.get_table_summary(table_name) for table_name in self.tables]

        self.table_description = {}

        self.table_info_embeddings = None

    def load_table_embeddings(self, table_description):
        if self.embedding_model is not None:
            tables = []
            sentences = []
            for i in table_description:
                if i.get('is_deprecated', False):
                    continue

                table_examples = i.get('examples', '')

                col = []
                for c in i['columns']:
                    if c.get('is_deprecated', False):
                        continue
                    if c['comment']:
                        col.append(f"{c['name']}({c['comment']})")
                    else:
                        col.append(f"{c['name']}")

                if len(col) > 0:
                    col_str = ', '.join(col)

                    table_str = f"表名:{i['table_name']} 表描述:{i['table_comment']} - 详细字段: [{col_str}]"
                    sentences.append(table_str)
                    tables.append(i['table_name'])
                    self.table_description.update({i['table_name']: [table_str, table_examples]})

            if len(tables) > 0:
                try:
                    embeddings = servers_embedding_text(sentences=sentences, model_name=self.embedding_model).json()[
                        'embeddings']
                    self.table_info_embeddings = {tables[i]: np.array(embeddings[i]) for i in range(len(embeddings))}
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

                return '\n'.join([self.table_description[t][0] for t in related_tables]), '\n'.join([self.table_description[t][1] for t in related_tables])
        else:
            if len(self.table_description) > 0:
                return '\n'.join([v[0] for v in self.table_description.values()]), '\n'.join([v[1] for v in self.table_description.values()])

        return self.table_summaries(), ''

    def get_table_summary(self, table_name):
        """Get table summary for table.
        example:
            table_name(column1(column1 comment),column2(column2 comment),column3(column3 comment) and index keys, and table comment: {table_comment})
        """
        return _parse_table_summary(self.db, self.summary_template, table_name)

    def table_summaries(self):
        """Get table summaries."""
        return '\n'.join(self.table_info_summaries)

    def get_table_info_all(self):
        tables = []
        for table_name in self.tables:
            table_comment, columns = self.get_table_info_by_table(table_name)

            tables.append({'table_name': table_name, 'table_comment': table_comment, 'columns': columns})

        return tables

    def get_table_info_by_table(self, table_name):

        return _parse_table_comment(self.db, table_name), _parse_table_columns(self.db, table_name)


def _parse_table_comment(conn: RDBMSDatabase, table_name: str):
    table_comment = None
    try:
        table_comment = conn._inspector.get_table_comment(table_name).get('text')
    except Exception as e:
        logger.error({'EXCEPTION': e})

    return table_comment


def _parse_table_columns(conn: RDBMSDatabase, table_name: str):
    columns = []
    for column in conn._inspector.get_columns(table_name):
        col = deepcopy(column)
        col.update({'type': str(col['type'])})
        col.update({'is_deprecated': False})
        columns.append(col)

    return columns


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
