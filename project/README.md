# Project

The description of the research project can be found in the [chapter 11 of the Network Science book](http://networksciencebook.com/chapter/11), subsection _Final Research Project_.

## Questions of Interest and How to Investigate

1. Which years had the most contributions?
    1. Rationale: it tells us the history of wikipedia and the community that maintains it;
    2. How: compute the total number of votes per year;
2. Who are the key people?
    1. Rationale: we want to know how much wikipedia depend on key people;
    2. How: analyse the robusttness to attack, per year;
3. How many connected components are there?
    1. Idea: this tell us something about how the community is divided;
    2. How:
        1. change the network to an underected one;
        2. compute the number of components;
        3. plot the size of each component
4. How active is the community?
    1. Idea: a statistical analysis of the in-degree and out-degree of the network may give us some insights;
    2. How: compute statistics with the out-degree of the network:
        1. plot the quatiles of the out-degree per year;
5. Is power law applicable?
    1. Idea: is it the case that few members contribute the most?
    2. How: plot the degree distribution of the network and make a curve fit: find out if it is governed by the power law;
