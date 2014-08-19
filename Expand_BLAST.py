#!/usr/bin/env python

# Author: Youri Lammers
# Contact: youri.lammers@naturalis.nl / youri.lammers@gmail.com

# This script expands the BLAST output file from the HTS-Barcode-Checker script with the number of reads per cluster.
# Currently it only works with clusters produced by the CD-hit_filter.py script

# command: Expand_BLAST.py -b [blast .tsv file] -c [.clstr cluster file]

# The output of the Expand_BLAST.py script is a BLAST file with the same name as the intput file + expanded append to it.
# The new BLAST file contains the number of reads per cluster in the second colomn.

# import modules used by the script
import argparse, os, itertools

# set argument parser
parser = argparse.ArgumentParser(description = 'Filter the output from CD-hit based on the minimum number of read per cluster.\nThe filtered output fasta file produced has the same name as the input file with  _min_[minimum size from -c argument].fasta attachted to the name.')

parser.add_argument('-b', '--blast', metavar='.tsv file', dest='blast', type=str,
			help='The .tsv blast file.')
parser.add_argument('-c', '--cluster', metavar='.clstr file', dest='cluster', type=str,
			help='The .clstr file producec by CD-hit that contains the cluster information.')
args = parser.parse_args()


def read_clstr():

	# parse through the .clstr file and create a dictionary
	# with the sequences per cluster

	# open the cluster file and set the output dictionary
	cluster_file, cluster_dic = open(args.cluster), {}

	# parse through the cluster file and store the cluster name + sequences in the dictionary
	cluster_groups = (x[1] for x in itertools.groupby(cluster_file, key=lambda line: line[0] == '>'))
	for cluster in cluster_groups:
		name, seqs = cluster.next().strip()[1:].replace(' ','_'), []

		seqs = [seq.split('>')[1].split('...')[0] for seq in cluster_groups.next()]
		cluster_dic[name] = len(seqs)

	# return the cluster dictionary
	return cluster_dic


def expand_blast(cluster_dic):

	# open the blast output file and expand the results with the number of reads per cluster
	
	# open the blast file and create a new file
	blast_list = [line.strip().split('\t') for line in open(args.blast)]
	output_blast = open(os.path.splitext(args.blast)[0] + '_expanded.tsv', 'w')

	# parse throuth the input blast hits
	for line in blast_list:
		if 'Query' in line[0]: line[1:1] = ['Num Reads']
		# grab the query sequence and look in the cluster_dic how many reads the cluster contains
		# insert this number in the second column and write the file
		else: line[1:1] = [str(cluster_dic[line[0]])]
		output_blast.write('\t'.join(line) + '\n')

	# close the new blsat file
	output_blast.close()
	
def main():

	# obtain a dictionary with the clusters and sequences
	cluster_dic = read_clstr()

	# expand the blast file
	expand_blast(cluster_dic)

if __name__ == '__main__':
	main()
