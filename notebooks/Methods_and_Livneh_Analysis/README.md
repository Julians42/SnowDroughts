# Snow Drought's Data Investigation 
Much of the early project was data exploration, transitioning to computation which was written mostly as scripts, and then analysis of results. The majority of the data exploration and results analysis was done primarily in jupyter notebooks both for the combined REPL / output format and because it was a convient way to tunnel into the GFDL servers using remote SSH. 

## Exploratory notebooks
The following notebooks were  primarily exploratory in nature, focusing on developing methods and examining raw snowpack data to develop our drought indices. While not specifically tied to results I believe they are helpful for understanding the process of how we arrived at our workflow and are fairly interesting!
 1. `Snow Drought Distribution Analysis` examines historical distributions of SWE across large watershed regions in the US West. Here we learned that SWE distributions both varied widely across mountainous regions and that modeling with a parametric distribution (e.g. normal) would not be appropriate.
 2.  `Cleaned Drought Classification` is an example run of our drought classification method. We examined how we thought analysis would perform over larger vs. smaller watershed regions (HUC2 vs HUC4). We settled on running analysis across the HUC2 regions and then going straight to a 1/2 degree grid. 
 3. `Livneh Initial Investigation` was essentially an exercise in plotting the Livneh dataset. It revealed that visually there was very little trend in the historical dataset. The plots look quite nice due to the 1/16 resolution.
 4. `Livneh Climatology Investigation` examines the temporal distribution of snowpack across the US as it varies by watershed region. For example, we found that snowpack in New England grew at a similar pace to Western watersheds, however the melt season was much more rapid. We hypothesize this is due to the East's lower topology.
 5. `Presentation Plots` scripts a few nice plots for presentations.
