# Project Data Dictionary and Metric Guide

Project title: Scalable Music Genre Classification and Audio Analytics Using the Free Music Archive Dataset

Student: Julian Devonish  
Programme: MSc Applied Data Science  
Course: COMP6830 - Data Science Capstone II  
Supervisor: Dr. Sean Miller

## Purpose of This Dictionary

This document explains the main fields, metrics, labels, scores, and categories used in the project code, notebooks, output files, and Streamlit demo. It is written for someone reviewing the project who may not already know the modelling terms.

The most important idea is that the system is a ranked genre prediction model. It does not only ask, "Was the first genre correct?" It also asks whether the expected genre appears near the top of the ranked list. This is why the project reports Top 1, Top 3, Top 5, window votes, confidence labels, and low-confidence flags.

## Core Project Terms

| Term | Meaning | Why it matters |
|---|---|---|
| FMA | Free Music Archive. It is an open music research dataset containing audio tracks, metadata, and genre labels. | It is the main dataset used to train and test the model. |
| FMA Large | The larger FMA audio collection used in this capstone. | It provides enough audio files to train deep learning models. |
| Track | One audio item from the FMA dataset. | FMA testing uses `track_id` values to identify songs. |
| Song | One external audio file used in Notebook 50 or uploaded to the demo app. | External testing uses song names and file names instead of FMA track IDs. |
| Genre | A music category such as Rock, Electronic, Folk, Hip-Hop, Pop, or Experimental. | Genre is the target being predicted. |
| Label | The machine-readable version of a genre, usually written as `genre_12` or `genre_38`. | The model predicts labels first, then the code maps them back to genre names. |
| Multi-label classification | A classification task where one song may have more than one correct genre. | Music often has overlapping genre signals, so this is more suitable than single-label classification. |
| Candidate label | A genre label that had enough training support to be predicted directly by the model. | The final direct model predicts 150 candidate labels. |
| Rare-tail label | A genre with too few examples for reliable direct modelling. | Rare-tail labels were treated with caution because sparse data can produce unstable predictions. |
| Inventory-only label | A genre retained in the full taxonomy but not directly modelled. | This keeps the full project taxonomy complete while avoiding unsupported predictions. |
| 163-genre inventory | The final project-wide genre inventory. | It includes 150 direct candidate labels, 10 rare-tail fallback labels, and 3 inventory-only labels. |
| 150 direct candidate labels | The labels predicted directly by the final audio model and Streamlit app. | These are the labels with enough support for direct prediction. |

## Genre Category Structure

The project used the FMA genre structure rather than treating every genre name as unrelated. The FMA taxonomy contains broad parent genres and more specific child genres.

| Category level | Meaning | Example |
|---|---|---|
| Root genre | A broad top-level genre family. | Rock, Electronic, International |
| Parent genre | A mid-level genre inside a broader family. | Punk under Rock |
| Subgenre | A more specific genre. | Hardcore, Indie-Rock |
| Rare-tail subgenre | A specific genre with limited examples. | Some niche or less frequent labels |

This matters because a model may miss the exact subgenre but still place a related genre family near the top. For example, a Rock song may be predicted as Experimental, Punk, or Indie-Rock depending on the sound and the FMA labels available during training.

## Streamlit Demo Terms

The Streamlit app is located at:

`streamlit_app.py`

The live demo is:

`https://capstone-fma-genre-demo.streamlit.app/`

### Main Demo Inputs

| Field or setting | Value or format | Explanation |
|---|---|---|
| Uploaded audio file | `.mp3`, `.wav`, `.flac`, `.ogg`, `.m4a`, or `.aac` | The user uploads one audio file for prediction. |
| `WINDOW_SECONDS` | `15` | Each analysed audio segment is 15 seconds long. |
| `MAX_WINDOWS` | `8` | The app analyses up to eight windows from a song. |
| `SR` | `22050` | Audio is loaded at a 22,050 Hz sample rate. |
| `N_MELS` | `64` | Each Mel-spectrogram uses 64 Mel frequency bands. |
| `N_FFT` | `2048` | FFT window size used when creating the spectrogram. |
| `HOP_LENGTH` | `1024` | Step size between audio frames in the spectrogram. |
| `LOW_CONFIDENCE_THRESHOLD` | `0.50` | If the top mean score is below 0.50, the song is flagged as low confidence. |

