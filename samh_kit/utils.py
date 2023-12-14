import numpy as np
import numpy.ma as ma
import pandas as pd


class mystat:
    def mb(obs, pred):
        return np.nanmean(pred - obs)

    def corr(obs, pred):
        return np.corrcoef(ma.masked_invalid(pred), ma.masked_invalid(obs))[
            0, 1
        ]

    def rmse(obs, pred):
        return np.sqrt(np.nanmean((pred - obs) ** 2))

    def mfb(obs, pred):
        return 2 * np.nanmean((pred - obs) / (pred + obs))

    def mfe(obs, pred):
        return 2 * np.nanmean(abs((pred - obs)) / (pred + obs))

    def evaluate_model(obs, pred):
        metrics = {}
        metrics["MB"] = "{:.2f}".format(np.nanmean(pred - obs))
        metrics["R"] = "{:.2f}".format(
            ma.corrcoef(ma.masked_invalid(pred), ma.masked_invalid(obs))[0, 1]
        )
        metrics["RMSE"] = "{:.2f}".format(
            np.sqrt(np.nanmean((pred - obs) ** 2))
        )
        metrics["MFB"] = "{:.2%}".format(
            2 * np.nanmean((pred - obs) / (pred + obs))
        )
        metrics["MFE"] = "{:.2%}".format(
            2 * np.nanmean(abs((pred - obs)) / (pred + obs))
        )
        return metrics

    def normalize(x):
        return (x - np.min(x)) / (np.max(x) - np.min(x))

    def timezone_to_local(
        data,
        dim="time",
        source_tz="UTC",
        target_tz="Asia/Shanghai",
        replace=True,
    ):
        time_sh = (
            pd.to_datetime(data[dim])
            .tz_localize(source_tz)
            .tz_convert(target_tz)
            .tz_localize(None)
        )
        if replace is True:
            data.coords[dim] = time_sh
        else:
            data.coords["time_loc"] = time_sh
        return data
