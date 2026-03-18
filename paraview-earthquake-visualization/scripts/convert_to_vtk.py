import pandas as pd
import numpy as np
import vtk
from vtk.util import numpy_support
import os

def csv_to_vtp(csv_path, vtp_path):
    """
    Converts earthquake CSV data from USGS into a VTK PolyData (.vtp) file.
    Maps latitude, longitude, and depth to 3D spherical coordinates.
    """
    print(f"Reading data from {csv_path}...")
    df = pd.read_csv(csv_path)

    # Filter out rows with missing coordinates or magnitude
    df = df.dropna(subset=['latitude', 'longitude', 'depth', 'mag'])

    # Filter out negative magnitudes (very small tremors that can cause visual artifacts)
    df = df[df['mag'] >= 0]

    # Earth radius in km
    R = 6371.0

    # Convert lat/lon/depth to 3D Cartesian coordinates (Spherical to Cartesian)
    # Latitude is 0 at equator, 90 at North Pole, -90 at South Pole
    # Longitude is 0 at Prime Meridian
    lat_rad = np.radians(df['latitude'])
    lon_rad = np.radians(df['longitude'])

    # Corrected spherical conversion:
    # x = r * cos(lat) * cos(lon)
    # y = r * cos(lat) * sin(lon)
    # z = r * sin(lat)
    r = np.clip(R - df['depth'], 0.1, R)

    x = r * np.cos(lat_rad) * np.cos(lon_rad)
    y = r * np.cos(lat_rad) * np.sin(lon_rad)
    z = r * np.sin(lat_rad)

    # Create VTK Points
    points = vtk.vtkPoints()
    vtk_coords = np.stack([x.values, y.values, z.values], axis=1).astype(np.float32)
    points.SetData(numpy_support.numpy_to_vtk(vtk_coords, deep=True))

    # Create VTK PolyData
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)

    # Add Magnitude as a scalar field
    mag_array = numpy_support.numpy_to_vtk(df['mag'].values.astype(np.float32), deep=True)
    mag_array.SetName("Magnitude")
    polydata.GetPointData().AddArray(mag_array)
    polydata.GetPointData().SetActiveScalars("Magnitude")

    # Add Depth as an additional field
    depth_array = numpy_support.numpy_to_vtk(df['depth'].values.astype(np.float32), deep=True)
    depth_array.SetName("Depth")
    polydata.GetPointData().AddArray(depth_array)

    # Write to .vtp file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(vtp_path)
    writer.SetInputData(polydata)
    writer.Write()

    print(f"Successfully saved VTK data to {vtp_path}")
    print(f"Total points processed: {len(df)}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_csv = os.path.join(base_dir, "data", "earthquakes.csv")
    output_vtp = os.path.join(base_dir, "data", "earthquakes.vtp")

    csv_to_vtp(input_csv, output_vtp)
