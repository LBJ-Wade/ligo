#!/usr/bin/env bash -l
#
#bash  ./run.sh


mkdir -p facts

java -jar ~/bin/yesworkflow-0.2.1-SNAPSHOT-jar-with-dependencies.jar  extract GW150914_tutorial.py -c extract.factsfile > facts/yw_extract_facts.P

java -jar ~/bin/yesworkflow-0.2.1-SNAPSHOT-jar-with-dependencies.jar model GW150914_tutorial.py -c model.factsfile > facts/yw_model_facts.P

bash materialize_yw_views.sh > yw_views.P

bash query.sh >query_output.txt 

