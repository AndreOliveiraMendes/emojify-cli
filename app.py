#!usr/env python
def to_regional_indicator(msg):
    res = []
    for l in msg:
        if l.isalpha():
            res.append(f":regional_indicator_{l.lower()}:")
        else:
            res.append(l)
    return " ".join(res)

msg = input("msg:")
print(to_regional_indicator(msg))

