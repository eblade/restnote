import requests
from lxml import etree
from urllib.parse import urlparse, urlunparse, urlencode, parse_qsl
from daemonize import Daemonize

instances = {}


class Instance:
    def __init__(self, name, user, password, http_session, namespaces):
        self.name = name
        self.user = user
        self.password = password
        self.http_session = http_session
        self.namespaces = namespaces
        self.logger = None


def init(session_info, instance_name=None, logger=None):
    http_session = requests.Session()
    http_session.auth = (session_info.user, session_info.password)
    instance = Instance(
        instance_name,
        session_info.user,
        session_info.password,
        http_session,
        session_info.namespaces)
    instance.logger = logger
    instances[instance_name] = instance
    session_info.start(instance)


def log(desc, data=None, fmt=None, name=None):
    inst = instances[name]
    if inst.logger is None:
        return
    inst.logger.log(desc, data, fmt)


def die(message=None):
    raise ValueError("Missing required data: ", message)


def fill(data, var):
    for k, v in var.items():
        data = data.replace('(%s)' % str(k), str(v))
    return data


def template(template, subs, name=None):
    log('substituting', subs, 'pp', name=name)
    scheme, netloc, path, params, query, fragment = urlparse(template)
    qparams = parse_qsl(query)
    new_qparams = []
    for k, v in qparams:
        if v.startswith('{'):
            pname = v.replace('{', '').replace('}', '').replace('?', '')
            if pname in subs:
                new_qparams.append((k, subs[pname]))
        else:
            new_qparams.append((k, v))
    url = urlunparse((scheme, netloc, path, params,
                      urlencode(new_qparams), fragment))
    log('resulting url', url, name=name)
    return url


def run(application, action, mode='application'):
    if mode == 'application':
        action()
    elif mode == 'daemon':
        filenos = []
        for inst in instances.values():
            try:
                filenos.append(inst.fh.fileno())
            except AttributeError:
                pass
        pid = '/tmp/%s.pid' % application
        daemon = Daemonize(app="autopublish", pid=pid, action=action,
                           keep_fds=filenos)
        daemon.start()


def colorify(value, color, name=None):
    inst = instances[name]
    if inst.logger is None:
        return value
    try:
        return inst.logger.colorify(value, color)
    except:
        return value


########################
# HTTP related functions


def GET(url, accept=None, headers={}, name=None):
    inst = instances[name]
    if accept is not None:
        headers = dict(headers)
        headers['accept'] = accept
    log("GET >>> " + str(url), headers, 'pp', name=name)
    response = inst.http_session.get(url, headers=headers)
    log("GET <<< [%s]" % response.status_code,
        dict(response.headers), 'pp', name=name)
    log(None, response.content.decode(),
        'xml' if 'xml' in response.headers.get('content-type', '')
        else None, name=name)
    return response


def PUT(url, data, content_type, headers={}, name=None):
    inst = instances[name]
    headers = dict(headers)
    headers['content-type'] = content_type
    log("PUT >>> " + str(url), headers, 'pp', name=name)
    try:
        data = etree.tostring(data)
    except AttributeError:
        pass
    except TypeError:
        pass
    log(None, data, 'xml', name=name)
    response = inst.http_session.put(url, data=data, headers=headers)
    log("PUT <<< [%s]" % response.status_code,
        dict(response.headers), 'pp', name=name)
    log(None, response.content.decode(),
        'xml' if 'xml' in response.headers.get('content-type', '')
        else None, name=name)
    return response


def POST(url, data, content_type, headers={}, name=None):
    inst = instances[name]
    headers = dict(headers)
    headers['content-type'] = content_type
    log("POST >>> " + str(url), headers, 'pp', name=name)
    try:
        data = etree.tostring(data)
    except AttributeError:
        pass
    except TypeError:
        pass
    log(None, data, 'xml', name=name)
    response = inst.http_session.post(url, data=data, headers=headers)
    log("POST <<< [%s]" % response.status_code,
        dict(response.headers), 'pp', name=name)
    log(None, response.content.decode(),
        'xml' if 'xml' in response.headers.get('content-type', '')
        else None, name=name)
    return response


def DELETE(url, headers={}, name=None):
    inst = instances[name]
    headers = dict(headers)
    log("DELETE >>> " + url, headers, 'pp', name=name)
    response = inst.http_session.delete(url, headers=headers)
    log("DELETE <<< [%s]" % response.status_code,
        dict(response.headers), 'pp', name=name)
    log(None, response.content.decode(),
        'xml' if 'xml' in response.headers.get('content-type', '')
        else None, name=name)
    return response


#######################
# XML related functions


def xml(response):
    try:
        return etree.fromstring(response.content)
    except AttributeError:
        return etree.fromstring(response.encode())


def xpath(element, path, fmt=None, name=None):
    inst = instances[name]
    try:
        result = element.xpath(path, namespaces=inst.namespaces)
    except AttributeError:
        raise TypeError('%s is not a valid XML element' % str(element))
    if fmt is not list:
        try:
            result = result[0]
        except IndexError:
            if not result:
                result = None
    log("Resolve xpath", (path, result), 'pp')
    return result


def xmod(dom, path, new_value, name=None):
    if path == '.' or path is None:
        element = dom
    else:
        element = xpath(dom, path, name=name)
    if element is not None:
        element.text = new_value
        log("New value", new_value, 'pp')


def xattr(dom, path, attr, new_value, name=None):
    element = xpath(dom, path, name=name)
    if element is not None:
        element.set(attr, new_value)
        log("New attribute value", '%s = "%s"' %
            (attr, new_value), 'pp', name=name)


def xadd(dom, path, tag, name=None):
    inst = instances[name]
    element = xpath(dom, path, name=name)
    if element is not None:
        prefix, name = tag.split(':', 1)
        return etree.SubElement(element,
                                '{%s}%s' % (inst.namespaces.get(prefix), name))
