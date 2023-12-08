#include <tvmgen_default.h>
#include <string.h>
#include "mlmci.h"

#include "model_iovars.h"
#include "model_params.h"
#include "model_binding.h"


#ifndef MODEL_NAME
#define MODEL_NAME "U_TOE_DEFAULT_MODEL"
#endif

static mlmodel_param_t model_params[MODEL_PARAMS_NUM];
static mlmodel_iovar_t model_input_vars[MODEL_INPUTS_NUM];
static mlmodel_iovar_t model_output_vars[MODEL_OUTPUTS_NUM];


static struct tvmgen_default_inputs tvm_default_inputs;
static struct tvmgen_default_outputs tvm_default_outputs;

static int _model_init(mlmodel_t *model) {
    (void) model;
    memcpy(model_params, get_model_params(), sizeof(model_params));
    memcpy(model_input_vars, get_model_input_vars(), sizeof(model_input_vars));
    memcpy(model_output_vars, get_model_output_vars(), sizeof(model_output_vars));


        
    return 0;
}

static int _model_inference(mlmodel_t *model) {

    model_bind_tvm_iovars(model, &tvm_default_inputs, &tvm_default_outputs);
    return tvmgen_default_run(&tvm_default_inputs, &tvm_default_outputs);
    
}

static int _model_backward_pass(mlmodel_t *model, mlmodel_iovar_t input_gradients[], mlmodel_iovar_t output_gradients[]) {
    (void) model;
    (void) input_gradients;
    (void) output_gradients;

    return 0;

}


static mlmodel_model_driver_t model_driver = {
    .init = &_model_init,
    .inference = &_model_inference,
    .backward_pass = &_model_backward_pass,
};


static mlmodel_t model = {
    .driver = &model_driver,
    
    .params = model_params,
    .num_params = MODEL_PARAMS_NUM,

    .input_vars = model_input_vars,
    .num_input_vars = MODEL_INPUTS_NUM,

    .output_vars = model_output_vars,
    .num_output_vars = MODEL_OUTPUTS_NUM,

    .operators = NULL,
    .num_operators = 0,

    .complete_cb = NULL,
    .status = MLMODEL_STATUS_STOP,

    .name = MODEL_NAME

};

mlmodel_t *model_ptr = &model;