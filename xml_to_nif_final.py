from pynif import NIFCollection
import os
import xml.etree.ElementTree as ET


#Preconditions: the files are named equally in each of the following directories
collection_name ="AQUAINT_DBpedia" 
path_raw = "/Users/Rico/Desktop/Bachelorarbeit/Datasets/AQUAINT/AQUAINT_dataset/RawTexts"
path_xml = "/Users/Rico/Desktop/Bachelorarbeit/Datasets/AQUAINT/Annotations_DBpedia/htm_dateien"
output_path = "/Users/Rico/Desktop/Bachelorarbeit/Datasets/AQUAINT/Annotations_DBpedia/NIF_dateien"


#creates collection
#collection = NIFCollection(uri=collection_name)

#the code iterates through each file and converts it into NIF

for filename in os.listdir(path_raw):
    if not filename.endswith(".htm"):
        continue
        
    with open(path_raw+"/"+filename, 'r') as f:
        raw_input = f.read()
        raw_input = raw_input.replace('\n',' ')
        #print(filename)
        #print(raw_input)
        #raw_texts.append(t)
        
        #creates collection
        collection = NIFCollection(uri=collection_name)
        
        context = collection.add_context(
            uri=filename,
            mention=raw_input)
        
#------------------------------------------

        tree = ET.parse(path_xml+"/"+filename)
        root = tree.getroot()

        #saves offsets in a list
        beginIndex_list = []
        for i in range(1,len(root)):
            begin = root[i][1].text
            begin = int(begin)
            beginIndex_list.append(begin)
        #print(beginIndex_list) 

        #calculates endIndex and saves it in a list
        endIndex_list = []
        for j in range(1,len(root)):
            begin = int(root[j][1].text)
            length = int(root[j][2].text)
            endIndex_list.append(begin+length)
        #print(endIndex_list)

        #extracts annotation from file
        anno_list = []
        for i in range(1,len(root)):
            anno = root[i][3].text
            anno_list.append(anno)
        anno_list = [x.replace('\n', '') for x in anno_list]
        anno_list = [x.replace('\t', '') for x in anno_list]
        #print(anno_list)
        
#--------------------------------------

        #add context to text
        for i in range(len(beginIndex_list)):
            context.add_phrase(
                beginIndex=beginIndex_list[i],
                endIndex=endIndex_list[i],
                #taClassRef=['http://dbpedia.org/ontology/SportsManager', 'http://dbpedia.org/ontology/Person', 'http://nerd.eurecom.fr/ontology#Person'],
                #score=0.9869992701528016,
                #annotator='http://freme-project.eu/tools/freme-ner',
                taIdentRef=anno_list[i])
        #print(context)   

#------------------------------

        #generates NIF and safes it in file
        generated_nif = collection.dumps(format='turtle')
        print(generated_nif)
        path = output_path+"/"+filename
        output_file = open(path,"w")
        output_file.write(generated_nif)
        output_file.close()

