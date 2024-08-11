from jinja2 import Environment, FileSystemLoader
from jisx0213 import JISX0213

codeconv = JISX0213()
tables = []
for plane in range(1, 3):
    for row in range(1, 95):
        # plane 2 has only characters in rows 1, 3–5, 8, 12–15, 78–94.
        if plane == 2 and row not in (1, *range(3, 6), 8, *range(12, 16), *range(78, 95)):
            continue
        t = [None] * 100
        for cell in range(1, 95):
            cp = (plane - 1) * 0x8080 | (row + 0x20) << 8 | (cell + 0x20)
            u = codeconv.unicode(cp)
            t[cell] = u
        tables.append({ 'plane': plane, 'row': row, 'table': t })

env = Environment(loader=FileSystemLoader('templates'))
env.trim_blocks = True
env.lstrip_blocks = True
template = env.get_template('catalog.html')
content = template.render(char_table=tables)
print(content)
