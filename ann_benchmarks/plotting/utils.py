import os, json, pickle
from ann_benchmarks.main import get_fn
from ann_benchmarks.plotting.metrics import all_metrics as metrics
import matplotlib.pyplot as plt
import numpy

results_cache = {}
results_call_set = {}

def create_pointset(algo, all_data, xm, ym):
    data = all_data[algo]
    rev = ym["worst"] < 0
    data.sort(key=lambda (a, n, xv, yv): yv, reverse=rev) # sort by y coordinate
    ls = [t[1] for t in data]

    axs, ays = [], []
    # Generate Pareto frontier
    xs, ys = [], []
    last_x = xm["worst"]
    comparator = \
      (lambda xv, lx: xv > lx) if last_x < 0 else (lambda xv, lx: xv < lx)
    for algo, algo_name, xv, yv in data:
        axs.append(xv)
        ays.append(yv)
        if comparator(xv, last_x):
            last_x = xv
            xs.append(xv)
            ys.append(yv)
    return xs, ys, axs, ays, ls

def enumerate_query_caches(ds):
    for f in os.listdir("queries/"):
        if f.startswith(ds + "_") and f.endswith(".p"):
            yield "queries/" + f

def load_results(datasets, xm, ym, limit = -1):
    ds_id = "".join(datasets) + xm["description"] + ym["description"] + str(limit)
    if ds_id in results_call_set:
        return results_call_set[ds_id]

    runs = {}
    all_algos = set()
    for ds in datasets:
        results_fn = get_fn("results", ds)
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
        if not ds in results_cache:
            with open(get_fn("results", ds, limit)) as f:
                results_cache[ds] = []
                for line in f:
                    try:
                        l = json.loads(line)
                    except:
                        print "Skipping line"
                    results_cache[ds].append(l)

        for run in results_cache[ds]:
            algo = run["library"]
            algo_name = run["name"]
            build_time = run["build_time"]
            search_time = run["best_search_time"]

            print "--"
            print algo_name
            xv = xm["function"](queries, run)
            yv = ym["function"](queries, run)
            print xv, yv
            if not xv or not yv:
                continue

            all_algos.add(algo)
            if not algo in runs[ds]:
                runs[ds][algo] = []
            runs[ds][algo].append((algo, algo_name, xv, yv))
    results_call_set[ds_id] = (runs, all_algos)
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

