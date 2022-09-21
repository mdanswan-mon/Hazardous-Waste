# Version 0.4
## Relevant Commits
| Commit | Date |
| - | - |
| 7663721 | 21/09/2022 |
| c1a084d | 20/09/2022 |
| 16189b0 | 20/09/2022 |
| e9f2ffd | 18/09/2022 |
| 0674229 | 29/08/2022 |
| bd940e5 | 29/08/2022 |
| e0d4d43 | 24/08/2022 |
## Summary
In Version 0.4, the following components were added: stop word processing was, Google Scholar scraping, and keyword extraction techniques testing. Further testing and prototyping was done to improve the reliability and consistency of the web scrapping foundations.
## Results
Currently, the web scrapping system can retrieve all common documents from google search (html/htm, pdf, doc/docx, etc) and process those document to retrieve x keywords of the documents using **Yake** and **KeyBERT**. 
___

### Challenges
- Preprocessing producing textual artifacts in the document processed by Yake / KeyBERT

### What's Next
- Preprocessing improvement - Use NLTK / Sklearn / other libraries to do preprocessing
- Implement csv reading of pre-reviewed documents (title, authors, abstract)
- Implement csv writing of 100 keywords of each document
- Setup module for further text analytics and exploration
- Implement clustering on each document with vectorized keywords 