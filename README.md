# AutomatedEssayScoring
Using NLP Methods for Automated Essay Scoring.

## Using low-level Writing Features 

### 1. Downloaded feature extraction tools from OSF Database ✅ ### 
* All Downloaded Versions Match the Authors

### 2. Ensure feature extraction tool works by running it on one of their ASAP essays and ensuring the features come out when I run it match those of when they run it ✅ (for now) ### 
* TO DO: They have more GAMET indices not even on official GAMET index sheet. Tried with GAMET 1.0 on Mac but no luck. Will try with GAMET 1.0 and 1.1 with Windows.
* TO DO: TAASC Components differ between our outputs and theirs. (perhaps it is just updated?) 

**NOTES:**       
* Windows used with JDK 17. MAC used with JDK 8.   
* Tested with first 14 essays in author's ASAP-D7/Training/ (17834-17850 excluding 17836.txt) 
* The files, for the mac version, were in us-ascii format according to the file -I command. Attempting to change the encodings to utf8  using the codecs python package as well as trying to use the chardet python package did not result in the encodings being changed. Turns out us-ascii is actually the preferred format because, as you will see below, GAMET does not handle seemingly utf-8 encoded files well...
* Options for the tools used to get the currect number of indices per tool (by cross-comparing with authors) stored in "Our Tool Options/"
* R File "ComparingOurOutputToAuthors.R" ensures all columns match and also checks for differing values between the dataframes.

* GAMET does not match (too little features in our gamet version) → 1.0 is the only one available on their website and no other options to check to get more features. GAMET works on MAC with JDK 8. GAMET does not work on Windows with JDK 17. 
* SEANCE matches with adjusted options. This is with negation control and matched with authors. Works on MAC and (probably) windows.
* TAALED matches with adjusted options. Works on MAC and (probably) Windows.
* TAACO matches with adjusted options. Works on MAC and (probably) Windows. 
* TAALES matches with adjusted options. Had to use on Windows with JDK 17 to get hypernyms working. TAALES idx spreadsheet was useful in finding the right features. 
* TAASC general output matches with adjusted options. Had to use TAASC on Windows with JDK 17. 
* **TAASC components output do not match. **
* TAASC SCA matches with adjusted options. 


### 3. Convert excel responses to .txt files ✅
* Converted excel file to csv to encode formulas as hard text and to get right number of rows. Used "Save as.." in Excel
* Then see code in EssayToTxt.ipynb on how files were converted to individual .txt files  

### 4. Run feature extraction tools on our data to get equilvalence to d7-training-gamet.csv etc… ✅
* Used GAMET, SEANCE, TAALED, and TAACO with JDK 8 on Mac. 
* Used TAALES and TAASC with JDK 17 on Windows.
* Ensured all columns (aside from GAMET) match with that of the authors using SampleEssayValidation.R 
* NOTE: File was saved as utf-8 format in code but when downloaded on MAC is still us-ascii despite attempts to change. All files were then converted to us-ascii to play nice with GAMET (see below). Unclear impact this will play. 

* GAMET: All files processed _after changing encoding to us-ascii_. 
  * One less missing column in our spreadsheet compared to earlier Tool Validation test ("SAY_TELL" no longer missing). But no we have 5 more columns that they do not have (""IS_CAUSE_BY", "LAYING_AROUND", "MAN_MEN", "WANT_THAT_I", "WAS_BEEN"). Originally 19 files were skipped by GAMET and seemed to have characters like: â and €. These files are encoded as utf-8 even though all the other files us-ascii. We converted these files to us-ascii and GAMET was then able to run on them and process all files. 
* SEANCE: Identitical Column Names
* TAACO: Identical Column Names
* TAALED: Identitical Column Names
  * Had a math domain error which was occuring because TAALED requires at least 50 words in the text to calculate its indices. Files lower than this were removed with "remove_essays_for_taaled.py" and resulting Essays were stored in SampleEssaysTAALED/ for TAALED to run on. 
* TAALES: Identical Column Names. 
* TAASC General: Identitcal Column Names. 
* TAASC Components: Identitical Column Names. 
* TAASC SCA: Identitical Column Names. 

### 5. Remove all files to match minimum number of processed files ✅
* Because TAALED resulted in only 277 files being processed (17 being removed due to having words < 50) we removed the files from the csv of the other tools with "MinimProcessedRows.R" 

### 6. Run feature_selection.py on our csv files generated on step 2 to get equivalence to d7-training-filtered.csv 
* Compare our filtered csv features to their filtered features and see what we are missing 

8. Decide on if using rubric_score_classifier.py, rubric_score_regressor.py, or rubric_score_multiple_regressor.py
9. Look into the chosen method from step 4 and download the respective pre-trained model from their osf source code. Pick the rubric section version that you want in our case probably start with rubric section 2 (organization) since it matches on both
10. Run model.predict to get the output of their model on our dataset. Then compare that to the actual marking key scores remembering to ceiling the output values at 5 (max marking key score of organization rubric).   
NOTE: Even though the prompts for the ASAP dataset are different let’s see if it learned something about organization…

Problems:
* The negation feature, which is based on Hutto and Gilbert (2014), checks for negation words in the 3 words preceding a target word. In SEANCE, any target word that is negated is ignored within the category of interest. For example, if SEANCE processes the sentence He is not happy the lexical item happy will not be counted as positive emotion word. → should we turn this on or not (obviously we should…)
* Their rubric and our rubric don’t align (eg we have spelling/grammar and vocab whereas they just have conventions)
* Scores don’t align (their max is 6 ours is 5)
* Their prompt is different from ours. ALSO each of our prompts are different unlike theirs where all essays followed the same prompt which means their test set had the same prompt as the training set


## Using Transformer-Based Model 

Double fine-tuning:    
ASAP-AES -> Text flagged with incorrect words and spelling error -> pre-trained LLM -> fine-tuned LLM  
Fine-tuned LLM -> Suhaib Dataset with flagged incorrect words and spelling error -> Fully fine-tuned LLM 

Additional Thigs to Try:   
* Using low-level writing features + raw text with a transformers model


