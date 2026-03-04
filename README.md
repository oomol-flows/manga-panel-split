# Manga Panel Split

Automatically break down comic and manga pages into individual panels with AI-powered detection. Perfect for organizing digital comics, creating reading materials, or analyzing comic layouts.

## What It Does

Manga Panel Split uses artificial intelligence to recognize and extract individual panels from comic and manga pages. Instead of manually cropping each panel, the tool automatically:

- Identifies where each panel begins and ends on the page
- Extracts panels in the correct reading order
- Saves each panel as a separate image file
- Creates a visual guide showing how the page was divided

This makes it easy to work with individual panels for presentations, digital reading apps, translation projects, or comic analysis.

## Available Block

### Extract Comic Panels

This block analyzes a comic or manga page and separates it into individual panel images.

**What you provide:**
- A comic or manga page image (JPG, PNG, or WebP format)
- Optionally, a folder location where you want the panels saved

**What you receive:**
- Individual image files for each detected panel, numbered in reading order
- A count of how many panels were found
- A visual reference showing the detected panel boundaries on the original page

The tool automatically handles different comic layouts, from simple grid patterns to complex arrangements with overlapping panels.

## Common Uses

**For Digital Comic Libraries**
Extract panels from pages to create panel-by-panel reading experiences or build searchable panel databases.

**For Translation Projects**
Isolate individual panels to work on text separately, making it easier to handle dialogue and captions.

**For Educational Materials**
Pull specific panels from comics for use in presentations, lesson plans, or analysis documents.

**For Content Creation**
Quickly grab panels from favorite comics to share on social media or use in creative projects.

## How Reading Order Works

The AI has been trained on thousands of comic pages and understands typical reading patterns. For most comics and manga, it correctly identifies the sequence panels should be read in, whether that's left-to-right, right-to-left, or more complex zigzag patterns.

Each extracted panel is numbered (panel_001.png, panel_002.png, etc.) in the order they should be read, making it simple to maintain the story flow.

## Supported Formats

The tool works with common image formats:
- JPEG/JPG files
- PNG files
- WebP files

Both color and black-and-white comics are supported. The AI works with various art styles, from traditional manga to Western comics.

## About the Technology

This project uses MAGI (Manga Whisperer), an AI model specifically designed for understanding comic and manga layouts. The model has been trained to recognize panels, characters, and text in sequential art, making it particularly effective for comic analysis tasks.

When you process a page, the AI examines the image and uses pattern recognition to identify panel boundaries, similar to how a human reader would visually separate the page into distinct sections.
