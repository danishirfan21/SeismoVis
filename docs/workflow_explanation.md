# Workflow Explanation: Global Earthquake Scientific Visualization using ParaView

## 1) Dataset characteristics
The USGS monthly earthquake feed is a point-event dataset where each row represents one detected earthquake event with geospatial and physical attributes. For visualization, the key fields are:

- `time`: event timestamp
- `latitude`, `longitude`: event location on Earth
- `depth`: focal depth in kilometers (positive downward)
- `mag`: earthquake magnitude

This project standardizes `mag` to `magnitude` and keeps the location/depth attributes for linked visual analysis.

## 2) Why VTK/PolyData format was chosen
CSV is great for tabular storage, but ParaView workflows are stronger when data is represented as explicit geometry plus attribute arrays. `vtkPolyData` is used because:

- Earthquakes are naturally *point* events.
- Point scalar arrays (`magnitude`, `depth_km`) can drive glyph size/color directly.
- PolyData works efficiently with Glyph, Contour (after interpolation), and camera animation pipelines.

The converter writes `data/earthquakes.vtp`, which is a portable XML VTK dataset readable by ParaView.

## 3) Data preprocessing decisions
The preprocessing script (`scripts/convert_to_vtk.py`) performs:

1. Required-column validation (`time`, `latitude`, `longitude`, `depth`, `mag`).
2. Numeric coercion and null filtering for stable rendering.
3. Geospatial conversion from latitude/longitude/depth into Earth-centered Cartesian coordinates:
   - radius = 6371 km - depth
   - x = r cos(lat) cos(lon)
   - y = r cos(lat) sin(lon)
   - z = r sin(lat)
4. Creation of one vertex cell per earthquake event in `vtkPolyData`.
5. Storage of point data arrays: `magnitude`, `depth_km`, `latitude`, `longitude`.

This creates a reusable scientific dataset for ParaView and reproducible portfolio demonstrations.

## 4) ParaView pipeline (step-by-step)

### A. Data import
1. Open ParaView.
2. `File -> Open` and select `data/earthquakes.vtp`.
3. Click **Apply** in the Properties panel.

### B. Glyph-based event representation
1. Select `earthquakes.vtp` in the Pipeline Browser.
2. `Filters -> Alphabetical -> Glyph`.
3. Configure:
   - **Glyph Type**: `Sphere`
   - **Orientation Array**: `None`
   - **Scale Array**: `magnitude`
   - **Scale Factor**: start near `5-20` (dataset-dependent)
   - **Glyph Mode**: `All Points`
4. Click **Apply**.

**Reasoning:** Sphere glyphs map each event to a perceptible 3D marker; scaling by magnitude makes larger events immediately visible.

### C. Color mapping
1. On the Glyph representation, set **Coloring** to `magnitude`.
2. Open color map editor and choose a perceptually ordered map (e.g., `Viridis` or `Inferno`).
3. Rescale to data range.

**Reasoning:** Mapping magnitude to both size and color reinforces seismic intensity through two visual channels.

### D. Contour/intensity layers
Contour requires gridded/scalar field support. For point events:

1. Select `earthquakes.vtp`.
2. Apply `Point Volume Interpolator` to generate a continuous scalar field from points.
   - Source: `Bounded Volume`
   - Kernel: `Gaussian` (tune radius for smoothing)
   - Pass point arrays including `magnitude`
3. Apply `Contour` on interpolated output.
   - Contour By: `magnitude`
   - Set several iso-values (e.g., 3.0, 4.5, 6.0)
4. Optional styling: low opacity + edge visibility.

**Reasoning:** Isosurfaces reveal spatial regions where local earthquake magnitudes cluster around target intensity thresholds.

### E. Camera, lighting, rendering
1. Use `Reset Camera` and switch to perspective mode.
2. Rotate to show both global spread and depth layering.
3. Adjust:
   - Representation shading: `Phong`
   - Ambient/Diffuse/Specular for sphere legibility
   - Add subtle background gradient
4. Increase render quality:
   - `View -> Color Palette` (dark background recommended)
   - `Edit -> Settings -> Render View` (anti-aliasing / samples)

### F. Animation
1. Open `View -> Animation View`.
2. Add a camera track (`Camera` keyframes).
3. Set start/end keyframes for ~360° azimuth orbit.
4. `File -> Save Animation`:
   - Format: MP4
   - Suggested resolution: `1920x1080`
   - Frame rate: `24`
   - Duration: `8-12` seconds

## 5) Export targets
- High-resolution still image: `renders/earthquake_visualization.png`
- Rotating animation: `renders/earthquake_animation.mp4`

## 6) Insights this visualization reveals
- Major plate boundary systems emerge as dense global seismic belts.
- Large magnitude events stand out immediately due to color + size coupling.
- Depth-aware 3D positioning exposes shallow vs deep-focus seismic regimes.
- Contour layers provide a macro-level view of regional intensity fields.

These are exactly the types of questions scientific visualization should accelerate: *where are events concentrated, how intense are they, and how are they distributed in depth and geography?*
