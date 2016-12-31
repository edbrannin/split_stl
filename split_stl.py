import click
import stl
from path import Path

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
        self.vertices = self.vertices.union(facet.vertices)

    def __contains__(self, facet):
        return self.vertices.intersection(set(facet.vertices))

    def merge(self, other):
        self.facets.extend(other.facets)
        self.vertices = self.vertices.union(other.vertices)


@click.command()
def main(filename="HippoLeg.stl"):
    with open(filename) as f:
        data = stl.read_ascii_file(f)
        print len(data.facets)
        groups = split(data)
        print len(groups)

if __name__ == '__main__':
    main()

