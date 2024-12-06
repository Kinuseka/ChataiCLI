# -*- mode: python ; coding: utf-8 -*-
block_cipher = None
from PyInstaller.utils.hooks import collect_data_files

fua_data = collect_data_files('fake_useragent', include_py_files=False)
datas = [
            ('./resources/app_icon_raw.jpg', 'resources/'),
            ('./resources/app_icon.ico', 'resources/'),
            ('./cert/certificate_file.crt', 'cert/'),
            ('./shipping_config.json', '.')
        ]
datas.extend(fua_data)

a = Analysis(
    ['main_cli.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ChataiV1.exe',
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
    version=None,
    uac_admin=False,
    icon=['resources\\app_icon.ico'],
)