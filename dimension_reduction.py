from numpy import array as np_array
from torch import load
import os
import umap
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

import pandas as pd


# def create_array(pt_folder,parent_folder):# create_array1 returns a tensor array and a list of the names before the dot (unused)
#     pt_files = sorted([f for f in os.listdir(parent_folder+pt_folder) if f.endswith(".pt")])
#     tensor_list = []
#     name_list=[]
#     for filename in pt_files:
#         file_path = os.path.join(parent_folder+pt_folder, filename)
#         data_dict = load(file_path)  # This is a dictionary that stores the values for the tensor and the name
#         #print(data_dict)

#         tensor = data_dict['tensor'] 
#         name_list.append(data_dict['name'].split(".")[0])#takes the category before the dot.
#         tensor_list.append(tensor.tolist())

#     return np.array(tensor_list),name_list

def create_array2(pt_folder,parent_folder):# create_array2 returns a tensor array and a list of the whole names
    pt_files = sorted([f for f in os.listdir(parent_folder+"/"+pt_folder) if f.endswith(".pt")])#finds the files that are of .pt format
    tensor_list = []
    name_list=[]
    for filename in pt_files:
        file_path = os.path.join(parent_folder+"/"+pt_folder, filename)
        data_dict = load(file_path)  # loads a dictionary from the tensor file
        #print(data_dict)

        tensor = data_dict['tensor']  
        name_list.append(data_dict['name'])
        # Converts tensor to list
        tensor_list.append(tensor.tolist())

    return np_array(tensor_list),name_list

def calculate_umap(array_for_umap):#uses u-map for dimension reduction
    u_maps_param=input("write comma separated values for n_neighbours,min_dist,metric or anything else for the default values")
    random_seed=input("write Y to use the same predermined seed(same diagramm with the same parameters)")
    try: #parameters of u-map
        paramlist=u_maps_param.split(',')
        n_neighbors=int(paramlist[0])
        min_dist=float(paramlist[1])
        metric=paramlist[2]
    except:
        n_neighbors=40
        min_dist=0.1
        metric='cosine'
    if random_seed!='Y' :reducer = umap.UMAP(min_dist=min_dist,n_neighbors=n_neighbors,metric=metric)#picks a state at random thus changing the u-map
    else:reducer = umap.UMAP(min_dist=min_dist,n_neighbors=n_neighbors,metric=metric,random_state = 42)
    scaled_data = StandardScaler().fit_transform(array_for_umap)
    embedding = reducer.fit_transform(scaled_data)
    #print(embedding.shape)
    return n_neighbors,min_dist,metric,embedding

def calculate_pca(array_for_pca):#uses pca for dimension reduction
    scaled_data = StandardScaler().fit_transform(array_for_pca)
    pca_values = PCA(n_components=2)
    principalComponents = pca_values.fit_transform(scaled_data)
    loadings = pd.DataFrame(pca_values.components_.T,
                        columns=[f'PC{i+1}' for i in range(pca_values.n_components_)])
    print(loadings.abs().sort_values(by='PC1', ascending=False))
    print('Explained variability per principal component: {}'.format(pca_values.explained_variance_ratio_))
    return principalComponents

def calculate_tsne(array_for_tsne):#uses t-sne for dimension reduction
    perplexity=float(input("write a value for perplexity"))
    scaled_data = StandardScaler().fit_transform(array_for_tsne)
    tsne = TSNE(n_components=2, random_state=42,perplexity=perplexity)
    X_tsne = tsne.fit_transform(scaled_data)
    tsne.kl_divergence_
    return perplexity,np_array(X_tsne)

# def show_umap_simple(embedding,save_name,parent_folder,n_neighbors=20,min_dist=0.1,metric='cosine'):
#     n_colors = 1
#     color = sns.color_palette("tab20", n_colors)
#     plt.scatter(
#         embedding[:, 0],
#         embedding[:, 1],
#         s=10,
#         color=color,
#         )
#     # Add the legend to the plot
#     plt.gca().set_aspect('equal', 'datalim')
#     plt.title('UMAP projection of the reduced Ligchan whole sequences dataset with '+str(n_neighbors)+' neighbors \n and '+str(min_dist)+' minimum distance and '+metric+' metric', fontsize=24)
#     #plt.show()
#     plt.savefig(parent_folder+save_name+str(n_neighbors)+"_"+str(int(10*min_dist))+".png", dpi=300, bbox_inches='tight')

