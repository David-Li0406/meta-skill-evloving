# Voxel Art - Validations

## Unity Voxel Texture Using Bilinear Filtering

### **Id**
unity-texture-filter-bilinear
### **Severity**
high
### **Category**
import
### **Description**
  Voxel palette textures should use Point (nearest neighbor) filtering to
  maintain crisp edges. Bilinear filtering blurs voxel colors together.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
filterMode\s*=\s*FilterMode\.Bilinear|FilterMode\.Trilinear
  #### **File Patterns**
    - *.cs
    - *.meta
### **Anti Pattern Example**
  // BAD: Bilinear filtering blurs voxel textures
  TextureImporter importer = assetImporter as TextureImporter;
  importer.filterMode = FilterMode.Bilinear;
  
### **Correct Example**
  // GOOD: Point filtering for crisp voxels
  TextureImporter importer = assetImporter as TextureImporter;
  importer.filterMode = FilterMode.Point;
  importer.mipmapEnabled = false;  // Also disable mipmaps
  
### **Fix Suggestion**
  Change texture filter mode to Point:
  ```csharp
  importer.filterMode = FilterMode.Point;
  importer.mipmapEnabled = false;
  ```
  

## Unity Voxel Texture Has Mipmaps Enabled

### **Id**
unity-voxel-mipmaps-enabled
### **Severity**
medium
### **Category**
import
### **Description**
  Mipmaps on voxel palette textures cause color bleeding at distance.
  They should be disabled for crisp voxel rendering at all distances.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
mipmapEnabled\s*=\s*true
  #### **File Patterns**
    - *.cs
    - *.meta
### **Anti Pattern Example**
  // BAD: Mipmaps cause voxel color bleeding
  TextureImporter importer = assetImporter as TextureImporter;
  importer.mipmapEnabled = true;
  
### **Correct Example**
  // GOOD: Disable mipmaps for voxel textures
  TextureImporter importer = assetImporter as TextureImporter;
  importer.mipmapEnabled = false;
  

## Missing Limited Dissolve in Voxel Export Script

### **Id**
blender-no-limited-dissolve
### **Severity**
high
### **Category**
optimization
### **Description**
  Blender scripts that export voxel meshes should apply Limited Dissolve to
  merge coplanar faces and dramatically reduce polygon count.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
export_scene\.(obj|fbx|gltf)
  #### **File Patterns**
    - *.py
### **Anti Pattern Example**
  # BAD: Export voxel mesh without optimization
  import bpy
  
  def export_voxel_model(filepath):
      bpy.ops.import_scene.obj(filepath="model.obj")
      bpy.ops.export_scene.fbx(filepath=filepath)
  
### **Correct Example**
  # GOOD: Optimize voxel mesh before export
  import bpy
  
  def export_voxel_model(filepath):
      # Import voxel OBJ
      bpy.ops.import_scene.obj(filepath="model.obj")
  
      # Select and enter edit mode
      obj = bpy.context.active_object
      bpy.ops.object.mode_set(mode='EDIT')
      bpy.ops.mesh.select_all(action='SELECT')
  
      # Optimize: merge coplanar faces
      bpy.ops.mesh.dissolve_limited(angle_limit=0.0001)
      bpy.ops.mesh.tris_to_quads()
  
      bpy.ops.object.mode_set(mode='OBJECT')
  
      # Export optimized mesh
      bpy.ops.export_scene.fbx(filepath=filepath)
  
### **Fix Suggestion**
  Add limited dissolve before export:
  ```python
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.ops.mesh.select_all(action='SELECT')
  bpy.ops.mesh.dissolve_limited(angle_limit=0.0001)
  bpy.ops.object.mode_set(mode='OBJECT')
  ```
  

## Voxel Export Without LOD Generation

### **Id**
blender-voxel-no-lod
### **Severity**
medium
### **Category**
optimization
### **Description**
  Voxel models for games should have LOD (Level of Detail) versions generated
  to maintain performance at various distances.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
export_scene\.(fbx|gltf)
  #### **File Patterns**
    - *.py
### **Correct Example**
  # GOOD: Generate LODs for voxel model
  import bpy
  
  def generate_voxel_lods(obj, lod_ratios=[1.0, 0.5, 0.25, 0.1]):
      """Generate LOD versions of voxel mesh"""
      lods = []
  
      for i, ratio in enumerate(lod_ratios):
          # Duplicate object
          bpy.ops.object.select_all(action='DESELECT')
          obj.select_set(True)
          bpy.context.view_layer.objects.active = obj
          bpy.ops.object.duplicate()
  
          lod_obj = bpy.context.active_object
          lod_obj.name = f"{obj.name}_LOD{i}"
  
          if ratio < 1.0:
              # Add decimate modifier
              mod = lod_obj.modifiers.new(name="Decimate", type='DECIMATE')
              mod.ratio = ratio
              bpy.ops.object.modifier_apply(modifier="Decimate")
  
          lods.append(lod_obj)
  
      return lods
  

