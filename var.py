# global variable

from threading import Lock
lock = Lock()

class GlobalVar:
    var_set = {}


def set(var_name, var_value):
    lock.acquire()
    GlobalVar.var_set[var_name] = var_value
    lock.release()


def get(var_name, default_value):
    lock.acquire()
    if not var_name in GlobalVar.var_set:
        GlobalVar.var_set[var_name] = default_value
    result = GlobalVar.var_set[var_name]
    lock.release()
    return result

