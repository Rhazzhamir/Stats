from text_to_array import textfile_to_farray
import numpy as np
import statistics
import warnings


def central_tendency(data):
    mode = statistics.multimode(data)
    result = {
        'N': len(data),
        'mean': np.mean(data),
        'median': np.median(data),
        'mode': [] if len(data) == len(set(data)) else mode
    }
    return result


def percentile(data, p):
    if p < 0 and p > 100:
        return
    
    n = len(data)

    if n == 1:
        return data[0]
    
    k = (n + 1) * (p / 100)
    i = int(k)
    d = k - float(i)
    if d == 0:
        return data[i - 1]
    else:
        if len(data) > 1:
            r = (data[i] - data[i - 1]) * d
        else:
            r = data[i - 1] * d
        return data[i - 1] + r


def measure_of_location(data, *args):
    data.sort()
    result = {
        'min': data[0],
        'max': data[-1],
        'Q1': percentile(data, 25),
        'Q2': percentile(data, 50),
        'Q3': percentile(data, 75)
    }
    for k in args:
        p = int(k[1:])
        if k[0].upper() == 'P':
            result[k] = percentile(data, p)
        elif k[0].upper() == 'D' and (p > 0 and p < 10):
            p *= 10
            result[k] = percentile(data, p)
        else:
            raise Exception
    return result


def measure_of_dispersion(data):
    data.sort()
    result = {
        'range': data[-1] - data[0],
        'IQR': percentile(data, 75) - percentile(data, 25),
        'sample variance': np.var(data, ddof=1),
        'population variance': np.var(data)
    }
    result['sample standard deviation'] = np.sqrt(result['sample variance'])
    result['population standard deviation'] = np.sqrt(
        result['population variance'])
    result['cofficient of variation'] = (
        result['sample standard deviation'] / np.mean(data)) * 100
    return result


def skew(data):
    result = {'Sk₁': {}}
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        modes = statistics.multimode(data)
        if len(modes) == len(set(data)):
            modes = []
        stddev = np.sqrt(np.var(data, ddof=1))
        mean = np.mean(data)
        N = len(data)
        if not stddev or np.isnan(stddev) or np.isinf(stddev):
            return {
                'Sk₁': 'Zero Division Error',
                'Sk₂': 'Zero Division Error',
                'moment-based': 'Zero Division Error'
            }

        for mode in modes:
            result['Sk₁'][mode] = (mean - mode) / stddev

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        try:
            result['Sk₂'] = (3 * (mean - np.median(data))) / stddev
        except (ZeroDivisionError, RuntimeWarning):
            result['Sk₂'] = 'Zero Division Error'

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        try:
            result['moment-based'] = (N / ((N - 1) * (N - 2))) * \
                (np.sum((data - mean) ** 3) / stddev ** 3)
        except (ZeroDivisionError, RuntimeWarning):
            result['moment-based'] = 'Zero Division Error'

    skewness = None
    if isinstance(result['moment-based'], float):
        skewness = result['moment-based']
    elif isinstance(result['Sk₂'], float):
        skewness = result['Sk₂']
    elif result['Sk₁']:
        skewness = result['Sk₁'][list(result['Sk₁'].keys())[0]]

    if skewness is not None:
        if skewness == 0:
            result['interpretation'] = 'Symmetric Distribution'
        elif skewness < 0:
            result['interpretation'] = 'Negatively Skewed Distribution (Skewed to the left)'
        elif skewness > 0:
            result['interpretation'] = 'Positively Skewed Distribution (Skewed to the right)'

        if skewness == 0:
            result['degree of skewness'] = 'Symmetric'
        elif skewness >= -0.5 and skewness <= 0.5:
            result['degree of skewness'] = 'Approximately Symmetric'
        elif skewness >= -1.0 and skewness <= 1.0:
            result['degree of skewness'] = 'Moderately Skewed'
        elif skewness < -1.0 or skewness > 1.0:
            result['degree of skewness'] = 'Highly Skewed'

    return result


def kurt(data):
    result = {}
    with warnings.catch_warnings():
        warnings.filterwarnings("error")
        try:
            mean = np.mean(data)
            N = len(data)
            m2 = (N * np.sum(data ** 2) - np.sum(data) ** 2) / N ** 2
            m4 = (np.sum(data ** 4) / N) - 4 * mean * (np.sum(data ** 3) /N) + 6 * mean ** 2 * (np.sum(data ** 2) / N) - 3 * mean ** 4

            result['Kurt₁'] = m4 / m2 ** 2
        except (ZeroDivisionError, RuntimeWarning):
            return {'Kurt₁': 'Zero Division Error', 'Kurt₂': 'Zero Division Error'}

        try:
            result['Kurt₂'] = (((N + 1) * (N - 1)) / ((N - 2) * (N - 3))) * \
                (result['Kurt₁'] - ((3 * (N - 1) / (N + 1))))

            if result['Kurt₂'] < 0:
                result['interpretation'] = 'platykurtic'
            elif result['Kurt₂'] > 0:
                result['interpretation'] = 'leptokurtic'
            elif result['Kurt₂'] == 0:
                result['interpretation'] = 'mesokurtic'
            return result
        except (ZeroDivisionError, RuntimeWarning):
            result['Kurt₂'] = 'Zero Division Error'
            if result['Kurt₁'] < 3:
                result['interpretation'] = 'platykurtic'
            elif result['Kurt₁'] > 3:
                result['interpretation'] = 'leptokurtic'
            elif result['Kurt₁'] == 3:
                result['interpretation'] = 'mesokurtic'
            return result


def population_moment(data):
    result = {}
    mean = np.mean(data)
    stddev = np.sqrt(np.var(data))
    N = len(data)
    sum2 = np.sum((data - mean) ** 2)
    sum3 = np.sum((data - mean) ** 3)
    sum4 = np.sum((data - mean) ** 4)

    result['raw'] = {
        'm1': mean,
        'm2': np.sum(data ** 2) / N,
        'm3': np.sum(data ** 3) / N,
        'm4': np.sum(data ** 4) / N
    }
    result['central'] = {
        'm2': sum2 / N,
        'm3': sum3 / N,
        'm4': sum4 / N
    }
    result['standard'] = {
        'm2': result['central']['m2'],
        'm3': (1 / N) * (sum3 / stddev ** 3),
        'm4': (1 / N) * (sum4 / stddev ** 4)
    }
    # (m2) Second standardised moment
    result['var'] = result['standard']['m2']
    # (m3) Third standardised moment
    result['skew'] = result['standard']['m3']
    # (m4) Fourth standardised moment
    result['kurt'] = result['standard']['m4'] - 3
    return result


def sample_moment(data):
    mean = np.mean(data)
    stddev = np.sqrt(np.var(data, ddof=1))
    N = len(data)
    result = population_moment(data)

    left = ((N * (N + 1)) / ((N - 1) * (N - 2) * (N - 3)))
    central = (np.sum((data - mean) ** 4) / stddev ** 4)
    right = (3 * (N - 1) ** 2) / ((N - 2) * (N - 3))

    result['standard'] = {
        'm2': np.sum(data ** 2 - mean) / (N - 1),
        'm3': (N / ((N - 1) * (N - 2))) * (np.sum((data - mean) ** 3) / stddev ** 3),
        'm4': left * central - right
    }
    # (m2) Second centralised moment
    result['var'] = result['standard']['m2']
    # (m3) Third standardised moment
    result['skew'] = result['standard']['m3']
    # (m4) Fourth standardised moment
    result['kurt'] = result['standard']['m4']
    return result
