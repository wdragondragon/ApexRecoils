# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['client.py'],
    pathex=[],
    binaries=[],
    datas=[('msdk.dll','.'),('kmbox_dll_64bit.dll','.'),('wy_hkm.dll','.'),('ProcessHider.exe','.'),('images/client.png','images/')],
    hiddenimports=['wmi'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='client',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='./images/client.png'
)
#coll = COLLECT(
#    exe,
#    a.binaries,
#    a.zipfiles,
#    a.datas,
#    strip=False,
#    upx=True,
#    upx_exclude=[],
#    name='client'
#)
