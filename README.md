# SAX-LDA

To run SAX-LDA go to view folder and run main_view.py. The main data stream folder can include multiple csv files, each representing one data stream. To re-create the experiments, use folder https://github.com/UniSurreyIoT/SAX-LDA/tree/master/Analysis/traffic.
The context data stream currently only supports one data stream represented by a csv file (see https://github.com/UniSurreyIoT/SAX-LDA/tree/master/Analysis/weather).
After setting both data streams and optionally adjusting the parameter, the experiment can be started by pressing the "Start" button. 

![alt text](https://github.com/UniSurreyIoT/SAX-LDA/blob/master/images/LDAPlusPlusGui.png)

The overall workflow of SAX-LDA consists of 4 steps as can be seen in the diagram. 

![alt text](https://github.com/UniSurreyIoT/SAX-LDA/blob/master/images/WorkflowNew.png)


# Data Discretisation and Pattern Recognition
Piecewise Aggregate Approximation (PAA) is used to reduce the dimensionality of the data.

![alt text](https://github.com/UniSurreyIoT/SAX-LDA/blob/master/images/paa.pdf)

Symbolic Aggregate approXimation (SAX) uses the output to discretise the con- tinuous, numerical data streams and to recognise (lower-level) patterns.

![alt text](https://github.com/UniSurreyIoT/SAX-LDA/blob/master/images/sax2.pdf)

# Labeling
We have implemented a rule-based engine which uses the SAX patterns and the statistical information of the time frame to produce human understandable labels. The general form of the rules is given in Equation 3 where < p > is the SAX pattern, < l > is the level, < f > is the feature, < mod > a modifier for the pattern movement and < pm > is the pattern movement. 

{< p > < mean >}
       => 
{<l><f >\[<mod>\]<pm>}

<l>, <m> and <pm> can take the following values:

< l > = [“low′′, “medium′′, “high′′] < f >= [“vehicleCount′′, “avgSpeed′′,
        “tempm′′, “wspdm′′]
< m > = [“slowly′′, “rapidly′′, 
        “upward′′, “downward′′]
< pm > = [“decreasing′′, “increasing′′,
         “steady′′, “peak′′, “varying′′]

# Virtual Document Generation
The labels are grouped together from different sources within a certain time-frame toform virtual documents which can be used as input for the LDA model.

#Latent Dirichlet Allocation (LDA)
We train and incrementally update an LDA model on the virtual documents that are generated from the data streams to identify and extract relations between the labels.
Below is a plate model representation of LDA. 

![alt text](https://github.com/UniSurreyIoT/SAX-LDA/blob/master/images/platemodel.pdf)

