# Hazardous-Waste
## Environment Setup
1. Install the **latest** [Conda](https://docs.conda.io/en/latest/miniconda.html) based on your architecture (most likely x64) - If you are unsure, for Windows 10/11, please review [this](https://www.tenforums.com/tutorials/4399-see-if-system-type-32-bit-x86-64-bit-x64-windows-10-a.html) site to find your system architecture.
2. Restart your Computer (sometimes necessary to complete installation)
2. Open Window Powershell in the root directory where you cloned this repository
3. Type the following to install all Python dependencies ```conda create --name HWaste --file requirements.txt```
4. Type the following to activate the Conda environment ```conda activate HWaste```
## Usage
### Search and Keyword Counts
This allows you to review Google Search results based on a keyword search. A keyword analysis is completed on each page in the result set, which is **optionally** displayed in a visualization and/or output to a CSV file.
<hr>

**Example Usage** From the root directory, run the following command:
``` python .\SearchAndAnalyze.py -t "Metal" "Waste" "Hazard" "Batteries" -p 2 --save-occurrences --save-wordclouds```

**Options**
|Name|Option|Possible Values|
|-|-|-|
|**Search Tags**|-t|Keywords, surrounded with double quotes **""**; Each keyword should be separated with a space|
|**Page Count**|-p|Number of pages of google search results to review|
|**Do / Don't Save Occurrences**|--save-occurrences / --no-save-occurrences|Whether to save keyword counts to a CSV file|
|**Do / Don't Save Word Cloud visualizations**|--save-wordclouds / --no-save-wordclouds|Whether to save word cloud visualizations|
|**Save Folder Path**|-path|The folder to which all files produced are saved|