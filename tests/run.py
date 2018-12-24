from incremental_trees.trees import StreamingRFC
from sklearn.ensemble import RandomForestClassifier
import dask_ml
import dask_ml.datasets
import dask_ml.cluster
from dask_ml.wrappers import Incremental
import dask as dd

x, y = dask_ml.datasets.make_blobs(n_samples=1e6,
                                   chunks=1e4,
                                   random_state=0,
                                   centers=3)

x = dd.dataframe.from_array(x)
y = dd.dataframe.from_array(y)

x.shape[0].compute()

ests_per_chunk = 2
chunks = len(x.divisions)

srfc = Incremental(StreamingRFC(n_estimators=ests_per_chunk,
                                max_n_estimators=chunks * ests_per_chunk))
srfc.fit(x, y)