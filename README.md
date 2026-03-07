# Global Earthquake Scientific Visualization using ParaView

A portfolio-ready scientific visualization case study demonstrating a full ParaView pipeline from raw USGS earthquake data to 3D rendered outputs.

## Project Overview
This project implements an end-to-end workflow used in real scientific visualization engineering:

1. Acquire raw earthquake event data from USGS (CSV feed).
2. Preprocess and validate the data in Python.
3. Convert events into VTK `PolyData` (`.vtp`) for ParaView-native workflows.
4. Build a ParaView pipeline with glyphs, scalar coloring, and contour-like magnitude surfaces.
5. Produce publication-quality still render and camera-orbit animation.

## Dataset Source
USGS Earthquake Hazards Program (monthly global feed):
- https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv

Fields used in this project:
- `time`
- `latitude`
- `longitude`
- `depth`
- `mag`

## Technology Stack
- **Python 3**
- **pandas** (CSV ingestion/cleanup)
- **VTK Python bindings** (geometry + `.vtp` export)
- **ParaView** (interactive and scripted visualization)

Install Python dependencies:

```bash
pip install pandas vtk
```

## Repository Structure

```text
paraview-earthquake-visualization
│
├── data
│   ├── earthquakes.csv
│   └── earthquakes.vtp                # generated
│
├── scripts
│   └── convert_to_vtk.py
│
├── paraview
│   └── earthquake_pipeline.pvsm
│
├── renders
│   ├── earthquake_visualization.png   # exported from ParaView
│   └── earthquake_animation.mp4       # exported from ParaView
│
├── docs
│   └── workflow_explanation.md
│
└── README.md
```

## Visualization Workflow

### 1) Prepare the dataset
Place the USGS CSV at `data/earthquakes.csv`.

> The repository includes a small schema-compatible sample file for offline demonstration. Replace it with the full USGS monthly CSV for production output.

### 2) Convert CSV to VTK PolyData
Run:

```bash
python scripts/convert_to_vtk.py --input data/earthquakes.csv --output data/earthquakes.vtp
```

Optional direct download mode (if network is available):

```bash
python scripts/convert_to_vtk.py --allow-download --output data/earthquakes.vtp
```

### 3) Open in ParaView and build pipeline
1. Open `data/earthquakes.vtp` and click **Apply**.
2. Add **Glyph** filter with `Sphere` glyphs.
3. Scale glyphs by `magnitude`.
4. Color glyphs by `magnitude` using a continuous colormap.
5. Interpolate points to a volume and apply **Contour** to reveal intensity layers.
6. Configure camera and lighting for global readability.
7. Save screenshot and camera animation:
   - `renders/earthquake_visualization.png`
   - `renders/earthquake_animation.mp4`

Detailed rationale and exact pipeline settings are documented in [`docs/workflow_explanation.md`](docs/workflow_explanation.md).

## Run Locally

```bash
# 1) Install dependencies
pip install pandas vtk

# 2) Convert CSV to VTK
python scripts/convert_to_vtk.py --input data/earthquakes.csv --output data/earthquakes.vtp

# 3) Open ParaView and load data/earthquakes.vtp
# 4) Apply pipeline steps from docs/workflow_explanation.md
# 5) Export still + animation to renders/
```

## Screenshots / Renders
After running the ParaView steps, commit outputs here:

- `renders/earthquake_visualization.png`
- `renders/earthquake_animation.mp4`

Example markdown embed for portfolio pages:

```md
![Global earthquake glyph visualization](renders/earthquake_visualization.png)
```

## Portfolio Value
This case study highlights practical skills expected in visualization engineering roles:

- Scientific data transformation for visualization systems
- VTK data model understanding (`vtkPolyData`, point arrays, scalars)
- Effective multivariate visual encoding (size + color)
- ParaView filter/pipeline reasoning and output production
