# -*- coding: utf-8 -*-

import sys
import json
from pathlib import Path

class ImmutableDictKeyError(Exception):
    '''
    自定义异常
    '''

class ImmutableDict(dict):
    '''
    这是一个自定义字典类，同时具有两个功能：
    1.  可以新增键值对，但不能对已存在的键重新赋值，也不能删除已存在的键值对；
    2.  支持属性读写，可以像一般对象一样操作字典；
    '''
    def __instancecheck__(self, instance):
        if hasattr(instance, "hanser"):
            return True
        return False

    def __setitem__(self, key, value):
        if key in self:
            raise ImmutableDictKeyError('不允许更改已存在的键值对!')
        super().__setitem__(key, value)

    def __getitem__(self, item):
        return super().__getitem__(item)

    def __delitem__(self, item):
        if item in self:
            raise ImmutableDictKeyError('不允许删除已存在的键值对！')
        return super().__delitem__(item)

    def __setattr__(self, name, value):
        self.__setitem__(name, value)

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __delattr__(self, item):
        return self.__delitem__(item)

    def pop(self, item):
        if item in self:
            raise ImmutableDictKeyError('不允许删除已存在的键值对！')
        return super().pop(item)

    def popitem(self):
        if len(self) > 0:
            raise ImmutableDictKeyError('不允许删除键值对！')
        return super().popitem()

def dict2obj(dictObj):
    '''
    将普通字典对象转换成ImmutableDict字典对象
    '''
    if not isinstance(dictObj, dict):
        return dictObj
    d = ImmutableDict()
    for k, v in dictObj.items():
        d[k] = dict2obj(v)
    return d

def json2dict(json_path, dump=False):
    '''
    读取json文件内容并返回字典对象
    '''
    d = {}
    json_file = Path(json_path)
    if json_file.is_file():
        try:
            with json_file.open('r', encoding='utf-8') as f:
                d = json.load(f)
            if dump:
                if len(d) > 0:
                    print(json.dumps(d, indent=4))
        except Exception as e:
            print('读取json文件{}出错！错误原因：{}'.format(json_path, repr(e)))
    return d

if __name__ == '__main__':
    CURRENT_DIR = Path(__file__).resolve().parent
    sw1_path = CURRENT_DIR.joinpath('sw1.json')
    sw1 = dict2obj(json2dict(sw1_path, dump=True))
    print(sw1.name)
    print(sw1.type)
    print(sw1.ip)
    print(sw1.telnet.support)
    print(sw1.telnet.port)
    print(sw1.interface.p1)
    print(sw1.interface.p20)