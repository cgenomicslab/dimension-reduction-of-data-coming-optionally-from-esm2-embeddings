# dimension-reduction-of-data-coming-optionally-from-esm2-embeddings
Two main scripts. One (protein_file_to_esm_embeddings.py) reads a fasta file and returns the esm2 embeddings of the protein of the file. The other (multi_dimensional_data_to_plot.py) reduces the input data into two dimensions with one of different methods(pca,t-sne, umap) and plots the results. They can be used together or independently

## Essential libraries
* torch
* esm (only for making the embeddings in protein_file_to_esm_embeddings.py)
* matplotlib
* pandas
* plotly
* pathlib
* fasta_reader
* umap
* scikit learn
* os
* numpy

## files overview

![files_overview](https://github.com/user-attachments/assets/0e8e1f21-acae-4dc2-a116-c7e503fe3462)

protein_file_to_esm_embeddings.py uses read_fasta1.py to read the fasta file and then it uses the esm library to calculate and then save the embeddings of each protein of the file.

multi_dimensional_data_to_plot.py uses the dimension_reduction.py file to reduce the dimensions of the data and then uses two_dimensions_to_plot.py to plot the two dimensional results.

## how to use protein_file_to_esm_embeddings.py

1. The code will ask the user for the name of the fasta file (could be .fasta or .fa). The name should be given with the whole Path to the file.
2. Then the code will ask for a folder to save the output tensors. Each tensor will have its own file with the name of the protein as the name of the file (without '.pt') and the tensor of the embeddings of the protein as the content of the file.

<img width="245" height="412" alt="pt overview" src="https://github.com/user-attachments/assets/d46b1292-2200-48ea-9e64-041b054b2b1b" />

 As a result the folder will contain as many files as proteins in the given fasta file.

 ## how to use multi_dimensional_data_to_plot.py

1. The code will ask for input the name of the folder that contains the different tensors that will be reduced.
2.  Then it will ask for the whole path to the name of the parent folder. That folder is the parent folder of the folder given before (the one that contains the tensor files).
3.   Then it will for the dimension reduction method that the user wants to use (principal component analysis, t-sne, umap). Depending on the result the code might ask for new inputs to use as parameters to the selected method.
4.    After the parameters are set the code will calculate the results and will save them in a np.array. The results and the parameters will be returned to the main script.
5.  Then the code will ask for the plotting library. plt (matplotlib.pyplot) will save the plot in an .svg file while pyplot will show the interactive plot in the browser (no internet needed).
6.  The next question will ask for colors. The different colors are the main way for categorisation of the data.
    *    One option for the colors is to be given in a single file that contains the name, the color and the label for the color.
    *    The other option is to give only the labels in a file and then the code will ask for input to create a dictionary matching the labels to the colors
    *    The third option will show all the points with the same color
7.  After the color the next question will ask if the categorisation should be based on the whole name or the part of it before the dot(".")
8.  The code will then ask for markers which can be used to add another way for categorisation. The markers should be given in a folder with different files. Each file will contain the names that share the same property so they will have the same marker.

## examples
### t-sne with different markers and the same color
<img width="569" height="554" alt="tsne_42 0" src="https://github.com/user-attachments/assets/ed3ae1e1-208d-483d-b472-fd1d11787520" />

 This is plotted using matplotlib.pyplot. The .png file of the plot can be found here:
 https://github.com/cgenomicslab/dimension-reduction-of-data-coming-optionally-from-esm2-embeddings/blob/main/examples/tsne_42.0.png
 
### principal component analysis with different colors
<img width="777" height="598" alt="pca_only_colors" src="https://github.com/user-attachments/assets/08f6c73d-c78c-4a11-bccf-bbbd21321c9d" />

This is plotted using plotly. The html file with the interactive plot can be found here:
https://github.com/cgenomicslab/dimension-reduction-of-data-coming-optionally-from-esm2-embeddings/blob/main/examples/pca_humans.html

### umap with color and markers
<img width="1101" height="672" alt="umap_30_0_manhattan" src="https://github.com/user-attachments/assets/1aa433e4-be44-4168-be42-450ba7fc609b" />

This is plotted using matplotlib.pyplot. The .png file of the diagram can be found here: https://github.com/cgenomicslab/dimension-reduction-of-data-coming-optionally-from-esm2-embeddings/blob/main/examples/umap_30_0_manhattan.png

And the .svg file can be found here: https://github.com/cgenomicslab/dimension-reduction-of-data-coming-optionally-from-esm2-embeddings/blob/main/examples/umap_30_0_manhattan.svg
## Credits
This code is developed using Torch, Matplotlib, SciKit Learn, pandas, fasta-reader, numpy and plotly. It also uses Umap and ESM. Special thanks to the contributors of these libraries.

## Licence
This code is under the MIT license but certain libraries used are under other libraries. Check the THIRD_PARTY_LIBRARIES.md for more information
