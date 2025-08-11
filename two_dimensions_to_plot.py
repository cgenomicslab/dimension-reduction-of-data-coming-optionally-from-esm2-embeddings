import plotly.io as pio
import plotly.graph_objects as go
from pandas import DataFrame
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# def simple_umap_to_plotly(name_list,colors_list,embedding,n_neighbors,min_dist,metric,color_dict):# simple because the markers are predetermined. Only the color changes
#     pio.renderers.default = "browser"#the plot appears on the browser
#     df=DataFrame(name_list,columns=['names'])
#     df['color']=colors_list[:]
#     df['dimension-1']=embedding[:,0]
#     df['dimension-2']=embedding[:,1]
#     fig = go.Figure()
#     inv_color_dict= {v: k for k, v in color_dict.items()}
#     for color in df['color'].unique():
#         group_df = df[(df['color'] == color)]
#         if not group_df.empty:
#             fig.add_trace(go.Scatter(
#                 x=group_df['dimension-1'],
#                 y=group_df['dimension-2'],
#                 mode='markers',
#                 name=f"{inv_color_dict[color]} ",
#                 marker=dict(
#                     opacity=0.7,
#                     color=color,
#                     size=8,
#                     symbol='circle'
#                 ),
#                 text=group_df['names'],
#                 hoverinfo='text',
#                 showlegend=True
#             ))

#     fig.update_layout(title="UMAP Scatter with "+str(n_neighbors)+' neighbors and '+str(min_dist)+' minimum distance and '+metric+' metric')
#     fig.show()    

def color_file_to_dicts(file_name,split_in_point=False):# returns two dictionaries. The first connects its type to a color and the second each data point to a type
    return_list=[]
    seen=set()
    typetocolordict={}
    nametotypedict={}
    with open (file_name,"r") as file:
        for line in file:
            data_point = line.split()
            return_list.append(str(data_point[1]))
            if split_in_point:name=(data_point[0]).split('.')[0]
            else: name=data_point[0]
            if data_point[2] not in seen:#if the color isn't already in the dictionary
                seen.add(data_point[2])
                typetocolordict[data_point[2]]=data_point[1]
            nametotypedict[name]=data_point[2]
    return typetocolordict,nametotypedict

def non_color_file_to_list(file_name,name_list,split_in_point=False):
        color_dict={"unknown":"#888888"}
        while True:
            try:
                inp=input("write colon seperated the type and the hexc code of the color (eg neuro:#663399) or write stop to finish the dictionary")
                if inp=='stop':break
                else:
                    inplist=inp.split(":")
                    color_dict[inplist[0]]=inplist[1]
                    print(color_dict)
            except:continue
        #color_dict={"neuro":"#004a8c","class_1":"#a17a8e","class_2":"#9d3a6b","unknown":"#888888"}
        protein_dict={}
        #color_dict={"neuro":"#004a8c73","class_1":"#a17a8e73","class_2":"#9d3a6b73","unknown":"#88888873"} for more transparent points in plt
        with open (file_name,"r") as colorfile:
            for line in colorfile:
                protein = line.split()
                protein_dict[protein[0]]=color_dict[protein[1]]
        ptypes=[]
        colors=[]
        for oneprotein in name_list:
            #print(oneprotein)
            if oneprotein in protein_dict:
                colors.append(protein_dict[oneprotein])
            else:
                colors.append("#888888")
                #colors.append("#88888873") for more transparent points in plt
        return color_dict,colors

