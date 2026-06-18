# FMA Capstone Submission README

Project title: Scalable Music Genre Classification and Audio Analytics Using the Free Music Archive Dataset

Student: Julian Devonish  
Programme: MSc Applied Data Science  
Course: COMP6830 - Data Science Capstone II  
Supervisor: Dr. Sean Miller

## Primary Submission Documents

- `requirements_capstone.txt`
- `documentation/DEMO_PRESENTATION_PLAN.md`
- `documentation/FMA_Capstone_Final_Technical_Paper_Julian_Devonish.docx`
- `documentation/FMA_Capstone_Final_Technical_Paper_Julian_Devonish.pdf`
- `documentation/FMA_Capstone_Management_Report_Julian_Devonish.docx`
- `documentation/FMA_Capstone_Management_Report_Julian_Devonish.pdf`
- `documentation/Capstone_Project_Proposal_Graded.pdf`
- `documentation/STREAMLIT_DEPLOYMENT_DOCUMENTATION.md`
- `documentation/SUBMISSION_READINESS_REPORT.md`
- `documentation/submission_key_file_check.csv`
- `documentation/submission_file_manifest_clean.csv`
- `software artefacts/notebook_pdfs/`
- `software artefacts/notebook_pdf_manifest.csv`

## Main Project Folders

- `data/` contains raw, processed, and external batch data used by the project.
- `models/` contains saved trained model artefacts.
- `notebook/` contains the full notebook implementation sequence.
- `outputs/` contains final Notebook 49 and Notebook 50 evaluation outputs.
- `documentation/` contains the final paper, proposal, readiness report, and submission manifests.
- `software artefacts/` contains PDF exports of the notebooks with code and outputs.
- `reports/` is reserved for report exports; final report outputs are stored in `documentation/`.
- `scripts/` is reserved for reusable scripts; the main implementation is notebook-based.
- `streamlit_app.py`, `streamlit_assets/`, `requirements.txt`, `packages.txt`, `runtime.txt`, and `.python-version` support the live Streamlit deployment.

## Recommended Review Order

1. Read the management report in `documentation/` for a concise decision-level summary.
2. Read the final technical paper in `documentation/` for the full technical explanation.
3. Review the graded proposal for approved scope alignment.
4. Review Notebooks 23-24 for full genre inventory and multi-label preparation.
5. Review Notebooks 34-38 for the Candidate-150 audio and hybrid benchmark.
6. Review Notebooks 39-47 for the full taxonomy and rare-tail inference strategy.
7. Review Notebook 49 for final FMA test-split evaluation.
8. Review Notebook 50 for external open-licence song batch evaluation.
9. Review the Streamlit deployment documentation and live app for the browser-based demonstration.

## Live Streamlit Demonstration

Live app:

`https://capstone-fma-genre-demo.streamlit.app/`

The deployed app allows a reviewer to upload an audio file and view ranked genre predictions. It uses the final audio CNN branch because uploaded external songs do not naturally include the structured FMA metadata needed by the hybrid branch. This is explained in `documentation/STREAMLIT_DEPLOYMENT_DOCUMENTATION.md`.

## Final Evaluation Outputs

- Notebook 49 output folder: `outputs/notebook49_fma_test_batch_evaluation/`
- Notebook 50 output folder: `outputs/notebook50_external_song_batch_windowed/`
- External manifest workbook: `data/external_audio_batch/external_audio_manifest.xlsx`

## Software Artefacts

Notebook PDF exports are stored in:

`software artefacts/notebook_pdfs/`

The folder contains 51 PDF notebook artefacts, including the patched Notebook 47 supporting notebook. Notebook 49 and Notebook 50 were executed into artefact copies before PDF export because their original `.ipynb` files did not contain embedded outputs.

## Packaging Note

The folder `notebook/.venv/` is a local Python environment. It is useful for local execution but is not required as a grading artefact if a compressed upload has a strict size limit. The notebooks, models, data, outputs, documentation, and manifest files are the important submission materials.



