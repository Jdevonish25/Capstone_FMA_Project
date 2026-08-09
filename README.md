# Capstone FMA Project

## Project Overview

This project explores how music can be organised by genre using data science.

The work uses the Free Music Archive dataset, which contains music files and
information about each track. The goal was to build a system that listens to a
song and suggests likely genres, such as Rock, Electronic, Experimental, Folk,
Hip-Hop, or Pop.

The final system does not claim to guess every genre perfectly. Music genre is
often subjective, and one song can fit more than one category. For that reason,
the project focuses on ranked predictions, such as Top 1, Top 3, and Top 5
genre suggestions.

## Live Demo

The project has a Streamlit demo for non-technical review:

https://capstone-fma-genre-demo.streamlit.app/

The demo lets a user upload a song and view ranked genre suggestions. It now
explains FMA and the Top 1, Top 3, and Top 5 measures at the top of the page, so
a viewer can understand the results without reading the technical paper first.
It should be read as a demonstration of the final workflow, not as a replacement
for the technical paper or notebook evidence.

## What The Project Does

The project:

- studies the Free Music Archive music dataset;
- prepares music metadata and audio files for analysis;
- trains machine learning and deep learning models;
- compares structured data, audio-based models, and hybrid models;
- tests the final model on FMA test songs;
- tests the model again on external open-licence songs;
- deploys a small Streamlit app for browser-based demonstration;
- produces final reports, notebooks, model files, and evaluation results.

## Main Result

The model worked best as a genre suggestion tool.

On the final FMA test set, the correct genre was usually found in the top few
suggestions. External songs were harder, but the Top 3 and Top 5 results still
showed useful ranking behaviour.

In simple terms, the model is useful for narrowing down likely genres, but a
person should still review the final genre choice.

## MongoDB Note

MongoDB was used during the project as a metadata and label-management layer.
Notebook 04 created the first MongoDB pipeline, and Notebook 25 expanded this
into the local `fma_capstone` database with `genres_lookup` and
`tracks_multilabel` collections.

The final notebooks and Streamlit demo use exported CSV, JSON, NumPy, and model
files instead of live MongoDB queries. This kept the evaluation and demo stable
on local hardware where repeated audio inference and model work were limited by
CPU, memory, and disk I/O.

## Main Folders

- `documentation/` contains the final technical paper, management report, code
  documentation, proposal, deployment documentation, and readiness notes.
- `notebook/` contains the full notebook work from the start of the project to
  the final testing stage.
- `software artefacts/` contains PDF versions of the notebooks with code and
  outputs.
- `models/` contains the saved trained models.
- `outputs/` contains the final test results from Notebook 49 and Notebook 50.
- `scripts/` and `reports/` contain supporting project files.

## Best Documents To Read First

For a quick understanding, start with:

1. `documentation/FMA_Capstone_Management_Report_Julian_Devonish.pdf`
2. `documentation/FMA_Capstone_Final_Technical_Paper_Julian_Devonish.pdf`
3. `documentation/FMA_Capstone_Code_Documentation_Julian_Devonish.pdf`
4. `documentation/SUBMISSION_READINESS_REPORT.md`
5. `documentation/STREAMLIT_DEPLOYMENT_DOCUMENTATION.md`
6. `documentation/PROJECT_DATA_DICTIONARY.md`

The management report gives the easiest summary. The technical paper explains
the full project in more detail. The code documentation explains the notebook
sequence, final output folders, and Streamlit app code. The Streamlit deployment
document explains how the final model was presented as a live browser demo. The
data dictionary explains the code fields, metrics, confidence labels, and output
columns.

## Important Notebooks

The project has many notebooks because it was completed in stages.

The most important final notebooks are:

- Notebook 49: final FMA test-set evaluation.
- Notebook 50: external song batch testing.

Earlier notebooks show how the data, models, and genre structure were built.

## Data Note

The raw music dataset is very large, so it is not stored directly in this
GitHub repository. The repository contains the notebooks, reports, saved models,
and final output files needed to understand the work.

## Project Details

Project title: Scalable Music Genre Classification and Audio Analytics Using
the Free Music Archive Dataset

Student: Julian Devonish

Programme: MSc Applied Data Science

Course: COMP6830 - Data Science Capstone II

Supervisor: Dr. Sean Miller
