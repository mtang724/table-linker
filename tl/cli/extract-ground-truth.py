import sys
import argparse
import traceback
import tl.exceptions


def parser():
    return {
        'help': 'extract ground truth file from input file'
    }

def add_arguments(parser):
    """
    Parse Arguments
    Args:
        parser: (argparse.ArgumentParser)

    """
    parser.add_argument('-t', '--target', action='store', type=str, dest='target', required=True,
                        help='the column in the input file to be linked to KG entities.')
    parser.add_argument('-i', '--kg-id', action='store', type=str, dest='kg_id', required=True,
                        help='the column in the input file containing KG identifier.')
    parser.add_argument('-l', '--kg-label', action='store', type=str, dest='kg_label', required=True,
                        help='the column in the input file containing KG label.')
    parser.add_argument('--tsv', action='store_true', dest='tsv')
    parser.add_argument('--csv', action='store_true', dest='csv')

    parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'), default=sys.stdin)


def run(**kwargs):
    from tl.preprocess import preprocess
    import pandas as pd

    file_type = 'tsv' if kwargs['tsv'] else 'csv'
    try:
        df = pd.read_csv(kwargs['input_file'], sep=',' if file_type == 'csv' else '\t', dtype=object)
        odf = preprocess.extract_ground_truth(kwargs['target'], kwargs['kg_id'], kwargs['kg_label'],
                                              df=df, file_type=file_type)
        odf.to_csv(sys.stdout, index=False)
    except:
        message = 'Command: extract-ground-truth\n'
        message += 'Error Message:  {}\n'.format(traceback.format_exc())
        raise tl.exceptions.TLException(message)
