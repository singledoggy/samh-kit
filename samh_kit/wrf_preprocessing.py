def ppm_to_ugm3(pol, t2, psfc, M):
    """
    Transform concentration from ppm to ugm⁻3

    Parameters
    ----------
    pol : xarray DataArray
        Pollutant concentration in ppm.
    t2 : xarray DataArray
        Temperature at 2m (K).
    psfc : xarray DataArray
        Surface pressure (Pa).
    M : int
        Pollutant molecular mass.

    Returns
    -------
    None.

    """
    R = 8.3142  # J/K mol
    pol_ugm3 = pol * psfc * M / (R * t2)
    pol_ugm3 = pol_ugm3.rename(pol.name)
    return pol_ugm3


def ppm_convert_batch(ds, vars, dict_M=None):
    """
    ds: xarray Dataset default loaded by salem.open_wrf_dataset
    vars: list of variables to be converted
    dict_M: dictionary of molecular mass for each variable
    """
    psfc = ds["PSFC"]
    t2 = ds["T2"]

    if dict_M is None:
        dict_M = {"o3": 48, "no2": 46, "co": 28, "so2": 64}

    for var in vars:
        if var not in dict_M:
            raise ValueError(f"Variable '{var}' not found in dict_M \n {dict_M}")

    for var in vars:
        ds[var] = ppm_to_ugm3(ds[var], t2, psfc, dict_M[var])

    return ds
