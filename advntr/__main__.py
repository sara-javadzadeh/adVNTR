#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from advntr.advntr_commands import genotype, view_model, add_model, del_model
from advntr import settings
from advntr import __version__


class CustomHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog):
        super(CustomHelpFormatter, self).__init__(prog, max_help_position=40, width=110)

    def _format_action_invocation(self, action):
        default = self._metavar_formatter(action, action.dest)
        args_string = self._format_args(action, default)
        return '/'.join(action.option_strings) + ' ' + args_string


def main():
    description = '=======================================================\n' \
                  'adVNTR %s: Genopyting tool for VNTRs\n' \
                  '=======================================================\n' \
                  'Source code: https://github.com/mehrdadbakhtiari/adVNTR\n' \
                  'Instructions: http://advntr.readthedocs.io\n' \
                  '-------------------------------------------------------\n' % __version__
    help = 'Command: genotype\tfind RU counts and mutations in VNTRs\n' \
           '         viewmodel\tview existing models in database\n' \
           '         addmodel\tadd custom VNTR to the database\n' \
           '         delmodel\tremove a model from database\n'

    usage = '\r{}\nusage: %(prog)s <command> [options]\n\n\r{}\r{}'.format(description.ljust(len('usage:')), help, '\n')
    parser = argparse.ArgumentParser(usage=usage, add_help=False)
    subparsers = parser.add_subparsers(title='Commands', dest='command')

    fmt = lambda prog: CustomHelpFormatter(prog)
    genotype_parser = subparsers.add_parser('genotype', usage='advntr genotype [options]', formatter_class=fmt,
                                            add_help=False)
    genotype_io_group = genotype_parser.add_argument_group("Input/output options")
    genotype_io_group.add_argument('-a', '--alignment_file', type=str, metavar='<file>',
                                   help='Alignment file in BAM format or SAM format')
    genotype_io_group.add_argument('-f', '--fasta', type=str, metavar='<file>',
                                   help='Fasta file containing raw reads',)
    genotype_io_group.add_argument('-p', '--pacbio', action='store_true',
                                   help='set this flag if input file contains PacBio reads instead of Illumina reads')
    genotype_io_group.add_argument('-n', '--nanopore', action='store_true',
                                   help='set this flag if input file contains Nanopore MinION reads instead of Illumina')
    genotype_io_group.add_argument('-of', '--outfmt', metavar='format', default='text', choices=['text', 'bed'],
                                   help='[output format %(default)s]')

    genotype_algortihm_group = genotype_parser.add_argument_group("Algorithm options")
    genotype_algortihm_group.add_argument('-fs', '--frameshift', action='store_true',
                                          help='set this flag to search for frameshifts in VNTR instead of copy'
                                          ' number. Supported VNTR IDs: %s' % settings.FRAMESHIFT_VNTRS)
    genotype_algortihm_group.add_argument('-e', '--expansion', action='store_true',
                                          help='set this flag to determine long expansion from PCR-free data')
    genotype_algortihm_group.add_argument('-c', '--coverage', type=float, metavar='<float>',
                                          help='average sequencing coverage in PCR-free sequencing')
    genotype_algortihm_group.add_argument('--haploid', action='store_true', default=False,
                                          help='set this flag if the organism is haploid')
    genotype_algortihm_group.add_argument('-naive', '--naive', action='store_true', default=False,
                                          help='use naive approach for PacBio reads')

    genotype_others_group = genotype_parser.add_argument_group("Other options")
    genotype_others_group.add_argument('-h', '--help', action='help',
                                       help='show this help message and exit')
    genotype_others_group.add_argument('--working_directory', type=str, metavar='<path>',
                                       help='working directory for creating temporary files needed for computation')
    genotype_others_group.add_argument('-m', '--models', type=str, metavar='<file>', default='vntr_data/hg19_VNTRs.db',
                                       help='file containing VNTRs information [%(default)s]')
    genotype_others_group.add_argument('-t', '--threads', type=int, metavar='<int>', default=4,
                                       help='number of threads [%(default)s]')
    genotype_others_group.add_argument('-u', '--update', action='store_true', default=False,
                                       help='set this flag to iteratively update the model')
    genotype_others_group.add_argument('-vid', '--vntr_id', type=str, metavar='<text>', default=None,
                                       help='comma-separated list of VNTR IDs')

    viewmodel_parser = subparsers.add_parser('viewmodel', usage='advntr viewmodel [options]', formatter_class=fmt)
    viewmodel_parser.add_argument('-g', '--gene', type=str, default='', metavar='<text>',
                                  help='comma-separated list of Gene Names')
    viewmodel_parser.add_argument('-p', '--pattern', type=str, default=None, metavar='<text>',
                                  help='repeating pattern of VNTR in forward (5\' to 3\') direction')

    addmodel_parser = subparsers.add_parser('addmodel', usage='advntr addmodel [options]', formatter_class=fmt,
                                            add_help=False)
    addmodel_args_group = addmodel_parser.add_argument_group("Required arguments")
    addmodel_other_group = addmodel_parser.add_argument_group("Other options")

    addmodel_args_group.add_argument('-r', '--reference', type=str, default=None, metavar='<text>',
                                  help='Reference genome')
    addmodel_args_group.add_argument('-c', '--chromosome', type=str, default=None, metavar='<text>',
                                  help='Chromosome (e.g. chr1)')
    addmodel_args_group.add_argument('-p', '--pattern', type=str, default=None, metavar='<text>',
                                  help='First repeating pattern of VNTR in forward (5\' to 3\') direction')
    addmodel_args_group.add_argument('-s', '--start', type=int, default=None, metavar='<int>',
                                  help='Start coordinate of VNTR in forward (5\' to 3\') direction')
    addmodel_args_group.add_argument('-e', '--end', type=int, default=None, metavar='<int>',
                                  help='End coordinate of VNTR in forward (5\' to 3\') direction')

    addmodel_other_group.add_argument('-g', '--gene', type=str, default=None, metavar='<text>',
                                  help='Gene name')
    addmodel_other_group.add_argument('-a', '--annotation', type=str, default=None, metavar='<text>',
                                  help='Annotation of VNTR region')
    addmodel_other_group.add_argument('-h', '--help', action='help',
                                      help='show this help message and exit')

    delmodel_parser = subparsers.add_parser('delmodel', usage='advntr delmodel [options]', formatter_class=fmt,
                                            add_help=False)
    delmodel_args_group = delmodel_parser.add_argument_group("Required arguments")
    delmodel_other_group = delmodel_parser.add_argument_group("Other options")

    delmodel_args_group.add_argument('-vid', '--vntr_id', type=str, metavar='<text>', default=None,
                                     help='VNTR ID')

    delmodel_other_group.add_argument('-h', '--help', action='help',
                                      help='show this help message and exit')

    args = parser.parse_args()
    if args.command == 'genotype':
        genotype(args, genotype_parser)
    elif args.command == 'viewmodel':
        view_model(args, viewmodel_parser)
    elif args.command == 'addmodel':
        add_model(args, addmodel_parser)
    elif args.command == 'delmodel':
        del_model(args, delmodel_parser)
    else:
        parser.error('Please specify a valid command')

if __name__ == '__main__':
    main()