### Why 15-Second Windows Are Used

The final audio model was trained on 15-second clips. A full song is longer than 15 seconds, so the app samples several 15-second windows across the song. Each window is scored by the model, and the scores are combined.

This design keeps live prediction close to the model's training setup. It also lets more of the song influence the final result. A song may have a quiet intro, a different chorus, or an instrumental section. Windowing reduces the risk of judging the whole song from one short segment.

## Streamlit Prediction Output Fields

These fields appear in the Streamlit app result table.

| Field | Type | Meaning | How to interpret it |
|---|---|---|---|
| `rank` | Integer | The position of the genre after sorting predictions. | Rank 1 is the highest predicted genre. |
| `genre` | Text | Human-readable genre name. | This is the label shown to the user. |
| `label_id` | Integer | Numeric FMA genre ID. | Used internally to connect labels to genre names. |
| `mean_score` | Decimal from 0 to 1 | Average model score for that genre across all analysed windows. | Higher means the genre was more consistently supported across the song. |
| `max_score` | Decimal from 0 to 1 | Highest score that genre received in any one window. | Useful when a genre is strong in one part of the song but not across the full song. |
| `window_votes` | Integer | Number of windows where the genre score met or exceeded the model threshold. | A higher count means the genre repeatedly passed the prediction threshold. |
| `top3_window_votes` | Integer | Number of windows where the genre appeared in that window's Top 3 predictions. | A high value means the genre was repeatedly near the top, even if it was not always first. |
| `confidence` | Text | Confidence label based on `mean_score`. | Summarises how strong the top averaged score is. |

### Mean Score

`mean_score` is the average score for one genre across all analysed windows.

Example:

If a song has four windows and Rock receives these scores:

`0.60, 0.50, 0.40, 0.70`

Then:

`mean_score = (0.60 + 0.50 + 0.40 + 0.70) / 4 = 0.55`

A high `mean_score` means the model found that genre signal across several parts of the song. A low `mean_score` means the model did not find consistent evidence for that genre.

### Max Score

`max_score` is the strongest score a genre received in any single window.

Using the same example:

`0.60, 0.50, 0.40, 0.70`

Then:

`max_score = 0.70`

This helps identify genres that appear strongly in one section of a song. For example, a track may have an Electronic intro but a Rock chorus. The `max_score` may detect the short strong signal, while `mean_score` shows whether it was consistent across the full track.

### Window Votes

`window_votes` counts how many windows crossed the prediction threshold.

The deployed model threshold is:

`stage1_threshold = 0.20`

If a genre receives these scores across eight windows:

`0.25, 0.31, 0.18, 0.40, 0.22, 0.10, 0.27, 0.35`

Six windows are at least `0.20`, so:

`window_votes = 6`

This measure is useful because a genre can be moderately strong across many windows without always having the highest score.

### Top 3 Window Votes

`top3_window_votes` counts how many windows included a genre within that window's three highest predictions.

Example:

| Window | Top 3 predicted genres |
|---|---|
| 1 | Rock, Punk, Indie-Rock |
| 2 | Rock, Electronic, Punk |
| 3 | Experimental, Rock, Folk |
| 4 | Rock, Pop, Punk |

Rock appears in the Top 3 for all four windows, so:

`top3_window_votes = 4`

Punk appears in three windows, so:

`top3_window_votes = 3`

This is different from `window_votes`. `window_votes` uses the score threshold. `top3_window_votes` uses ranking position within each window.

### Confidence Labels

The Streamlit app assigns confidence from `mean_score`.

| Confidence label | Score range | Meaning |
|---|---:|---|
| High | `mean_score >= 0.70` | The model strongly favoured this genre across the analysed windows. |
| Moderate | `0.50 <= mean_score < 0.70` | The model found a useful genre signal, but the result should still be read as a ranked suggestion. |
| Low to moderate | `0.30 <= mean_score < 0.50` | The model found some signal, but the prediction is uncertain. |
| Low | `mean_score < 0.30` | The model did not strongly support the genre. Treat the prediction with caution. |

Confidence is not the same as accuracy. It does not prove that the genre is correct. It only describes how strongly the model preferred that genre based on its score.

