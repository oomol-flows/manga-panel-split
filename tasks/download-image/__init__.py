#region generated meta
import typing
class Inputs(typing.TypedDict):
    image_url: str
    output_dir: str | None
class Outputs(typing.TypedDict):
    image_path: typing.NotRequired[str]
    filename: typing.NotRequired[str]
#endregion

from oocana import Context
import requests
import os
import uuid
from urllib.parse import urlparse, unquote

async def main(params: Inputs, context: Context) -> Outputs:
    url = params.get("image_url")
    if not url:
        raise ValueError("image_url is required")
    
    # Validate URL
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {url}")
    
    # Determine output directory
    output_dir = params.get("output_dir") or context.session_dir
    os.makedirs(output_dir, exist_ok=True)
    
    # Download image
    try:
        response = requests.get(url, timeout=30, stream=True)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"Failed to download image from {url}: {e}")
    
    # Determine file extension from URL or Content-Type
    content_type = response.headers.get("Content-Type", "")
    ext = None
    
    # Try to get extension from URL
    path = unquote(parsed.path)
    url_ext = os.path.splitext(path)[1].lower()
    if url_ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
        ext = url_ext
    else:
        # Infer from Content-Type
        content_type_map = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/webp": ".webp",
            "image/gif": ".gif",
        }
        ext = content_type_map.get(content_type.split(";")[0].strip(), ".jpg")
    
    # Generate unique filename
    filename = f"{uuid.uuid4().hex}{ext}"
    image_path = os.path.join(output_dir, filename)
    
    # Save image
    with open(image_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    return {
        "image_path": image_path,
        "filename": filename
    }