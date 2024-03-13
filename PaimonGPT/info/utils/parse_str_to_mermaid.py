# *_*coding:utf-8 *_*
# @Author : YueMengRui
import re

punctuationMap = {
    '，': ',',
    '；': ';',
    '。': '.',
    '：': ':',
    '！': '!',
    '？': '?',
    '“': '"',
    '”': '"',
    '‘': "'",
    '’': "'",
    '【': '[',
    '】': ']',
    '（': '(',
    '）': ')',
    '《': '<',
    '》': '>',
    '、': ','
}


def parse_str_to_mermaid(data: str):
    mermaid = ''
    ret = re.search(r'```mermaid[^`]+```', data)

    if ret is not None:
        mermaid = ret.group(0).replace('```mermaid', '').replace('```', '')
        mermaid = mermaid.lstrip()
        for k, v in punctuationMap.items():
            mermaid = mermaid.replace(k, v)

        mermaid = mermaid.replace('\n', ';').replace('(', ' ').replace(')', ' ').replace(';;', ';').replace(';;', ';')

    return mermaid
