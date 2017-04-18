from datetime import datetime
from random import random, choice


class Entity(object):
    def __init__(self, x, y, z, name):
        self.x = x
        self.y = y
        self.z = z
        self.name = name


class AnonEntity(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def look_first(entities):
    for e in entities:
        if hasattr(e, 'name'):
            foo = "{}: {}".format(e.name, sum([e.x, e.y, e.z]))


def leap_first(entities):
    for e in entities:
        try:
            foo = "{}: {}".format(e.name, sum([e.x, e.y, e.z]))
        except AttributeError:
            pass


def leap_first_getattr(entities):
    for e in entities:
        try:
            foo = "{}: {}".format(getattr(e, 'name'), sum([e.x, e.y, e.z]))
        except AttributeError:
            pass

def leap_first_getattr_default(entities):
    for e in entities:
        name = getattr(e, 'name', None)
        if name:
            foo = "{}: {}".format(name, sum([e.x, e.y, e.z]))


names = ["alice", "bob", "charlie", "derek", "elanor", "francine", "georgia"]
entities = []
for i in range(100000):
    if i % 2 == 0:
        e = Entity(random(), random(), random(), choice(names))
    else:
        e = AnonEntity(random(), random(), random())

    entities.append(e)


start = datetime.now()
look_first(entities)
print "\n        Look first with hasattr: {}".format(datetime.now() - start)

start = datetime.now()
leap_first(entities)
print "            Leap first with try: {}".format(datetime.now() - start)

start = datetime.now()
leap_first_getattr(entities)
print "Leap first with try and getattr: {}".format(datetime.now() - start)

start = datetime.now()
leap_first_getattr_default(entities)
print "Leap first with getattr default: {}\n".format(datetime.now() - start)

# TODO: test entities with mostly anon and mostly named