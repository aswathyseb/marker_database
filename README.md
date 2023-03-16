### Marker Database
	
	Creation of a customizable marker database based on user-specifed marker sequence and taxa list.


#### usage:
	make -f src/marker.mk TAXA=plant_taxa.txt MARKER=rbcL marker_fasta

#### Input(s)
	1) Marker name = rbcL
	2) Taxa list
		cat plant_taxa.txt
		Viridiplantae

### Output(s)	
	Fasta file of marker sequences
	Sqlite database file of markers
		



