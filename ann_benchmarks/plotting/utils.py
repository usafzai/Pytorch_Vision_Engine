from __future__ import absolute_import

import os, json, pickle
from ann_benchmarks.main import get_fn
from ann_benchmarks.results import get_results
from ann_benchmarks.plotting.metrics import all_metrics as metrics
import matplotlib.pyplot as plt
import numpy

def create_pointset(algo, all_data, xn, yn):
    xm, ym = (metrics[xn], metrics[yn])
    data = all_data[algo]
    rev = ym["worst"] < 0
    data.sort(key=lambda (a, n, rs): rs[yn], reverse=rev) # sort by y coordinate

    axs, ays, als = [], [], []
    # Generate Pareto frontier
    xs, ys, ls = [], [], []
    last_x = xm["worst"]
    comparator = \
      (lambda xv, lx: xv > lx) if last_x < 0 else (lambda xv, lx: xv < lx)
    for algo, algo_name, results in data:
        xv, yv = (results[xn], results[yn])
        if not xv or not yv:
            continue
        axs.append(xv)
        ays.append(yv)
        als.append(algo_name)
        if comparator(xv, last_x):
            last_x = xv
            xs.append(xv)
            ys.append(yv)
            ls.append(algo_name)
    return xs, ys, ls, axs, ays, als

def enumerate_query_caches(ds):
    for f in os.listdir("queries/"):
        if f.startswith(ds + "_") and f.endswith(".p"):
            yield "queries/" + f

def load_results(datasets, limit = -1):
    runs = {}
    all_algos = set()
    for ds in datasets:
        queries_fn = list(enumerate_query_caches(ds))
        assert len(queries_fn) > 0, '''\
no query cache files exist for dataset "%s"''' % ds
        if len(queries_fn) > 1:
            print """\
warning: more than one query cache file exists for dataset "%s", using only the
first (%s)""" % (ds, queries_fn[0])
        queries_fn = queries_fn[0]

        queries = pickle.load(open(queries_fn))
        runs[ds] = {}
        # XXX: these parameters won't be allowed to be None for long
        for run in get_results(ds, limit, None, None):
            algo = run["library"]
            algo_name = run["name"]
            build_time = run["build_time"]
            search_time = run["best_search_time"]

            print "--"
            print algo_name
            results = {}
            for name, metric in metrics.items():
                v = metric["function"](queries, run)
                results[name] = v
                if v:
                    print "%s: %g" % (name, v)

            all_algos.add(algo)
            if not algo in runs[ds]:
                runs[ds][algo] = []
            runs[ds][algo].append((algo, algo_name, results))
    return (runs, all_algos)

def create_linestyles(algos):
    colors = plt.cm.Set1(numpy.linspace(0, 1, len(algos)))
    faded = [[r, g, b, 0.3] for [r, g, b, a] in colors]
    linestyles = {}
    for i, algo in enumerate(algos):
        linestyles[algo] = (colors[i], faded[i], ['--', '-.', '-', ':'][i%4], ['+', '<', 'o', '*', 'x'][i%5])
    return linestyles

def get_up_down(metric):
    if metric["worst"] == float("inf"):
        return "down"
    return "up"

def get_left_right(metric):
    if metric["worst"] == float("inf"):
        return "left"
    return "right"

def get_plot_label(xm, ym):
    return "%(xlabel)s-%(ylabel)s tradeoff - %(updown)s and to the %(leftright)s is better" % {
            "xlabel" : xm["description"], "ylabel" : ym["description"], "updown" : get_up_down(ym), "leftright" : get_left_right(xm) }

