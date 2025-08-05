from fasta_reader import read_fasta

def fasta_to_dict(file1):#not-used 
    dict={}
    for item in read_fasta(file1):
        dict[item.defline]=item.sequence
    return dict

def fasta_to_list(file1):#returns a list of all the proteins from the file.Each item in protein_list has an index number, a list spliting the name of the protein in each dot and a string of the sequence of the protein
    protein_list=[]
    i=0
    for item in read_fasta(file1):
        protein_list.append([i,item.defline.split("."),item.sequence])
        i=i+1
    return protein_list

