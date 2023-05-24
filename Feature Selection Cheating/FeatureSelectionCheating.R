## ========================================== ## 
## For Feature Selection Cheating: Just use the features they have so 
## we can use their model 
## TO DO 
## 
## 
## 
## Changelog:
## 05/23/23 - Created file 
## ========================================== ## 

library(tidyverse)


# Ensure this is top-level folder for Feature Selection Cheating (.../Feature Selection Cheating)
base_folder = "~/Desktop/AES/Feature Selection Cheating"
setwd(base_folder)

# use the normalized data to generate final filtered features
our_output_folder = "SampleEssaysFeaturesTruncNormalized/"
author_output_folder = "../Feature Selection/AuthorFeaturesFiltered/"

# Get a list of all CSV files in the folder
our_file_list <- list.files(path = our_output_folder, pattern = "*.csv", full.names = TRUE)
author_file_list <- list.files(path = author_output_folder, pattern = "*.csv", full.names = TRUE)

# Store output data in dictionary in format (gamet: gamet_data, seance: seance_data, etc...)
our_output_dict <- list()
author_output_dict <- list()

# Construct our output dictionary 
for (file in our_file_list) {
  filename <- basename(file)  # Extract the filename from the full path ("d7-training-gamet" -> "gamet")
  key <- gsub(".csv$", "", sub(".*-", "", filename))  # Extract the key from the filename
  data <- read.csv(file)
  
  # Check if the column name is "Filename" or "filename" and convert it to "filename"
  if ("Filename" %in% colnames(data)) {
    colnames(data)[colnames(data) == "Filename"] <- "filename"
  } else if ("filename" %in% colnames(data)) {
    colnames(data)[colnames(data) == "filename"] <- "filename"
  }
  
  # Get basename for each file in csv ("../../17834.txt" -> "17834.txt")
  file_path = data$filename[1] # 1-based indexing
  # Fix windows filepaths so below basename() function works 
  if (startsWith(file_path, "C:")) {
    # Replacing backslashes with forward slashes
    data$filename <- gsub("\\\\", "/", data$filename)
  }
  
  # Replace full file paths with basename in the "filename" column so it matches authors column  
  data$filename <- basename(data$filename)
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

#### Keep Features only from the Filtered Author's Features ####

# Remove columns not in author_output_dict
new_output_folder <- "SampleEssaysFeaturesTruncCheatingNormalizedFiltered/"
for (key in names(our_output_dict)) {
  if (key %in% names(author_output_dict)) {
    our_df <- our_output_dict[[key]]
    author_df <- author_output_dict[[key]]
    
    # Get common columns
    common_cols <- intersect(colnames(our_df), colnames(author_df))
    
    # Remove columns not in author_output_dict
    our_output_dict[[key]] <- our_df[, common_cols]
    
    # Save the updated dataframe as a new CSV file
    new_filename <- paste0(new_output_folder, "/", "Cheating-SampleEssays-", key, "-filtered.csv")
    write.csv(our_output_dict[[key]], new_filename, row.names = FALSE)
  }
}
