# Desc: File I/O utilities
import itertools
import numpy as np
import pandas as pd
import xarray as xr


def split_by_chunks(dataset):
    chunk_slices = {}
    for dim, chunks in dataset.chunks.items():
        slices = []
        start = 0
        for chunk in chunks:
            if start >= dataset.sizes[dim]:
                break
            stop = start + chunk
            slices.append(slice(start, stop))
            start = stop
        chunk_slices[dim] = slices
    for slices in itertools.product(*chunk_slices.values()):
        selection = dict(zip(chunk_slices.keys(), slices))
        yield dataset[selection]


def create_filepath(ds, prefix='filename', root_path="."):
    """
    Generate a filepath when given an xarray dataset
    """

    if isinstance(ds.time.data[0], np.datetime64):
        start = ds.time.data[0].astype('datetime64[D]').astype(str)
        end = ds.time.data[-1].astype('datetime64[D]').astype(str)
    elif isinstance(ds.time.data[0], pd.Timestamp):
        start = ds.time.data[0].strftime('%Y-%m-%d')
        end = ds.time.data[-1].strftime('%Y-%m-%d')
    else:
        raise ValueError("Unsupported time format")

    filepath = f'{root_path}/{prefix}_{start}_{end}.nc'
    return filepath
