from pathlib import Path
import json
import math
import tempfile

import librosa
import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf


PROJECT_ROOT = Path(__file__).resolve().parent
MODELS_DIR = PROJECT_ROOT / "models"
ASSETS_DIR = PROJECT_ROOT / "streamlit_assets"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

MODEL_PATH = MODELS_DIR / "audio_multilabel_candidate150_expanded_final.keras"
LABEL_COLUMNS_PATH = ASSETS_DIR / "audio_multilabel_candidate150_expanded_label_columns.npy"
THRESHOLD_PATH = ASSETS_DIR / "audio_multilabel_candidate150_expanded_best_threshold.txt"
GENRES_PATH = ASSETS_DIR / "genres.csv"

WINDOW_SECONDS = 15
MAX_WINDOWS = 8
SR = 22050
N_MELS = 64
N_FFT = 2048
HOP_LENGTH = 1024
MAX_FRAMES = int(np.ceil((WINDOW_SECONDS * SR) / HOP_LENGTH)) + 1
LOW_CONFIDENCE_THRESHOLD = 0.50

FMA_EXPLANATION = (
    "FMA means the Free Music Archive, an open music research dataset used to "
    "train and test this project. It contains audio tracks, genre labels, and "
    "metadata that are commonly used for music information retrieval research."
)

TOP_K_EXPLANATION = (
    "Top 1 is the model's first choice. Top 3 means the correct or expected "
    "genre appears anywhere in the first three suggestions. Top 5 means it "
    "appears anywhere in the first five suggestions."
)


st.set_page_config(
    page_title="FMA Genre Prediction Demo",
    page_icon="audio",
    layout="wide",
)


@st.cache_resource(show_spinner=False)
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)


@st.cache_data(show_spinner=False)
def load_metadata():
    labels = np.load(LABEL_COLUMNS_PATH, allow_pickle=True)
    labels = [str(x) for x in labels.tolist()]

    with open(THRESHOLD_PATH, "r", encoding="utf-8") as f:
        threshold = float(f.read().strip())

    genres = pd.read_csv(GENRES_PATH)
    id_to_name = dict(zip(genres["genre_id"].astype(int), genres["title"].astype(str)))

    return labels, threshold, id_to_name


@st.cache_data(show_spinner=False)
def load_project_summaries():
    summaries = {}
    fma_summary_path = OUTPUTS_DIR / "notebook49_fma_test_batch_evaluation" / "fma_test_summary.json"
    external_summary_path = OUTPUTS_DIR / "notebook50_external_song_batch_windowed" / "notebook50_external_batch_summary.json"

    if fma_summary_path.exists():
        with open(fma_summary_path, "r", encoding="utf-8") as f:
            summaries["fma"] = json.load(f)

    if external_summary_path.exists():
        with open(external_summary_path, "r", encoding="utf-8") as f:
            summaries["external"] = json.load(f)

    return summaries


def genre_name_from_label(label_col, id_to_name):
    genre_id = int(str(label_col).replace("genre_", ""))
    return id_to_name.get(genre_id, f"Genre {genre_id}")


def confidence_label(score):
    if score >= 0.70:
        return "High"
    if score >= 0.50:
        return "Moderate"
    if score >= 0.30:
        return "Low to moderate"
    return "Low"


def load_uploaded_audio(uploaded_file):
    suffix = Path(uploaded_file.name).suffix.lower() or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = Path(tmp.name)

    try:
        y, sr = librosa.load(tmp_path, sr=SR, mono=True)
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except Exception:
            pass

    if y is None or len(y) == 0:
        raise ValueError("The uploaded audio file could not be read.")

    return y.astype(np.float32), sr


def window_starts(y, sr, window_seconds=WINDOW_SECONDS, max_windows=MAX_WINDOWS):
    total_len = len(y)
    window_len = int(window_seconds * sr)

    if total_len <= window_len:
        return [0]

    max_start = total_len - window_len
    n_windows = min(max_windows, max(2, math.ceil(total_len / window_len)))
    starts = np.linspace(0, max_start, num=n_windows)
    return sorted(list(dict.fromkeys([int(x) for x in starts])))[:max_windows]


