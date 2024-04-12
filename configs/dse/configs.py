import argparse
import m5.objects
from m5 import fatal
from m5.objects.FuncUnitConfig import *

def addCPUOptions(parser):
    # Pipeline width
    parser.add_argument(
        "--fetch-width",
        action="store",
        type=int,
        default=8,
        help="Fetch width",
    )
    parser.add_argument(
        "--decode-width",
        action="store",
        type=int,
        default=8,
        help="Decode width",
    )
    parser.add_argument(
        "--rename-width",
        action="store",
        type=int,
        default=8,
        help="Rename width",
    )
    parser.add_argument(
        "--dispatch-width",
        action="store",
        type=int,
        default=8,
        help="Dispatch width",
    )
    parser.add_argument(
        "--issue-width",
        action="store",
        type=int,
        default=8,
        help="Issue width",
    )
    parser.add_argument(
        "--writeback-width",
        action="store",
        type=int,
        default=8,
        help="Writeback width",
    )
    parser.add_argument(
        "--commit-width",
        action="store",
        type=int,
        default=8,
        help="Commit width",
    )
    # Fetch buffer
    parser.add_argument(
        "--fetch-buffer-size",
        action="store",
        type=int,
        default=64,
        help="Fetch buffer size in bytes",
    )
    # Fetch queue
    parser.add_argument(
        "--fetch-queue-size",
        action="store",
        type=int,
        default=32,
        help="Fetch queue size in micro-ops per-thread",
    )
    # ROB
    parser.add_argument(
        "--num-rob-entries",
        action="store",
        type=int,
        default=192,
        help="Number of reorder buffer entries",
    )
    # Int RF
    parser.add_argument(
        "--num-phys-int-regs",
        action="store",
        type=int,
        default=256,
        help="Number of physical integer registers",
    )
    # Fp RF
    parser.add_argument(
        "--num-phys-float-regs",
        action="store",
        type=int,
        default=256,
        help="Number of physical floating point registers",
    )
    # IQ
    parser.add_argument(
        "--num-iq-entries",
        action="store",
        type=int,
        default=64,
        help="Number of instruction queue entries",
    )
    # LQ
    parser.add_argument(
        "--num-lq-entries",
        action="store",
        type=int,
        default=64,
        help="Number of load queue entries",
    )
    # SQ
    parser.add_argument(
        "--num-sq-entries",
        action="store",
        type=int,
        default=64,
        help="Number of store queue entries",
    )


def config_cpu(cpu, args):
    cpu.fetchWidth          = args.fetch_width
    cpu.decodeWidth         = args.decode_width
    cpu.renameWidth         = args.rename_width
    cpu.dispatchWidth       = args.dispatch_width
    cpu.issueWidth          = args.issue_width
    cpu.wbWidth             = args.writeback_width
    cpu.commitWidth         = args.commit_width
    cpu.fetchBufferSize     = args.fetch_buffer_size
    cpu.fetchQueueSize      = args.fetch_queue_size
    cpu.numROBEntries       = args.num_rob_entries
    cpu.numPhysIntRegs      = args.num_phys_int_regs
    cpu.numPhysFloatRegs    = args.num_phys_float_regs
    cpu.numIQEntries        = args.num_iq_entries
    cpu.LQEntries           = args.num_lq_entries
    cpu.SQEntries           = args.num_sq_entries


def addPredictorOptions(parser):
    # Tournament BP
    parser.add_argument(
        "--local-predictor-size",
        action="store",
        type=int,
        default=2048,
        help="Size of local predictor",
    )
    parser.add_argument(
        "--global-predictor-size",
        action="store",
        type=int,
        default=8192,
        help="Size of global predictor",
    )
    parser.add_argument(
        "--choice-predictor-size",
        action="store",
        type=int,
        default=8192,
        help="Size of choice predictor",
    )
    # RAS
    parser.add_argument(
        "--num-ras-entries",
        action="store",
        type=int,
        default=16,
        help="Number of RAS entries",
    )
    # BTB
    parser.add_argument(
        "--num-btb-entries",
        action="store",
        type=int,
        default=4096,
        help="Number of BTB entries",
    )


def config_pred(pred, args):
    pred.localPredictorSize = args.local_predictor_size
    pred.globalPredictorSize = args.global_predictor_size
    pred.choicePredictorSize = args.choice_predictor_size
    pred.ras.numEntries = args.num_ras_entries
    pred.btb.numEntries = args.num_btb_entries


def addFUPoolOptions(parser):
    # IntALU
    parser.add_argument(
        "--num-int-alu",
        action="store",
        type=int,
        default=6,
        help="Number of integer ALUs",
    )
    # IntMultDiv
    parser.add_argument(
        "--num-int-mult-div",
        action="store",
        type=int,
        default=2,
        help="Number of integer multipliers and dividers",
    )
    # FpALU
    parser.add_argument(
        "--num-fp-alu",
        action="store",
        type=int,
        default=4,
        help="Number of floating-point ALUs",
    )
    # FpMultDiv
    parser.add_argument(
        "--num-fp-mult-div",
        action="store",
        type=int,
        default=2,
        help="Number of floating-point multipliers and dividers",
    )


def config_fu_pool(fu_pool, args):
    for fu_desc in fu_pool.FUList:
        if isinstance(fu_desc, IntALU):
            fu_desc.count = args.num_int_alu
        if isinstance(fu_desc, IntMultDiv):
            fu_desc.count = args.num_int_mult_div
        if isinstance(fu_desc, FP_ALU):
            fu_desc.count = args.num_fp_alu
        if isinstance(fu_desc, FP_MultDiv):
            fu_desc.count = args.num_fp_mult_div


def addDSEOptions(parser):
    addCPUOptions(parser)
    addPredictorOptions(parser)
    addFUPoolOptions(parser)


def config_dse(cpu_cls, cpu_list, args):
    if issubclass(cpu_cls, m5.objects.DerivO3CPU):
        for cpu in cpu_list:
            config_cpu(cpu, args)
            config_pred(cpu.branchPred, args)
            config_fu_pool(cpu.fuPool, args)
    # else:
    #     fatal()