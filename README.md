# AutomatedEssayScoring

Using NLP Methods for Automated Essay Scoring. This is previous work that worked on grading essays using low-level writing features. 

**NOTE: Onging work is stored in separate repository that now utilizes large language models including PaLM 2 with Vertex AI and distributed cloud computing, Llama 2, and BERT.**

## Using low-level Writing Features

**Low-Level Writing Features Advantages:**

- Advantages of using low-level writing features is that we can use the 20 most important low-level features the author found per rubric and report that to the user and say how they did on those features and they can use that to improve...
- As shown in the paper here (https://osf.io/2uahv) GPT alone does a worse job predicting essay scores than using low-level features alone. Paper also shows lower reliability (QWK) when using GPT alone vs low-level features alone

### 1. Downloaded feature extraction tools from OSF Database ✅

- All Downloaded Versions Match the Authors

### 2. Ensure feature extraction tool works by running it on one of their ASAP essays and ensuring the features come out when I run it match those of when they run it ✅ (for now)

- TO DO: They have more GAMET indices not even on official GAMET index sheet. Tried with GAMET 1.0 on Mac but no luck. Will try with GAMET 1.0 and 1.1 with Windows.
- TO DO: TAASC Components differ between our outputs and theirs. (perhaps it is just updated?)

- Windows used with JDK 17. MAC used with JDK 8.
- Tested with first 14 essays in author's ASAP-D7/Training/ (17834-17850 excluding 17836.txt)
- The files, for the mac version, were in us-ascii format according to the file -I command. Attempting to change the encodings to utf8 using the codecs python package as well as trying to use the chardet python package did not result in the encodings being changed. Turns out us-ascii is actually the preferred format because, as you will see below, GAMET does not handle seemingly utf-8 encoded files well...
- R File "ComparingOurOutputToAuthors.R" ensures all columns match and also checks for differing values between the dataframes.

**Tools:**

- Options for the tools used to get the currect number of indices per tool (by cross-comparing with authors) stored in "Our Tool Options/"
- **GAMET does not match (too little features in our gamet version)** → 1.0 is the only one available on their website and no other options to check to get more features. GAMET works on MAC with JDK 8. GAMET does not work on Windows with JDK 17.
- SEANCE matches with adjusted options. This is with negation control and matched with authors. Works on MAC and (probably) windows.
- TAALED matches with adjusted options. Works on MAC and (probably) Windows.
- TAACO matches with adjusted options. Works on MAC and (probably) Windows.
- TAALES matches with adjusted options. Had to use on Windows with JDK 17 to get hypernyms working. TAALES idx spreadsheet was useful in finding the right features.
- TAASC general output matches with adjusted options. Had to use TAASC on Windows with JDK 17.
- **TAASC components output do not match.**
- TAASC SCA matches with adjusted options.

### 3. Convert excel responses to .txt files ✅

- Converted excel file to csv to encode formulas as hard text and to get right number of rows. Used "Save as.." in Excel
- Then see code in EssayToTxt.ipynb on how files were converted to individual .txt files

### 4. Run feature extraction tools on our data to get equilvalence to d7-training-gamet.csv etc… ✅

- Used GAMET, SEANCE, TAALED, and TAACO with JDK 8 on Mac.
- Used TAALES and TAASC with JDK 17 on Windows.
- Ensured all columns (aside from GAMET) match with that of the authors using SampleEssayValidation.R
- NOTE: File was saved as utf-8 format in code but when downloaded on MAC is still us-ascii despite attempts to change. All files were then converted to us-ascii to play nice with GAMET (see below). Unclear impact this will play.

- GAMET: All files processed _after changing encoding to us-ascii_.
  - One less missing column in our spreadsheet compared to earlier Tool Validation test ("SAY_TELL" no longer missing). But no we have 5 more columns that they do not have (""IS_CAUSE_BY", "LAYING_AROUND", "MAN_MEN", "WANT_THAT_I", "WAS_BEEN"). Originally 19 files were skipped by GAMET and seemed to have characters like: â and €. These files are encoded as utf-8 even though all the other files us-ascii. We converted these files to us-ascii and GAMET was then able to run on them and process all files.
- SEANCE: Identitical Column Names
- TAACO: Identical Column Names
- TAALED: Identitical Column Names
  - Had a math domain error which was occuring because TAALED requires at least 50 words in the text to calculate its indices. Files lower than this were removed with "remove_essays_for_taaled.py" and resulting Essays were stored in SampleEssaysTAALED/ for TAALED to run on.
- TAALES: Identical Column Names.
- TAASC General: Identitcal Column Names.
- TAASC Components: Identitical Column Names.
- TAASC SCA: Identitical Column Names.

### 5. Remove all files to match minimum number of processed files ✅

- Because TAALED resulted in only 277 files being processed (17 being removed due to having words < 50) we removed the files from the csv of the other tools with "MinimProcessedRows.R"
- Saved in "SampleEssaysFeaturedTrunc/"

### 6. Run feature_selection.py on our csv files generated get equivalence to d7-training-filtered.csv ✅

- Ran feature_selection on "SampleEssaysFeaturedTrunc/" using FeatureSelection.ipynb
- Since the feature_selection package could not be imported for some reason just copied the source code into google colab
- Compare our filtered csv features to their filtered features and see what we have in common using FeatureSelectionValidation.R
- Saved in SampleEssaysFeaturedTruncFiltered/

After filtering we are left with 609 (minus the header) features to use for model training which will **not work!**.

Their workflow consisted of concatenating all their filtered features into a giant array of shape (1597, 397) where each row was an essay and each column was a filtered feature. They then split this into training and testing and ran a DNN Classifier on top of this to get their results.

The problem is we can't just use their pre-trained classifier since it expects an input of 397 columns. We instead have 608 features so we would have to train our own classifier for this to work.
OR  
**We could see what columns they had after filtering and hope our dataset has those too and just use those columns rather than using their feature_selection.py method. That way our inputs to the model match.** <- This is what we're going to do with "cheating" in the next step

## 7. Cheating with feature_selection ✅

Rather than doing the feature_selection process outlined in feature_selection.py we will take the features that they selected for and just use those columns from our essays. This will ensure our input to their model is the same as their input.

We still have to ensure to MinMaxScaler() our variables as that is done in feature_selection.py. MinMaxScaler() was the only transformation done on the actual values of the cells which was confirmed in FeatureSelectionCheating.ipynb. The MinMaxScaler transformation was also done in FeatureSelectionCheating.ipynb and the normalized datasets were saved to SampleEssaysFeaturesTruncNormalized/. The file FeatureSelectionCheating.R was then used to generate the normalized datasets with the final features to be used in the input. These datasets are located at SampleEssaysFeaturesTruncCheatingNormalizedFiltered/

We confirmed the features we had and the authors matched in ValidatingInput.py.

## 8. Using rubric_score_classifier.py to generate scores for our essays ✅

Now that we have confirmed the features we have and the authors match in ValidatingInput.py we can run their pre-trained model on our dataset.

**Our Rubric vs Authors:**  
Authors:  
R1 - Ideas : Is the story told with ideas that are clearly focused on the topic and are thoroughly developed with specific, relevant details?  
R2 - Organization : Are organization and connections between ideas and/or events clear and logically sequenced?  
R3 - Style :Does the command of language, including effective and compelling word choice and varied sentence structure, clearly support the writer’s purpose and audience?  
R4 - Conventions: Is the use of conventions of Standard English for grammar, usage, spelling, capitalization, and punctuation consistent and appropriate for the grade level?

Ours:  
R1 - CONTENT: Inclusion and elaboration of ideas and sense of audience and purpose.  
R2 - ORGANISATION: Coherence and cohesion.  
R3 - GRAMMAR: Use of syntactic patterns and grammatical accuracy.  
R4 - VOCABULARY: Range and appropriateness.
R5 - SPELLING AND PUNCTUATION.

Workflow:

1. Make sure our filename column in each of our tools-filtered.csv files are in the same order. This is done with OrderRows.py and the correctly ordered CSV filse are saved in SampleEssaysFeaturesTruncCheatingNormalizedFilteredOrdered/
2. Re-validate we didn't lose any features, feature order, or our overall shape when re-ordering the rows by running ValidatingInput.py
3. Use Model Testing/model_classifier.py and global variables depending on the rubric used. This script will then save the predicted labels in PredictedLabels/
   - This script loads in their pre-trained model for a given rubric they trained on and then uses that model to predict a given Markign Key from the sample essays

From original paper regarding scoring:

> For D7, the resolved rubric scores were computed by adding the human raters’ rubric scores. Hence, each human rater gave a score between 0 and 3 for each rubric (Ideas, Organization, Style, and Conventions; see Table 3). Subsequently, the two scores were added together, yielding a rubric score between 0 and 6. Finally, the holistic score was determined according to the following formula: HS = R1 + R2 + R3 + (2 ∗ R4), for a score ranging from 0 to 30.

## 9. Evaluate generated scores for our essays from rubric_score_classifier

The Evaluating is done in Model Testing/evaluate_preds.py

1. Change Global Variables at top of file to what Rubric Model you want to use from the author's and what Marking Key Labels from our dataset do you want to compare that model's output to

Pre-Processing our Labels:

2. Remove predicted labels for file names that are not included in the 277.
3. Clip our actual labels to the maximum marking scores
4. Write the mapping function to use for your corresponding rubric and assign it to the global variables. (Their range is [0,6] while our range varies from [1,5], [1,4], and even [1,2])

Majority Classifier:  
5. Compare our model with a majority classifier which is a naive ML model that just uses the mode of the labels to predict the lables - it is a good baseline to compare your model against and what the author's used

Metrics:  
6. Use Metrics from the author's file like accuracy and adjacent score accuracy  
7. Use our own metrics like classification reports, heatmaps, correlations, plots

TO DO:

- Save Metrics in files by using format "Rubric2ModelforMarkingKey3" meaning it used the Author's Rubric 2 model to generate predictions for MarkingKey3 - metrics to save: label_distributions, classificaiton_report, accuracies, QWK, HeatMap
  - Add QWK (in author's metrics.py) and HeatMap (see GPT)
- Have separate folders for each metric and save files for that given metric in that metric's folder with the above format

- See what low level features of the 397 are from what tool -> possible allows us to know if we can eliminate tools from our pipeline if their features are not going to be used OR could limit the options we have to select for certain tools (such as the incredibly long LDA option). However, if we train our own model we will have to actually filter the features by variance and colinearity and hence, will get a new set of features that we will have to see what tools it comes from.

### 10. Conclusions from Evaluation

- Based on the classification report it looks like it routinely does not predict very low scores. This may be due to the little amount of low essays in the original dataset per rubric:
  ![image](https://github.com/Varun-Krishnan1/AutomatedEssayScoring/assets/19865419/bab71dd0-7109-4243-9338-28f9b3962e93)
  <img width="1288" alt="image" src="https://github.com/Varun-Krishnan1/AutomatedEssayScoring/assets/19865419/2ca9dc80-a823-46ab-964a-609d10767dde">

- Their majority classifier (see image below) does significantly worse than our majority classifier meaning we have an imbalanced dataset with too small of samples for analysis to be useful. Also could be that predicting scores between 1-5 is just not granular enough to be useful because you can just use mode for pretty good results...
  <img width="1308" alt="image" src="https://github.com/Varun-Krishnan1/AutomatedEssayScoring/assets/19865419/216266df-dd29-44a2-91b9-5f5cdae61e04">

  - Our model does **not** outperform a majority classifier

- However, the power of our model is explainability and feedback which the majority classifier doesn't allow for. Furthermore, you have to look at the F1 score which takes into account precision and recall which is a better evaluator than just acurracy.

**For RUBRIC 2 (Organization):**

- Due to our max marking key score being 4 while their max marking key value is 6 we did a heuristic mapping to try to evaluate the predictions vs actual labels.  
  Our Key : Their Key
  1 : 1,2
  2 : 3
  3 : 4
  4 : 5,6
- This mapping resulted in the following result.     
  <img width="426" alt="image" src="https://github.com/Varun-Krishnan1/AutomatedEssayScoring/assets/19865419/003d936c-0487-4457-b045-61683ea38008">         
  While not the greatest result manaully evaluating the output labels to the essays it doesn't seem too bad.

**For RUBRIC 3 (Content):**

**For RUBRIC 4 (Test):**

## Problems with Low-Level Features:

**Problem's that can be solved if we train our own classifier:**

- Their rubric and our rubric don’t align (eg we have spelling/grammar and vocab whereas they just have conventions)
- Scores don’t align (their max is 6 ours is 5,4, and even 2)
- Their prompt is different from ours.

**Problems that we need to ask Suhaib about:**

- The dataset we have - does the distribution of rubric scores match that of the real-world?
- the dataset we have is incredibly noisy and responses that shouldn't be getting very high scores are getting those scores (eg, essays 2,3,4, etc...)
- Each of the prompts in the paper he gave us are different unlike the Author's model where all essays followed the same prompt which means their test set had the same prompt as the training set.
  - This also allows for learnign the content/ideas rubric because it's trained on prompt so doesn't need context of prompt whereas if the prompts are different everytime we need to somehow use a model that has context of that question (transformer-based model)
- What is going to be the range of the grading rubric? (Hopefully a bigger range so a majority classifier doesn't do just as well as us)
- Are the rubrics going to be the same for all essays or will the rubrics vary?

## Using Transformer-Based Model

**Transformer-Based Model Advantages:**

- Can allow for context of prompts letting you predict essays with different prompt from training data
- Lu and Hu (2022) showed that two of the context-aware lexical sophistication measures created with contextualized word embeddings using the BERT model correlated more strongly with L2 English writing quality than traditional lexical sophistication measures obtained with TAALES.

Process:

- Can do Double fine-tuning:
  - ASAP-AES -> Text flagged with incorrect words and spelling error -> pre-trained LLM -> fine-tuned LLM
  - Fine-tuned LLM -> Suhaib Dataset with flagged incorrect words and spelling error -> Double fine-tuned LLM

## Using GPT

### 1. Preparing Input

- Inspired from this paper: https://osf.io/2uahv
- Code located in the GPT/ folder
- PrepareInput.py: Creates a prompt followed by the essay to score based on prompt from above paper. Essays to score are saved in batches due to limitations of GPT input size. Batches are saved in GPT4_Input/
- NOTE: The prompt assumes that the minimum score in Suhaib's marking is 1 and maximum score is the max from that rubric - in reality it looks like minimum score can be less than 1 for some rubrics (eg, marking key 3 grammer with min of 0) -> this will have to be fixed

### 2. Predicting Labels

- Each file (i.e batch of essays) in GPT4_Input/ is fed one-by-one to GPT4 and the corresponding labels predicted by GPT4 are hard-coded in evaluateGPTLabeling.py

### 3. Evlauting Labels

- The evaluation was done using Marking Key 3 Grammer with RUBRIC_MAX_SCORE = 5
- The evluation is done in evaluateGPTLabeling.py: similar to how the model created from Kumar et al's paper is evaluated in Model Testing/evaluate_preds.py the same evaluation metrics are used. The labels from GPT are from 1 - RUBRIC_MAX_SCORE. However, the scores of some rubric are 0 so we need to convert all 0 values to 1 and all values above the RUBRIC_MAX_SCORE to RUBRIC_MAX_SCORE

Results:    
<img width="488" alt="image" src="https://github.com/Varun-Krishnan1/AutomatedEssayScoring/assets/19865419/f650bd17-0de1-4aee-bf95-286ccdf95c3e">
- You can see it does slightly worse with F1 score compared to our model but the acurracy and percentage of adjacent matches are similar.

TO DO:

- Try with different rubrics
- Adjust minimum score in prompt for Marking Key 3. The prompt assumes that the minimum score in Suhaib's marking is 1 and maximum score is the max from that rubric - in reality it looks like minimum score can be less than 1 for some rubrics (eg, marking key 3 grammer with min of 0)

### 4. Conclusions from GPT Evaluation

## Future Steps

- Best state-of-the-art model right now is apparently BERT + low-level features by Lagakis & Demetriadis (2021) according to GPT paper (https://osf.io/2uahv)
