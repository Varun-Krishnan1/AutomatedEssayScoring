# AutomatedEssayScoring
Using NLP Methods for Automated Essay Scoring.

## Using low-level Writing Features 

### 1. Downloaded feature extraction tools from OSF Database ✅ ### 
* All Downloaded Versions Match the Authors

### 2. Ensure feature extraction tool works by running it on one of their ASAP essays and ensuring the features come out when I run it match those of when they run it ### 
* TO DO: Run TAASC will take a while due to dataset loading - use below options 
<img width="412" alt="Screen Shot 2023-05-23 at 12 19 21 AM" src="https://github.com/Varun-Krishnan1/AutomatedEssayScoring/assets/19865419/9ed7e565-5d62-470c-ae13-04d5807d408e">

* TO DO: Use R to see what columns are missing and cross-reference with Gamet Index Spreaedsheet. Seance might not match due to negation control -> try again with it turned off if doesn't match. 
* TO DO: Try TAALES on windows to see if hypernym + polysenyms load. If not exclude the hyper_ and poly_ indices based on index spreadhset (last set of indices on d7-training-taales.csv) 
* TO DO: Use R to make sure all columns that match between the files have same values 

Tested with first 14 essays in author's ASAP-D7/Training/ (17834-17850)    
Options for the tools used to get the currect number of indices per tool (by cross-comparing with authors) stored in "Our Tool Options/"

* GAMET does not match (too little features in our gamet version) → 1.0 is the only one available on their website and no other options to check to get more features.
* SEANCE matches with adjusted options. Turned on negation control but unsure if that is what authors used. 
* TAALED matches with adjusted options 
* TAACO matches with adjusted options but only works on MAC! 
* TAALES stuck at "Loading Hypernymy..." ! All other indices besides hyper_ and poly_ match. TAALES idx spreadsheet was useful in finding the right features. 
* TAASC outputs 3 files - ...-taasc.csv, ...-taasc-sca.csv, ...-taasc-components.csv. TAASC spreadsheet useless.


3. Download excel file from Suhaib then change it to csv to encode formulas as hard text and to get right number of rows
4. Run feature extraction tools on our data to get equilvalence to d7-training-gamet.csv etc…
5. Run feature_selection.py on our csv files generated on step 2 to get equivalence to d7-training-filtered.csv
6. Decide on if using rubric_score_classifier.py, rubric_score_regressor.py, or rubric_score_multiple_regressor.py
7. Look into the chosen method from step 4 and download the respective pre-trained model from their osf source code. Pick the rubric section version that you want in our case probably start with rubric section 2 (organization) since it matches on both
8. Run model.predict to get the output of their model on our dataset. Then compare that to the actual marking key scores remembering to ceiling the output values at 5 (max marking key score of organization rubric).   
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


