import csv, sys, re, argparse

# This script parses tab delimited file produced by blastdbcmd command
# and extract marker sequence accessions for each taxids.

# The blastcmd command should produce a file of he format
# accession\ttitle\tseq_length\ttaxid\tscientific_name\tcommon_name

# The output of this script is a tab delimited file with the following columns
# accession,title,length,taxid,scientific_name,common_name,marker,genomic_location

csv.field_size_limit(sys.maxsize)

ribosomal_12S = ["12S", "12SrRNA", "rnr1 rRNA", "rRNA small subunit", "rrnS rRNA",
                 "s-rRNA", "small subunit rRNA", "small rRNA subunit RNA", "small subunit ribosomal RNA"]

ribosomal_16S = ["16S", "l-RNA", "l-rRNA", "large rRNA subunit RNA",
                 "large subunit rRNA", "LSU rRNA", "mtLSU rRNA", "rnl rRNA", "rnr2 rRNA",
                 "rRNA large subunit", "rrnL rRNA", "large subunit ribosomal RNA"]

cyctochromB = ["cytb", "cytochrome b", "cyt b", "cyto B"]

COI = ["COI", "CO1", "COX1", "COXI", "MT-CO1", "CO 1",
       "CO I", "COX I", "COX 1", "MT CO1", "cytochrome c oxidase I",
       "cytochrome c oxidase 1", "cytochrome oxidase I", "cytochrome oxidase 1",
       "Cytochrome c oxidase subunit I", "Cytochrome c oxidase subunit 1",
       "Cytochrome oxidase subunit I", "Cytochrome oxidase subunit 1",
       "cytochrome c oxidase I"]

COII = ["COII", "CO2", "COX2", "COXII", "MT-CO2", "CO 2",
        "CO II", "COX II", "COX 2", "MT CO2", "cytochrome c oxidase II",
        "cytochrome c oxidase 2", "cytochrome oxidase II", "cytochrome oxidase 2",
        "Cytochrome c oxidase subunit II", "Cytochrome c oxidase subunit 2",
        "Cytochrome oxidase subunit II", "Cytochrome oxidase subunit 2",
        "cytochrome c oxidase II"]

COIII = ["COIII", "CO3", "COX3", "COXIII", "MT-CO3", "CO 3",
         "CO III", "COX IIII", "COX 3", "MT CO3", "cytochrome c oxidase III",
         "cytochrome c oxidase 3", "cytochrome oxidase III", "cytochrome oxidase 3",
         "Cytochrome c oxidase subunit III", "Cytochrome c oxidase subunit 3",
         "Cytochrome oxidase subunit III", "Cytochrome oxidase subunit 3",
         "cytochrome c oxidase III"]

RBCL = ["rbcL", "ribulose-1,5-bisphosphate carboxylase/oxygenase large subunit"]

genome = ["complete genome", "partial genome"]
MARKERS = genome + ribosomal_12S + ribosomal_16S + cyctochromB + COI + COII + COIII + RBCL

REGION = ["mitochondri", "chloroplast"]

region_map = {"mitochondri": "Mitochondria",
              "chloroplast": "Chloroplast"}

marker_map = {"coi": "COI",
              "co1": "COI",
              "coxi": "COI",
              "cox1": "COI",
              "mt-co1": "COI",
              "co 1": "COI",
              "co i": "COI",
              "cox i": "COI",
              "cox 1": "COI",
              "mt co1": "COI",

              "coii": "COII",
              "co2": "COII",
              "coxii": "COII",
              "cox2": "COII",
              "mt-co2": "COII",
              "co 2": "COII",
              "co ii": "COII",
              "cox ii": "COII",
              "cox 2": "COII",
              "mt co2": "COII",

              "coiii": "COIII",
              "co3": "COIII",
              "coxiii": "COIII",
              "cox3": "COIII",
              "mt-co3": "COIII",
              "co 3": "COIII",
              "co iii": "COIII",
              "cox iii": "COIII",
              "cox 3": "COIII",
              "mt co3": "COIII",

              "cytochrome c oxidase subunit i": "COI",
              "cytochrome oxidase subunit i": "COI",
              "cytochrome oxidase subunit 1": "COI",
              "cytochrome c oxidase subunit 1": "COI",
              "cytochrome c oxidase i": "COI",
              "cytochrome c oxidase 1": "COI",
              "cytochrome oxidase i": "COI",
              "cytochrome oxidase 1": "COI",

              "cytochrome c oxidase subunit ii": "COII",
              "cytochrome oxidase subunit ii": "COII",
              "cytochrome oxidase subunit 2": "COII",
              "cytochrome c oxidase subunit 2": "COII",
              "cytochrome c oxidase ii": "COII",
              "cytochrome c oxidase 2": "COII",
              "cytochrome oxidase ii": "COII",
              "cytochrome oxidase 2": "COII",

              "cytochrome c oxidase subunit iii": "COIII",
              "cytochrome oxidase subunit iii": "COIII",
              "cytochrome oxidase subunit 3": "COIII",
              "cytochrome c oxidase subunit 3": "COIII",
              "cytochrome c oxidase iii": "COIII",
              "cytochrome c oxidase 3": "COIII",
              "cytochrome oxidase iii": "COIII",
              "cytochrome oxidase 3": "COIII",

              "cytochrome b": "Cyt b",
              "cyt b": "Cyt b",
              "cyto b": "Cyt b",
              "cytb": "Cyt b",

              "12s": "12S",
              "12Srrna": "12S",
              "rnr1 rrna": "12S",
              "small subunit ribosomal RNA": "12S",
              "rrna small subunit": "12S", "small rrna subunit rna": "12S",
              "rrnS rrna": "12S", "s-rrna": "12S", "small subunit rRNA": "12S",

              "16s": "16S", "l-rna": "16S", "large rrna subunit rna": "16S",
              "large subunit rrna": "16S", "lsu rrna": "16S", "mtlsu rrna": "16S",
              "rnl rrna": "16S", "rnr2 rrna": "16S", "rrna large subunit": "16S",
              "rrnl rrna": "16S",
              "large subunit ribosomal RNA": "16S",

              "complete genome": "complete genome",

              "partial genome": "partial genome",
              "rbcl": "rbcL",
              "ribulose-1,5-bisphosphate carboxylase/oxygenase large subunit" : "rbcL",
              }


