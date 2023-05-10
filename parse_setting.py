from yaml import load, Loader

from ast import literal_eval 

def flatten(d: dict, mode : str):
    for k, v in d[mode].items():
        d[k] = v
    ret = dict()
    for k, v in d.items():
        if isinstance(v, str):
            ret[k] = literal_eval(v) 
        else:
            ret[k] = v
    return ret


def parse_setting(fname: str, mode : str):
    return flatten(load(open(fname), Loader), mode)

if __name__ == '__main__':
    print(parse_setting("camera_setting.yml"))