def extract_window(y, start_sample, sr, window_seconds=WINDOW_SECONDS):
    window_len = int(window_seconds * sr)
    segment = y[start_sample:start_sample + window_len]

    if len(segment) < window_len:
        segment = np.pad(segment, (0, window_len - len(segment)), mode="constant")

    return segment.astype(np.float32)


def build_mel_input(segment, sr):
    mel = librosa.feature.melspectrogram(
        y=segment,
        sr=sr,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS,
    )
    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_db = np.clip((mel_db + 80.0) / 80.0, 0.0, 1.0)

    if mel_db.shape[1] < MAX_FRAMES:
        mel_db = np.pad(mel_db, ((0, 0), (0, MAX_FRAMES - mel_db.shape[1])), mode="constant")
    else:
        mel_db = mel_db[:, :MAX_FRAMES]

    return mel_db.astype(np.float32)[None, :, :, None]


def predict_song(uploaded_file, model, label_cols, id_to_name, threshold):
    y, sr = load_uploaded_audio(uploaded_file)
    duration_seconds = len(y) / sr
    starts = window_starts(y, sr)

    window_scores = []
    window_rows = []

    for i, start_sample in enumerate(starts):
        segment = extract_window(y, start_sample, sr)
        model_input = build_mel_input(segment, sr)
        probs = model.predict(model_input, verbose=0)[0]
        window_scores.append(probs)

        order = np.argsort(probs)[::-1][:5]
        window_rows.append({
            "window": i + 1,
            "start_second": round(start_sample / sr, 1),
            "top_genre": genre_name_from_label(label_cols[int(order[0])], id_to_name),
            "top_score": round(float(probs[int(order[0])]), 3),
        })

    score_matrix = np.vstack(window_scores)
    mean_scores = score_matrix.mean(axis=0)
    max_scores = score_matrix.max(axis=0)
    threshold_votes = (score_matrix >= threshold).sum(axis=0)
    top3_votes = np.zeros(len(label_cols), dtype=int)

    for row in np.argsort(-score_matrix, axis=1)[:, :3]:
        for idx in row:
            top3_votes[int(idx)] += 1

    rows = []
    for idx, label in enumerate(label_cols):
        rows.append({
            "rank": 0,
            "genre": genre_name_from_label(label, id_to_name),
            "label_id": int(str(label).replace("genre_", "")),
            "mean_score": float(mean_scores[idx]),
            "max_score": float(max_scores[idx]),
            "window_votes": int(threshold_votes[idx]),
            "top3_window_votes": int(top3_votes[idx]),
            "confidence": confidence_label(float(mean_scores[idx])),
        })

    results = pd.DataFrame(rows).sort_values(
        ["mean_score", "window_votes", "top3_window_votes"],
        ascending=[False, False, False],
    ).reset_index(drop=True)
    results["rank"] = results.index + 1

    summary = {
        "duration_seconds": duration_seconds,
        "windows_used": len(starts),
        "threshold": threshold,
        "low_confidence": bool(float(results.iloc[0]["mean_score"]) < LOW_CONFIDENCE_THRESHOLD),
    }

    return summary, results, pd.DataFrame(window_rows)


def metric_card(label, value):
    st.metric(label, value)


def show_project_results():
    summaries = load_project_summaries()

    st.subheader("Project Results From The Final Test")
    st.write(
        "These results show how often the model placed the accepted genre near "
        "the top of its ranked list. The project uses ranked prediction because "
        "music often fits more than one genre."
    )
    cols = st.columns(4)

    fma = summaries.get("fma", {})
    additional = fma.get("additional_metrics", {})
    with cols[0]:
        metric_card("Top 1 on FMA test songs", f"{additional.get('top1_hit_rate', 0) * 100:.1f}%")
    with cols[1]:
        metric_card("Top 3 on FMA test songs", f"{additional.get('top3_hit_rate', 0) * 100:.1f}%")
    with cols[2]:
        metric_card("Top 5 on FMA test songs", f"{additional.get('top5_hit_rate', 0) * 100:.1f}%")
    with cols[3]:
        metric_card("FMA songs tested", f"{additional.get('num_successful_tracks', 0)}")

    external = summaries.get("external", {}).get("manifest_overall_metrics", {})
    st.caption(
        "External open-licence test: "
        f"Top 1 = {external.get('top1_hit_rate', 0) * 100:.1f}%, "
        f"Top 3 = {external.get('top3_hit_rate', 0) * 100:.1f}%, "
        f"Top 5 = {external.get('top5_hit_rate', 0) * 100:.1f}%."
    )


