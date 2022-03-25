
import numpy
import scipy.stats
import patsy
import pandas

from .summary import summarize
from .model import model
from .utility import *


def predict_y(mdl_data):
    """


    Parameters
    ----------
    mdl_data : ols or anova data object
        Class object which is returned from the ols or anova command.

    Returns
    -------
    Array
        Returns an array containing the linear prediction.

    """
    return mdl_data.IV @ mdl_data.model_data["betas"]


def residuals(mdl_data):
    """


    Parameters
    ----------
    mdl_data : ols or anova data object
        Class object which is returned from the ols or anova command.

    Returns
    -------
    Array
        Returns an array containing the residuals.

    """
    predicted_y = mdl_data.IV @ mdl_data.model_data["betas"]
    return mdl_data.DV - predicted_y


def standardized_residuals(mdl_data):
    """


    Parameters
    ----------
    mdl_data : ols or anova data object
        Class object which is returned from the ols or anova command.

    Returns
    -------
    Array
        Returns an array containing the standardized residuals.

    """
    resids = residuals(mdl_data)

    std_e = numpy.sqrt(
        (mdl_data.model_data["mse"] * (1 - numpy.diag(mdl_data.model_data["H"]))))

    t = resids / numpy.reshape(std_e, (mdl_data.nobs, 1))

    return t


def studentized_residuals(mdl_data):
    """


    Parameters
    ----------
    mdl_data : ols or anova data object
        Class object which is returned from the ols or anova command.

    Returns
    -------
    Array
        Returns an array containing the studentized (jackknifed) residuals.

    """

    d = []

    resid_standardized = standardized_residuals(mdl_data)
    n = mdl_data.nobs
    k = len(mdl_data._IV_design_info.column_names) - 1

    for i in range(0, n):

        r_i = resid_standardized[i]

        t_i = r_i * numpy.sqrt(((n - k - 2) / (n - k - 1 - r_i**2)))

        d.append(float(t_i))

    return numpy.array(d).reshape(n, 1)


def leverage(mdl_data):
    """


    Parameters
    ----------
    mdl_data : ols or anova data object
        Class object which is returned from the ols or anova command.

    Returns
    -------
    Array
        Returns an array containing the leverage of each observation.

    """

    return numpy.diag(mdl_data.model_data['H']).reshape(mdl_data.nobs, 1)


def predict(mdl_data={}, estimate=None):
    """


    Parameters
    ----------
    mdl_data : ols or anova data object
        Class object which is returned from the ols or anova command.

    estimate : string
        A string value to indicate which estimate is desired. Available options are:

            estimate in ["y", "xb"] : linear prediction
            estimate in ["residuals", "res", "r"] : residuals
            estimate in ["standardized_residuals", "standardized_r", "rstand"] : standardized residuals
            estimate in ["studentized_residuals", "student_r", "rstud"] : studentized (jackknifed) residuals
            estimate in ["leverage", "lev"] : The leverage of each observation


    Returns
    -------
    Array containing the desired estimate.

    """
    if estimate not in ["y", "xb", "residuals", "res", "r", "standardized_residuals", "standardized_r", "rstand", "studentized_residuals", "student_r", "rstud", "leverage", "lev"]:
        return print("\n", "ERROR: estimate option provided is not supported. Please use help(predict) for supported options.")

    if estimate in ["y", "xb"]:
        return predict_y(mdl_data)

    elif estimate in ["residuals", "res", "r"]:
        return residuals(mdl_data)

    elif estimate in ["standardized_residuals", "standardized_r", "rstand"]:
        return standardized_residuals(mdl_data)

    elif estimate in ["studentized_residuals", "student_r", "rstud"]:
        return studentized_residuals(mdl_data)

    elif estimate in ["leverage", "lev"]:
        return leverage(mdl_data)
