# *_*coding:utf-8 *_*
# @Author : yuemengrui
import hashlib
import os
from io import IOBase
from info import logger


def md5hex(data: bytes):
    try:
        m = hashlib.md5()
        m.update(data)
        return str(m.hexdigest())
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return ''


def md5salt(data: bytes):
    m = hashlib.md5(bytes('YueMengRui', encoding='utf-8'))
    m.update(data)
    return str(m.hexdigest())


def md5sum(fname):
    """ 计算文件的MD5值"""

    def read_chunks(fh):
        fh.seek(0)
        chunk = fh.read(8096)
        while chunk:
            yield chunk
            chunk = fh.read(8096)
        else:  # 最后要将游标放回文件开头
            fh.seek(0)

    m = hashlib.md5()
    if isinstance(fname, str) and os.path.exists(fname):
        with open(fname, "rb") as fh:
            for chunk in read_chunks(fh):
                m.update(chunk)
    # 上传的文件缓存 或 已打开的文件流
    elif isinstance(fname, IOBase):
        for chunk in read_chunks(fname):
            m.update(chunk)
    else:
        return ""
    return m.hexdigest()


# if __name__ == '__main__':
#     with open('/Users/yuemengrui/Downloads/2.jpg', 'rb') as f:
#         data = f.read()
#
#     h = md5hex(data)
#     print(h)
#     print(h == '081e8b9de5834f9951dfcd1dd60687d1')
#     # print(md5hex(open('/Users/yuemengrui/Downloads/2.jpg').read()))
