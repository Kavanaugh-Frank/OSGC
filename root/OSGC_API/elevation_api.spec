# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('data', 'data'), ('C:\\Users\\kavan\\anaconda3\\envs\\myenv\\Lib\\site-packages\\pyproj\\proj_dir\\share\\proj', 'proj')],
    hiddenimports=['rasterio.sample', 'rasterio._base', 'rasterio._shim', 'rasterio.enums', 'rasterio.errors', 'rasterio.dtypes', 'rasterio.io', 'rasterio.transform', 'rasterio.profiles', 'rasterio.coords', 'rasterio.crs', 'rasterio.control', 'rasterio.plot', 'rasterio.vrt', 'rasterio.warp', 'rasterio.windows', 'rasterio._features'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5'],
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
