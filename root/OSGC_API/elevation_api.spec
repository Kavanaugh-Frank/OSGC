# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files

# Get the path to the conda environment
conda_env_path = os.path.join('C:\\Users\\kavan\\anaconda3\\envs\\myenv')

# Add required DLLs
binaries = [
    # GDAL-related DLLs
    (os.path.join(conda_env_path, 'Library', 'bin', 'gdal.dll'), '.'),
    (os.path.join(conda_env_path, 'Library', 'bin', 'proj_9_3.dll'), '.'),  # Updated DLL name
    (os.path.join(conda_env_path, 'Library', 'bin', 'geos_c.dll'), '.'),
]

# Add data files
datas = [
    ('data', 'data'),
    # PROJ data
    (os.path.join(conda_env_path, 'Lib', 'site-packages', 'pyproj', 'proj_dir', 'share', 'proj'), 'proj'),
    # GDAL data
    (os.path.join(conda_env_path, 'Library', 'share', 'gdal'), 'gdal'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        'rasterio.sample', 'rasterio._base', 'rasterio._shim', 
        'rasterio.enums', 'rasterio.errors', 'rasterio.dtypes', 
        'rasterio.io', 'rasterio.transform', 'rasterio.profiles', 
        'rasterio.coords', 'rasterio.crs', 'rasterio.control', 
        'rasterio.plot', 'rasterio.vrt', 'rasterio.warp', 
        'rasterio.windows', 'rasterio._features', 'pyproj.proj_dir'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['runtime_hook.py'],
    excludes = [
    'PyQt5'
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TerrainExtractionAutomator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='elevation_api',
)