def main():
    st.title("Music Genre Prediction Demo")
    st.write(
        "Upload a song and the model will suggest likely genres. The main result "
        "is the Top Genre Prediction, followed by Top 3 and Top 5 suggestions for "
        "review."
    )

    with st.container(border=True):
        st.markdown("### What this demo means")
        st.write(FMA_EXPLANATION)
        st.write(TOP_K_EXPLANATION)
        st.write(
            "In plain terms, the model is not only judged by whether its first "
            "guess is correct. It is also judged by whether the right genre is "
            "close to the top of the list."
        )

    with st.expander("Why the demo uses 15-second windows", expanded=False):
        st.write(
            "The model was trained on 15-second audio clips. For a full song, the "
            "app samples several 15-second windows, predicts each window, and then "
            "combines those scores. This lets more of the song influence the final "
            "ranked genre list."
    )

    show_project_results()

    st.divider()
    st.subheader("Try A Song")

    uploaded_file = st.file_uploader(
        "Upload an audio file",
        type=["mp3", "wav", "flac", "ogg", "m4a", "aac"],
    )

    with st.expander("How to read the result", expanded=False):
        st.write(
            "The model splits the song into 15-second windows, predicts genres for each "
            "window, and then averages the scores. A low confidence flag means the top "
            "score is not strong enough to treat as a final answer without review."
        )
        st.write(TOP_K_EXPLANATION)
        st.write(
            "Top 3 window votes count how often a genre appears inside the top three "
            "predictions across the analysed windows."
        )

    if not uploaded_file:
        st.info("Upload a song to see genre predictions.")
        return

    try:
        with st.spinner("Loading model and analysing audio..."):
            label_cols, threshold, id_to_name = load_metadata()
            model = load_model()
            summary, results, windows = predict_song(
                uploaded_file,
                model,
                label_cols,
                id_to_name,
                threshold,
            )
    except Exception as exc:
        st.error("The app could not analyse this audio file.")
        st.exception(exc)
        return

    top5 = results.head(5).copy()
    top3_names = ", ".join(top5.head(3)["genre"].tolist())
    top5_names = ", ".join(top5["genre"].tolist())
    top1 = top5.iloc[0]

    st.success("Prediction complete.")

    cols = st.columns(4)
    cols[0].metric("Top Genre", str(top1["genre"]))
    cols[1].metric("Top Score", f"{float(top1['mean_score']):.3f}")
    cols[2].metric("Windows Used", int(summary["windows_used"]))
    cols[3].metric("Confidence", str(top1["confidence"]))

    if summary["low_confidence"]:
        st.warning(
            "Low confidence flag: the model can still suggest likely genres, but this "
            "song should be reviewed before assigning a final label."
        )

    st.subheader("Top Genre Prediction")
    st.write(
        f"The strongest single prediction is **{top1['genre']}**. The broader "
        "ranked list should also be reviewed because songs can contain more than "
        "one genre signal."
    )
    st.write("**Top 3 genre suggestions:**", top3_names)
    st.write("**Top 5 genre suggestions:**", top5_names)

    display_cols = [
        "rank",
        "genre",
        "mean_score",
        "max_score",
        "window_votes",
        "top3_window_votes",
        "confidence",
    ]
    st.dataframe(
        top5[display_cols].style.format({
            "mean_score": "{:.3f}",
            "max_score": "{:.3f}",
        }),
        use_container_width=True,
        hide_index=True,
    )

    with st.expander("Window-level view"):
        st.dataframe(windows, use_container_width=True, hide_index=True)

    with st.expander("Show more candidate genres"):
        more = results.head(15)[display_cols]
        st.dataframe(
            more.style.format({
                "mean_score": "{:.3f}",
                "max_score": "{:.3f}",
            }),
            use_container_width=True,
            hide_index=True,
        )


if __name__ == "__main__":
    main()
