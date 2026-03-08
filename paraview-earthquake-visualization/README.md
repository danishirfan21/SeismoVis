# Global Earthquake Scientific Visualization using ParaView

This project demonstrates a complete scientific visualization workflow using **ParaView**, **VTK**, and **Python**. It transforms raw earthquake data from the USGS into a professional 3D visualization, highlighting seismic patterns across the globe.

![Earthquake Visualization](renders/earthquake_visualization.png)

## 🚀 Project Overview

The goal of this case study is to demonstrate the end-to-end process of scientific data visualization:
1.  **Data Ingestion**: Loading raw CSV data from the USGS.
2.  **Preprocessing**: Converting spherical coordinates (lat/lon/depth) into 3D Cartesian points using Python and VTK.
3.  **Visualization Pipeline**: Constructing a multi-stage pipeline in ParaView to represent earthquake magnitude through glyph size and color mapping.
4.  **Analysis**: Interpreting the visual results to understand global seismic activity.

## 📊 Dataset

- **Source**: [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv)
- **Timeframe**: Past 30 Days (all earthquakes)
- **Attributes**: Time, Latitude, Longitude, Depth, Magnitude.

## 🛠️ Technology Stack

- **ParaView**: For interactive visualization and pipeline construction.
- **Python 3**: For data preprocessing.
- **Pandas**: For data manipulation and filtering.
- **VTK (Visualization Toolkit)**: For generating `.vtp` datasets and offline rendering.

## 📂 Project Structure

```bash
paraview-earthquake-visualization
├── data/               # Raw and processed datasets (CSV, VTP)
├── scripts/            # Python scripts for preprocessing and rendering
├── paraview/           # ParaView state files (.pvsm)
├── renders/            # Static images and animation frames
├── docs/               # Scientific workflow documentation
└── README.md           # Project overview and instructions
```

## ⚙️ Installation & Usage

### 1. Install Dependencies
```bash
pip install pandas vtk
```

### 2. Preprocess Data
Run the conversion script to transform the CSV into a ParaView-compatible VTK format:
```bash
python scripts/convert_to_vtk.py
```

### 3. Open in ParaView
You can either manually build the pipeline following the [Workflow Documentation](docs/workflow_explanation.md) or load the state file:
- Open ParaView.
- Go to `File > Load State`.
- Select `paraview/earthquake_pipeline.pvsm`.

### 4. Generate Renders (Headless)
To generate the visualization assets without opening the GUI, run:
```bash
python scripts/generate_renders.py
```
The script will output `earthquake_visualization.png` and 30 animation frames in the `renders/` directory.

### 5. Create Animation (Optional)
To encode the animation frames into a high-quality video using `ffmpeg`, run:
```bash
ffmpeg -framerate 10 -i renders/frames/frame_%03d.png -c:v libx264 -pix_fmt yuv420p renders/earthquake_animation.mp4
```

## 🧠 Scientific Reasoning

The visualization uses **Glyphs** (spheres) to represent discrete seismic events.
- **Magnitude is mapped to Size**: Larger spheres immediately draw attention to high-energy events.
- **Magnitude is mapped to Color**: A red-to-blue gradient provides a clear distinction between intensity levels.
- **Geospatial Mapping**: Converting to 3D Cartesian coordinates allows the data to be viewed in its true global context, clearly showing tectonic plate boundaries.

For a deeper dive into the methodology, see [docs/workflow_explanation.md](docs/workflow_explanation.md).
