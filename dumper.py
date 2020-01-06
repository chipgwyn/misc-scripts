def dumper(obj, indent=0):
    if isinstance(obj, dict):
        print('  ' * indent + '{')
        for key, val in obj.items():
            if isinstance(val, (dict, list, tuple)):
                print('  ' * (indent + 1) + str(key) + ': ')
                dumper(val, indent + 2)
            else:
                print('  ' * (indent + 1) + str(key) + ': ' + str(val))
        print('  ' * indent + '}')
    elif isinstance(obj, list):
        print('  ' * indent + '[')
        for item in obj:
            dumper(item, indent + 1)
        print('  ' * indent + ']')
    elif isinstance(obj, tuple):
        print('  ' * indent + '(')
        for item in obj:
            dumper(item, indent + 1)
        print('  ' * indent + ')')
    else:
        print('  ' * indent + str(obj))

