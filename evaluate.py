from riotctrl.ctrl import RIOTCtrl
import re
import analysis
from tabulate import tabulate
from datetime import datetime
from connector import get_local_controller, get_fit_iotlab_controller
import json
from model_converter import load_model, compile_per_model_eval, load_from_tflite
from utils import generate_model_io_vars_header, extract_io_vars_from_module

LOG_DIR = './logs'

def evaluate_per_model(model_path, board='stm32f746g-disco', trials_num=10, use_iotlab=False, iotlab_node=None, random_seed=42):
    mod, params = load_model(model_path)
    moudle = compile_per_model_eval(mod, params, board, './models/default/default.tar')
    input_vars, output_vars = extract_io_vars_from_module(moudle)
    generate_model_io_vars_header(input_vars=input_vars, output_vars=output_vars)

    env = {'BOARD': board, 'UTOE_TRIAL_NUM': str(trials_num), 'UTOE_RANDOM_SEED': str(random_seed)}
    print('Flashing...')

    if use_iotlab:
        riot_ctrl = get_fit_iotlab_controller(env, iotlab_node=iotlab_node)
        if iotlab_node is not None:
            riot_ctrl.flash(stdout=None)
    else:
        riot_ctrl = get_local_controller(env)
        riot_ctrl.flash(stdout=None)

    print('Flashing...done')
    with riot_ctrl.run_term(reset=True): #reset should be false for risc v
        try:
            # riot_ctrl.term.expect_exact('start >')
            riot_ctrl.term.sendline('s')
            riot_ctrl.term.expect_exact('finished >',timeout=25)
            raw_output = riot_ctrl.term.before
        except:
            print("Exception Occured, term buffer:")
            print(riot_ctrl.term.before)
        finally:
            riot_ctrl.stop_exp()

    evaluation_record = {'board' : env['BOARD'], 'datetime': datetime.now().strftime("%Y%m%d-%H%M%S"),
                         'memory': 0, 'storage': 0, 
                         'trials_record': None, 'trials_stats': None,
                         'model_path': model_path, 'random_seed': random_seed}

    evaluation_record['trials_record'] = parse_per_model_output(raw_output)
    evaluation_record['trials_stats_in_usec'] = analysis.analysis_compute_latency(evaluation_record['trials_record'])
    
    memory, storage = get_memory_storage_from_buildsize(board)
    evaluation_record['memory'] = memory
    evaluation_record['storage'] = storage
    
    print_per_model_evaluation(evaluation_record.copy())
    save_evaluation_record(evaluation_record)

def parse_per_model_output(raw_output : str):
    pattern = re.compile('trial: ([0-9]+), usec: ([0-9]+), ret: ([0-9]+)')
    results_list = pattern.findall(raw_output)
    return { 'trial' : [int(x[0]) for x in results_list],
             'usec' : [int(x[1]) for x in results_list],
             'ret' :  [int(x[2]) for x in results_list]  }

import numpy as np

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def save_evaluation_record(rec):
    file_name = rec['board'] + '_' + str(rec['datetime']) + '.json'
    file_path = LOG_DIR + '/' + file_name
    with open(file_path, 'w') as f:
        json.dump(rec, f, cls=NpEncoder)


def get_memory_storage_from_buildsize(board):
    import subprocess
    output = subprocess.check_output(f"make BOARD={board} info-buildsize", shell=True)
    output = output.split(b'\n')
    output = output[1].split(b'\t')
    text = int(output[0].strip())
    data = int(output[1].strip())
    bss = int(output[2].strip())
    memory = data + bss
    storage = text + data
    return memory, storage


def print_per_model_evaluation(rec):
    headers = ['Board', 'Memory (KB)', 'Storage (KB)', 
               '95-CI (ms)', 'Mean (ms)', 'Median (ms)', 'Min. (ms)', 'Max. (ms)']
    
    if not isinstance(rec, list):
        rec = [rec]
    
    output_list = []
    for r in rec:
        stats = r['trials_stats_in_usec']
        ci = [0, 0]
        ci[0] = int(stats['95ci'][0]) / 1e3
        ci[1] = int(stats['95ci'][1]) / 1e3

        mean = int(stats['mean']) / 1e3
        median = int(stats['median']) / 1e3
        min = int(stats['min']) / 1e3
        max = int(stats['max']) / 1e3
        output_list.append([r['board'], r['memory'] / 1e3, r['storage'] / 1e3,
                                ci, mean, median, min ,max])
    
    tabular_output = tabulate(output_list, headers=headers)
    print(tabular_output)

def load_logs_from_folder(dir_path):
    import glob
    json_dict = []
    for filepath in glob.iglob(f'{dir_path}/*'):
        with open(filepath, 'r') as f:
            json_dict.append(json.load(f))
    print_per_model_evaluation(json_dict)


def evaluate_per_operator():
    #TODO: Wait for bugfix
    pass

if __name__ == '__main__':
    # from model_converter import RIOT_BOARD_TO_TARGET
    # for board in RIOT_BOARD_TO_TARGET.keys():
    #     try:
    #         evaluate_per_model(model_path='./model_zoo/mnist_0.983_quantized.tflite', 
    #                         board=board, use_iotlab=True, iotlab_node=None)
    #     except:
    #         print(f'Evaluation Failed: {board}')
    evaluate_per_model(model_path='./model_zoo/mnist_0.983_quantized.tflite', 
                            board='stm32f746g-disco', use_iotlab=False, iotlab_node=None)