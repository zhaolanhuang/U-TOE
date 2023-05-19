import numpy as np
from scipy import stats as st

def analysis_compute_latency(trials_record):
    usec_array = np.array(trials_record['usec'])
    ci = st.t.interval(alpha=0.95, df=usec_array.size-1, loc=usec_array.mean(), scale=st.sem(usec_array))
    return {'95ci': ci, 
            'min': usec_array.min(), 'max' : usec_array.max(), 
            'mean': usec_array.mean(),
            'median': np.median(usec_array)}