# Global Earthquake Scientific Visualization Workflow

This document explains the scientific reasoning and technical steps taken to visualize global earthquake data using ParaView.

## 1. Dataset Characteristics
The dataset is sourced from the **USGS Earthquake Hazards Program**, specifically the "All Earthquakes (Past 30 Days)" feed.
- **Time**: Temporal distribution of events.
- **Latitude & Longitude**: Geographic location on the Earth's surface.
- **Depth**: Subsurface vertical position (in km).
- **Magnitude**: Energy released by the earthquake.

## 2. Technical Decisions

### Why VTK Format?
We chose the **VTK PolyData (.vtp)** format for several reasons:
- **Efficiency**: ParaView handles VTK-native formats much faster than CSV, especially for large datasets.
- **Coordinate Conversion**: The preprocessing script converts spherical coordinates (lat/lon/depth) into 3D Cartesian points, allowing for a realistic 3D representation on a global scale.
- **Attribute Mapping**: Point data like magnitude and depth are explicitly stored as scalar fields, making them immediately available for filters in ParaView.

### Visualization Filters

#### Glyph Filter (Spheres)
- **Purpose**: Represents each discrete earthquake event as a 3D object.
- **Reasoning**: Unlike simple points, spheres provide volume and can be scaled to represent quantitative data visually.

#### Scaling (Magnitude to Size)
- **Reasoning**: Mapping magnitude to the size of the glyph allows viewers to instantly distinguish minor tremors from major seismic events. This mimics the intuitive perception of intensity.

#### Color Mapping (Magnitude to Gradient)
- **Reasoning**: A gradient color map (e.g., Cool-to-Warm or Rainbow) adds another layer of information. High-magnitude events are colored in "hotter" colors (red/orange) to draw the viewer's attention to areas of high seismic risk.

#### Contour Visualization (Seismic Density)
- **Purpose**: To show areas of high seismic activity density rather than just individual points.
- **Method**: Using a **Gaussian Splatter** (or Gaussian Resampling) to interpolate discrete points into a volumetric field, followed by a **Contour Filter**.
- **Reasoning**: This provides a "heat map" effect in 3D, highlighting clusters where multiple earthquakes occur in close proximity, even if they are individually small.

## 3. ParaView Pipeline Construction (Manual Steps)

To recreate this visualization in ParaView:

1. **Load Data**:
   - Open ParaView and go to `File > Open`.
   - Select `data/earthquakes.vtp`.
   - Click `Apply`.

2. **Apply Glyph Filter**:
   - Go to `Filters > Alphabetical > Glyph`.
   - **Glyph Type**: Sphere.
   - **Scale Array**: Magnitude.
   - **Scale Factor**: Adjust to ~50.0 - 100.0.
   - Click `Apply`.

3. **Configure Color Map**:
   - Select the Glyph filter in the Pipeline Browser.
   - In the Properties panel, under **Coloring**, select `Magnitude`.
   - Click `Edit Color Map` and choose a preset like "Rainbow Desaturated".

4. **Create Density Contours**:
   - Select the original `earthquakes.vtp`.
   - Apply `Filters > Alphabetical > Gaussian Resampling`.
   - Set **Resampling Grid** (e.g., 100x100x100).
   - Click `Apply`.
   - Apply `Filters > Alphabetical > Contour` to the result.
   - Choose an Iso-surface value that highlights the clusters.
   - Set Opacity to ~0.3 for a "glow" effect.

5. **Lighting and Rendering**:
   - In the Properties panel for the Glyphs, enable **Specular** lighting (set to ~0.5) to give the spheres a professional, polished look.
   - Under **Render View** settings, enable **Ambient Occlusion** if your hardware supports it for better depth perception.

6. **Add Context**:
   - Create a Sphere source (`Sources > Sphere`) with radius 6360.0.
   - Set Color to Black or Dark Grey and Opacity to 0.4 to represent the Earth's core/mass.

## 4. Scientific Insights
The final visualization reveals:
- **Geographic Clustering**: Clear visualization of tectonic plate boundaries (e.g., the Ring of Fire).
- **Subduction Zones**: Depth mapping shows how earthquakes occur deeper in certain regions, indicating subducting plates.
- **Intensity hotspots**: High-magnitude clusters are easily identifiable through the combination of size and color mapping, while density contours highlight areas of chronic seismic activity.
