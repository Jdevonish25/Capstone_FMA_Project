# Streamlit Deployment Documentation

Project title: Scalable Music Genre Classification and Audio Analytics Using the Free Music Archive Dataset

Student: Julian Devonish  
Programme: MSc Applied Data Science  
Course: COMP6830 - Data Science Capstone II  
Supervisor: Dr. Sean Miller  
Deployment URL: https://capstone-fma-genre-demo.streamlit.app/  
Repository: https://github.com/Jdevonish25/Capstone_FMA_Project  
Deployment platform: Streamlit Community Cloud

## Deployment Summary

The Streamlit deployment was added after the main modelling work had already been completed. Its purpose is to make the final music genre pipeline easier to demonstrate. Instead of asking a reviewer to open Notebook 49 or Notebook 50, the deployed app allows a user to upload an audio file and see ranked genre suggestions directly in the browser.

This deployment should be read as a demonstration layer, not as a new modelling experiment. The trained model, candidate labels, threshold, genre metadata, and final evaluation logic come from the existing capstone pipeline. The app wraps that work in a simpler interface so that the main idea can be shown quickly: the model is most useful when it returns Top-1, Top-3, and Top-5 genre suggestions rather than one final genre label.

After supervisor feedback, the opening section of the app was revised to explain two points before any results appear. First, it defines FMA as the Free Music Archive, an open music research dataset containing audio tracks, genre labels, and metadata. Second, it explains Top-1, Top-3, and Top-5 in plain language. Top-1 is the model's first choice. Top-3 means the accepted genre appears anywhere in the first three suggestions. Top-5 means it appears anywhere in the first five suggestions. This change was made because a demo viewer should not need prior knowledge of the project vocabulary before reading the results.

## Why Streamlit Was Selected

Streamlit was selected because the final project needed a lightweight way to present the model. A full web application with a separate backend, database, authentication layer, and hosted API would have added extra engineering work that was not central to the capstone question. The main academic question was not whether a production software platform could be built. It was whether audio-based and hybrid modelling could rank likely music genres in a useful way.

Streamlit also matched the review setting. A supervisor, marker, or non-technical viewer can open the deployed URL, upload a song, and read the model output without running notebooks. This made Streamlit a better fit than a command-line script. It also avoided the need to package the raw FMA dataset, which is too large for GitHub and unnecessary for a live demo.

Alternative approaches were considered. A Flask or FastAPI app would have given more control over the backend, but it would also have required more deployment setup. Gradio would have been suitable for a machine-learning demo, especially for file upload. Streamlit was chosen because it supports clear report-style layout, summary metrics, tables, warnings, and explanatory text in one page. That structure fits the capstone presentation better than a minimal prediction form.

## Deployment Architecture

The deployed app uses a small number of files from the final repository. The raw FMA data remains outside GitHub because it is large and not needed for the demonstration. The model file and small metadata files are enough to run upload-based inference.

| Component | Repository location | Role in deployment |
|---|---|---|
| Streamlit app | `streamlit_app.py` | Provides the upload interface, prediction workflow, tables, and user-facing explanation. |
| Audio model | `models/audio_multilabel_candidate150_expanded_final.keras` | Scores each 15-second audio window across the 150 direct candidate labels. |
| Label columns | `streamlit_assets/audio_multilabel_candidate150_expanded_label_columns.npy` | Keeps the model output aligned with the correct genre IDs. |
| Threshold file | `streamlit_assets/audio_multilabel_candidate150_expanded_best_threshold.txt` | Stores the final decision threshold used by the audio candidate model. |
| Genre metadata | `streamlit_assets/genres.csv` | Converts genre IDs into readable genre names. |
| Python dependencies | `requirements.txt` | Tells Streamlit which Python packages to install. |
| Linux packages | `packages.txt` | Installs `ffmpeg` and `libsndfile1` for audio loading support. |
| Python version hints | `.python-version` and `runtime.txt` | Record that Python 3.11 is the intended deployment version. |

This table matters because it separates the deployed demonstration from the full research environment. The full capstone contains notebooks, processed data, model comparisons, and output artefacts. The deployed app uses only the subset needed to run a single-song prediction. That decision keeps the app smaller and easier to maintain.

## Inference Workflow Used by the App

The app follows the same practical idea as Notebook 50. A full uploaded song is not forced into one model input. Instead, the app splits the audio into a maximum of eight evenly spaced 15-second windows. Each window is converted into a Mel-spectrogram using the same basic audio settings used in the final pipeline: 22,050 Hz sampling rate, 64 Mel bands, 2,048 FFT size, 1,024 hop length, and 15-second windows.

Each window is scored by the trained audio CNN. The app then averages the genre scores across windows and ranks the candidate labels. This design was selected because the audio model was trained on 15-second inputs. Using full-song windows respects that training design while still allowing more of the uploaded song to influence the final prediction.

The app reports Top-1, Top-3, and Top-5 genre suggestions. It also reports window-level information and a confidence label. A low-confidence warning appears when the highest mean score is below 0.50. This warning is important because the final project evidence does not support blind automatic tagging. The model is better understood as a ranked review tool.

The deployed interface now uses the heading "Top Genre Prediction" for the main output. This wording is more direct than only showing a table of scores. It tells a non-technical viewer where to look first, while still keeping the Top-3 and Top-5 lists visible for interpretation. The design choice reflects the final evaluation evidence: the first-ranked genre matters, but the strongest project result is the model's ability to place the accepted genre near the top of a ranked list.

## Final Model Evidence Used to Justify the Demo

The deployment design follows the evidence from Notebook 49 and Notebook 50.