### Low-Confidence Flag

The app also creates a `low_confidence` flag.

| Field | Rule | Meaning |
|---|---|---|
| `low_confidence` | `True` when the top `mean_score` is below `0.50` | The model's best genre is not strong enough to treat as a final label without review. |

This flag is mainly a warning for users. The model may still provide useful Top 3 or Top 5 suggestions, but the first prediction should not be overclaimed.

## Top-K Metrics

Top-k metrics check whether the expected genre appears within the first `k` predictions.

| Metric | Meaning | Example |
|---|---|---|
| Top 1 | The expected genre is the first-ranked prediction. | Expected genre is Rock, and Rank 1 is Rock. |
| Top 3 | The expected genre appears anywhere in the first three predictions. | Expected genre is Rock, and Rock is Rank 2. |
| Top 5 | The expected genre appears anywhere in the first five predictions. | Expected genre is Rock, and Rock is Rank 5. |

Top-k metrics were used because music genre labels are often subjective. A song can reasonably sit between multiple genres. A model that places the expected genre in the Top 3 can still be useful, even when the first prediction is not exact.

### Hit-Any Metrics

For multi-label data, a song may have more than one true genre. A hit-any metric checks whether any accepted true label appears in the model's Top-k list.

Example:

True labels:

`Rock | Punk`

Model Top 3:

`Experimental | Punk | Electronic`

The Top 1 is not a hit, but Top 3 is a hit because Punk appears in the first three predictions.

## Classification Metrics

These metrics appear in Notebook 49 outputs.

| Metric | Meaning | Interpretation |
|---|---|---|
| Precision | Of the labels predicted by the model, how many were correct. | Higher precision means fewer incorrect positive predictions. |
| Recall | Of the true labels, how many the model found. | Higher recall means fewer missed true labels. |
| F1 | Harmonic mean of precision and recall. | Balances precision and recall into one score. |
| Support | Number of true label examples used in the metric. | Low support can make a label's score unstable. |
| Micro average | Calculates metrics globally across all labels. | Gives more weight to common labels. |
| Macro average | Calculates each label separately, then averages labels equally. | Shows whether the model performs well across rare labels too. |
| Samples average | Calculates metrics per song, then averages songs. | Useful for multi-label song-level evaluation. |
| Hamming loss | Fraction of incorrect label decisions across all labels. | Lower is better. |
| Jaccard samples | Overlap between predicted labels and true labels per song. | Higher means more overlap between predicted and true label sets. |

### Why Micro F1 and Macro F1 Differ

The project's final results show stronger Micro F1 than Macro F1. This is expected in an imbalanced genre dataset. Common genres have many examples and influence Micro F1 more. Rare genres have fewer examples and are weighted equally in Macro F1, so weak rare-label performance lowers Macro F1.

This difference is important. It shows the model learned stronger patterns for common labels but struggled with sparse labels. That is why the final system separates direct candidate labels from rare-tail labels.

## Project Thresholds and Settings

| Setting | Value | Used in | Meaning |
|---|---:|---|---|
| `stage1_threshold` | `0.20` | Notebook 49, Notebook 50, model outputs | A label score at or above 0.20 can be treated as a positive predicted label. |
| `low_confidence_threshold` | `0.50` | Notebook 49, Notebook 50, Streamlit app | A top score below 0.50 is treated as low confidence. |
| `window_seconds` | `15` | Notebook 50, Streamlit app | Each audio window is 15 seconds long. |
| `max_windows` | `8` | Notebook 50, Streamlit app | Up to eight windows are sampled from a full song. |
| `window_selection_mode` | `evenly_spaced` | Notebook 50 | Windows are spread across the full song rather than taken only from the start. |
| `min_window_votes` | `2` | Notebook 50 | A stable prediction must appear in at least two windows. |
| `structured_weight` | `0.10` | Notebook 49 summary | Hybrid evaluation gave 10 percent weight to structured predictions. |
| `audio_weight` | `0.90` | Notebook 49 summary | Hybrid evaluation gave 90 percent weight to audio predictions. |

## Notebook 49 Output Dictionary

Notebook 49 evaluates the final model on the FMA test split.

Main folder:

`outputs/notebook49_fma_test_batch_evaluation/`

