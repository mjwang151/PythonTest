# -*- coding: utf-8 -*-

# @Time  : 2021/2/11 8:56 上午

# @Author : zcj

import json


class FastJson:
    def __str__(self):
        return f"{id(self)} @{self.__dict__}"

    __repr__ = __str__


class ArrayList(FastJson, list):
    def __init__(self, classz):
        super().__init__()
        self.type_tag = classz

        assert classz != type, "请传入类对象"

    def append(self, obj: object) -> None:
        assert isinstance(obj, self.type_tag), "传入的类型不一致"
        super().append(obj)

    def __str__(self):
        return list.__str__(self)

    def __repr__(self):
        return list.__repr__(self)


def jsonToPyobj(jsonDict: dict, pythonObj: object) -> object:
    assert isinstance(pythonObj, FastJson), "非FastJson类型对象"
    field_dict = pythonObj.__dict__

    def set_(k, v):
        if not isinstance(v, FastJson):
            pythonObj.__setattr__(k, jsonDict.get(k))
        if isinstance(v, FastJson):
            jsonToPyobj(jsonDict.get(k), v)

    for k, v in field_dict.items():
        if not isinstance(v, ArrayList):
            set_(k, v)
        if isinstance(v, ArrayList):
            arrayList = jsonDict.get(k)
            if arrayList is None:
                pythonObj.__setattr__(k, None)
                continue
            if len(arrayList) == 0:
                pythonObj.__setattr__(k, [])
                continue
            if FastJson not in v.type_tag.__bases__:
                for i in arrayList:
                    v.append(v.type_tag(i))
                pythonObj.__setattr__(k, v)
            else:
                for i in arrayList:
                    o = jsonToPyobj(i, v.type_tag())
                    v.append(o)
                pythonObj.__setattr__(k, v)
    return pythonObj


def do_obj_dict(pythonObj: object) -> dict:
    dict_1 = pythonObj.__dict__
    new_dict = {}

    def add(k, v):
        if not isinstance(v, FastJson):
            new_dict.update({k: v})
        if isinstance(v, FastJson):
            new_dict.update({k: do_obj_dict(v)})

    for k, v in dict_1.items():
        if k == "type__tag":
            continue
        if not isinstance(v, ArrayList):
            add(k, v)
        if isinstance(v, ArrayList):
            if len(v) == 0:
                new_dict.update({k: []})
                continue
            if FastJson not in v.type_tag.__bases__:
                new_list = [v.type_tag(i) for i in v]
                new_dict.update()
                new_dict.update({k: new_list})
            else:
                list2 = []
                for array in v:
                    res = do_obj_dict(array)
                    list2.append(res)
                new_dict.update({k: list2})
    return new_dict


def pyToJsonObj(pythonObj: object) -> str:
    if not isinstance(pythonObj, FastJson):
        raise Exception("非 FastJson 类型对象")
    return json.dumps(do_obj_dict(pythonObj))


if __name__ == '__main__':
    """
    测试 json 字符串 转成对象
    """


    class Person(FastJson):
        def __init__(self):
            self.name = None
            self.age = None


    class PoJO(FastJson):
        def __init__(self):
            self.name = None
            self.person = Person()
            self.list1 = ArrayList(int)
            self.personlist = ArrayList(Person)


    test_str = dict(name="pojo", person=dict(name="person", age=18), personlist=[], dad=1)
    # print(test_str)
    o: PoJO = jsonToPyobj(test_str, PoJO())
    print(o)


    # 测试 python 对象转json 字符串
    class Demo(FastJson):
        def __init__(self):
            self.name = None
            self.listPerson = ArrayList(Person)
            self.list1 = ArrayList(str)


    d: Demo = Demo()
    d.name = "小高"
    l = ArrayList(str)
    l.append("1")
    l.append("2")
    d.list1 = l
    p = Person()
    p.name = "大铁锤"
    p.age = 18
    d.listPerson.append(p)
    print(pyToJsonObj(d))
