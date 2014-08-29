from restnote.session import xpath, colorify, log, instances


def entry_mapper(entry, mapper, fields, graphical=False, name=None):
    values = {}
    for k in fields:
        v = mapper[k]
        value = xpath(entry, v['xpath'], name=name)
        if v.get('color-map', False):
            color = v.get('color-map').get(value) or 'black'
            value = colorify(value, color, name=name)
        if v.get('color', False):
            color = v.get('color')
            value = colorify(value, color, name=name)
        elif graphical:
            if v.get('template', False):
                value = v.get('template') % value
        values[k] = value
    return [values[field] for field in fields]


def feed_table(feed, mapper, fields, graphical=False, name=None):
    inst = instances.get(name)
    old_mute = None
    if inst.logger is not None:
        old_mute = inst.logger.mute
        inst.logger.mute = True
    headings = [mapper.get(field).get('title') for field in fields]
    rows = [entry_mapper(entry, mapper, fields, graphical, name=name)
            for entry in xpath(feed, '/atom:feed/atom:entry', list)]
    if inst.logger is not None:
        inst.logger.mute = old_mute
    log(headings, rows, 'table', name=name)
