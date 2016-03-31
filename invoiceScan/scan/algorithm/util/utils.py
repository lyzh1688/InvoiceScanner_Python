def enum(args, start=0):
    class Enum(object):
        __slots__ = args.split(',')
        def __init__(self):
            for i, key in enumerate(Enum.__slots__, start):
                setattr(self, key, i)
    return Enum()