### `fma_test_prediction_summary.csv`

| Field | Meaning |
|---|---|
| `track_id` | FMA track identifier. |
| `audio_path` | Local path to the FMA audio file. |
| `true_labels` | Accepted FMA labels for the track, separated by `|`. |
| `predicted_labels` | Labels predicted as positive after applying the threshold. |
| `top1_label` | Highest-ranked predicted label. |
| `top1_score` | Score for the highest-ranked predicted label. |
| `topk_labels` | Top ranked labels, usually the Top 5, separated by `|`. |
| `topk_scores` | Scores matching `topk_labels`, separated by `|`. |
| `low_confidence` | Whether the top score was below the low-confidence threshold. |
| `num_windows` | Number of windows used for prediction. |
| `window_starts` | Start positions of analysed windows. |
| `status` | Processing result, usually `ok` when prediction succeeded. |
| `error` | Error message if processing failed. |

### `fma_test_topk_predictions.csv`

| Field | Meaning |
|---|---|
| `track_id` | FMA track identifier. |
| `rank` | Rank position of a predicted label. |
| `label` | Predicted label at that rank. |
| `score` | Model score for that ranked label. |
| `is_true_label` | Whether the predicted label is one of the accepted true labels. |
| `true_labels` | Accepted true labels for the track. |

This file is useful for checking where the correct genre appeared in the ranked list.

### `fma_test_metrics_summary.csv`

| Field | Meaning |
|---|---|
| `metric_group` | Averaging method, such as `micro`, `macro`, or `samples`. |
| `precision` | Share of predicted labels that were correct. |
| `recall` | Share of true labels found by the model. |
| `f1` | Balance between precision and recall. |
| `support` | Number of true label instances used in the metric. |

### `fma_test_per_label_metrics.csv`

| Field | Meaning |
|---|---|
| `label` | Genre label being evaluated. |
| `precision` | Precision for that specific label. |
| `recall` | Recall for that specific label. |
| `f1` | F1 score for that specific label. |
| `support` | Number of true examples for that label. |

This file is important because it shows which genres were easier or harder for the model.

### `fma_test_all_label_scores.csv`

| Field pattern | Meaning |
|---|---|
| `track_id` | FMA track identifier. |
| `score__genre_<id>` | Model score for a specific genre label. |

Each `score__genre_<id>` column stores the model's score for one candidate genre. These scores are the raw material used to build Top 1, Top 3, Top 5, threshold predictions, and evaluation metrics.

### `fma_test_low_confidence_cases.csv`

This file has the same core fields as `fma_test_prediction_summary.csv`, but only includes cases where the top prediction was flagged as low confidence.

### `fma_test_runtime_log.csv`

| Field | Meaning |
|---|---|
| `timestamp` | Time the record was processed. |
| `track_id` | FMA track identifier. |
| `status` | Processing status. |
| `seconds` | Runtime for the track. |
| `error` | Error message if one occurred. |

## Notebook 50 Output Dictionary

Notebook 50 evaluates external songs using full-song windowed inference.

Main folder:

`outputs/notebook50_external_song_batch_windowed/`

### `notebook50_external_song_summary.csv`

| Field | Meaning |
|---|---|
| `song_name` | Clean song identifier used by the project. |
| `file_name` | Audio file name. |
| `relative_path` | Path relative to the external audio folder. |
| `audio_path` | Full local path to the audio file. |
| `status` | Processing result, usually `ok`. |
| `error` | Error message if processing failed. |
| `original_duration_seconds` | Actual length of the audio file. |
| `inference_duration_seconds` | Length used during inference. |
| `audio_was_looped` | Whether a short file was looped to create enough audio for inference. |
| `windows_used` | Number of 15-second windows analysed. |
| `window_seconds` | Window length in seconds. |
| `main_label` | Highest-ranked label after combining window scores. |
| `main_genre_id` | Numeric genre ID for the main label. |
| `main_genre_name` | Human-readable name of the main predicted genre. |
| `main_score` | Mean score for the main predicted genre. |
| `main_confidence_level` | Confidence label for `main_score`. |
| `main_threshold_vote_count` | Number of windows where the main genre passed the threshold. |
| `main_top1_window_vote_count` | Number of windows where the main genre was the top prediction. |
| `main_top3_window_vote_count` | Number of windows where the main genre appeared in the Top 3. |
| `low_confidence` | Whether `main_score` was below 0.50. |
| `top1_labels` | Top 1 label. |
| `top1_genres` | Top 1 genre name. |
| `top1_scores` | Score for the Top 1 genre. |
| `top3_labels` | Top 3 labels separated by `|`. |
| `top3_genres` | Top 3 genre names separated by `|`. |
| `top3_scores` | Top 3 scores separated by `|`. |
| `top5_labels` | Top 5 labels separated by `|`. |
| `top5_genres` | Top 5 genre names separated by `|`. |
| `top5_scores` | Top 5 scores separated by `|`. |
| `stable_predicted_labels` | Labels that met the stability rule across windows. |
| `stable_predicted_genres` | Genre names for stable predictions. |
| `seconds` | Runtime for processing that song. |

