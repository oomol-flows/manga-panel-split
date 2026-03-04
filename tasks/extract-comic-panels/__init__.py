#region generated meta
import typing
class Inputs(typing.TypedDict):
    comic_image: str
    output_dir: str | None
class Outputs(typing.TypedDict):
    panel_images: typing.NotRequired[list[str]]
    panel_count: typing.NotRequired[float]
    visualization: typing.NotRequired[str]
#endregion

from oocana import Context
from transformers import AutoModel
import numpy as np
from PIL import Image
import torch
import os

async def main(params: Inputs, context: Context) -> Outputs:
    """Extract comic panels using MAGI AI model."""

    # Validate input
    comic_image_path = params["comic_image"]
    if not os.path.exists(comic_image_path):
        raise FileNotFoundError(f"Comic image not found: {comic_image_path}")

    # Set output directory
    output_dir = params.get("output_dir")
    if output_dir is None:
        output_dir = context.session_dir
    os.makedirs(output_dir, exist_ok=True)

    context.report_progress(10)

    # Load image
    def read_image_as_np_array(image_path: str) -> np.ndarray:
        with open(image_path, "rb") as file:
            image = Image.open(file).convert("L").convert("RGB")
            image = np.array(image)
        return image

    image = read_image_as_np_array(comic_image_path)

    context.report_progress(20)

    # Load MAGI model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AutoModel.from_pretrained("ragavsachdeva/magi", trust_remote_code=True)
    model = model.to(device)

    context.report_progress(40)

    # Detect panels and other elements
    with torch.no_grad():
        results = model.predict_detections_and_associations([image])
        result = results[0]

    context.report_progress(60)

    # Extract panel bounding boxes
    panels = result.get("panels", [])
    if not panels:
        raise ValueError("No panels detected in the comic image")

    # Sort panels by reading order (already provided by MAGI in correct order)
    panel_images = []
    base_name = os.path.splitext(os.path.basename(comic_image_path))[0]

    # Extract and save each panel
    pil_image = Image.fromarray(image)
    for i, panel in enumerate(panels):
        # Panel is a list [x1, y1, x2, y2]
        if isinstance(panel, dict):
            bbox = panel["bbox"]
        else:
            bbox = panel
        x1, y1, x2, y2 = map(int, bbox)

        # Crop panel from image
        panel_crop = pil_image.crop((x1, y1, x2, y2))

        # Save panel
        panel_filename = f"{base_name}_panel_{i+1:03d}.png"
        panel_path = os.path.join(output_dir, panel_filename)
        panel_crop.save(panel_path)
        panel_images.append(panel_path)

        # Report progress
        progress = 60 + int((i + 1) / len(panels) * 30)
        context.report_progress(progress)

    # Generate visualization
    visualization_path = os.path.join(output_dir, f"{base_name}_visualization.png")
    model.visualise_single_image_prediction(image, result, filename=visualization_path)

    context.report_progress(95)

    # Preview the visualization
    context.preview({"type": "image", "data": visualization_path})

    context.report_progress(100)

    return {
        "panel_images": panel_images,
        "panel_count": len(panel_images),
        "visualization": visualization_path
    }
