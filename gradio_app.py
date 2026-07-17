# gradio_app.py

import gradio as gr
import uuid
from pathlib import Path
import os

from app.models.schemas import ManifestRow
from app.pipeline import run_pipeline

DESKTOP_DIR = Path.home() / "Desktop"
UPLOAD_DIR = DESKTOP_DIR / "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def process_files(files, progress=gr.Progress()):

    table_data = []

    if not files:
        return []

    for file in files:
        clip_id = str(uuid.uuid4().hex[:8])
        destination_path = os.path.join(
            UPLOAD_DIR, f"{clip_id}_{os.path.basename(file.name)}"
        )
        table_data.append(
            [
                clip_id,
                os.path.basename(file.name),
                "Success",
                "No",
                "No Flags",
            ]
        )

    return table_data


with gr.Blocks(title="Resonate TTS QC") as app:
    gr.Markdown("Resonate TTS QC Pipeline")

    with gr.Tab("TTS Upload & Run"):
        file_input = gr.File(file_count="multiple", label="Upload TTS audio files")
        run_btn = gr.Button("Run QC", variant="primary")
        results_tbl = gr.DataFrame(
            headers=["Clip ID", "File", "Status", "Excluded", "Flags"],
            label="TTS QC Results",
        )
        run_btn.click(fn=process_files, inputs=file_input, outputs=results_tbl)


if __name__ == "__main__":
    app.launch()