### `notebook50_external_window_predictions.csv`

| Field | Meaning |
|---|---|
| `song_name` | Song identifier. |
| `audio_path` | Full local path to the audio file. |
| `window_index` | Window number. |
| `start_sample` | Start position in audio samples. |
| `start_second` | Start time of the window in seconds. |
| `end_second` | End time of the window in seconds. |
| `top1_label` | Top label for that window. |
| `top1_genre_name` | Top genre name for that window. |
| `top1_score` | Score for the window's top genre. |
| `top3_labels` | Top 3 labels for that window. |
| `top3_genre_names` | Top 3 genre names for that window. |
| `top5_labels` | Top 5 labels for that window. |
| `top5_genre_names` | Top 5 genre names for that window. |

This file explains how the full-song result was built. It shows whether the prediction was stable across the song or driven by only one part.

### `notebook50_external_candidate_scores_topn.csv`

| Field | Meaning |
|---|---|
| `song_name` | Song identifier. |
| `audio_path` | Full local path to the audio file. |
| `genre_id` | Numeric FMA genre ID. |
| `label` | Machine-readable genre label. |
| `genre_name` | Human-readable genre name. |
| `mean_audio_score` | Average score for that genre across windows. |
| `max_audio_score` | Highest score for that genre in any window. |
| `confidence_level` | Confidence label based on the mean score. |
| `threshold_vote_count` | Number of windows where the genre score met the threshold. |
| `threshold_vote_rate` | Share of windows where the genre score met the threshold. |
| `top1_window_vote_count` | Number of windows where the genre ranked first. |
| `top3_window_vote_count` | Number of windows where the genre ranked in the Top 3. |
| `top5_window_vote_count` | Number of windows where the genre ranked in the Top 5. |
| `required_window_votes` | Minimum number of votes needed for stability. |
| `stable_prediction` | Whether the genre met the stability rule. |
| `relationship_to_main` | Whether the candidate is the main prediction or another supporting prediction. |

### `notebook50_external_manifest_evaluation.csv`

This file joins model predictions to the external audio manifest. It is used to calculate whether the predictions matched the expected or acceptable genres for each external song.

| Field | Meaning |
|---|---|
| `expected_primary_genre` | Main expected genre for the external song. |
| `acceptable_genres` | Genres accepted as reasonable matches for the song. |
| `acceptable_labels` | Machine-readable labels corresponding to acceptable genres. |
| `source` | Source used to obtain the external song. |
| `source_item_url` | Web page for the source item. |
| `source_file_url` | Direct file URL where available. |
| `license_url` | Licence information for the song. |
| `manifest_matched` | Whether the prediction row matched a manifest row. |
| `top1_hit` | Whether the Top 1 prediction matched an acceptable genre. |
| `top3_hit` | Whether any Top 3 prediction matched an acceptable genre. |
| `top5_hit` | Whether any Top 5 prediction matched an acceptable genre. |
| `stable_prediction_hit` | Whether a stable prediction matched an acceptable genre. |
| `expected_primary_name_top1_exact` | Whether the Top 1 genre exactly matched the expected primary genre name. |

### `notebook50_external_manifest_evaluation_by_genre.csv`

