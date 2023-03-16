
TAXA?=plant_taxa.txt
MARKER?=rbcL

# Makefile customizations.
.RECIPEPREFIX = >
.DELETE_ON_ERROR:
.ONESHELL:
MAKEFLAGS += --warn-undefined-variables --no-print-directory

# create NT database table
nt_table:
> make -f src/nt_table.mk create_table

# Create marker fasta
marker_fasta:
> time make -f src/marker.mk TAXA=plant_taxa.txt MARKER=rbcL marker_fasta
