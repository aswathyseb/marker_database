#
# Create a tabular file of nt datbase. This needs to be done once whenever nt is updated.
# Pre-requisite: BLASTDB should be in the path
# 
#
OUT ?= nt_seq.txt

# Makefile customizations.
.RECIPEPREFIX = >
.DELETE_ON_ERROR:
.ONESHELL:
MAKEFLAGS += --warn-undefined-variables --no-print-directory

# Make NT table 

# Print usage information.
usage::
> @echo "#"
> @echo "# nt_table.mk: creates a tabular file from blast databases."
> @echo "# The columns in the table are accession, title,sequence_length,taxid,scientific_name,common_name"
> @echo "#"
> @echo "# make create_table OUT=${OUT}"
> @echo "#"


create_table:
> blastdbcmd -db nt -dbtype 'nucl' -outfmt "%a#####%t#####%l#####%T#####%S#####%L" -out ${OUT} -entry all
#
# format table
#
#Change the delimiter to tab.
>cat ${OUT} |  sed 's/#####/\t/g'  >nt_seq_tab.txt
>mv nt_seq_tab.txt ${OUT}
