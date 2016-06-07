# SAX-LDA

To run SAX-LDA go to view folder and run main_view.py. The main data stream folder can include multiple csv files, each representing one data stream. To re-create the experiments, use folder https://github.com/UniSurreyIoT/SAX-LDA/tree/master/Analysis/traffic.
The context data stream currently only supports one data stream represented by a csv file (see https://github.com/UniSurreyIoT/SAX-LDA/tree/master/Analysis/weather).
After setting both data streams and optionally adjusting the parameter, the experiment can be started by pressing the "Start" button. 

![alt text](https://github.com/UniSurreyIoT/SAX-LDA/blob/master/images/LDAPlusPlusGui.png)

The overall workflow of SAX-LDA consists of 4 steps as can be seen in the diagram. 

![alt text](https://github.com/UniSurreyIoT/SAX-LDA/blob/master/images/WorkflowNew.pdf)


# Data Discretisation and Pattern Recognition
Piecewise Aggregate Approximation (PAA) is used to reduce the dimensionality of the data.

![alt text](https://github.com/UniSurreyIoT/SAX-LDA/blob/master/images/paa.pdf)

Symbolic Aggregate approXimation (SAX) uses the output to discretise the con- tinuous, numerical data streams and to recognise (lower-level) patterns.

![alt text](https://github.com/UniSurreyIoT/SAX-LDA/blob/master/images/sax2.pdf)

# Labeling
The information obtained from the pat- tern. The rules are explained in Section 5.3 together with the statistical values are translated into labels based on rules.

# Virtual Document Generation
The labels are grouped together from different sources within a certain time-frame toform virtual documents which can be used as input for the LDA model.

#Latent Dirichlet Allocation (LDA)
We train and incrementally update an LDA model on the virtual documents that are generated from the data streams to identify and extract relations between the labels.
Below is a plate model representation of LDA. 

![alt text](https://github.com/UniSurreyIoT/SAX-LDA/blob/master/images/platemodel.pdf)

