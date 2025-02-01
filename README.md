# SERGIA: AI Chatbot and Summarization

## Description

SERGIA is an AI-powered chatbot designed to assist patients during their waiting time before consulting a doctor. It uses a fine-tuned **IndoBERT** model from Hugging Face, trained on a custom dataset, to provide summarization of patient concerns. This allows doctors to access pre-consultation summaries, making the consultation process more efficient and effective.


## Introduction

SERGIA leverages the power of **IndoBERT**, a state-of-the-art language model for Indonesian, to create an AI chatbot capable of summarizing patient concerns. The chatbot is designed to improve the efficiency of healthcare consultations by providing doctors with summarized patient data before the consultation begins.

## Features

- **AI Chatbot:** Engages with patients to collect their concerns and symptoms.
- **Summarization:** Generates concise summaries of patient inputs for doctors.
- **IndoBERT Model:** Utilizes a fine-tuned version of the IndoBERT model from Hugging Face.
- **Custom Dataset:** Trained on a dataset tailored for healthcare consultations.
- **Efficiency:** Reduces consultation time by providing pre-consultation summaries.

## Dataset

The dataset used for training the SERGIA chatbot consists of patient-doctor interactions, including patient concerns and corresponding summaries. The dataset is structured as follows:

- **Patient Inputs:** Textual data containing patient concerns and symptoms.
- **Summaries:** Concise summaries of the patient inputs, created for doctor reference.

Dataset download :
https://huggingface.co/datasets/Bilal-Mamji/Medical-summary

### Creating the Dataset

1. **Collecting Data:**
   - Gather patient-doctor interaction data from healthcare providers.
   - Anonymize the data to ensure patient privacy.

2. **Preprocessing:**
   - Clean and preprocess the text data (e.g., remove special characters, normalize text).
   - Split the data into training, validation, and test sets.

3. **Annotation:**
   - Annotate the data to create summaries for each patient input.

## Model Architecture

The SERGIA chatbot is built using the **IndoBERT** model, which is fine-tuned on the custom dataset. The architecture includes:

- **Input Layer:** Accepts patient input text.
- **IndoBERT Encoder:** Processes the input text to generate contextual embeddings.
- **Summarization Head:** A fine-tuned layer that generates concise summaries from the embeddings.

Model Architecture download :
https://huggingface.co/MbahLaba/Sergia_Summarization

## Results
The fine-tuned IndoBERT model achieves high accuracy in generating patient summaries. Detailed results, including ROUGE scores and error analysis, will be documented here after training and evaluation.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

