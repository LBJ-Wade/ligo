rm -rf model_query.db

FILE=*.csv

for f in $FILE
do
 NAME=`echo "$f" | cut -d'.' -f1`
 MESSAGE=".mode csv\n.import $f $NAME"
 echo -e $MESSAGE | sqlite3 model_query.db
 # do something on $f
done

python model_query.py