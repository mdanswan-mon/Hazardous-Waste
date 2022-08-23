# Version 0.3
## Relevant Commits
| Commit | Date |
| - | - |
| 7b739da | 22/08/2022 |
| b8cb511 | 22/08/2022 |
| 461d386 | 19/08/2022 |
## Summary
In Version 0.3, several changes were made to produce a runnable script for running search and analysis. 
## Results
From the above commits, there is a runnable script which produces the occurrence analysis (+ csv), word cloud, and meta data for each website visited in the google search query.
___

### Challenges
- PDF results from Google Search queries are not traversable currently, which reduces the overall results returned, therefore analyzed

### What's Next
- TF-IDF testing and analysis, comparison to occurrence results
- Domain specific stop-word removal (either by visual analysis, or dynamic analysis)
- Top n keywords
- Alter current approach to fit on all retrieved pages (corpus), before applying transformations