def markers_from_many_files_plt(parent_folder,name_list):#returns the markers of each data_point and a dictionary connecting the marker to their label for use in matplotlib.pyplot or plt
    folder_path=Path(parent_folder)
    file_names = [f.name for f in folder_path.iterdir() if f.is_file()]
    #print(file_names)
    data_dict={}
    markersdict={'s':'no-type'}
    plt_markers=['o','X','^','P','d','*','H','v','$V$','$U$','$Y$','$#$']#markers for plt
    for i in range (len(file_names)):#saves the name of each file minus the .txt to use as a label
        markersdict[plt_markers[i]]=file_names[i][:-4]
        with open (parent_folder+"/"+file_names[i],"r") as file:#opens each file
            for data_point in file:
                data_dict[data_point.strip()]=plt_markers[i]#adds to the dictionary the name as a key and the corresponding marker as the value
    markers=[]

    # if the point exists in the dictionary it adds the correct marker in the correct place. If it doesn't it adds a square for no-type
    for data_point in name_list:
        #print(oneprotein)
        if data_point in data_dict:
            markers.append(data_dict[data_point])
        else:
            markers.append("s")
    return markers,markersdict

def markers_from_many_files_plotly(parent_folder,name_list):#returns the markers of each data_point and a dictionary connecting the marker to their label for use in plotly
    markersdict={'square':'no-type'}
    plotly_markers=['circle','x','arrow-up','cross','diamond','star','hexagon-2','arrow-down','arrow-wide','star-triangle-down-open','circle-open']
    folder_path=Path(parent_folder)
    file_names = [f.name for f in folder_path.iterdir() if f.is_file()]
    #print(file_names)
    data_dict={}
    for i in range (len(file_names)):#for all the names of files
        markersdict[plotly_markers[i]]=file_names[i][:-4]#saves the name of each file minus the .txt to use as a label
        #print(parent_folder+file_names[i])
        with open (parent_folder+"/"+file_names[i],"r") as thisfile:#opens each file
            for data_point in thisfile:
                data_dict[data_point.strip()]=plotly_markers[i]#adds to the dictionary the name as a key and the corresponding marker as the value
    markers=[]

    # if the point exists in the dictionary it adds the correct marker in the correct place. If it doesn't it adds a square for no-type
    for data_point in name_list:
        #print(oneprotein)
        if data_point in data_dict:
            markers.append(data_dict[data_point])
        else:
            markers.append("square")
    return markers,markersdict

def color_list_to_dict(color_list,name_list,typetocolordict):
    inv_color_dict= {v: k for k, v in typetocolordict.items()}
    nametotypedict={}
    for i in range(len(name_list)):
        nametotypedict[name_list[i]]=inv_color_dict[color_list[i]]
    return nametotypedict

def dict_to_color_list(name_list,typetocolordict,nametotypedict,split_in_point=False):
    color_list=[]
    for i in range(len(name_list)):
        if split_in_point:
            spec_name=name_list[i].split(".")[0]
            color_list.append(typetocolordict[nametotypedict[spec_name]])
        else:
            color_list.append(typetocolordict[nametotypedict[name_list[i]]])
    return color_list

def plot_title(method:str,variable_list:list):#returns the title of the plot and part of the name of the file to save the graph if this option is chosen
    if method=="pca":return "Principal Component Analysis","pca"
    elif method=='t-sne':return "T-sne method with "+str(variable_list[0])+" perplexity","tsne_"+str(variable_list[0])
    else:return "U-map plot with "+str(variable_list[0])+" neighbors, "+str(variable_list[1])+" min_dist and "+ str(variable_list[2])+" metric","umap "+str(variable_list[0])+"_"+str(int(10*variable_list[1]))+'_'+variable_list[2]

def color_plot_to_plotly(name_list:list,colors_list:list,embedding:list,plot_title:str,typetocolordict:dict):# plots with the same markers and different colors from the color list
    pio.renderers.default = "browser"#the plot appears on the browser

    #dataframe with names,colors and dimensions
    df=DataFrame(name_list,columns=['names'])
    df['color']=colors_list[:]
    df['dimension-1']=embedding[:,0]
    df['dimension-2']=embedding[:,1]


    fig = go.Figure()
    inv_color_dict= {v: k for k, v in typetocolordict.items()}#inverse color_dict
    print(inv_color_dict)
    for color in df['color'].unique():#for every different color
        group_df = df[(df['color'] == color)]#a smaller dataframe with the points with the same color
        if not group_df.empty:
            fig.add_trace(go.Scatter(
                x=group_df['dimension-1'],
                y=group_df['dimension-2'],
                mode='markers',
                name=f"{inv_color_dict[color]} ",
                marker=dict(
                    opacity=0.7,
                    color=color,
                    size=8,
                    symbol='circle'
                ),
                text=group_df['names'],
                hoverinfo='text',
                showlegend=True
            ))

    fig.update_layout(title=plot_title)
    fig.show()        

