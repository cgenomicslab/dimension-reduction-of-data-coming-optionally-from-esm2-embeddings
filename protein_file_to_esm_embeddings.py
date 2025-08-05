
from read_fasta1 import fasta_to_list
from torch import no_grad
from torch import save as torch_save
import esm

def protein_tensor(protein,model,alphabet,batch_converter):
    batch_labels, batch_strs, batch_tokens = batch_converter([protein])
    batch_lens = (batch_tokens != alphabet.padding_idx).sum(1)
    with no_grad():
        results = model(batch_tokens, repr_layers=[33], return_contacts=True)
    token_representations = results["representations"][33]

    tokens_len = batch_lens[0]
    sequence_representation = token_representations[0, 1 : tokens_len - 1].mean(0)

    return sequence_representation

if __name__=='__main__':

    file1=input("insert the name of the protein file")
    protein_list=fasta_to_list(file1) #returns a list of all the proteins from the file.Each item in protein_list has an index number, a list spliting the name of the protein in each dot and a string of the sequence of the protein
    output_file=input("insert the whole name of the output file")

    # Load ESM-2 model
    model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()
    batch_converter = alphabet.get_batch_converter()
    model.eval()  # disables dropout for deterministic results

    #check_name=protein_list[0][1][0]
    for i in range(len(protein_list)):#for every protein saves in the chosen file a different .pt file with the name of the protein as the name of the file and the tensor of the protein as the content of the file
        #tensors_list.append(protein_tensor(('.'.join(protein_list[i][1]),protein_list[i][2]),model,alphabet,batch_converter))
        torch_save(protein_tensor(('.'.join(protein_list[i][1]),protein_list[i][2]),model,alphabet,batch_converter),output_file+"/"+str('.'.join(protein_list[i][1]))+'.pt')

