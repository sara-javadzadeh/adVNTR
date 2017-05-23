from settings import *
from utils import get_chromosome_reference_sequence, get_gc_content
import pysam


class CoverageBiasDetector:
    """Find the coverage distribution based on GC content."""

    def __init__(self, sam_file='original_reads/paired_dat.sam'):
        self.sam_file = sam_file

    def get_sam_file_from_read_files(self):
        pass

    def get_gc_contents_of_reference_windows(self):
        gc_map = {}
        for chromosome in CHROMOSOMES:
            gc_map[chromosome] = {}
            chromosome_reference = get_chromosome_reference_sequence(chromosome)
            for window_number in range(len(chromosome_reference) / GC_CONTENT_WINDOW_SIZE):
                start = window_number * GC_CONTENT_WINDOW_SIZE
                end = start + GC_CONTENT_WINDOW_SIZE
                gc_content = get_gc_content(chromosome_reference[start:end])
                gc_map[chromosome][window_number] = gc_content
        return gc_map

    def add_bp_to_coverage_map(self, covered_bps, chromosome, window_number, read_start, read_end):
        start = max(window_number * GC_CONTENT_WINDOW_SIZE, read_start)
        end = min(window_number * GC_CONTENT_WINDOW_SIZE + GC_CONTENT_WINDOW_SIZE, read_end)
        if window_number not in covered_bps[chromosome]:
            covered_bps[chromosome][window_number] = 0
        covered_bps[chromosome][window_number] += end - start
        if read_end > window_number * GC_CONTENT_WINDOW_SIZE + GC_CONTENT_WINDOW_SIZE:
            self.add_bp_to_coverage_map(covered_bps, chromosome, window_number+1, end, read_end)

    def get_gc_content_coverage_map(self):
        reference_gc_map = self.get_gc_contents_of_reference_windows()
        samfile = pysam.AlignmentFile(self.sam_file, "r")
        covered_bps = {}
        for chromosome in CHROMOSOMES:
            covered_bps[chromosome] = {}
        for read in samfile.fetch():
            window_number = read.reference_start / GC_CONTENT_WINDOW_SIZE
            read_start = read.reference_start
            read_end = read.reference_end
            self.add_bp_to_coverage_map(covered_bps, read.reference_name, window_number, read_start, read_end)

        gc_coverage_map = {}
        for chromosome in covered_bps.keys():
            for window_number in covered_bps[chromosome]:
                windows_gc = reference_gc_map[chromosome][window_number]
                windows_gc = int(windows_gc * 100)
                windows_coverage = covered_bps[chromosome][window_number]
                if windows_gc not in gc_coverage_map:
                    gc_coverage_map[windows_gc] = []
                gc_coverage_map[windows_gc].append(windows_coverage)

        return gc_coverage_map


class CoverageCorrector:
    """Normalize the coverage based on the coverage distribution."""
    pass