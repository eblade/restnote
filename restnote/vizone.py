from restnote.session import GET, xml, xpath


class VizOneSession:
    namespaces = {
        "atom": "http://www.w3.org/2005/Atom",
        "vdf": "http://www.vizrt.com/types",
        "md": "http://ns.vizrt.com/ardome/metadata",
        "core": "http://ns.vizrt.com/ardome/core",
        "app": "http://www.w3.org/2007/app",
        "vaext": "http://www.vizrt.com/atom-ext",
        "vizid": "http://www.vizrt.com/opensearch/vizid",
        "mam": "http://www.vizrt.com/2010/mam",
        "dcterms": "http://purl.org/dc/terms/",
        "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
        "vizmedia": "http://www.vizrt.com/opensearch/mediatype",
        "media": "http://search.yahoo.com/mrss/",
        "vizsort": "http://www.vizrt.com/opensearch/sortorder",
        "time": "http://a9.com/-/opensearch/extensions/time/1.0/",
        "asbatch": "http://atomserver.org/namespaces/1.0/batch",
        "acl": "http://www.vizrt.com/2012/acl",
        "playout": "http://ns.vizrt.com/ardome/playout",
        "task": "http://ns.vizrt.com/ardome/task"
    }

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.instance = None
        self.secure = False

    def start(self, instance):
        self.instance = instance.name
        r = GET(
            '%s://%s/thirdparty' % (
                'https' if self.secure else 'http',
                self.host), name=self.instance)
        self.servicedoc = xml(r)

    def get_endpoint(self, api):
        return xpath(
            self.servicedoc,
            '/app:service/app:workspace/app:collection[app:categories/' +
            'atom:category[@scheme="http://www.vizrt.com/types"]/@term="' +
            api + '"]/@href', name=self.instance)

    def get_searchlink(self, api):
        return xpath(
            self.servicedoc,
            '/app:service/app:workspace/app:collection[app:categories/' +
            'atom:category[@scheme="http://www.vizrt.com/types"]/@term="' +
            api + '" and app:categories/atom:category[' +
            '@scheme="http://www.vizrt.com/types"]/@term="search"]/' +
            'atom:link[@rel="search"]/@href', name=self.instance)

    kw_colors = {
        'online': 'green',
        'offline': 'black',
        'importing': 'blue',
        'failed': 'red',
        'new': 'gray',
        'empty': 'gray',
    }

    atom_mapper = {
        'id': {'xpath': 'atom:id/text()', 'title': 'Id'},
        'title': {'xpath': 'atom:title/text()', 'title': 'Title'},
    }

    asset_mapper = dict(atom_mapper)
    asset_mapper.update({
        'thumb': {'xpath': 'media:thumbnail/@url',
                  'template': '<img src="%%s" />'},
        'status': {'xpath': 'mam:mediastatus/text()', 'title': 'Status',
                   'color-map': kw_colors},
        'type': {'xpath': 'vizmedia:media/text()', 'title': 'Type'},
    })
