def arg_check_type(args, types):

    single = True
    
    try:
        null = args.__iter__
        single = False
    except AttributeError:
        args = [args]

    try:
        null = types.__iter__
    except AttributeError:
        types = [types]
        
    length = min(len(args), len(types))
    for i in range(0, length):
        if type(args[i]) != types[i]:
            raise AssertionError("Bad argument type.")
            return i
    if single:
        return args[0]
    else:
        return tuple(args)

def arg_check_in(vals, data):

    single = True
    
    try:
        null = vals.__iter__
        single = False
    except AttributeError:
        vals = [vals]

    try:
        null = data.__iter__
    except AttributeError:
        data = [data]

    for i in vals:
        if i not in data:
            raise AssertionError("Argument(s) not in specified data")
            return i
    if single:
        return vals[0]
    else:
        return tuple(vals)
