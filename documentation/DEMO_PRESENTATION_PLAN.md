# Model Presentation and Demo Plan

Project: Scalable Music Genre Classification and Audio Analytics Using the FMA Dataset  
Supervisor: Dr. Sean Miller

## Current Submission Position

The capstone folder already contains the main submission materials: final technical paper, management report, graded proposal, notebooks, exported notebook PDFs, trained model artefacts, final evaluation outputs, external batch audio manifest, and submission readiness files. The final model evidence is strongest in Notebook 49 and Notebook 50, so the demo should focus on those results and the full-song windowed inference workflow.

## Recommended Demo Option

The recommended presentation format is a small Streamlit application.

Streamlit is the best fit because it can present the project like a professional dashboard while still using the existing Python inference code, TensorFlow/Keras model files, joblib structured model files, librosa audio processing, and CSV/JSON outputs. It also supports file upload, tables, charts, status messages, and explanatory panels without needing a separate frontend/backend build.

## Option Comparison

| Option | Strengths | Limitations | Fit |
|---|---|---|---|
| Streamlit app | Fast to build, Python-native, strong for dashboards, easy file upload and charts | Styling is less custom than a full website | Best choice for capstone demo |
| Gradio app | Very quick ML demo interface, simple upload/prediction flow | Less suitable for project-level reporting and multi-section dashboard narrative | Good backup option |
| Lightweight website | Most polished visually, full control over layout | Requires a backend API for model inference and more integration work | Best only if time allows after Streamlit |

## Proposed Streamlit Demo Structure

1. Project Overview
   - Short summary of the problem, dataset, final system, and 163-genre strategy.
   - Display final Notebook 49 and Notebook 50 headline metrics.

2. Upload Song Demo
   - Upload one audio file.
   - Split the audio into fixed-length windows.
   - Run the Candidate-150 audio/hybrid inference flow.
   - Aggregate window scores into full-song predictions.
   - Show Top-1, Top-3, and Top-5 genre predictions.
   - Show low-confidence flag where appropriate.

3. External Batch Results
   - Load Notebook 50 output files.
   - Show external test performance by genre.
   - Show Top-1, Top-3, Top-5 hit rates and stable prediction hit rate.

4. FMA Test Results
   - Load Notebook 49 output files.
   - Show FMA test-split Top-1, Top-3, Top-5 and multi-label metrics.

5. Artefacts and Reproducibility
   - List final notebooks, exported notebook PDFs, trained model files, documentation, and output folders.

## Files the Demo Should Use

- `models/audio_multilabel_candidate150_expanded_final.keras`
- `models/final_structured_multilabel_candidate150_best_model.joblib`
- `models/final_structured_multilabel_candidate150_scaler.joblib`
- `data/processed/audio_multilabel_candidate150_expanded_label_columns.npy`
- `data/processed/hybrid_multilabel_candidate150_expanded_label_columns.npy`
- `outputs/notebook49_fma_test_batch_evaluation/fma_test_summary.json`
- `outputs/notebook50_external_song_batch_windowed/notebook50_external_batch_summary.json`
- `outputs/notebook50_external_song_batch_windowed/notebook50_external_manifest_evaluation_by_genre.csv`
- `outputs/notebook50_external_song_batch_windowed/notebook50_external_song_summary.csv`

## Remaining Demo Build Tasks

1. Extract the reusable inference functions from Notebook 50 into a Python module under `scripts/`.
2. Build `demo/streamlit_app.py` around those functions.
3. Add a small `demo/README_DEMO.md` with setup and run commands.
4. Test with at least two songs from the existing external batch folder.
5. Capture screenshots for possible inclusion in the final presentation.

## Suggested Run Command

After the demo app is created, the expected command should be:

```powershell
cd E:\SCHOOL\Masters\Capstone_FMA_Project
python -m streamlit run demo\streamlit_app.py
```

## Notes for Presentation

The demo should not overclaim exact Top-1 genre classification. The strongest narrative is that music genre is multi-label and ambiguous, so the project reports Top-1, Top-3, and Top-5 predictions. This aligns with the observed results: the system is much stronger when evaluated as a ranked recommendation-style genre classifier than as a single exact-label classifier.
