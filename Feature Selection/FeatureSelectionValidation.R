## ========================================== ## 
## For Feature Selection: Check to see features (cols) that are different 
## between our filtered dataset and theirs
## TO DO 
## 
## 
## 
## Changelog:
## 05/23/23 - Created file 
## ========================================== ## 

library(tidyverse)

# Specify the file path to write the output
# output_file <- "ComparisonResults.txt"
# sink(output_file)

# Ensure this is top-level folder for Sample Essays (.../Sample Essays)
base_folder = "~/Desktop/AES/Feature Selection"
setwd(base_folder)

our_output_folder = "SampleEsssaysTruncFiltered/"
author_output_folder = "AuthorFeaturesFiltered/"

# Get a list of all CSV files in the folder
our_file_list <- list.files(path = our_output_folder, pattern = "*.csv", full.names = TRUE)
author_file_list <- list.files(path = author_output_folder, pattern = "*.csv", full.names = TRUE)

# Store output data in dictionary in format (gamet: gamet_data, seance: seance_data, etc...)
our_output_dict <- list()
author_output_dict <- list()

# Construct our output dictionary 
for (file in our_file_list) {
  # Extract the filename from the full path ("d7-training-gamet-filtered" -> "gamet")
  words <- strsplit(file, "-")[[1]]
  word_before_last_hyphen <- words[length(words) - 1]
  
  key <- word_before_last_hyphen
  
  data <- read.csv(file)
  our_output_dict[[key]] <- data
}

# Construct author output dictionary 
for (file in author_file_list) {
  # Extract the filename from the full path ("d7-training-gamet-filtered" -> "gamet")
  words <- strsplit(file, "-")[[1]]
  word_before_last_hyphen <- words[length(words) - 1]
  
  key <- word_before_last_hyphen
  
  data <- read.csv(file)
  author_output_dict[[key]] <- data
}

# Ensure keys match 
print(names(our_output_dict))
print(names(author_output_dict))

#### Ensure all rows have same number of rows as original (277 after truncating) #### 
# Ensure we didn't lose any rows during feature selection
print("### Checking Matching Number of Rows ###")
total_essays = 277
print(paste("Total Essays (Rows): ", total_essays))

for (key in names(our_output_dict)) {
  print(paste("---", toupper(key), "---"))
  df <- our_output_dict[[key]]
  if(nrow(df) != total_essays) {
    print(paste("!DF Num Rows does not match!: ", nrow(df)))
  }
  else {
    print("Num Rows Match")
  }
}


#### Compare the data frames columns between two dictionaries ####

print("### Checking Matching Column Names ###")

total_our_features = 0 
total_author_features = 0
for (key in names(our_output_dict)) {
  print(paste("---", toupper(key), "---"))
  if (is.null(author_output_dict[[key]])) {
    print(paste("Key", key, "is present in our_output_dict but not in author_output_dict"))
    next
  }
  
  df1 <- our_output_dict[[key]]
  df2 <- author_output_dict[[key]]
  
  # keep track of total features after filtering
  total_our_features = total_our_features + length(names(df1)) 
  total_author_features = total_author_features + length(names(df2)) 
  # Check if the data frames have the same columns
  if (!identical(names(df1), names(df2))) {
    identical = TRUE 
    
    missing_cols1 <- setdiff(names(df2), names(df1))
    missing_cols2 <- setdiff(names(df1), names(df2))
    
    if (length(missing_cols1) > 0 && !(length(missing_cols1) == 1 && missing_cols1 %in% c("Filename", "filename"))) {
      print(paste("Columns missing in our_output_dict for key", key, ":"))
      print(missing_cols1)
      print(paste(length(missing_cols1), "missing"))
      identical = FALSE
    }
    
    if (length(missing_cols2) > 0 && !(length(missing_cols2) == 1 && missing_cols2 %in% c("Filename", "filename"))) {
      print(paste("Columns missing in author_output_dict for key", key, ":"))
      print(missing_cols2)
      print(paste(length(missing_cols2), "missing"))
      identical = FALSE
    }
    
    if(identical) {
      print("Identitical Column Names")
    }
  }
  else {
    print("Identitical Column Names")
  }
  
}
print(paste("Total Our features after filtering:", total_our_features))
print(paste("Total Author features after filtering:", total_author_features))
