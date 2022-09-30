library(gtable)
library(gt)
require(tidyr)
require(tidyverse)

# We use the aesthetic gt tables package to produce publication-worthy tables

# format dataframe with statistics from historical analysis
df <- data.frame(region = c("Upper Colorado", "Lower Colorado", "Great Basin", "Pacific Northwest", "California"),
                 livneh_inc = c("4", "14", "45", "-55", "9"),
                 spear_inc = c("53", "26", "48", "43", "46"), 
                 spear_ci = c("[30, 77]", "[13, 40]", "[26, 70]", "[16, 71]", "[25, 67]"), 
                 spear_range = c("[-50, 236]", "[-39, 107]", "[-40, 225]", "[-68, 255]", "[-34, 192]"))

# plot historical Changes
gt(df) %>% tab_header(
  title= md("**Historical Changes in Snow Drought Frequency by Region (%)**")
) %>% 
  cols_label(
    region = md("**HUC2 Region**"),
    livneh_inc = md("**Livneh Increase**"),
    spear_inc = md("**SPEAR Avg Increase**"),
    spear_ci = md("**SPEAR Mean 95% CI**"),
    spear_range = md("**SPEAR Ensemble Range**")
  ) %>% 
  opt_row_striping()%>% 
  cols_align(align = c("center"))
  
# classification scheme
df_dc <- data.frame(class = c("D4", "D3", "D2", "D1", "D0", "NN", "W0", "W1", "W2",  "W3", "W4"), 
                    desc = c("Exceptional Drought", "Extreme Drought", "Severe Drought", "Moderate Drought",
                             "Abnormally Dry", "Near Normal", "Abnormally Wet", "Moderate Wet Spell", "Severe Wet Spell", 
                             "Extreme Wet Spell", "Exceptional Wet Spell"),
                    # zval = c("$\\alpha$"),
                    zval = c("ZSWE ≤ -2.0", "-2.0 < ZSWE ≤ -1.6","-1.6 < ZSWE ≤ -1.3",
                             "-1.3 < ZSWE ≤ -0.8","-0.8 < ZSWE ≤ -0.5","-0.5 < ZSWE < 0.5",
                             "0.5 ≤ ZSWE < 0.8","0.8 ≤ ZSWE < 1.3","1.3 ≤ ZSWE < 1.6",
                             "1.6 ≤ ZSWE 2.0", "2 ≤ ZSWE"),
                    ext = c(0.023, 0.055, 0.097, 0.21, 0.31, "--", 0.31, 0.21, 0.097, 0.055, 0.023)
                    )

gt(df_dc)%>% tab_header(
  title= md("**Snow Drought Classification by ZSWE Score**")
) %>% 
  cols_label(
    class = md("**Drought Severity**"),
    desc = md("**Description**"),
    zval = md("**ZSWE Range**"),
    ext = md("**Probability of more Extreme**")
  ) %>% 
  opt_row_striping() %>% 
  cols_align(align = c("center"))


test <- data.frame(class = c("$$\\alpha$$"))
gt(test)
library(knitr)
kable(test, escape = FALSE, index = FALSE)

gt(df_dc, sanitize(str, type = "latex"))
m <- xtable(df_dc)
print(m, sanitize.text.function = function(x) {x})


df2 <- data.frame(key = 1, 
                 equation = c("$$exp(1.6 - 3.327 \\times x^2)$$"))

kable(df2, escape = FALSE)


df_sf2 <- data.frame(region = c("Upper Colorado", "Lower Colorado", "Great Basin", "Pacific Northwest", "California"),
                     at50 = c(83, 87, 100, 100, 100),
                     at75 = c(0, 23, 7, 3, 93), 
                     at90 = c(0, 7, 0, 0, 17))
df_sf5 <- data.frame(region = c("Upper Colorado", "Lower Colorado", "Great Basin", "Pacific Northwest", "California"),
                     at50 = c(100, 100, 100, 100, 100),
                     at75 = c(97, 100, 100, 100, 100), 
                     at90 = c(30, 83, 70, 53, 100))
df_sf2$ssp <- "245"
df_sf5$ssp <- "585"

new <- rbind(df_sf2, df_sf5)
new %>% pivot_wider(values_from = c(at50, at75, at90), names_from = c(ssp)) %>% 
  gt()%>% tab_header(
    title= md("**Probability of No-Snow Transition by 2100**")
  ) %>% 
  tab_spanner(
    label = "Area Threshold under SSP2-4.5",
    columns = c(at50_245, at75_245, at90_245)
  ) %>% 
  tab_spanner(
    label = "Area Threshold under SSP5-8.5",
    columns = c(at50_585, at75_585, at90_585)
  ) %>% 
  cols_label(
    region = md("**Region**"),
    at50_245 = md("**50%**"),
    at75_245 = md("**75%**"),
    at90_245 = md("**90%**"),
    at50_585 = md("**50%**"),
    at75_585 = md("**75%**"),
    at90_585 = md("**90%**")
  ) %>% 
  opt_row_striping() %>% 
  cols_align(align = c("center")) %>% 
  data_color(
    columns = c(at50_245, at75_245, at90_245, at50_585, at75_585, at90_585),
    colors = scales::col_numeric(
      palette = c("#1C5C9F", "white", "#A51429"),
      domain = c(0, 100)
      ),
    alpha = 1
  )