def read_taxids(fname):
    store = dict()
    stream = csv.reader(open(fname), delimiter="\t")
    for row in stream:
        name, tid = row[0], row[1]
        store[tid] = name if name else None
    return store


def match_patterns(title, pattern_list, func=lambda x: x.lower()):
    # Find a match in a list of patterns
    # Returns first match found.
    for pattern in pattern_list:
        # Apply extra function to pattern to
        # enhance/relax searches.
        pattern = func(pattern)
        match = re.search(pattern, title)
        if match:
            return match.group(0)
    return


def parse_title(title):
    pattern_func = lambda p: r'\b' + p.lower() + r'\b'

    title = title.lower()

    # Return the first matched marker and region
    marker = match_patterns(title, pattern_list=MARKERS, func=pattern_func)
    region = match_patterns(title, pattern_list=REGION)

    return marker, region


def parse_nt_seq_table(fname, taxids, marker_gene):
    """
    This file 'fname' is produced by blastdbcmd command and has the format
    accession\ttitle\tseq_length\ttaxid\tscientific_name\tcommon_name
    """

    header = ["accession", "title", "length", "taxid",
              "scientific_name", "common_name", "marker", "genomic_location", ]
    print("\t".join(header))

    stream = csv.reader(open(fname), delimiter="\t")

    for row in stream:

        acc = row[0]
        title = row[1]
        taxid = row[3].strip()

        if taxid not in taxids:
            continue

        marker, genomic_location = parse_title(title)

        # if marker is None or genomic_location is None:
        #     continue

        if marker is None:
            continue

        if marker in marker_map:
            marker = marker_map[marker]

        if genomic_location in region_map:
            genomic_location = region_map[genomic_location]

        genomic_location = genomic_location if genomic_location else ""

        if marker_gene == "ALL" or marker.upper() == marker_gene.upper():
            out = "\t".join(row)
            parsed = "\t".join([out, marker, genomic_location])
            print(parsed)

    return


def check_input_marker(marker_gene):
    if marker_gene not in ['ALL', 'COI', 'COII', 'COIII', '12S', '16S', 'CYTB', 'COMPLETE_GENOME', 'RBCL']:
        print(
            "Specified marker gene is not allowed. Possible options are COI, COII, COIII, 12S, 16S, Cytb, complete_genome, rbcL.")
        sys.exit()
    return marker_gene


def main():
    # nt_file = sys.argv[1]  # "nt_seq.txt"
    # taxid_file = sys.argv[2]  # "all_fish_species_tids.txt"
    parser = argparse.ArgumentParser(description='''Create a Mitochondrial marker file for specified taxa(s)''')
    parser.add_argument('--nt_file', dest='nt_file', type=str, required=True,
                        help='Tab delimited Blastdbcmd parsed file with accession,sequence title, sequence length, taxid, scientific name, common taxonomic name as columns.')
    parser.add_argument('--taxid_file', dest='taxid_file', type=str, required=True,
                        help="""Tab delimited file with species names and taxid as columns.
                                     """)
    parser.add_argument('--marker_gene', dest='marker_gene', type=str, required=False, default="ALL",
                        help="""Marker gene of interest. Possible options are COI, COII, COIII, 12S, 16S, CYTB, complete_genome.
                                If nothing is specified, all markers will be included in the output.""")

    args = parser.parse_args()
    taxid_file = args.taxid_file
    nt_file = args.nt_file
    marker_gene = args.marker_gene
    marker_gene = marker_gene.upper()

    # Check marker gene
    marker_gene = check_input_marker(marker_gene)
    taxids = read_taxids(taxid_file)
    parse_nt_seq_table(nt_file, taxids, marker_gene)


if __name__ == "__main__":
    main()