| Evaluation source | Setting | Key result | Interpretation for deployment |
|---|---|---|---|
| Notebook 49 | FMA processed test split | Top-1 hit-any = 72.0%, Top-3 hit-any = 98.0%, Top-5 hit-any = 99.0% | The model was strong when the test songs came from the same project data setting. This supports ranked suggestions on familiar-style audio. |
| Notebook 49 | FMA processed test split | Micro F1 = 0.450, Samples F1 = 0.445, Macro F1 = 0.052 | The model handled common labels better than rare labels. The low Macro F1 shows why the app should avoid overclaiming rare subgenre certainty. |
| Notebook 50 | External open-licence songs | Top-1 = 21.7%, Top-3 = 66.7%, Top-5 = 83.3% | External songs were harder, but the correct genre family often appeared within the ranked list. This supports a Top-k demo rather than a single-answer demo. |
| Notebook 50 | External open-licence songs | Low-confidence rate = 48.3% | Many external songs needed caution. This supports the low-confidence warning shown in the deployed app. |

These results explain the final interface. The app does not hide uncertainty. It displays ranked outputs because the final evidence suggests that genre ranking is more credible than single-label assignment. The difference between FMA test performance and external-song performance also explains why the app includes explanatory text for non-technical users.

## Deployment Challenges and Fixes

The main deployment challenge was dependency compatibility. The first Streamlit build attempted to use Python 3.14.6. TensorFlow 2.20.0 did not have a compatible wheel for that Python version, so installation failed before the app could start. The error was not caused by the model code. It came from a mismatch between the cloud Python version and TensorFlow support.

The fix was to select Python 3.11 in the Streamlit deployment settings and record the intended version in `.python-version` and `runtime.txt`. The repository also includes `requirements.txt` for Python packages and `packages.txt` for system audio dependencies. Streamlit documentation notes that Community Cloud apps require dependency files such as `requirements.txt`, and that external Linux dependencies can be listed in `packages.txt`. It also notes that Python version selection is handled in the deployment settings.

A second challenge was repository access. The repository was initially private, so Streamlit did not immediately show it in the repository picker. Using the direct GitHub URL to `streamlit_app.py`, and ensuring Streamlit had access to the repository, allowed the deployment process to continue. This is a practical limitation of GitHub-linked deployment rather than a modelling issue.

## Trade-offs in the Deployed Version

The deployed app uses the audio CNN branch rather than the full hybrid branch. This was a deliberate trade-off. The hybrid branch depends on structured metadata and engineered feature tables. For an uploaded external song, those structured FMA features are not naturally available. Creating them during upload would require additional feature extraction and alignment logic, and it would increase the risk of mismatch between the live app and the trained structured model.

Using the audio branch keeps the demonstration honest. The user uploads an audio file, and the app predicts from audio. This matches the external-song testing logic in Notebook 50 more closely than a metadata-dependent hybrid interface would. The trade-off is that the deployed app does not show every part of the final research pipeline. It shows the most practical live inference path.

Another trade-off is resource use. TensorFlow is a large dependency, and Streamlit Community Cloud has limited compute resources. The app therefore uses a maximum of eight windows per uploaded song. This keeps inference time reasonable while still sampling the song beyond the first 15 seconds. A production system could process more windows, use batching more aggressively, or serve the model through a dedicated API.

## Limitations of the Deployment

The deployed app should not be treated as a commercial music-tagging service. It is an academic demonstration of the final capstone model. The model was trained on FMA data, so external music may differ in audio quality, mixing style, genre naming, and production context.

The app also does not evaluate whether a user-uploaded song has a known ground-truth genre. It can only return ranked suggestions. This is appropriate for demonstration, but it means the app is not a live accuracy test unless the uploaded songs have known accepted labels.

Rare labels remain a limitation. The final project separated the full 163-genre inventory into 150 direct candidate labels, 10 rare-tail fallback labels, and 3 inventory-only labels. The deployed app focuses on the 150 direct candidate labels because those are supported by the trained audio model output. This avoids giving users a false sense that every rare label is equally reliable.

## Lessons Learned from Deployment

The deployment stage confirmed that model performance is only one part of an applied data science project. A working model also needs a clear interface, manageable dependencies, and a deployment environment that matches the model's library requirements. The TensorFlow and Python version issue was a useful reminder that cloud deployment can fail before any model logic runs.

The deployment also clarified the value of a simple interface. The notebooks contain the full technical record, but they are not the easiest way to communicate the final system. The Streamlit app gives a reviewer a quick way to see the model's behaviour. It also makes the Top-k interpretation easier to explain because the ranked suggestions appear directly on screen.

## Future Deployment Improvements

Future work could add a download button for prediction results, a clearer comparison between Top-1, Top-3, and Top-5 outputs, and a small explanation of how each genre relates to the FMA hierarchy. A later version could also support batch uploads, but that would need careful resource controls on Streamlit Community Cloud.

Another improvement would be to move model inference behind a lightweight API. That would make the user interface faster to load and easier to maintain. It would also allow the model to run on a server with more predictable compute resources. For the current capstone, however, a single Streamlit app is enough to demonstrate the final prediction workflow.

## References

Defferrard, M., Benzi, K., Vandergheynst, P., & Bresson, X. (2017). FMA: A dataset for music analysis. *Proceedings of the 18th International Society for Music Information Retrieval Conference*.

McFee, B., Raffel, C., Liang, D., Ellis, D. P. W., McVicar, M., Battenberg, E., & Nieto, O. (2015). librosa: Audio and music signal analysis in Python. *Proceedings of the 14th Python in Science Conference*.

Streamlit. (n.d.). *App dependencies for your Community Cloud app*. https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies

Streamlit. (n.d.). *Deploy your app on Community Cloud*. https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

TensorFlow. (n.d.). *TensorFlow*. https://www.tensorflow.org/