| Field | Meaning |
|---|---|
| `expected_primary_genre` | External genre group being evaluated. |
| `songs` | Number of songs in that genre group. |
| `top1_hit_rate` | Share of songs where Top 1 matched an acceptable genre. |
| `top3_hit_rate` | Share of songs where Top 3 included an acceptable genre. |
| `top5_hit_rate` | Share of songs where Top 5 included an acceptable genre. |
| `stable_prediction_hit_rate` | Share of songs where a stable prediction matched an acceptable genre. |
| `exact_expected_name_top1_rate` | Share of songs where Top 1 exactly matched the primary expected genre name. |
| `avg_main_score` | Average main score for songs in the group. |
| `low_confidence_rate` | Share of songs in the group flagged as low confidence. |

## File and Path Fields

| Field | Meaning |
|---|---|
| `audio_path` | Full local path to the audio file. |
| `relative_path` | Path relative to the project data folder. |
| `file_name` | Name of the audio file. |
| `song_name` | Project-friendly name derived from the file. |
| `track_id` | FMA dataset track identifier. |

These fields support traceability. They allow a reviewer to connect a prediction back to the exact audio file or FMA track.

## Status and Error Fields

| Field | Values | Meaning |
|---|---|---|
| `status` | Usually `ok` or an error status | Whether the record processed successfully. |
| `error` | Empty text or an error message | Explains why a record failed. |
| `seconds` | Decimal runtime | Time taken to process the song or track. |

Notebook 49 and Notebook 50 both produced zero error records in the final run, based on the final summary files.

## How to Read a Prediction Row

A typical prediction row should be read in this order:

1. Check `status`. If it is not `ok`, read `error`.
2. Read `main_genre_name` or `top1_label`.
3. Check `main_score` or `top1_score`.
4. Check `main_confidence_level` or `confidence`.
5. Review Top 3 and Top 5 genres.
6. Check `window_votes` or `top3_window_votes` to see whether the prediction was stable across the song.
7. If evaluating against known genres, check Top 1, Top 3, Top 5, and stable prediction hit fields.

This order avoids over-reading the first genre. The ranked list and window stability provide more context than a single label.

## Common Interpretation Rules

| Situation | Interpretation |
|---|---|
| High Top 3 or Top 5 hit rate but lower Top 1 hit rate | The model is useful as a ranked suggestion tool, but less reliable as a single-answer classifier. |
| High Micro F1 but low Macro F1 | The model handles common labels better than rare labels. |
| High `max_score` but low `mean_score` | The genre appeared strongly in one part of the song but was not consistent across the full song. |
| High `top3_window_votes` | The genre repeatedly appeared near the top across several windows. |
| Low confidence flag is `True` | The model's best answer should be reviewed carefully. |
| Many stable predictions | Several genres were consistently supported across windows. This can happen with multi-genre songs. |

## Final Results Referenced by the Dictionary

| Evaluation | Result |
|---|---:|
| Notebook 49 FMA Top 1 hit rate | 72.0% |
| Notebook 49 FMA Top 3 hit rate | 98.0% |
| Notebook 49 FMA Top 5 hit rate | 99.0% |
| Notebook 49 Micro F1 | 0.450 |
| Notebook 49 Samples F1 | 0.445 |
| Notebook 49 Macro F1 | 0.052 |
| Notebook 50 external Top 1 hit rate | 21.7% |
| Notebook 50 external Top 3 hit rate | 66.7% |
| Notebook 50 external Top 5 hit rate | 83.3% |
| Notebook 50 external low-confidence rate | 48.3% |

These results should be read together. The FMA test split shows strong ranked performance inside the project data setting. The external test shows that new songs are harder, but the Top 3 and Top 5 lists still often contain acceptable genre matches.

## Short Glossary

| Term | Plain meaning |
|---|---|
| Audio CNN | A neural network that learns patterns from audio spectrogram images. |
| Mel-spectrogram | A visual representation of sound over time and frequency. |
| Threshold | A score cut-off used to decide whether a label is active. |
| Probability-like score | Model output between 0 and 1. It behaves like confidence but should not be treated as a guaranteed probability. |
| Ranked prediction | A sorted list of likely genres from strongest to weakest. |
| Stable prediction | A genre that appears strongly enough across multiple windows. |
| Hit rate | Share of songs where the model placed an acceptable genre in the target rank range. |
| Low-confidence case | A prediction where the top score is below the defined confidence threshold. |

