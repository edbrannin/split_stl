import os

import click
import stl

def split(stl_data):
    groups = list()
    for facet in stl_data.facets:
        new = True
        for group in groups:
            if facet in group:
                group.add(facet)
                new = False
                continue
        if new:
            groups.append(FacetGroup(facet))
    while True:
        touched = False
        for group in groups:
            for other_group in groups:
                if group == other_group:
                    continue
                if group in other_group:
                    touched = True
                    group.merge(other_group)
                    groups.remove(other_group)
                    break
        if not touched:
            break
    return groups

class FacetGroup(object):
    def __init__(self, facet=None):
        self.facets = list()
        self.vertices = set()
        if facet:
            self.add(facet)

    def add(self, facet):
        self.facets.append(facet)
        if "vertices" in dir(facet):
            self.vertices = self.vertices.union(facet.vertices)

    def add_all(self, facets):
        for facet in facets:
            self.add(facet)

    def __contains__(self, facet):
        return self.vertices.intersection(set(facet.vertices))

    def merge(self, other):
        self.facets.extend(other.facets)
        self.vertices = self.vertices.union(other.vertices)

    def to_solid(self):
        return stl.Solid(facets=self.facets)


@click.group()
def main():
    pass

@main.command()
@click.argument("filename")
def split(filename):
    with open(filename) as f:
        data = stl.read_ascii_file(f)
        groups = split(data)
        print "Before: {}; after: {}".format(len(data.facets), len(groups))
        for i, group in enumerate(groups):
            out_name = "{}.{}.stl".format(os.path.splitext(filename)[0], i)
            with open(out_name, 'w') as out_file:
                group.to_solid().write_ascii(out_file)
                print "Wrote {}".format(out_name)


@main.command()
@click.argument("files", type=click.File(), nargs=-1)
@click.option("-o", "--out", default="-", type=click.File("w"))
def join(files, out):
    group = FacetGroup()
    for f in files:
        data = stl.read_ascii_file(f)
        group.add_all(data.facets)
    group.to_solid().write_ascii(out)

if __name__ == '__main__':
    main()

