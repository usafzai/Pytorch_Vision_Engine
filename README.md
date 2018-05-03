Benchmarking nearest neighbors
==============================

[![travis badge](https://img.shields.io/travis/erikbern/ann-benchmarks/master.svg?style=flat)](https://travis-ci.org/erikbern/ann-benchmarks)

Doing fast searching of nearest neighbors in high dimensional spaces is an increasingly important problem, but so far there has not been a lot of empirical attempts at comparing approaches in an objective way.

This project contains some tools to benchmark various implementations of approximate nearest neighbor (ANN) search for different metrics. We have pregenerated datasets (in HDF5) formats and we also have Docker containers for each algorithm. There's a [test suite](https://travis-ci.org/erikbern/ann-benchmarks) that makes sure every algorithm works.

Evaluated
=========

* [Annoy](https://github.com/spotify/annoy)
* [FLANN](http://www.cs.ubc.ca/research/flann/)
* [scikit-learn](http://scikit-learn.org/stable/modules/neighbors.html): LSHForest, KDTree, BallTree
* [PANNS](https://github.com/ryanrhymes/panns)
* [NearPy](http://nearpy.io)
* [KGraph](https://github.com/aaalgo/kgraph)
* [NMSLIB (Non-Metric Space Library)](https://github.com/searchivarius/nmslib): SWGraph, HNSW, BallTree, MPLSH
* [RPForest](https://github.com/lyst/rpforest)
* [FAISS](https://github.com/facebookresearch/faiss.git)
* [DolphinnPy](https://github.com/ipsarros/DolphinnPy)
* [Datasketch](https://github.com/ekzhu/datasketch)
* [PyNNDescent](https://github.com/lmcinnes/pynndescent)

Data sets
=========

We have a number of precomputed data sets for this. All data sets are pre-split into train/test and come with ground truth data in the form of the top 100 neighbors. We store them in a HDF5 format:

| Dataset                                                           | Dimensions | Train size | Test size | Neighbors | Distance  | Download                                                                     |
| ----------------------------------------------------------------- | ---------: | ---------: | --------: | --------: | --------- | ---------------------------------------------------------------------------- |
| [Fashion-MNIST](https://github.com/zalandoresearch/fashion-mnist) |        784 |     60,000 |    10,000 |       100 | Euclidean | [HDF5](http://vectors.erikbern.com/fashion-mnist-784-euclidean.hdf5) (217MB) |
| [GIST](http://corpus-texmex.irisa.fr/)                            |        960 |  1,000,000 |     1,000 |       100 | Euclidean | [HDF5](http://vectors.erikbern.com/gist-960-euclidean.hdf5) (3.6GB)          |
| [GloVe](http://nlp.stanford.edu/projects/glove/)                  |         25 |  1,183,514 |    10,000 |       100 | Angular   | [HDF5](http://vectors.erikbern.com/glove-25-angular.hdf5) (121MB)            |
| GloVe                                                             |         50 |  1,183,514 |    10,000 |       100 | Angular   | [HDF5](http://vectors.erikbern.com/glove-50-angular.hdf5) (235MB)            |
| GloVe                                                             |        100 |  1,183,514 |    10,000 |       100 | Angular   | [HDF5](http://vectors.erikbern.com/glove-100-angular.hdf5) (463MB)           |
| GloVe                                                             |        200 |  1,183,514 |    10,000 |       100 | Angular   | [HDF5](http://vectors.erikbern.com/glove-200-angular.hdf5) (918MB)           |
| [MNIST](http://yann.lecun.com/exdb/mnist/)                        |        784 |     60,000 |    10,000 |       100 | Euclidean | [HDF5](http://vectors.erikbern.com/mnist-784-euclidean.hdf5) (217MB)         |
| [NYTimes](https://archive.ics.uci.edu/ml/datasets/bag+of+words)   |        256 |    290,000 |    10,000 |       100 | Angular   | [HDF5](http://vectors.erikbern.com/nytimes-256-angular.hdf5) (301MB)         |
| [SIFT](https://corpus-texmex.irisa.fr/)                           |        128 |  1,000,000 |    10,000 |       100 | Euclidean | [HDF5](http://vectors.erikbern.com/sift-128-euclidean.hdf5) (501MB)          |

Results
=======


glove-100-angular

![glove-100-angular](https://raw.github.com/erikbern/ann-benchmarks/master/results/glove-100-angular.png)

sift-128-euclidean

![glove-100-angular](https://raw.github.com/erikbern/ann-benchmarks/master/results/sift-128-euclidean.png)

fashion-mnist-784-euclidean

![fashion-mnist-784-euclidean](https://raw.github.com/erikbern/ann-benchmarks/master/results/fashion-mnist-784-euclidean.png)

gist-960-euclidean

![gist-960-euclidean](https://raw.github.com/erikbern/ann-benchmarks/master/results/gist-960-euclidean.png)

nytimes-256-angular

![nytimes-256-angular](https://raw.github.com/erikbern/ann-benchmarks/master/results/nytimes-256-angular.png)

glove-25-angular

![glove-25-angular](https://raw.github.com/erikbern/ann-benchmarks/master/results/glove-25-angular.png)

Results as of Feb 2018-02-05, running all benchmarks on a c5.4xlarge machine on AWS.

Install
=======

The only prerequisite is Python (tested with 3.6) and Docker.

1. Clone the repo.
2. Run `pip install -r requirements.txt`.
3. Run `python install.py` to build all the libraries inside Docker containers (this can take a while, like 10-30 minutes).

Running
=======

1. Run `python run.py` (this can take an extremely long time, potentially days)
2. Run `python plot.py` to plot results.

You can customize the algorithms and datasets if you want to:

* Check that `algos.yaml` contains the parameter settings that you want to test
* To run experiments on SIFT, invoke `python run.py --dataset glove-100-angular`. See `python run.py --help` for more information on possible settings. Note that experiments can take a long time. 
* To process the results, either use `python plot.py --dataset glove-100-angular` or `python createwebsite.py`. An example call: `python createwebsite.py --plottype recall/time --latex --scatter --outputdir website/`. 

Including your algorithm
========================

1. Add your algorithm into `ann_benchmarks/algorithms` by providing a small Python wrapper.
2. Add a Dockerfile in `install/` for it
3. Add it to `algos.yaml`

Principles
==========

* Everyone is welcome to submit pull requests with tweaks and changes to how each library is being used.
* In particular: if you are the author of any of these libraries, and you think the benchmark can be improved, consider making the improvement and submitting a pull request.
* This is meant to be an ongoing project and represent the current state.
* Make everything easy to replicate, including installing and preparing the datasets.
* Try many different values of parameters for each library and ignore the points that are not on the precision-performance frontier.
* High-dimensional datasets with approximately 100-1000 dimensions. This is challenging but also realistic. Not more than 1000 dimensions because those problems should probably be solved by doing dimensionality reduction separately.
* No batching of queries, use single queries by default. ANN-Benchmarks saturates CPU cores by using a thread pool.
* Avoid extremely costly index building (more than several hours).
* Focus on datasets that fit in RAM. Out of core ANN could be the topic of a later comparison.
* We currently support CPU-based ANN algorithms. GPU support is planned as future work.
* Do proper train/test set of index data and query points.
* Note that Hamming distance and set similarity was supported in the past. This might hopefully be added back soon.

Authors
=======

Built by [Erik Bernhardsson](https://erikbern.com) with significant contributions from [Martin Aumüller](http://itu.dk/people/maau/) and [Alexander Faithfull](https://github.com/ale-f).
