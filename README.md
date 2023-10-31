# flavorpred

Matching mass spectrometry data to human sensory profiles of distillates to predict their flavor profiles

## StatisticalAnalysis.ipynb
Statistical analyses were conducted on an extensive LC-MS data and human sensory evaluations. Noteworthy correlations between the Mass Spectrometry (MS) data and the expert panelist assessments have revealed previously undiscovered molecules associated with specific flavors

## Ontology.ipynb
The Ontology approach incorporates MS data and expert knowledge by utilizing a flavor wheel as an ontology to predict distinct flavor profiles. 
The results show qualitative connections between the identified molecules and flavors, discerning whether a sample has a specific flavor

## LinearRegression.ipynb
Linear Regression aims to find optimal parameters for each identified molecule from the MS, weighing it correspondingly, to establish reasonable correlations between
the reference and panelist data. Meaningful correlations between these two datasets could be created. Especially when conducting it with the newly found molecules from
the statistical analysis. This approach proves how specific molecules can contribute to a flavor.

## FuzzySweet.ipynb
In this approach, the intensity of the flavors ’Sweet’, ’Fruity’ and ’Woody’ are predicted by examining the individual molecule intensities identified in the MS analysis. By incorporating fuzzy logic it enables us not only to determine the presence of a flavor but also quantify its specific intensity.
This approach involves fuzzification, rule setup, and defuzzification. Five different defuzzification methods are explored to determine the most effective one for the
data. Among these methods, the ’bisector’ one demonstrated the best correlation for the available data.
