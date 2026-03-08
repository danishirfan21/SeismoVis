import vtk
import os
import numpy as np

def generate_renders(vtp_path, output_png, frames_dir):
    """
    Simulates a ParaView visualization using VTK and saves high-quality renders.
    """
    # Create directory for frames if it doesn't exist
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)

    # 1. Read the VTP data
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(vtp_path)
    reader.Update()

    # 2. Setup Glyph filter (Spheres for earthquakes)
    sphere_source = vtk.vtkSphereSource()
    sphere_source.SetThetaResolution(16)
    sphere_source.SetPhiResolution(16)

    glyph = vtk.vtkGlyph3D()
    glyph.SetSourceConnection(sphere_source.GetOutputPort())
    glyph.SetInputConnection(reader.GetOutputPort())
    glyph.SetScaleModeToScaleByScalar()
    glyph.SetScaleFactor(100.0)  # Adjust base size
    glyph.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, "Magnitude")
    glyph.Update()

    # 3. Setup Color Mapping
    # We use a Rainbow lookup table similar to ParaView's default
    lut = vtk.vtkLookupTable()
    lut.SetHueRange(0.667, 0.0)  # Blue (low) to Red (high)
    lut.SetNumberOfTableValues(256)
    lut.Build()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(glyph.GetOutputPort())
    mapper.SetScalarRange(reader.GetOutput().GetPointData().GetArray("Magnitude").GetRange())
    mapper.SetLookupTable(lut)

    # 4. Setup Contour Visualization (representing seismic density)
    # Since we have points, we need to interpolate into a volume first.
    splatter = vtk.vtkGaussianSplatter()
    splatter.SetInputConnection(reader.GetOutputPort())
    splatter.SetSampleDimensions(100, 100, 100)
    splatter.SetRadius(0.05)
    splatter.ScalarWarpingOff()

    contour = vtk.vtkContourFilter()
    contour.SetInputConnection(splatter.GetOutputPort())
    contour.SetValue(0, 0.01) # Define a density threshold

    contour_mapper = vtk.vtkPolyDataMapper()
    contour_mapper.SetInputConnection(contour.GetOutputPort())
    contour_mapper.ScalarVisibilityOff()

    contour_actor = vtk.vtkActor()
    contour_actor.SetMapper(contour_mapper)
    contour_actor.GetProperty().SetColor(1.0, 1.0, 0.5)
    contour_actor.GetProperty().SetOpacity(0.3)
    contour_actor.GetProperty().SetRepresentationToSurface()

    # 5. Setup Actor and Renderer
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetSpecular(0.6)
    actor.GetProperty().SetSpecularPower(30)
    actor.GetProperty().SetAmbient(0.2)
    actor.GetProperty().SetDiffuse(0.8)

    # Create a background earth sphere for context
    earth_sphere = vtk.vtkSphereSource()
    earth_sphere.SetRadius(6371.0)
    earth_sphere.SetThetaResolution(64)
    earth_sphere.SetPhiResolution(64)

    earth_mapper = vtk.vtkPolyDataMapper()
    earth_mapper.SetInputConnection(earth_sphere.GetOutputPort())

    earth_actor = vtk.vtkActor()
    earth_actor.SetMapper(earth_mapper)
    earth_actor.GetProperty().SetColor(0.2, 0.2, 0.2)
    earth_actor.GetProperty().SetOpacity(0.5)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.AddActor(contour_actor)
    renderer.AddActor(earth_actor)

    # Lighting setup
    light = vtk.vtkLight()
    light.SetLightTypeToHeadlight()
    light.SetIntensity(0.8)
    renderer.AddLight(light)

    renderer.SetBackground(0.05, 0.05, 0.1) # Dark blue-grey space background

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(1920, 1080)
    render_window.SetOffScreenRendering(1)

    camera = renderer.GetActiveCamera()
    camera.SetPosition(20000, 20000, 20000)
    camera.SetFocalPoint(0, 0, 0)
    renderer.ResetCamera()
    camera.Dolly(1.5)

    render_window.Render()

    # 6. Save static screenshot
    w2if = vtk.vtkWindowToImageFilter()
    w2if.SetInput(render_window)
    w2if.Update()

    writer = vtk.vtkPNGWriter()
    writer.SetFileName(output_png)
    writer.SetInputConnection(w2if.GetOutputPort())
    writer.Write()
    print(f"Static render saved to {output_png}")

    # 7. Generate animation frames (rotating camera)
    num_frames = 30
    for i in range(num_frames):
        camera.Azimuth(360.0 / num_frames)
        render_window.Render()

        w2if.Modified()
        w2if.Update()

        frame_path = os.path.join(frames_dir, f"frame_{i:03d}.png")
        writer.SetFileName(frame_path)
        writer.Write()

    print(f"Animation frames saved to {frames_dir}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vtp_data = os.path.join(base_dir, "data", "earthquakes.vtp")
    out_png = os.path.join(base_dir, "renders", "earthquake_visualization.png")
    frames = os.path.join(base_dir, "renders", "frames")

    generate_renders(vtp_data, out_png, frames)
