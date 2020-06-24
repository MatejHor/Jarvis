#!/usr/bin/python


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


def dynamic_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


def get_methods(wsdl_url_=None):
    if not wsdl_url_:
        print('WSDL must be filled')
        exit()
    soup_client_ = zeep.Client(wsdl=wsdl_url_)
    methods_ = get_service_methods(soup_client_)
    print('methods for this wsdl are')
    print(re.sub("[\[\]]", "", str(list(methods_.keys()))))


def get_params(wsdl_url_=None, method_=None):
    if not wsdl_url_ or not method_:
        print('WSDL or METHOD must be filled')
        exit()
    soup_client_ = zeep.Client(wsdl=wsdl_url_)
    methods_ = get_service_methods(soup_client_)
    print('params for this wsdl and method are')
    print(re.sub("u'", "\n", re.sub("[{}]", "", str(methods_[method_]))))


dynamic_import('zeep')
dynamic_import('argparse')
dynamic_import('re')
dynamic_import('sys')

parser = argparse.ArgumentParser(description='Python SOAP')
parser.add_argument('-u', '--url', default='http://pis.predmety.fiit.stuba.sk/pis/ws/TextCipher?WSDL',
                    help='define wsdl url to use', type=str)
parser.add_argument('-m', '--method', default='encrypt_text', help='define method to use')
parser.add_argument('-p', '--param', help='define params to use divided with ","', nargs="*")

parser.add_argument('--methods', action='store_true', help='print all methods of wsdl')
parser.add_argument('--params', action='store_true', help='print all params of wsdl method')

args = parser.parse_args()
wsdl = args.url
method = args.method
params = {}

while args.param:
    params[args.param[0]] = args.param[1]
    args.param.remove(args.param[0])
    args.param.remove(args.param[0])

if args.methods:
    get_methods(wsdl)
    exit()

if args.params:
    get_params(wsdl, method)
    exit()

soup_client = zeep.Client(wsdl=wsdl)
methods = get_service_methods(soup_client)

try:
    method_index = int(method) % len(list(methods.keys()))
    method = list(methods.keys())[method_index]
except:
    method = list(methods.keys())[0] if method == "" else method

for param in params.keys():
    if 'Double' in methods[method][param]['data_type']:
        try:
            params[param] = float(params[param])
        except:
            params[param] = 0.0
            print('Soap ERROR: ' + param + ' param must be Double or Float, used 0.0')
    elif 'Int' in methods[method][param]['data_type']:
        try:
            params[param] = int(params[param])
        except:
            params[param] = 0
            print('Soap ERROR: ' + param + ' param must be Integer, used 0')
    elif 'Boolean' in methods[method][param]['data_type']:
        try:
            params[param] = bool(params[param])
        except:
            params[param] = True
            print('Soap ERROR: ' + param + ' param must be Boolean, used True')
    elif 'String' in methods[method][param]['data_type']:
        params[param] = str(params[param])

# Create object (wsd) with specific method
result = getattr(soup_client.service, method)
# Call wsdl method
try:
    result = result(**params)
    print(result)
except Exception as e:
    print('Soap ERROR: ' + str(e))
