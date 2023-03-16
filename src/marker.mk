#
# Extract marker sequence for a taxa list
#
# pre-requisites : taxonkit and blast nt database should be in the path

# Taxa list for which marker sequences need to be extracted
TAXA ?= test_taxa.txt

# Marker sequence name
MARKER ?= rbcL

# NT database in tabular format
NTSEQ ?= nt_seq.txt

# SQLITE3 Database of markers
DBNAME ?= markers.db

# Directory to store intermediate files
MISC ?= misc

# File to store taxids
TIDS ?= ${MISC}/species_tids.txt

# File to store extracted marker info in tabular format
MARKER_TABLE=${MISC}/marker_table.txt

# File with marker accessions
MARKER_ACC= marker_acc.txt

# File with marker fasta
MARKER_FASTA= marker.fa


# Makefile customizations.
.RECIPEPREFIX = >
.DELETE_ON_ERROR:
.ONESHELL:
MAKEFLAGS += --warn-undefined-variables --no-print-directory

# Print usage information.
usage::
> @echo "#"
> @echo "# Creates marker fasta file for input taxa and marker sequence"
> @echo "#"
> @echo "# make marker_fasta TAXA=${TAXA} MARKER=${MARKER}"
> @echo "#"

#
# Create a tabular format of NT database. 
# This needs to be done only once when nt database is updated
#
nt_table:
> make -f src/nt_table.mk create_table

# Create folders
folders:
> mkdir -p ${MISC}

# Extract taxids for the taxa list
extract_tids:
> python src/extract_species_tids.py --names ${TAXA} --children >${TIDS}

# Extract marker info in tabular format
extract_marker_info:
> python src/extract_marker_from_nt.py --nt_file ${NTSEQ} --taxid_file ${TIDS} --marker_gene ${MARKER} >${MARKER_TABLE}

# Extract marker accessions
extract_marker_acc:
> cat ${MARKER_TABLE}| tail -n+2 |cut -f 1 >${MARKER_ACC}

# Get fast sequnces from accession list
get_fasta:
> blastdbcmd -db nt -entry_batch ${MARKER_ACC} >${MARKER_FASTA}

# Create an sqlite database of marker
create_db:
> python src/create_marker_db.py --database ${DBNAME} --sequence_table ${MARKER_TABLE}

marker_fasta: folders extract_tids extract_marker_info extract_marker_acc get_fasta
> @ls -l ${MARKER_FASTA}

# Do all steps when NT database is updated.
all: nt_table marker_fasta create_db
> @ls -l ${MARKER_FASTA} ${DBNAME}



