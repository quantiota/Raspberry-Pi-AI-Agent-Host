

# Productivity Tools

This folder contains **optional pre-installed utilities and resources** to extend Claude Code’s capabilities inside the AI Agent Host.


These tools allow the AI to perform tasks beyond coding, enabling **end-to-end workflows** without leaving the environment.

## Architecture Note

These are **infrastructure utilities** pre-installed for any AI to use. They maintain the AI Agent Host's model-agnostic design - Claude Code, local LLMs, or future AI can leverage these same tools without modification.

## Structure

* **`documents/`** – Tools and examples for working with text documents (Markdown, PDF, DOCX, RTF, etc.).
* **`images-videos/`** – Utilities for image conversion, resizing, format changes, basic editing and for videos conversion, transcoding, format conversion, and compression.

## Purpose

By organizing these tools here, Claude can:

* Generate reports (e.g., Markdown → PDF via Pandoc).
* Process and transform media files.
* Automate repetitive content preparation tasks.
* Keep all assets in a unified, self-contained workspace.

**Note:** All utilities are available to Claude directly in this environment — no external cloud services required.


