from dimension_reduction import *
from two_dimensions_to_plot import *

if __name__=='__main__':

    pt_folder=input("write the relative name of the data folder")#the folder of the data
    parent_folder=input("write the whole name of the parent folder")
    tensor_list,name_list=create_array2(pt_folder,parent_folder)# a list of the input tensors and another with their names
    while True:#asks the user to pick a dimension reduction method
        method=input("write umap,t-sne or pca to use the corresponding dimension reduction method")
        if method=='t-sne':
            perplexity,embedding=calculate_tsne(tensor_list)
            plot_title,save_title=plot_title("t-sne",[perplexity])
            break
        elif method=='umap':
            n_neighbors,min_dist,metric,embedding =calculate_umap(tensor_list)
            plot_title,save_title=plot_title("Umap",[n_neighbors,min_dist,metric])
            break
        elif method=='pca':
            embedding=calculate_pca(tensor_list)
            plot_title,save_title=plot_title("pca",[])
            break
        else: print("the input was invalid")

    nametotypedict={}#keys: names , values: the type on the chosen categorization
    seen = set()
    typetocolordict={}#keys: the types on the chosen categorization, values: the color that corresponds to each type
     colors_list=[]
    chosen_library=input("write plt to save the plot in a .svg file or write plotly to see an interactive plot")
    
    colorsask=input("write 1 to read from a file with lines on format <<name color type>> 2 to read from a file with only the types and 0 to not show any color")
    if (input('write 1 if you want as name only the part before the dot or 0 to take the whole name')=='1'):split_bool=True#asks to split the name before a dot. Can be used to organise the data into larger categories
    else: split_bool=False

    if colorsask=='1':
        file_name=input('write the whole path to the .txt file that contains the colors and the categories of different data points')
        typetocolordict,nametotypedict= color_file_to_dicts(file_name,split_in_point=split_bool)
    elif colorsask=='2':
        #split_bool=bool(input('write 1 if you want to take the name only from before the first point or 0 to take the whole name'))
        file_name=input('write the whole path to the .txt file that contains the categories of different data points')     
        typetocolordict,colors_list=non_color_file_to_list(file_name,name_list,split_in_point=split_bool)
    else: 
        colors_list=['#663399' for _ in range(len(name_list))]
        typetocolordict={"all":"#663399"}
        for name in name_list: nametotypedict[name.split(".")[0]]="all"
    
    markers_bool=input("write 1 to have markers or 0 for no markers")
    if markers_bool=='1':
        marker_folder=input('copy the whole path to the folder with the different .txt files')
    name_set=set(name_list)

    name_dict={}
    for i in range(len(name_set)):
        name_dict[list(name_set)[i]]=i
    #for i in range(len(name_list)):
    #    colors.append(typetocolordict[nametotypedict[name_list[i].split(".")[0]]])
    if markers_bool=='1':
        if not nametotypedict:nametotypedict=color_list_to_dict(colors_list,name_list,typetocolordict)#if the dictionary is empty
        if chosen_library=='plotly':#for the interactive plot using plotly
            markers,marker_dict=markers_from_many_files_plotly(marker_folder,name_list)#finds the markers
            color_and_marker_plot_to_plotly(name_list=name_list,markers_list=markers,embedding=embedding,plot_title=plot_title,marker_dict=marker_dict,nametotypedict=nametotypedict,typetocolordict=typetocolordict)
        elif chosen_library=='plt':#to save the plot in a svg file using matplotlib.pyplot
            markers,marker_dict=markers_from_many_files_plt(marker_folder,name_list)
            color_and_marker_plot_to_plt(name_list,markers,marker_dict,embedding,plot_title,nametotypedict,typetocolordict,save_title,parent_folder)
    else:
        if not colors_list:colors_list=dict_to_color_list(name_list,typetocolordict,nametotypedict)#if the list is empty
        if chosen_library=='plotly':#for the interactive plot using plotly
            color_plot_to_plotly(name_list=name_list,colors_list=colors_list,embedding=embedding,plot_title=plot_title,typetocolordict=typetocolordict)
        elif chosen_library=='plt':#to save the plot in a svg file using matplotlib.pyplot
            color_plot_to_plt(colors_list=colors_list,embedding=embedding,plot_title=plot_title,typetocolordict=typetocolordict,save_title=save_title,parent_folder=parent_folder)      
