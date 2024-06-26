# -*- coding: utf-8 -*-
"""Final_Facerecognentin.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VSq3fQ6NWghiRF2CD-sYgaQFgOc5LFF0
"""



# Import necessary libraries
def import_libraries():
    global os, cv, np, plt, MTCNN, FaceNet, cosine, re, Counter
    import os
    import cv2 as cv
    import numpy as np
    import matplotlib.pyplot as plt
    from mtcnn.mtcnn import MTCNN
    from keras_facenet import FaceNet
    from scipy.spatial.distance import cosine
    import re
    from collections import Counter

# Suppress TensorFlow warnings
def suppress_tf_warnings():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Mount Google Drive
def mount_drive():
    from google.colab import drive
    drive.mount('/content/drive')
# Create a directory to save embeddings
def create_embedding_save_directory():
    embedding_save_directory = '/content/drive/My Drive/Embedding'
    if not os.path.exists(embedding_save_directory):
        os.makedirs(embedding_save_directory)
    return embedding_save_directory

# Define the FaceLoading class for loading and processing images
class FaceLoading:
    def __init__(self, directory):
        self.directory = directory
        self.target_size = (160, 160)
        self.detector = MTCNN()

    def ExtractFace(self, filename):
        img = cv.imread(filename)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        x, y, w, h = self.detector.detect_faces(img)[0]['box']
        x, y = abs(x), abs(y)
        face = img[y:y + h, x:x + w]
        face_arr = cv.resize(face, self.target_size)
        return face_arr

    def LoadFace(self, file_path):
        faces = []
        try:
            single_face = self.ExtractFace(file_path)
            faces.append(single_face)
        except Exception as e:
            pass
        return faces

    def LoadClasses(self):
        x = []
        y = []
        for file_name in os.listdir(self.directory):
            if file_name.endswith('.jpg') or file_name.endswith('.png') or file_name.endswith('.jpeg'):
                file_path = os.path.join(self.directory, file_name)
                faces = self.LoadFace(file_path)
                labels = [file_name] * len(faces)
                print(f"Loaded successfully: {len(labels)}")
                x.extend(faces)
                y.extend(labels)
        return np.asarray(x), np.asarray(y)

    def encode_and_save_embeddings(self, embedding_save_directory):
        X, y = self.LoadClasses()
        embedder = FaceNet()
        embedded_x = [self.GetEmbedding(embedder, img) for img in X]

        # Save embeddings inside the created folder
        for i, (embedding, label) in enumerate(zip(embedded_x, y)):
            np.save(os.path.join(embedding_save_directory, f'{label}_embeddings.npy'), embedding)
        return np.array(embedded_x), np.array(y)

    def GetEmbedding(self, embedder, face_img):
        face_img = face_img.astype('float32')
        face_img = np.expand_dims(face_img, axis=0)
        yhat = embedder.embeddings(face_img)
        return yhat[0]

    def load_or_encode_and_save_embeddings(self, embedding_save_directory):
        embedding_files = [f for f in os.listdir(embedding_save_directory) if f.endswith('.npy')]

        if not embedding_files:
            print("Embeddings not found. Encoding and saving embeddings...")
            return self.encode_and_save_embeddings(embedding_save_directory)
        else:
            print("Embeddings found. Loading embeddings...")
            embedded_x, dataset_labels = [], []
            for file in embedding_files:
                data = np.load(os.path.join(embedding_save_directory, file))
                embedded_x.append(data)
                dataset_labels.append(file.replace('_embeddings.npy', ''))
            embedded_x = np.asarray(embedded_x)
            dataset_labels = np.asarray(dataset_labels)
            return embedded_x, dataset_labels

# Define functions for preprocessing, finding closest matches, and checking for match
def preprocess_label(label):
    label = re.sub(r'\d+', '', label)
    label = re.sub(r'\.\w{3,4}|\.', '', label)
    label = re.sub(r'\[.*?\]|\(.*?\)|\{.*?\}', '', label)
    label = re.sub(r'_[\w\d]+.*$', '', label)
    label = label.strip()
    return label

def find_closest_matches(embedded_input, embedded_dataset, dataset_labels, top_n=7):
    distances = []
    outlabels = []
    for input_embedding in embedded_input:
        distances_for_input = [cosine(input_embedding, dataset_embedding) for dataset_embedding in embedded_dataset]
        min_distance_index = np.argmin(distances_for_input)
        distances.append(distances_for_input[min_distance_index])
        outlabels.append(dataset_labels[min_distance_index])

    sorted_indices = np.argsort(distances)
    sorted_distances = np.array(distances)[sorted_indices]
    sorted_labels = np.array(outlabels)[sorted_indices]

    top_matches = [(sorted_labels[i], sorted_distances[i]) for i in range(top_n)]
    return top_matches

def check_for_match(top_matches):
    labels = [preprocess_label(label) for label, _ in top_matches]
    distances = [distance for _, distance in top_matches]
    frequent_labels = Counter(labels).most_common()

    for label, count in frequent_labels:
        if count >= 4:
            label_distances = [distance for orig_label, distance in top_matches if preprocess_label(orig_label) == label]
            avg_similarity = sum(label_distances) / count
            if avg_similarity < 0.5:
                return True, avg_similarity, label

        elif count == 3:
            label_distances = [distance for orig_label, distance in top_matches if preprocess_label(orig_label) == label]
            avg_similarity = sum(label_distances) / count
            if avg_similarity < 0.5:
                return True, avg_similarity, label

    return False, None, None