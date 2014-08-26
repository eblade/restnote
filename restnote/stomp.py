import stomp
from urllib.parse import urlparse, parse_qs


class Client:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.connections = {}

    def listen(self, url, listener, auto_reconnect=True):
        urldata = urlparse(url)
        hostname = urldata.hostname
        port = urldata.port
        q = parse_qs(urldata.query)
        destination = q.get('destination')[0]

        conn = stomp.Connection([(hostname, port)],
                                user=self.user,
                                passcode=self.password)

        conn.set_listener('', listener)
        listener.connection = conn
        listener.auto_reconnect = auto_reconnect
        listener.destination = destination
        conn.start()
        conn.connect(wait=True)
        conn.subscribe(destination=destination, ack='auto')

        self.connections[url] = conn

    def __repr__(self):
        return "<restnote.stomp.Client>"

    def close(self, url):
        conn = self.connections.get(url)
        if conn is not None:
            conn.stop()
            del self.connections[url]


class Listener(stomp.ConnectionListener):
    def __init__(self):
        self.routes = {}
        self.auto_reconnect = False
        self.connection = None
        self.destination = None

    def __repr__(self):
        return "<restnote.stomp.Listener>"

    def on_error(self, headers, message):
        self.route('error', Response(headers, message, 500))

    def on_message(self, headers, message):
        self.route('message', Response(headers, message, 200))

    def on_connecting(self, hap):
        self.route('connecting', '%s:%s' % (hap[0], str(hap[1])))

    def on_disconnected(self):
        self.route('disconnected', None)
        if self.auto_reconnect:
            self.conn.connect(wait=True)
            self.conn.subscribe(destination=self.destination, ack='auto')

    def on_heartbeat_time_out(self):
        self.route('heartbeat_time_out', None)

    def route(self, where, what):
        if where in self.routes:
            callback = self.routes[where]
            callback = callback.copy()
            callback.var.update({callback.args[0]: what})
            callback.run()

    def register(self, where, callback):
        self.routes[where] = callback


class Response:
    def __init__(self, headers, content, status_code):
        self.headers = headers
        self.content = content.encode()
        self.status_code = status_code
