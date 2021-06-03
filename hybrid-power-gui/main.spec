from kivy_deps import sdl2, glew

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/home/bello/Documents/projects/hybrid-power/hybrid-power/hybrid-power-gui'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
a.data += [('Code\design.kv', 'C:\\hybrid-power\\gui\\design.kv', 'DATA')]
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
    Tree('C:\\hybrid-power\\gui\\design.kv'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sld2.dep_bins+glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
