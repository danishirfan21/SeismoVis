#!/usr/bin/env python3
"""Convert USGS earthquake CSV data into VTK PolyData (.vtp).

This script is intentionally production-oriented for portfolio use:
- validates required columns
- handles missing rows gracefully
- maps latitude/longitude/depth to Earth-centered Cartesian coordinates
- stores scientific attributes (magnitude, depth, time, coordinates) on points

Usage:
    python scripts/convert_to_vtk.py \
      --input data/earthquakes.csv \
      --output data/earthquakes.vtp
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import vtk
from vtk.util.numpy_support import numpy_to_vtk

USGS_MONTHLY_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv"
EARTH_RADIUS_KM = 6371.0
REQUIRED_COLUMNS = ["time", "latitude", "longitude", "depth", "mag"]


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/earthquakes.csv"),
        help="Path to local CSV file. If missing and --allow-download is set, pulls from USGS.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/earthquakes.vtp"),
        help="Output VTP path.",
    )
    parser.add_argument(
        "--allow-download",
        action="store_true",
        help="Download CSV from USGS if local input is unavailable.",
    )
    return parser.parse_args()


def load_dataset(input_path: Path, allow_download: bool) -> pd.DataFrame:
    """Load earthquake dataset from local CSV or optional USGS URL."""
    if input_path.exists():
        return pd.read_csv(input_path)

    if allow_download:
        print(f"Local file not found at {input_path}. Downloading from USGS feed...", file=sys.stderr)
        return pd.read_csv(USGS_MONTHLY_URL)

    raise FileNotFoundError(
        f"Input CSV not found: {input_path}. Place the USGS CSV there or rerun with --allow-download."
    )


def validate_and_prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Keep required fields and sanitize numeric values for visualization."""
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset missing required columns: {missing}")

    work = df[REQUIRED_COLUMNS].copy()
    for col in ["latitude", "longitude", "depth", "mag"]:
        work[col] = pd.to_numeric(work[col], errors="coerce")

    clean = work.dropna(subset=["latitude", "longitude", "depth", "mag"]).reset_index(drop=True)
    if clean.empty:
        raise ValueError("No valid earthquake rows remain after filtering nulls.")

    clean = clean.rename(columns={"mag": "magnitude"})
    return clean


def spherical_to_cartesian(lat_deg: pd.Series, lon_deg: pd.Series, depth_km: pd.Series):
    """Convert geodetic coordinates to Earth-centered Cartesian coordinates in kilometers."""
    # Earthquake depth is positive downward, so we subtract depth from Earth radius.
    radius = EARTH_RADIUS_KM - depth_km.to_numpy()
    lat = lat_deg.to_numpy() * (3.141592653589793 / 180.0)
    lon = lon_deg.to_numpy() * (3.141592653589793 / 180.0)

    x = radius * (np.cos(lat) * np.cos(lon))
    y = radius * (np.cos(lat) * np.sin(lon))
    z = radius * np.sin(lat)
    return x, y, z


def dataframe_to_polydata(df: pd.DataFrame) -> vtk.vtkPolyData:
    """Build vtkPolyData with point coordinates + scalar attributes."""
    x, y, z = spherical_to_cartesian(df["latitude"], df["longitude"], df["depth"])

    points = vtk.vtkPoints()
    points.SetData(
        numpy_to_vtk(
            np.column_stack((x, y, z)),
            deep=True,
            array_type=vtk.VTK_FLOAT,
        )
    )

    poly = vtk.vtkPolyData()
    poly.SetPoints(points)

    vertices = vtk.vtkCellArray()
    for i in range(len(df)):
        vertices.InsertNextCell(1)
        vertices.InsertCellPoint(i)
    poly.SetVerts(vertices)

    arrays = {
        "magnitude": df["magnitude"].to_numpy(),
        "depth_km": df["depth"].to_numpy(),
        "latitude": df["latitude"].to_numpy(),
        "longitude": df["longitude"].to_numpy(),
    }

    for name, values in arrays.items():
        vtk_array = numpy_to_vtk(values, deep=True, array_type=vtk.VTK_FLOAT)
        vtk_array.SetName(name)
        poly.GetPointData().AddArray(vtk_array)

    time_array = vtk.vtkStringArray()
    time_array.SetName("time")
    for value in df["time"].astype(str):
        time_array.InsertNextValue(value)
    poly.GetPointData().AddArray(time_array)

    poly.GetPointData().SetActiveScalars("magnitude")
    return poly


def write_vtp(poly: vtk.vtkPolyData, output_path: Path) -> None:
    """Serialize vtkPolyData to .vtp on disk."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(str(output_path))
    writer.SetInputData(poly)
    if writer.Write() != 1:
        raise IOError(f"Failed to write VTP file: {output_path}")


def main() -> int:
    args = parse_args()
    df = load_dataset(args.input, args.allow_download)
    clean = validate_and_prepare(df)
    poly = dataframe_to_polydata(clean)
    write_vtp(poly, args.output)

    print(
        f"Converted {len(clean)} earthquake events to VTP: {args.output}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
