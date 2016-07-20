#!/usr/bin/env bash -l

# This script is NOT meant to be executed "as is".
# Rather this is for copy-pasting, one command at a time,
# while explaining what's going on. 

# Get the docker image (note: use "sudo" on Linux), using an explicit version id or image id: 

#docker run -it -v $HOME:$HOME idaks/ligo:0.2.0.6

docker run -it -v $HOME:$HOME 7fa7eda02176 

# change into demo directory 
cd ligo/query

# remove all derived products
rm -rf  facts *.xwam *.gv *.png *.pdf *.P *.txt ../../rules/*.xwam

# for database facts
mkdir -p facts


# run YesWorkflow on the script to extract YW facts and model

java -jar /home/ligo/bin/yesworkflow-0.2.0.jar  extract GW150914_tutorial.py -c extract.factsfile > facts/yw_extract_facts.P

java -jar /home/ligo/bin/yesworkflow-0.2.0.jar model GW150914_tutorial.py -c model.factsfile > facts/yw_model_facts.P

# create some high-level YW views
bash materialize_yw_views.sh > yw_views.P


# run queries
bash query.sh >query_output.txt 


