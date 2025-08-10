## **Productivity Tools for Claude Code**

This folder contains utilities installed in the AI Agent Host environment to enhance Claude’s **agentic capabilities** for **image and video processing** directly inside the Docker stack — no cloud services required.

### **Included Tools**

#### **Images**

* **ImageMagick** – Convert, resize, crop, and annotate images (`convert`, `mogrify`).
* **GraphicsMagick** – Faster alternative for bulk image processing.
* **OptiPNG / jpegoptim** – Lossless optimization for PNG and JPEG files.
* **ExifTool** – Read and modify image metadata (EXIF, IPTC, XMP).
* **FFmpeg** – Extract frames or still images from video files.

#### **Videos**

* **FFmpeg** – Convert video formats, trim clips, extract audio, change resolution/frame rate.
* **MKVToolNix** – Edit and manipulate MKV files without re-encoding.
* **Gifsicle** – Optimize and edit GIF animations.



### **Example Agentic Tasks**

Claude can now autonomously:

* Convert `.png` to `.jpg` or `.webp`
* Resize an image to specific dimensions
* Batch-optimize all images in a folder
* Extract a 5-second clip from a video
* Create a GIF from a `.mp4` video



### **Why This Matters**

These tools turn Claude Code into a **full local multimedia assistant** inside the AI Agent Host:

* **Self-contained**: Works without any external API or cloud service.
* **Fast**: Executes directly inside the Docker environment.
* **Flexible**: Supports hundreds of file formats and operations.