def color_plot_to_plt(colors_list:list,embedding:list,plot_title:str,typetocolordict:dict,save_title:str,parent_folder:str):
    legend_elements = [  
    Line2D([0], [0], marker='o', color='w', label=label,
           markerfacecolor=color, markersize=8)
    for label, color in typetocolordict.items()
    ]   #creates a legend with the different colors
    plt.scatter(
        embedding[:, 0],
        embedding[:, 1],
        s=10,
        color=colors_list[:],
        )
    # Add the legend to the plot
    plt.gca().set_aspect('equal', 'datalim')
    plt.title(plot_title, fontsize=24)
    #plt.show()
    plt.legend(handles=legend_elements, title=' Type', loc='best')
    plt.savefig(parent_folder+"/"+save_title+".svg", dpi=300, bbox_inches='tight')

def color_and_marker_plot_to_plt(name_list,markers_list,marker_dict,embedding,plot_title,nametotypedict,typetocolordict,save_title,parent_folder):
        legend_elements = [
        Line2D([0], [0], marker=marker, color='b', label=label,
                markersize=8)
        for  marker,label in marker_dict.items()]
        color_legend = [
        Line2D([0], [0], marker='o', color=color, label=label, linestyle='None', markersize=8)
        for label, color in typetocolordict.items()
        ]#creates a legend with the different color and marker combinations
        
        for i in range(len(embedding)):
            label=nametotypedict[name_list[i].split(".")[0]]
            plt.scatter(
                embedding[i, 0],
                embedding[i, 1],
                s=10,
                marker=markers_list[i % len(markers_list)],  # Cycle through marker list
                color=typetocolordict[label]+"a1"
            )   
        plt.gca().set_aspect('equal', 'datalim')
        plt.title(plot_title, fontsize=24)
        plt.legend(handles=legend_elements+color_legend, title=' Type', bbox_to_anchor=(1.05, 0))
        plt.savefig(parent_folder+"/"+save_title+".svg", dpi=300, bbox_inches='tight')

def color_and_marker_plot_to_plotly(name_list,markers_list,embedding,plot_title,marker_dict,nametotypedict,typetocolordict):# simple because the markers are predetermined. Only the color changes
    pio.renderers.default = "browser"#the plot appears on the browser
    df = DataFrame(name_list, columns=["name"])
    df['markers']=markers_list[:]
    df['label'] = df['name'].apply(lambda x: nametotypedict[x.split('.')[0]])
    df["color"]=df['label'].apply(lambda x: typetocolordict[x])
    df['dimension-1'] = embedding[:, 0]
    df['dimension-2'] = embedding[:, 1] 

    fig = go.Figure()
    for label in df['label'].unique():
        for marker_symbol in df['markers'].unique():
            group_df = df[(df['label'] == label) & (df['markers'] == marker_symbol)]
            if not group_df.empty:
                fig.add_trace(go.Scatter(
                    x=group_df['dimension-1'],
                    y=group_df['dimension-2'],
                    mode='markers',
                    name=f"{label} | {marker_dict[marker_symbol]}",
                    marker=dict(
                        opacity=0.7,
                        color=group_df['color'],  
                        size=8,
                        symbol=marker_symbol
                    ),
                    text=group_df['name'],
                    hoverinfo='text',
                    showlegend=True
                ))

    fig.update_layout(title=plot_title)
    fig.show()
