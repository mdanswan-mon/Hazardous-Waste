# Version 0.1
## Relevant Commits
| Commit | Date |
| - | - |
## Summary
A basic Jupyter Notebook was created with a simple example of web scrapping from Google using the web scrapping framework, [Scrapy](https://scrapy.org/).
## Results
The simple example outputs the selectors for each element in the web page body which contains the class **fP1Qef**, which is specific to the container elements of each of the Google search results.
___

## Web Scrapping
### Candidate Framework
Scrapy - Open Source, Popular, and Flexible. Provides the tools to request web pages and query the content of those pages with XPath / CSS selectors
### Challenges
- Durability of anchors / identifiers in a Website body used to identify regions of interest
### What's Next
- Fleshing out element selection so we can extract meaningful information from each of the elements
- Generalizing the search criteria input to be easier to work with