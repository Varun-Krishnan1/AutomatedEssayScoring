## ========================================== ## 
## For Sample Essays: Truncate other CSV files to match that of TAALED's rows 
## since those will be the # of essays we can use 
## TO DO 
## 
## 
## 
## Changelog:
## 05/23/23 - Created file 
## ========================================== ## 

library(dplyr)
library(tools)
library(fs)


# Ensure this is top-level folder for Sample Essays (.../Sample Essays)
base_folder = "~/Desktop/AES/TestingWithSampleEssays"
setwd(base_folder)

# Path to the folder containing the CSV files
folder_path <- "SampleEssaysFeatures/"
output_folder <- "SampleEssaysFeaturesTrunc/"

# Path to the minimum row file (TAALED file)
minimum_row_file <- "SampleEssaysFeatures//SampleEssays-taaled.csv"

# Get the list of CSV files from the folder
csv_files <- list.files(folder_path, pattern = "\\.csv$", full.names = TRUE)

# Remove the minimum row file from the csv_files list
csv_files <- setdiff(csv_files, minimum_row_file)

# Read the minimum row file
minimum_row_data <- read.csv(minimum_row_file)

# Get the values from the specific column in the minimum row file
values_to_keep <- minimum_row_data$filename

# Iterate over the CSV files
for (csv_file in csv_files) {
  print(csv_file)
  # Read the CSV file
  data <- read.csv(csv_file)
  
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
  
  # Replace full file paths with basename in the "filename" column 
  data$filename <- basename(data$filename)
  
  # Filter rows based on the values in the specific column
  filtered_data <- data %>% filter(filename %in% values_to_keep)
  
  print(paste("New num. rows: ", nrow(filtered_data)))
  
  # Extract the filename without extension
  file_name <- fs::path_file(csv_file)
  file_name <- gsub("\\.csv$", "", file_name)
  
  # Create the output file path with "trunc-" prefix
  output_file <- file.path(output_folder, paste0("trunc-", file_name, ".csv"))
  
  # Write the filtered data to the new CSV file
  write.csv(filtered_data, file = output_file, row.names = FALSE)
  
  cat("Filtered data saved to:", output_file, "\n")
}
