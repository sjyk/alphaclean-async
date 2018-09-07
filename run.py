from quality.qfn import qfn, pointwise
from core.relation import relation
from quality.dc import dc, fd, md
from quality.logic import *
from core.single import satransform

from generators.exhaustive import exhaustive
from generators.noise import noise
from generators.outlier import outlier
from generators.dedup import dedup
from generators.minhash import minhash

from core.search import search, greedysearch, rgreedysearch, gridsearch, randomsearch

import distance


"""
data3 = [{"a": 'q', "b": "ny"},
        {"a": 'a', "b": "nyc"},
        {"a": 'f', "b": "chi"},
        {"a": 'g', "b": "mon"}]

data3 = data3

r = relation(data3)
r.setTypes(("cat", "cat"))

q = md(distance.levenshtein, ['b'], 2)

print(q.run(r))

t = satransform('b','nyc', 'ny',EQ)


rclean = t.apply(r)

print(rclean)

e = exhaustive(r)
for s in e.score(q):
    print(s)

si = search(r, q, exhaustive)
print(si.run())
"""
data4 = [{"a": 5, "b": "ny"},
        {"a": 6, "b": "nyc"},
        {"a": 100, "b": "chi"},
        {"a": 12, "b": "mon"}]
data4 = data4*100

r = relation(data4, ("a", "b"))
r.setTypes(("num", "cat"))
q = pointwise(lambda s: s['a'] > 30)
#q = md(distance.levenshtein, ['b'], 2) #pointwise(lambda s: s['a'] > 30) #md(distance.levenshtein, ['b'], 2) + pointwise(lambda s: s['a'] > 30)
#si = gridsearch(r, q, [minhash, outlier], [[(2,3), (3,6)], [1,2,3,4,5,6]])
#si = gridsearch(r, q, [dedup, minhash, outlier], [[(distance.levenshtein,3), (distance.levenshtein,6)], [(2,3), (3,6)], [1,2,3,4,5,6]])
#si = greedysearch(r, q, [minhash, noise, outlier], [[(2,3), (3,6)], [100], [1,2,3,4,5,6]])

si = rgreedysearch(r, q, [noise], [[100]])

print(si.run())
print(si.search_stats)
