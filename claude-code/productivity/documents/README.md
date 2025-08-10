

## Productivity Tools for the Agentic Environment

This folder contains additional Linux utilities pre-installed in the AI Agent Host, enabling Claude Code to autonomously perform advanced developer tasks.

### Included Tools

* **pandoc** — Allows Claude to convert documents between formats such as Markdown, HTML, LaTeX, and PDF. Ideal for generating reports or transforming documentation.
* **poppler-utils** — Enables Claude to manipulate PDFs, including text extraction and format conversion.

### Why It Matters

With these tools, Claude Code can:

* Generate professional PDF reports from project documentation.
* Convert files on the fly between multiple formats.
* Process and analyze documents directly inside the agentic environment — without relying on any cloud service.

This turns the AI Agent Host into a self-contained, fully capable development and documentation powerhouse.



### Usage Examples

* Convert `report.md` to PDF:
  ```bash
  pandoc report.md -o report.pdf
  ```

* Extract text from `input.pdf` into `output.txt`:
  ```bash
  pdftotext input.pdf output.txt
  ```

* Convert Markdown to HTML with custom styling:
  ```bash
  pandoc document.md -o document.html --css style.css
  ```


