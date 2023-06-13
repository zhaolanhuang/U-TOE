from evaluate import evaluate_per_model, evaluate_per_operator
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("model_file", help="path to machine leearning model file.",
                        type=str)
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--per-model", help="Per-Model Evaluation (default).",
                            action="store_true")
    mode_group.add_argument("--per-ops", help="Per-Operator Evaluation.",
                            action="store_true")
    parser.add_argument("--board", help="IoT board name", default="stm32f746g-disco",
                        type=str)
    parser.add_argument("--use-iotlab", help="use remote board in FIT IoT-LAB.",
                        action="store_true")
    parser.add_argument("--iotlab-node", help="remote node url. It will start an new experiment if this field is empty.",
                        default=None)
    parser.add_argument("--random-seed", default=42, type=int, help="default: 42")
    parser.add_argument("--trials-num", default=10, type=int, help="defalut: 10")
    args = parser.parse_args()
    if args.per_ops:
        evaluate_per_operator(args.model_file, args.board, args.use_iotlab, args.iotlab_node)
    else:
        evaluate_per_model(args.model_file, args.board, args.trials_num, args.use_iotlab, args.iotlab_node, args.random_seed)

