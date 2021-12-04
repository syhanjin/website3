# -*- coding: utf-8 -*-

def has(string, texts):
    for i in texts:
        if i in string:
            return True
    return False