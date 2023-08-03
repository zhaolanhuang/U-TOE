from riotctrl.ctrl import RIOTCtrl
from types import MethodType

def get_local_controller(env, application_directory='.'):
    ctrl =  RIOTCtrl(application_directory='.', env=env)
    ctrl.stop_exp = MethodType(lambda self: None, ctrl)
    ctrl.cosy = MethodType(lambda self: self.make_run(['cosy']), ctrl)
    return ctrl


def get_fit_iotlab_controller(env, application_directory='.', iotlab_node=None):
    
    # no node specified, create experiment automatically
    if iotlab_node is None:
        env['IOTLAB_NODES'] = '1'
        env['IOTLAB_DURATION'] = '10'
        env['IOTLAB_TYPE'] = '$(IOTLAB_ARCHI)'
        ctrl = RIOTCtrl(application_directory='.', env=env)
        ctrl.FLASH_TARGETS = ('iotlab-flash',)
        ctrl.TERM_TARGETS = ('iotlab-term', )
        ctrl.RESET_TARGETS = ('iotlab-reset',)
        ctrl.stop_exp = MethodType(lambda self: self.make_run(['iotlab-stop']), ctrl)
        print("String FIT IoT-lab Experiment...")
        ctrl.make_run(['elffile', 'binfile', 'hexfile', 'iotlab-exp',])
        print("String FIT IoT-lab Experiment...done")
    else:
        env['IOTLAB_NODE'] = iotlab_node
        ctrl = RIOTCtrl(application_directory='.', env=env)
        ctrl.stop_exp = MethodType(lambda self: None, ctrl)
    return ctrl

    
