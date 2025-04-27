# PracaInz

Repository for the engineering thesis project (Polish language was required for naming conventions).

This repository contains a simple desktop application that recommends cars based on user preferences.  
The application is built in **Python** with a GUI created using **tkinter**, and uses CSV data as input.  
The system implements four recommendation algorithms based on various similarity measures between vehicles.

The program ranks cars according to user-defined criteria and priority weights for each feature.  
Results are saved into Excel files, showing rankings both with and without feature weighting.

## Features
- Graphical user interface (GUI) for easy data input
- Car recommendation based on 4 similarity algorithms:
  - Euclidean Distance
  - Minkowski Distance (p=4)
  - Pearson Correlation Coefficient
  - Kendall's Tau Coefficient
- Support for user-defined weights for each feature (importance: 0-3 scale)
- Normalization of features to [0,1] range
- Export of results to Excel (.xlsx) files
- Robust error handling (invalid inputs, missing files, etc.)

## Technologies Used
- Python 3.x
- tkinter
- numpy
- pandas
- os.path

## How to Run
1. Clone the repository.
2. Install the required libraries:
   ```bash
   pip install numpy pandas openpyxl
   ```
3. Run the main application:
   ```bash
   python car_recommendation_app.py
   ```
(Alternatively, use the provided executable file — no Python installation needed.)

## Data
- Dataset of above 300 sports cars
- 18 features per car, including dimensions, engine specifications, acceleration, and vehicle segment
- Data sources: https://www.auto-data.net/ and https://www.car.info/
- Features normalized to [0,1] for better comparability

## How it works
1. The user inputs desired values and priority weights for selected car features via a graphical form.
2. The application calculates similarity scores between user preferences and cars in the dataset using all four algorithms.
3. Results are sorted into rankings and saved to separate Excel files for each method.
4. The user can customize the number of cars displayed in the output.

## Example Use Cases
- Finding the best matching sports car according to specific preferences
- Comparing different recommendation algorithms based on real user inputs
- Learning how feature weighting impacts recommendation results
