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


def balance_brackets(s):
    stack = []  # 创建一个栈来跟踪括号
    for char in s:
        if char == '[':
            stack.append(char)  # 遇到左括号，入栈
        elif char == ']':
            if stack and stack[-1] == '[':  # 如果栈顶是左括号，出栈
                stack.pop()
            else:
                # 如果栈顶不是左括号或者栈为空，说明右括号缺少配对
                # 在此处插入左括号以补全配对
                s = s[:s.index(char)] + '[' + s[s.index(char):]
                # 更新栈以反映新添加的左括号
                stack.append('[')
    # 检查栈中是否还有未配对的左括号
    if stack:
        # 如果有，说明缺少右括号，需要在字符串末尾补全
        for _ in stack:
            s += ']'
    return s


def parse_str_to_mermaid(data: str):
    mermaid = ''
    ret = re.search(r'```mermaid[^`]+```', data)

    if ret is not None:
        mermaid = ret.group(0).replace('```mermaid', '').replace('```', '')
        mermaid = mermaid.lstrip()
        if '//' in mermaid:
            mermaid = mermaid[:mermaid.index('//')]
        for k, v in punctuationMap.items():
            mermaid = mermaid.replace(k, v)

        mermaid = mermaid.replace('\n', ';').replace('(', ' ').replace(')', ' ').replace(';;', ';').replace(';;', ';')

        chunks = mermaid.split(';')

        for i in range(len(chunks)):
            chunks[i] = balance_brackets(chunks[i])

        mermaid = ';'.join(chunks)

    return mermaid
