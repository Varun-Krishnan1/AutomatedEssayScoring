## ========================================== ## 
## For Sample Essays: Ensure columns match between our sample essay features 
## and the author's features 
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
base_folder = "~/Desktop/AES/TestingWithSampleEssays"
setwd(base_folder)

our_output_folder = "SampleEssaysFeatures/"
author_output_folder = "../Tool Validation/Author Essay Indices Output/"

# Get a list of all CSV files in the folder
our_file_list <- list.files(path = our_output_folder, pattern = "*.csv", full.names = TRUE)
author_file_list <- list.files(path = author_output_folder, pattern = "*.csv", full.names = TRUE)

# Store output data in dictionary in format (gamet: gamet_data, seance: seance_data, etc...)
our_output_dict <- list()
author_output_dict <- list()

# Read each CSV file and store it in the dictionary
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
  print(file_path)
  # Fix windows filepaths so below basename() function works 
  if (startsWith(file_path, "C:")) {
    # Replacing backslashes with forward slashes
    data$filename <- gsub("\\\\", "/", data$filename)
  }
  
  # Replace full file paths with basename in the "filename" column so it matches authors column  
  data$filename <- basename(data$filename)
  our_output_dict[[key]] <- data
  
}

for (file in author_file_list) {
  filename <- basename(file)  # Extract the filename from the full path
  key <- gsub(".csv$", "", sub(".*-", "", filename))  # Extract the key from the filename
  data <- read.csv(file)
  
  # Check if the column name is "Filename" or "filename" and convert it to "filename"
  if ("Filename" %in% colnames(data)) {
    colnames(data)[colnames(data) == "Filename"] <- "filename"
  } else if ("filename" %in% colnames(data)) {
    colnames(data)[colnames(data) == "filename"] <- "filename"
  }
  
  author_output_dict[[key]] <- data
}

# Ensure keys match 
print(names(our_output_dict))
print(names(author_output_dict))

#### Compare the data frames columns between two dictionaries ####
for (key in names(our_output_dict)) {
  print(paste("---", toupper(key), "---"))
  if (is.null(author_output_dict[[key]])) {
    print(paste("Key", key, "is present in our_output_dict but not in author_output_dict"))
    next
  }
  
  df1 <- our_output_dict[[key]]
  df2 <- author_output_dict[[key]]
  
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