## Find Missing People

This repository hosts a machine learning project aimed at identifying and finding missing people using image recognition techniques.

## Overview

This project utilizes deep learning models for facial recognition and lifespan estimation to aid in finding missing individuals. It includes integration with Streamlit for a user-friendly web interface.

## Features

- **Face Recognition:** Utilizes MTCNN and FaceNet models to recognize faces and match them against a dataset.
- **Lifespan Estimation:** Predictive models for estimating the lifespan of individuals.
- **Web Interface:** Implemented using Streamlit to facilitate easy image upload and searching for missing persons.

## Technologies Used

- **Python Libraries:** OpenCV, TensorFlow/Keras, Scikit-learn
- **Data Handling:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Development:** Jupyter Notebooks for experimentation and development

## Installation

### Local Environment Setup

1. Clone the repository and navigate to the project directory:

    ```bash
    git clone https://github.com/BOD-27/Find_Missing_People.git
    cd Find_Missing_People
    ```

2. Install dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

3. Download and extract necessary datasets:

    ```bash
    # Add commands to download and extract datasets if applicable
    ```

### Google Colab Setup

To run this project in Google Colab, follow these steps:

1. Mount Google Drive to access necessary files:

    ```python
    import os
    from google.colab import drive
    drive.mount('/content/drive')
    ```

2. Clone the repository and navigate to the project directory:

    ```bash
    !git clone https://github.com/BOD-27/Find_Missing_People.git
    import os
    os.chdir('Find_Missing_People')
    ```

3. Extract the required datasets:

    ```bash
    !unzip /content/Find_Missing_People/FinalTest_dataset.zip
    !unzip /content/Find_Missing_People/Final_dataset.zip
    ```

4. Install necessary Python packages:

    ```bash
    !pip install streamlit
    !pip install mtcnn
    !pip install keras-facenet
    !pip install -r /content/drive/MyDrive/LifeSpan_Downloads/Lifespan_Age_Transformation_Synthesis/requirements.txt
    ```

### Running the Application

1. Create a Streamlit application script (`app.py`):

    ```python
    %%writefile app.py

    # Paste your Python code here
    ```

2. Run the Streamlit application:

    ```bash
    !streamlit run app.py & npx localtunnel --port 8501
    ```

3. Access the application through the provided localtunnel URL.

## Usage

1. Upload an image of the missing person using the web interface.
2. Select the gender of the person.
3. Click on "Search" to initiate the recognition process.
4. View results, including potential matches and similarity scores.

 and commands are accurately represented and tested in your development environment before updating the README on GitHub.
- Provide clear instructions for setting up and running the project to ensure users can easily replicate the environment and use the application.

This README structure provides a comprehensive overview of your project, including setup instructions for both local and Google Colab environments, usage guidelines, contribution details, licensing information, and contact details. Adjust the content and formatting as necessary to fit your specific project requirements and updates.