## Chunk Mesh Generation on Main Thread

### **Id**
chunk-mesh-main-thread
### **Severity**
critical
### **Category**
performance
### **Description**
  Generating chunk meshes synchronously on the main thread causes frame
  drops. Voxel chunk regeneration should be done asynchronously.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
GenerateMesh|RebuildMesh|UpdateChunk|RegenerateMesh
  #### **File Patterns**
    - *.cs
### **Anti Pattern Example**
  // BAD: Synchronous mesh generation blocks main thread
  public class VoxelChunk : MonoBehaviour
  {
      public void OnVoxelDestroyed(int x, int y, int z)
      {
          voxels[x, y, z] = 0;
          GenerateMesh();  // BLOCKS! Causes stutter
      }
  
      void GenerateMesh()
      {
          // Complex mesh generation...
          for (int x = 0; x < size; x++)
              for (int y = 0; y < size; y++)
                  for (int z = 0; z < size; z++)
                      // Generate faces...
      }
  }
  
### **Correct Example**
  // GOOD: Async mesh generation with job system
  using Unity.Jobs;
  using Unity.Collections;
  using Unity.Burst;
  
  public class VoxelChunk : MonoBehaviour
  {
      private bool isDirty = false;
      private MeshGenerationJob currentJob;
      private JobHandle jobHandle;
  
      public void OnVoxelDestroyed(int x, int y, int z)
      {
          voxels[x, y, z] = 0;
          isDirty = true;  // Flag for async rebuild
      }
  
      void LateUpdate()
      {
          // Complete previous job if ready
          if (jobHandle.IsCompleted)
          {
              jobHandle.Complete();
              ApplyMesh(currentJob.result);
          }
  
          // Start new job if dirty
          if (isDirty && !jobHandle.IsCompleted)
          {
              currentJob = new MeshGenerationJob(voxels);
              jobHandle = currentJob.Schedule();
              isDirty = false;
          }
      }
  }
  
  [BurstCompile]
  struct MeshGenerationJob : IJob
  {
      public NativeArray<byte> voxels;
      public NativeList<Vector3> result;
  
      public void Execute()
      {
          // Mesh generation runs on worker thread
      }
  }
  
### **Fix Suggestion**
  Move mesh generation to async/background thread:
  - Unity: Use Job System with Burst
  - Unreal: Use AsyncTask or GameThread delegates
  - General: Move to separate thread, swap mesh on main thread
  

## Voxel Chunk Size Too Large

### **Id**
large-chunk-size
### **Severity**
medium
### **Category**
performance
### **Description**
  Chunk sizes larger than 32x32x32 cause slow mesh regeneration and
  excessive memory usage. Smaller chunks update faster but increase draw calls.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
chunkSize\s*=\s*(64|128|256)|CHUNK_SIZE\s*=\s*(64|128|256)
  #### **File Patterns**
    - *.cs
    - *.cpp
    - *.h
### **Anti Pattern Example**
  // BAD: Chunk too large - slow regeneration
  public const int CHUNK_SIZE = 64;  // 262,144 voxels per chunk!
  
### **Correct Example**
  // GOOD: Balanced chunk size
  public const int CHUNK_SIZE = 16;  // 4,096 voxels - fast updates
  // Or
  public const int CHUNK_SIZE = 32;  // 32,768 voxels - balanced
  
### **Fix Suggestion**
  Use chunk sizes between 16 and 32:
  - 16x16x16: Fast updates, more draw calls
  - 32x32x32: Balanced for most games
  - 64x64x64: Only for static content
  

## Voxel Rendering Without Greedy Meshing

### **Id**
no-greedy-meshing
### **Severity**
high
### **Category**
performance
### **Description**
  Rendering voxels without greedy meshing creates 6-12 triangles per voxel.
  Greedy meshing can reduce this by 90%+.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
GenerateVoxelFace|AddVoxelQuad|CreateCube|DrawVoxel
  #### **File Patterns**
    - *.cs
    - *.cpp
    - *.js
    - *.ts
