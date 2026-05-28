# Manyfold Supported File Formats

Complete list of file formats indexed by Manyfold. Files not in these lists are ignored.

## 3D Models

| File Type | Extensions | MIME Type | Preview | Analyze |
|-----------|------------|-----------|---------|---------|
| 3D Studio | .3ds, .max | application/x-3ds | ✅ | |
| 3MF | .3mf | model/3mf | ✅ | |
| AMF | .amf | application/x-amf | | |
| Alembic | .abc | model/x-alembic | | |
| Autodesk DWG | .dwg | image/vnd.dwg | | |
| Autodesk DXF | .dxf | image/vnd.dxf | | |
| Autodesk Inventor | .iam, .ipt | model/x-inventor-* | | |
| BRep | .brep | model/x-brep | | |
| Blender | .blend | model/x-blender | | |
| Cheetah3D | .jas | model/x-cheetah3d | | |
| Collada | .dae | model/vnd.collada+xml | | |
| DRACO | .drc | model/vnd.google.draco | ✅ | |
| Filmbox | .fbx | model/x-fbx | ✅ | |
| FreeCAD | .fcstd | model/x-freecad | | |
| Fusion360 | .f3d, .f3z | model/x-fusion | | |
| GLTF | .gltf, .glb | model/gltf+json, model/gltf+binary | ✅ | |
| HueForge | .hfp | model/x-hfp | | |
| IGES | .iges, .igs | model/iges | | |
| LDraw | .ldr, .mpd | application/x-ldraw | ✅ | |
| Maya | .ma, .mb | model/x-maya | | |
| Meshmixer | .mix | model/x-meshmixer | | |
| Modo | .lxo | model/x-modo | | |
| OpenSCAD | .scad | application/x-openscad | | |
| PLY | .ply | model/x-ply | ✅ | |
| STEP | .step, .stp | model/x-step | | |
| **STL** | .stl | model/stl | ✅ | ✅ |
| Sketchup | .skp | model/x-sketchup | | |
| Solidworks | .sldprt | model/x-solidworks-part | | |
| Speedtree | .spm | model/x-speedtree | | |
| VRML | .wrl | model/vrml | | |
| **Wavefront OBJ** | .obj, .mtl | model/obj | ✅ | ✅ |
| X3D | .x3d | model/x3d | | |

**Preview**: Can be rendered in the web viewer
**Analyze**: Geometric analysis (mesh errors, non-manifold detection)

## Print & Slicer Files

| File Type | Extensions | MIME Type | Preview |
|-----------|------------|-----------|---------|
| Chitubox | .chitubox, .ctb | model/x-chitubox | |
| **GCode** | .gcode | model/x-gcode | ✅ |
| Lychee | .lys, .lyt | model/x-lychee | |

## Images

| File Type | Extensions | MIME Type | Preview |
|-----------|------------|-----------|---------|
| BMP | .bmp | image/bmp | ✅ |
| GIF | .gif | image/gif | ✅ |
| JPEG | .jpg, .jpeg, .jpe, .pjpeg | image/jpeg | ✅ |
| PNG | .png | image/png | ✅ |
| SVG | .svg | image/svg+xml | ✅ |
| TIFF | .tiff, .tif | image/tiff | ✅ |
| WebP | .webp | image/webp | ✅ |

## Video

| File Type | Extensions | MIME Type | Preview |
|-----------|------------|-----------|---------|
| MP4 | .mp4, .m4v | video/mp4 | ✅ |
| MPEG | .mpeg, .mpg, .mpe | video/mpeg | ✅ |
| WebM | .webm | video/webm | ✅ |

## Documents

| File Type | Extensions | MIME Type | Preview |
|-----------|------------|-----------|---------|
| HTML | .html | text/html | |
| **Markdown** | .md | text/markdown | ✅ |
| Microsoft Word | .doc, .docx | application/msword | |
| **PDF** | .pdf | application/pdf | ✅ |
| **Text** | .txt, .text | text/plain | ✅ |

## Archives (for upload)

| File Type | Extensions | MIME Type |
|-----------|------------|-----------|
| 7-Zip | .7z | application/x-7z-compressed |
| bzip2 | .bz2 | application/x-bzip2 |
| gzip | .gzip, .gz | application/gzip |
| RAR | .rar | application/x-rar-compressed |
| ZIP | .zip | application/zip |

## Other / Specialty

| File Type | Extensions | MIME Type |
|-----------|------------|-----------|
| Binary blobs | .bin | application/octet-stream |
| Excellon (PCB) | .drl | application/x-excellon |
| Gerber (PCB) | .grb, .gerber, .geb, .gb, .grbjob | application/x-gerber |
| KiCad | .kicad_pro, .kicad_mod, .kicad_pcb, .kicad_sym, .kicad_sch, .kicad_wks | application/x-kicad-* |

## File Conversion

Manyfold can convert inefficient formats to 3MF:
- ASCII STL → 3MF: ~95% space savings
- OBJ → 3MF: ~50% space savings

To convert, use the "Convert to 3MF" action on individual files or in bulk.

## Notes

- `x-` MIME types are unofficial and may only be used within Manyfold
- Files not in these lists are ignored during scanning
- Request new format support via GitHub feature request
