YesWorkflow-NoWorkflow using the Python script “LIGO gravitational wave detection”

======================

The LIGO repository contains implementation for YesWorkFlow (YW) and ReproZip using LIGO gravitational wave detection as a use case.


Overview
--------

YesWorkflow is very effective tool for Reproducibility of Data-Oriented Experiments. This experiment utilizes YesWorkflow tools to interpret the YW comments and produce graphical output that reveals the stages of computation and the flow of data in the LIGO script. 



### 1. Run YesWorkflow on the LIGO python script

#### Creating a workflow graph for a script

Generated “combined view” in YW

    $ yw graph GW150914_tutorial_uri.py -config graph.view=combined -config graph.layout=tb | dot -Tpng -o GW150914_tutorial_uri.png && open GW150914_tutorial_uri.png
    
    
#### YesWorkflow output

The image below was produced by YesWorkflow using the YW comments added to a conventional (non-dataflow oriented) python script ([GW150914_tutorial_uri.py](https://github.com/idaks/ligo/blob/master/GW150914_tutorial_uri.py "GW150914_tutorial_uri.py")):

![example](https://raw.githubusercontent.com/idaks/ligo/master/GW150914_tutorial_uri.png)

The green blocks represent stages in the computation performed by the script. The labels on arrows name the input, intermediate, and final data products of the script.



### 2. Reproduce the LIGO python script on Docker container.

#### Built a LIGO docker image from a dockerfile


    FROM  java:8

    ENV VERSION 0.2.0.6

    RUN echo '***** Update packages *****' \
    && apt-get -y update

    RUN echo '***** Install packages REQUIRED for creating this image *****' \
    && apt-get -y install apt-utils curl makepasswd gcc make

    RUN echo '***** Install packages required by YesWorkflow and noWorkflow *****' \
    && apt-get -y install graphviz python3 python3-pip swi-prolog expect

    RUN echo '***** Install packages NOT required to run yesworkflow *****' \
    && apt-get -y install sudo man less file tree vim emacs

    RUN echo '***** Install noWorkflow *****' \
    && pip3 install noworkflow[all]

    RUN echo '***** Create the ligo user *****' \
    && useradd ligo --gid sudo \
                 --shell /bin/bash \
                 --create-home \
    && echo "ligo ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/ligo \
    && chmod 0440 /etc/sudoers.d/ligo

    # perform remaining commands as the user and within the user's home directory
    ENV HOME /home/ligo
    USER  ligo
    WORKDIR $HOME

    # specify name, version, and location of YW jar to be used
    ENV YW_MAVEN_URL http://repo1.maven.org/maven2/org/yesworkflow
    ENV YW_VERSION 0.2.0
    ENV YW_JAR_IN_MAVEN yesworkflow-$YW_VERSION-jar-with-dependencies.jar
    ENV YW_JAR $HOME/bin/yesworkflow-$YW_VERSION.jar

    RUN echo '***** Download yw-prototypes executable jar, expand examples, and create alias *****' \
    && mkdir $HOME/bin  \
    && echo $YW_MAVEN_URL/yesworkflow/$YW_VERSION/$YW_JAR_IN_MAVEN \
    && curl -o $YW_JAR $YW_MAVEN_URL/yesworkflow/$YW_VERSION/$YW_JAR_IN_MAVEN \
    && echo "alias yw='java -jar $YW_JAR'"  >> $HOME/.bash_aliases

    RUN echo '***** Download and build XSB 3.6 *****'  \
    && svn checkout svn://svn.code.sf.net/p/xsb/src/trunk/XSB xsb-3.6 \
    && cd xsb-3.6/build \
    && ./configure \
    && ./makexsb \
    && cd $HOME \
    && echo 'export PATH="/home/ligo/xsb-3.6/bin:$PATH"' >> .bashrc

    RUN echo '***** Clone ligo and build examples repo *****' \
    && git clone https://github.com/idaks/ligo.git \
    && export PATH=/home/ligo/xsb-3.6/bin:$PATH 


    # start an interactive bash login shell when the image is run
    CMD  /bin/bash -il
    
    
#### Pipe Dockerfile via STDIN ([Dockerfile.txt](https://raw.githubusercontent.com/idaks/ligo/master/docker/Dockerfile.txt "Dockerfile.txt"))

    $ docker build - < Dockerfile.txt


#### List the images on our local host
     
     

                        ##         .
                  ## ## ##        ==
               ## ## ## ## ##    ===
           /"""""""""""""""""\___/ ===
      ~~~ {~~ ~~~~ ~~~ ~~~~ ~~~ ~ /  ===- ~~~
           \______ o           __/
             \    \         __/
              \____\_______/


    docker is configured to use the default machine with IP 192.168.99.100
    For help getting started, check out the docs at https://docs.docker.com

    $ docker images
    REPOSITORY                  TAG                 IMAGE ID            CREATED             SIZE
    <none>                      <none>              7fa7eda02176        6 days ago          1.525 GB
    ubuntu                      latest              cf62323fa025        2 weeks ago         125 MB
    java                        8                   264282a59a95        6 weeks ago         669.2 MB
    yesworkflow/yw-noworkflow   0.2.0.6             08a4d2abb890        6 weeks ago         1.511 GB
    yesworkflow/yw-noworkflow   latest              08a4d2abb890        6 weeks ago         1.511 GB
    google/golang               latest              09ec5b5ecced        6 months ago        664.9 MB
     
#### Run a LIGO container 

    $ run -it -v $HOME:$HOME 7fa7eda02176
    
    
#### Reproduce in LIGO docker container ([ligo_demo.sh](https://raw.githubusercontent.com/idaks/ligo/master/docker/ligo_demo.sh "ligo_demo.sh"))


    $ cd ligo/query
    
    $ rm -rf  facts *.xwam *.gv *.png *.pdf *.P *.txt ../../rules/*.xwam
    
    $ mkdir -p facts
    
    $ java -jar /home/ligo/bin/yesworkflow-0.2.0.jar  extract GW150914_tutorial.py -c extract.factsfile > facts/yw_extract_facts.P
    
    $ java -jar /home/ligo/bin/yesworkflow-0.2.0.jar model GW150914_tutorial.py -c model.factsfile > facts/yw_model_facts.P
    
    $ bash materialize_yw_views.sh > yw_views.P
    
    $ bash query.sh >query_output.txt







### 3. Reproduce the LIGO python script on Reprozip

ReproZip is a tool aimed at creating reproducible experiments from command-line executions which includes packing step  (tracking and creating dependencies) and unpacking step (reproducing the results )

Since packing experiments is only available for Linux distributions, we need configure Ubuntu in Virtual Box to execute reprozip, then run LIGO in Ubuntu.

    
#### Package dependencies for Running LIGO in Ubuntu


    $ sudo pip install numpy
    
    $ sudo pip install scipy
    
    $ sudo apt-get install python-numpy 
    
    $ sudo apt-get install python-scipy 
    
    $ sudo apt-get install python-matplotlib
    
    $ sudo apt-get install ipython 
    
    $ sudo apt-get install ipython-notebook 
    
    $ sudo apt-get install python-pandas 
    
    $ sudo apt-get install python-sympy 
    
    $ sudo apt-get install python-nose
    
    $ sudo pip install h5py
    


##### Pack the LIGO experiment

- Install Reprozip in Ubuntu:

    ```$ sudo apt-get install libsqlite3-dev```
    
    ```$ sudo pip install reprozip```


- Run your experiment with reprozip

    ```$ reprozip trace python GW150914_tutorial_uri.py```


- Check a configuration file under reprozip-trace ([config.yml](https://raw.githubusercontent.com/idaks/ligo/master/reprozip/config.yml "config.yml"))

    ```$ vim .reprozip-trace/config.yml```
    

- Create a ReproZip package named ligo_pack:

    ```$ reprozip pack ligo_pack.rpz```
    
    
##### Unpack and reproduce LIGO package in Mac OS

- Install reprounzip

    ```$ pip install reprounzip```
    
    
- Check out some information about a pack

    ```$ reprounzip info ligo_pack.rpz ```
    
    
- Check out input and output file names in a pack

    ```$ reprounzip showfiles ligo_pack.rpz``` 


- Generates a provenance graph from the trace data ligo_pack.rpz  ( [graph.png](https://raw.githubusercontent.com/idaks/ligo/master/reprozip/graph.png "graph") )

    ```$ reprounzip graph --packages drop --otherfiles io --processes run graph.dot ligo_pack.rpz```

    ```$ dot -Tpng graph.dot -o graph.png```



### 4. Analyze LIGO script with reproducibility tools


This experiment is conducted to find the bridge between 2 different reproducibility tools YesWorkflow/NoWorkflow on Docker which captures software dependencies and Reprozip which represents data dependencies. The Docker container contain YW, NW, as well as the capability to query across them using the bridge prototype, and ReproZip. 


One of the limitation of the LIGO script is lack of valid variations to either the data (input, parms) and / or the script (implementation / method) for a complex type of experiment such as LIGO which requires specific expertise. Another limitation is the scale-free problems. A small-scale version of the input data can still yields valid result
but there is a doubt whether we can run the experiment at a large scale and still get significant results.

