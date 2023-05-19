from string import Template
import re

def _shape_to_size(shape, dtype):
    bits_per_item = int(
        re.match(r"((float)|(int)|(uint))(?P<width_bits>[0-9]+)", dtype).group("width_bits")
    )
    assert bits_per_item is not None, f"don't know how to compute size of type {dtype}"
    total_bits = bits_per_item
    for s in shape:
        total_bits *= s

    return (total_bits + 7) // 8


def generate_model_io_vars_header(input_vars : dict, output_vars : dict, output_path='./model_io_vars.h'):
    HEADER_TEMPLATE = """ /* U-TOE Auto-generated File */
    static char input[$input_size];
    static char output[$output_size];
    struct tvmgen_default_inputs default_inputs = {
            $input_fields
        };
    struct tvmgen_default_outputs default_outputs = {
            $output_fields
        };
    """
    def get_fields_and_size(vars, pool_var_name=None):
        fields = ""
        size = 0
        for v in vars:
            fields += f'.{v["name"]}' + f' = &{pool_var_name}[{size}], \n'
            size += v['size']
        return fields, size
    
    input_fields, input_size = get_fields_and_size(input_vars, 'input')
    output_fields, output_size = get_fields_and_size(output_vars, 'output')
    io_vars_header = Template(HEADER_TEMPLATE).substitute(input_size=input_size, output_size=output_size,
                                                          input_fields=input_fields, output_fields=output_fields)
    with open(output_path, "w") as f:
        f.write(io_vars_header)
    return io_vars_header

def extract_io_vars_from_module(mod):
    metadata = mod.executor_codegen_metadata
    input_names = metadata.inputs
    output_names = metadata.outputs
    
    input_vars = [{'name' : name, 'size': _shape_to_size(tensor_type.shape, tensor_type.dtype)}
                  for name,tensor_type in zip(input_names, metadata.input_tensor_types)]
    
    output_vars = [{'name' : name, 'size': _shape_to_size(tensor_type.shape, tensor_type.dtype)}
                  for name,tensor_type in zip(output_names, metadata.output_tensor_types)]
    return input_vars, output_vars