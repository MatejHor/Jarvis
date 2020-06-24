

# Extract input parameters
def parse_elements(elements):
    all_elements = {}
    for name, element in elements:
        all_elements[name] = {}
        all_elements[name]['optional'] = element.is_optional
        if hasattr(element.type, 'elements'):
            all_elements[name]['data_type'] = parse_elements(element.type.elements)
        else:
            all_elements[name]['data_type'] = str(element.type)

    return all_elements


# Get methods names from soup services
def get_service_methods(service_client):
    methods_and_parameters = {}
    for service in service_client.wsdl.services.values():
        for port in service.ports.values():
            for operation in port.binding._operations.values():
                methods_and_parameters[operation.name] = parse_elements(operation.input.body.type.elements)
    return methods_and_parameters


# Import or install package zeep, re
def dynamic_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


dynamic_import('zeep')
dynamic_import('re')

# Load wsdl
wsdl = input('Enter wsdl url with ?wsdl at end -> ') or 'http://pis.predmety.fiit.stuba.sk/pis/ws/TextCipher?WSDL'

# Create soup client and get all methods
soup_client = zeep.Client(wsdl=wsdl)
methods = get_service_methods(soup_client)
print('methods for this wsdl -->', end='\n\t')
print(re.sub("[\[\]]", "", str(list(methods.keys()))))

# Load method which will be call
method = input('Enter method to execute -> ') or list(methods.keys())[0]

params = {}
if method in methods.keys():
    for param in methods[method]:
        param_value = input('\t\'' + param + '\' --> ' + re.sub("[{}]", "", str(methods[method][param])) + '\n\t') or None
        if not param_value and methods[method][param]['optional']:
            print('Skip this param')
        elif 'Double' in methods[method][param]['data_type']:
            try:
                params[param] = float(param_value)
            except:
                params[param] = 0.0
        elif 'Int' in methods[method][param]['data_type']:
            try:
                params[param] = int(param_value)
            except:
                params[param] = 0
        elif 'Boolean' in methods[method][param]['data_type']:
            try:
                params[param] = bool(param_value)
            except:
                params[param] = True
        else:
            params[param] = str(param_value)
else:
    print('method doesnt exist in this wsdl service', end='\n\t')
    exit()
print('params -> ' + re.sub("[{}]", "", str(params)), end='\n')

# Create object (wsd) with specific method
result = getattr(soup_client.service, method)
# Call wsdl method
result = result(**params, )

print('\n--------------------Result--------------------\n' + str(result))
