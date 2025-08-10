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

* **Convert `.png` to `.jpg`:**
  ```bash
  convert image.png image.jpg
  ```

* **Resize image to 800x600:**
  ```bash
  convert input.jpg -resize 800x600 output.jpg
  ```

* **Extract 5-second video clip:**
  ```bash
  ffmpeg -i input.mp4 -ss 00:01:30 -t 00:00:05 -c copy clip.mp4
  ```

* **Create GIF from video:**
  ```bash
  ffmpeg -i video.mp4 -vf "fps=10,scale=320:-1" output.gif
  ```



### **Why This Matters**

These tools turn Claude Code into a **full local multimedia assistant** inside the AI Agent Host:

* **Self-contained**: Works without any external API or cloud service.
* **Fast**: Executes directly inside the Docker environment.
* **Flexible**: Supports hundreds of file formats and operations.
