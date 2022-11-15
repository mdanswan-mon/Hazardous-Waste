# Version 0.5
## Relevant Commits
| Commit | Date |
| - | - |
| 79b4289 | 14/11/2022 |
| 977418c | 07/10/2022 |
| 0a269f5 | 03/10/2022 |
| 16fd961 | 29/09/2022 |
## Summary
In Version 0.5, link selection fixes in the webpage scraping process were applied to ensure links are found for Google Scholar results, Google Scholar search results are now output to a json file, titles and abstracts of resolved from within webpages / pdfs, and improved the efficiency of the web crawler. Other changes were made to file / folder structure for improved modularity, to support future development.

## Results
The system can now generate results for the web scrapping process, which will be used in subsequent scripts (to be added) for keyword analysis and visualization using previously developed approaches
___

### Challenges
- Consistently extracting key information (e.g. abstract) from each webpage retrieved from Google Scholar
- Avoiding web scrapping bans from certain domains (primarily Google Scholar)

### What's Next
- Add module for keyword processing of web scrapping json output 
- Implement clustering on keyword processing with vectorized keywords
- Add notebook example of end-to-end process