### **Anti Pattern Example**
  // BAD: Naive per-voxel face generation
  void GenerateMesh(int[,,] voxels)
  {
      for (int x = 0; x < size; x++)
      {
          for (int y = 0; y < size; y++)
          {
              for (int z = 0; z < size; z++)
              {
                  if (voxels[x,y,z] != 0)
                  {
                      // Creates 6 quads per visible voxel
                      if (IsExposed(x+1,y,z)) AddQuad(Right);
                      if (IsExposed(x-1,y,z)) AddQuad(Left);
                      // ... etc
                  }
              }
          }
      }
  }
  
### **Correct Example**
  // GOOD: Greedy meshing - merge coplanar faces
  // Reference: 0fps.net/2012/06/30/meshing-in-a-minecraft-game/
  
  void GenerateMeshGreedy(int[,,] voxels)
  {
      // For each face direction
      for (int d = 0; d < 3; d++)
      {
          // For each slice in that direction
          for (int slice = 0; slice < size; slice++)
          {
              // Get 2D mask of visible faces
              bool[,] mask = GetSliceMask(d, slice);
  
              // Greedy merge: find largest rectangles
              while (HasUnprocessedFaces(mask))
              {
                  // Find starting point
                  var start = FindStart(mask);
  
                  // Expand width while same material
                  int width = ExpandWidth(mask, start);
  
                  // Expand height while same material
                  int height = ExpandHeight(mask, start, width);
  
                  // Create single quad for entire rectangle
                  AddGreedyQuad(d, slice, start, width, height);
  
                  // Mark as processed
                  MarkProcessed(mask, start, width, height);
              }
          }
      }
  }
  
### **Fix Suggestion**
  Implement greedy meshing for voxel rendering.
  See reference implementation at 0fps.net for algorithm details.
  

## Voxel Animation Without Compression

### **Id**
animation-no-compression
### **Severity**
medium
### **Category**
storage
### **Description**
  Storing full voxel frames for animation wastes storage. Delta compression
  or run-length encoding should be used.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
animationFrames|voxelFrames|frameData
  #### **File Patterns**
    - *.cs
    - *.cpp
    - *.ts
### **Anti Pattern Example**
  // BAD: Full copy of each animation frame
  public class VoxelAnimation
  {
      // 32x32x32 x 8 frames = 262,144 bytes per animation!
      public byte[,,,] frames = new byte[8, 32, 32, 32];
  }
  
### **Correct Example**
  // GOOD: Delta-compressed animation frames
  public class VoxelAnimation
  {
      // Base frame stored fully
      public byte[,,] baseFrame = new byte[32, 32, 32];
  
      // Delta frames store only changes
      public List<VoxelDelta>[] deltas = new List<VoxelDelta>[8];
  
      public struct VoxelDelta
      {
          public ushort position;  // Packed x,y,z
          public byte oldValue;
          public byte newValue;
      }
  
      public byte[,,] GetFrame(int index)
      {
          var frame = (byte[,,])baseFrame.Clone();
  
          for (int i = 1; i <= index; i++)
          {
              foreach (var delta in deltas[i])
              {
                  int x = delta.position & 0x1F;
                  int y = (delta.position >> 5) & 0x1F;
                  int z = (delta.position >> 10) & 0x1F;
                  frame[x, y, z] = delta.newValue;
              }
          }
  
          return frame;
      }
  }
  

## Inconsistent Voxel Animation Frame Naming

### **Id**
voxel-frame-naming
### **Severity**
low
### **Category**
organization
### **Description**
  Voxel animation frames should use consistent naming with zero-padded
  numbers for proper sorting.
  
### **Detection**
  #### **Type**
regex
  #### **Pattern**
_\d\.vox$|_[a-z]\.vox$
  #### **File Patterns**
    - *.vox
### **Anti Pattern Example**
  # BAD: Inconsistent naming
  character_walk_1.vox
  character_walk_2.vox
  character_walk_10.vox  # Sorts wrong!
  
### **Correct Example**
  # GOOD: Zero-padded frame numbers
  character_walk_01.vox
  character_walk_02.vox
  character_walk_10.vox
  
  # ALSO GOOD: Explicit naming
  character_idle_frame01.vox
  character_idle_frame02.vox
  

## Missing Shared Palette File

### **Id**
voxel-no-palette-file
### **Severity**
low
### **Category**
organization
### **Description**
  Voxel projects should have a shared palette file for consistency across
  all models. MagicaVoxel palettes are 256x1 PNG files.
  
### **Detection**
  #### **Type**
file_exists
  #### **Expected Files**
    - palette.png
    - palette/*.png
    - assets/palette.png
  #### **File Patterns**
    - *.vox
### **Correct Example**
  # Project structure with shared palette
  project/
    palette/
      main_palette.png      # Master palette
      character_palette.png # Character-specific
      environment_palette.png
    models/
      character.vox
      prop.vox
  