"""
GraphCast model adapted for ocean velocity prediction
Adapted from the reference GraphCast implementation to handle:
1. 2D ocean velocity data (u, v components)
2. Multi-frame input/output for video prediction
3. Pseudo-3D processing by adding a depth dimension
4. 240x240 spatial resolution
"""

import numpy as np
import torch
import torch.nn as nn
from einops import rearrange, repeat
from typing import Tuple, List, Union, Optional
from sklearn.neighbors import NearestNeighbors
from scipy.spatial import transform

import dgl
import dgl.function as fn
from dgl import DGLGraph

from .base import BaseModel

# =============================================================================
# Geometry Utilities
# =============================================================================

def deg2rad(deg: torch.Tensor) -> torch.Tensor:
    return deg * np.pi / 180


def rad2deg(rad: torch.Tensor) -> torch.Tensor:
    return rad * 180 / np.pi


def latlon2xyz(
    latlon: torch.Tensor, radius: float = 1, unit: str = "deg"
) -> torch.Tensor:
    """Convert lat/lon to 3D cartesian coordinates."""
    if unit == "deg":
        latlon = deg2rad(latlon)
    lat, lon = latlon[..., 0], latlon[..., 1]
    x = radius * torch.cos(lat) * torch.cos(lon)
    y = radius * torch.cos(lat) * torch.sin(lon)
    z = radius * torch.sin(lat)
    return torch.stack([x, y, z], dim=-1)


def xyz2latlon(xyz: torch.Tensor, radius: float = 1, unit: str = "deg") -> torch.Tensor:
    """Convert 3D cartesian to lat/lon coordinates."""
    lat = torch.arcsin(xyz[..., 2] / radius)
    lon = torch.arctan2(xyz[..., 1], xyz[..., 0])
    result = torch.stack([lat, lon], dim=-1)
    return rad2deg(result) if unit == "deg" else result


def geospatial_rotation(
    invar: torch.Tensor, theta: torch.Tensor, axis: str, unit: str = "rad"
) -> torch.Tensor:
    """Rotate coordinates around specified axis."""
    if unit == "deg":
        theta = deg2rad(theta)

    invar = rearrange(invar, "... d -> ... d 1")
    rotation = torch.zeros((*theta.shape, 3, 3), device=theta.device)
    cos, sin = torch.cos(theta), torch.sin(theta)

    if axis == "x":
        rotation[..., 0, 0] = 1.0
        rotation[..., 1, 1] = cos
        rotation[..., 1, 2] = -sin
        rotation[..., 2, 1] = sin
        rotation[..., 2, 2] = cos
    elif axis == "y":
        rotation[..., 0, 0] = cos
        rotation[..., 0, 2] = sin
        rotation[..., 1, 1] = 1.0
        rotation[..., 2, 0] = -sin
        rotation[..., 2, 2] = cos
    elif axis == "z":
        rotation[..., 0, 0] = cos
        rotation[..., 0, 1] = -sin
        rotation[..., 1, 0] = sin
        rotation[..., 1, 1] = cos
        rotation[..., 2, 2] = 1.0

    outvar = torch.matmul(rotation, invar)
    return rearrange(outvar, "... d 1 -> ... d")


# =============================================================================
# Mesh Generation
# =============================================================================

class TriangularMesh:
    def __init__(self, vertices: np.ndarray, faces: np.ndarray):
        self.vertices = vertices
        self.faces = faces


def get_icosahedron() -> TriangularMesh:
    """Generate icosahedron mesh."""
    phi = (1 + np.sqrt(5)) / 2
    vertices = []
    for c1 in [1.0, -1.0]:
        for c2 in [phi, -phi]:
            vertices.extend([(c1, c2, 0.0), (0.0, c1, c2), (c2, 0.0, c1)])

    vertices = np.array(vertices, dtype=np.float32)
    vertices /= np.linalg.norm([1.0, phi])

    faces = [
        (0, 1, 2), (0, 6, 1), (8, 0, 2), (8, 4, 0), (3, 8, 2),
        (3, 2, 7), (7, 2, 1), (0, 4, 6), (4, 11, 6), (6, 11, 5),
        (1, 5, 7), (4, 10, 11), (4, 8, 10), (10, 8, 3), (10, 3, 9),
        (11, 10, 9), (11, 9, 5), (5, 9, 7), (9, 3, 7), (1, 6, 5),
    ]

    # Rotation for proper alignment
    angle = 2 * np.arcsin(phi / np.sqrt(3))
    rotation_angle = (np.pi - angle) / 2
    rotation = transform.Rotation.from_euler(seq="y", angles=rotation_angle)
    vertices = vertices @ rotation.as_matrix().T

    return TriangularMesh(vertices.astype(np.float32), np.array(faces, dtype=np.int32))


def split_mesh(mesh: TriangularMesh) -> TriangularMesh:
    """Split each triangle into 4 smaller triangles."""
    vertex_cache = {}
    all_vertices = list(mesh.vertices)

    def get_midpoint(i1: int, i2: int) -> int:
        key = tuple(sorted([i1, i2]))
        if key not in vertex_cache:
            midpoint = (mesh.vertices[i1] + mesh.vertices[i2]) / 2
            midpoint /= np.linalg.norm(midpoint)
            vertex_cache[key] = len(all_vertices)
            all_vertices.append(midpoint)
        return vertex_cache[key]

    new_faces = []
    for i1, i2, i3 in mesh.faces:
        i12 = get_midpoint(i1, i2)
        i23 = get_midpoint(i2, i3)
        i31 = get_midpoint(i3, i1)
        new_faces.extend(
            [[i1, i12, i31], [i12, i2, i23], [i31, i23, i3], [i12, i23, i31]]
        )

    return TriangularMesh(
        np.array(all_vertices, dtype=np.float32), np.array(new_faces, dtype=np.int32)
    )


def get_mesh_hierarchy(splits: int) -> List[TriangularMesh]:
    """Generate hierarchy of meshes."""
    meshes = [get_icosahedron()]
    for _ in range(splits):
        meshes.append(split_mesh(meshes[-1]))
    return meshes


def merge_meshes(meshes: List[TriangularMesh]) -> TriangularMesh:
    """Merge multiple meshes into one."""
    return TriangularMesh(
        vertices=meshes[-1].vertices,
        faces=np.concatenate([m.faces for m in meshes], axis=0),
    )


def faces_to_edges(faces: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Convert face indices to edge indices."""
    src = np.concatenate([faces[:, i] for i in range(3)])
    dst = np.concatenate([faces[:, (i + 1) % 3] for i in range(3)])
    return src, dst


# =============================================================================
# Graph Construction
# =============================================================================

def create_graph(src: List, dst: List, bidirected: bool = True) -> DGLGraph:
    """Create DGL graph from edge lists."""
    graph = dgl.graph((src, dst), idtype=torch.int32)
    if bidirected:
        graph = dgl.to_bidirected(graph)
    return graph


def add_edge_features(
    graph: DGLGraph, src_pos: torch.Tensor, dst_pos: torch.Tensor
) -> DGLGraph:
    """Add edge features based on node positions."""
    src_idx, dst_idx = graph.edges()
    src_coords = src_pos[src_idx.long()]
    dst_coords = dst_pos[dst_idx.long()]

    # Convert to local coordinate system
    dst_latlon = xyz2latlon(dst_coords, unit="rad")
    theta_az = torch.where(
        dst_latlon[:, 1] >= 0, 2 * np.pi - dst_latlon[:, 1], -dst_latlon[:, 1]
    )
    theta_polar = torch.where(
        dst_latlon[:, 0] >= 0, dst_latlon[:, 0], 2 * np.pi + dst_latlon[:, 0]
    )

    src_rot = geospatial_rotation(src_coords, theta_az, "z", "rad")
    src_rot = geospatial_rotation(src_rot, theta_polar, "y", "rad")

    # Edge features: displacement + distance
    disp = src_rot - torch.tensor([1, 0, 0], device=src_rot.device)
    dist = torch.norm(disp, dim=-1, keepdim=True)
    max_dist = dist.max()

    graph.edata["x"] = torch.cat([disp / max_dist, dist / max_dist], dim=-1)
    return graph


# =============================================================================
# Graph Operations
# =============================================================================

def concat_efeat_dgl(
    efeat: torch.Tensor, src_feat: torch.Tensor, dst_feat: torch.Tensor, graph: DGLGraph
) -> torch.Tensor:
    """Concatenate edge and node features using manual indexing.
    
    This avoids device conflicts when graph is on CPU but features are on GPU.
    """
    # Get edge connections (on CPU)
    src, dst = graph.edges()
    
    # Move indices to feature device and index
    device = efeat.device
    src_indexed = src_feat[src.to(device)]  # [num_edges, src_dim]
    dst_indexed = dst_feat[dst.to(device)]  # [num_edges, dst_dim]
    
    # Concatenate edge features with source and destination node features
    return torch.cat([efeat, src_indexed, dst_indexed], dim=-1)


def aggregate_and_concat_dgl(
    efeat: torch.Tensor, dst_feat: torch.Tensor, graph: DGLGraph, agg: str = "sum"
) -> torch.Tensor:
    """Aggregate edge features to nodes and concatenate using manual indexing.
    
    This avoids device conflicts when graph is on CPU but features are on GPU.
    """
    # Get edge connections (on CPU)
    _, dst = graph.edges()
    
    # Move dst indices to feature device
    device = efeat.device
    dst_device = dst.to(device)
    
    # Aggregate edge features to destination nodes
    num_dst_nodes = dst_feat.shape[0]
    aggregated = torch.zeros(num_dst_nodes, efeat.shape[1], device=device, dtype=efeat.dtype)
    
    if agg == "sum":
        aggregated.index_add_(0, dst_device, efeat)
    else:  # mean
        aggregated.index_add_(0, dst_device, efeat)
        # Count edges per node for mean
        counts = torch.zeros(num_dst_nodes, device=device, dtype=torch.float32)
        counts.index_add_(0, dst_device, torch.ones_like(dst_device, dtype=torch.float32))
        aggregated = aggregated / counts.clamp(min=1).unsqueeze(-1)
    
    return torch.cat([aggregated, dst_feat], dim=-1)


# =============================================================================
# Neural Network Modules
# =============================================================================

class MLP(nn.Module):
    """Multi-layer perceptron with LayerNorm."""

    def __init__(self, in_dim: int, out_dim: int, hidden_dim: int, n_layers: int = 1):
        super().__init__()
        layers = [nn.Linear(in_dim, hidden_dim), nn.SiLU()]
        for _ in range(n_layers - 1):
            layers.extend([nn.Linear(hidden_dim, hidden_dim), nn.SiLU()])
        layers.extend([nn.Linear(hidden_dim, out_dim), nn.LayerNorm(out_dim)])
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class EdgeMLP(nn.Module):
    """MLP for edge updates with node feature concatenation."""

    def __init__(
        self,
        edge_dim: int,
        node_dim: int,
        out_dim: int,
        hidden_dim: int,
        n_layers: int = 1,
    ):
        super().__init__()
        self.mlp = MLP(edge_dim + 2 * node_dim, out_dim, hidden_dim, n_layers)

    def forward(
        self,
        efeat: torch.Tensor,
        src_feat: torch.Tensor,
        dst_feat: torch.Tensor,
        graph: DGLGraph,
    ) -> torch.Tensor:
        cat_feat = concat_efeat_dgl(efeat, src_feat, dst_feat, graph)
        return self.mlp(cat_feat)


class Encoder(nn.Module):
    """Grid to mesh encoder."""

    def __init__(self, hidden_dim: int, n_layers: int, agg: str = "sum"):
        super().__init__()
        self.edge_mlp = EdgeMLP(
            hidden_dim, hidden_dim, hidden_dim, hidden_dim, n_layers
        )
        self.src_mlp = MLP(hidden_dim, hidden_dim, hidden_dim, n_layers)
        self.dst_mlp = MLP(hidden_dim + hidden_dim, hidden_dim, hidden_dim, n_layers)
        self.agg = agg

    def forward(
        self,
        g2m_efeat: torch.Tensor,
        grid_feat: torch.Tensor,
        mesh_feat: torch.Tensor,
        graph: DGLGraph,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        efeat = self.edge_mlp(g2m_efeat, grid_feat, mesh_feat, graph)
        agg_feat = aggregate_and_concat_dgl(efeat, mesh_feat, graph, self.agg)
        mesh_feat_new = mesh_feat + self.dst_mlp(agg_feat)
        grid_feat_new = grid_feat + self.src_mlp(grid_feat)
        return grid_feat_new, mesh_feat_new


class Decoder(nn.Module):
    """Mesh to grid decoder."""

    def __init__(self, hidden_dim: int, n_layers: int, agg: str = "sum"):
        super().__init__()
        self.edge_mlp = EdgeMLP(
            hidden_dim, hidden_dim, hidden_dim, hidden_dim, n_layers
        )
        self.node_mlp = MLP(hidden_dim + hidden_dim, hidden_dim, hidden_dim, n_layers)
        self.agg = agg

    def forward(
        self,
        m2g_efeat: torch.Tensor,
        grid_feat: torch.Tensor,
        mesh_feat: torch.Tensor,
        graph: DGLGraph,
    ) -> torch.Tensor:
        efeat = self.edge_mlp(m2g_efeat, mesh_feat, grid_feat, graph)
        agg_feat = aggregate_and_concat_dgl(efeat, grid_feat, graph, self.agg)
        return grid_feat + self.node_mlp(agg_feat)


class ProcessorLayer(nn.Module):
    """Single processor layer for mesh."""

    def __init__(self, hidden_dim: int, n_layers: int, agg: str = "sum"):
        super().__init__()
        self.edge_mlp = EdgeMLP(
            hidden_dim, hidden_dim, hidden_dim, hidden_dim, n_layers
        )
        self.node_mlp = MLP(hidden_dim + hidden_dim, hidden_dim, hidden_dim, n_layers)
        self.agg = agg

    def forward(
        self, efeat: torch.Tensor, nfeat: torch.Tensor, graph: DGLGraph
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        efeat_new = efeat + self.edge_mlp(efeat, nfeat, nfeat, graph)
        agg_feat = aggregate_and_concat_dgl(efeat_new, nfeat, graph, self.agg)
        nfeat_new = nfeat + self.node_mlp(agg_feat)
        return efeat_new, nfeat_new


class Processor(nn.Module):
    """Mesh graph processor with multiple layers."""

    def __init__(
        self, hidden_dim: int, n_layers: int, mlp_layers: int, agg: str = "sum"
    ):
        super().__init__()
        self.layers = nn.ModuleList(
            [ProcessorLayer(hidden_dim, mlp_layers, agg) for _ in range(n_layers)]
        )

    def forward(
        self, efeat: torch.Tensor, nfeat: torch.Tensor, graph: DGLGraph
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        for layer in self.layers:
            efeat, nfeat = layer(efeat, nfeat, graph)
        return efeat, nfeat


# =============================================================================
# Graph Builder
# =============================================================================

class GraphBuilder:
    """Build graphs for GraphCast."""

    def __init__(
        self, lat_lon_grid: torch.Tensor, mesh_level: int = 5, multimesh: bool = True
    ):
        self.lat_lon_flat = rearrange(lat_lon_grid, "h w c -> (h w) c")

        # Build mesh hierarchy
        meshes = get_mesh_hierarchy(mesh_level)
        finest = meshes[-1]
        mesh = merge_meshes(meshes) if multimesh else finest

        self.mesh_vertices = torch.from_numpy(mesh.vertices).float()
        mesh_src, mesh_dst = faces_to_edges(mesh.faces)

        # Create mesh graph
        self.mesh_graph = create_graph(mesh_src, mesh_dst)
        self.mesh_graph = add_edge_features(
            self.mesh_graph, self.mesh_vertices, self.mesh_vertices
        )
        self.mesh_graph.ndata["pos"] = self.mesh_vertices

        # Create g2m graph (grid to mesh)
        grid_xyz = latlon2xyz(self.lat_lon_flat)
        max_edge_len = self._get_max_edge_len(finest)
        self.g2m_graph = self._create_bipartite_graph(
            grid_xyz, self.mesh_vertices, max_edge_len * 0.6, is_g2m=True
        )

        # Create m2g graph (mesh to grid)
        centroids = self._get_centroids(mesh)
        self.m2g_graph = self._create_m2g_graph(grid_xyz, centroids, mesh.faces)

    def _get_max_edge_len(self, mesh: TriangularMesh) -> float:
        src, dst = faces_to_edges(mesh.faces)
        diffs = mesh.vertices[src] - mesh.vertices[dst]
        return np.sqrt(np.max(np.sum(diffs**2, axis=1)))

    def _get_centroids(self, mesh: TriangularMesh) -> np.ndarray:
        return np.mean(mesh.vertices[mesh.faces], axis=1)

    def _create_bipartite_graph(
        self,
        src_pos: torch.Tensor,
        dst_pos: Union[np.ndarray, torch.Tensor],
        max_dist: float,
        is_g2m: bool,
    ) -> DGLGraph:
        # Convert to numpy for sklearn if needed
        dst_pos_np = (
            dst_pos.cpu().numpy() if isinstance(dst_pos, torch.Tensor) else dst_pos
        )

        nbrs = NearestNeighbors(n_neighbors=4).fit(dst_pos_np)
        distances, indices = nbrs.kneighbors(src_pos.cpu().numpy())

        src_idx, dst_idx = [], []
        for i in range(len(src_pos)):
            for j in range(4):
                if distances[i][j] <= max_dist:
                    src_idx.append(i)
                    dst_idx.append(indices[i][j])

        graph = dgl.heterograph(
            {("src", "edge", "dst"): (src_idx, dst_idx)}, idtype=torch.int32
        )
        graph.srcdata["pos"] = src_pos.float()

        # Handle both tensor and numpy array
        if isinstance(dst_pos, torch.Tensor):
            graph.dstdata["pos"] = dst_pos.float()
        else:
            graph.dstdata["pos"] = torch.from_numpy(dst_pos).float()

        graph = add_edge_features(graph, graph.srcdata["pos"], graph.dstdata["pos"])
        return graph

    def _create_m2g_graph(
        self, grid_xyz: torch.Tensor, centroids: np.ndarray, faces: np.ndarray
    ) -> DGLGraph:
        nbrs = NearestNeighbors(n_neighbors=1).fit(centroids)
        _, indices = nbrs.kneighbors(grid_xyz.cpu().numpy())
        indices = indices.flatten()

        src_idx = [p for i in indices for p in faces[i]]
        dst_idx = [i for i in range(len(grid_xyz)) for _ in range(3)]

        graph = dgl.heterograph(
            {("src", "edge", "dst"): (src_idx, dst_idx)}, idtype=torch.int32
        )
        graph.srcdata["pos"] = self.mesh_vertices
        graph.dstdata["pos"] = grid_xyz.float()
        graph = add_edge_features(graph, graph.srcdata["pos"], graph.dstdata["pos"])
        return graph


# =============================================================================
# Main GraphCast Model for Ocean Velocity Prediction
# =============================================================================

class GraphCast(BaseModel):
    """
    GraphCast model adapted for ocean velocity prediction.

    Key adaptations:
    1. Handles 2D ocean velocity data (u, v components)
    2. Supports multi-frame input and output for video prediction
    3. Adds pseudo-3D processing capability
    4. Optimized for 240x240 spatial resolution
    """

    def __init__(self, args):
        super(BaseModel, self).__init__()

        # Temporal configuration
        self.input_len = args.get('input_len', 7)
        self.output_len = args.get('output_len', 1)
        self.in_channels = args.get('in_channels', 2)  # u, v velocity components

        # Spatial configuration
        input_res = args.get('input_res', [240, 240])
        self.input_res = tuple(input_res) if isinstance(input_res, list) else input_res

        # Model architecture parameters
        self.hidden_dim = args.get('hidden_dim', 128)
        self.mesh_level = args.get('mesh_level', 4)  # Reduced for 240x240 resolution
        self.processor_layers = args.get('processor_layers', 8)
        self.mlp_layers = args.get('mlp_layers', 1)
        self.multimesh = args.get('multimesh', True)
        self.aggregation = args.get('aggregation', 'sum')

        # Processing options
        self.add_3d_dim = args.get('add_3d_dim', True)  # Process 2D as pseudo-3D
        self.temporal_encoding = args.get('temporal_encoding', 'concat')  # 'concat' or 'rnn'

        # Build graphs
        lat = torch.linspace(-90, 90, self.input_res[0])
        lon = torch.linspace(-180, 180, self.input_res[1] + 1)[1:]
        lat_lon_grid = torch.stack(torch.meshgrid(lat, lon, indexing="ij"), dim=-1)

        self.graph_builder = GraphBuilder(lat_lon_grid, self.mesh_level, self.multimesh)

        # Calculate input dimensions based on temporal encoding
        if self.temporal_encoding == 'concat':
            # Concatenate all input frames
            grid_input_dim = self.input_len * self.in_channels
            if self.add_3d_dim:
                # Add pseudo depth channels (replicate 2D data)
                grid_input_dim *= 2  # Process as both surface and pseudo-depth
        else:
            # RNN-based temporal encoding
            # Note: After RNN encoding, the output dimension is hidden_dim, not in_channels
            grid_input_dim = self.hidden_dim
            self.temporal_encoder = nn.GRU(
                input_size=self.in_channels,
                hidden_size=self.hidden_dim,
                num_layers=2,
                batch_first=True
            )

        # Feature embedders
        self.grid_embed = MLP(grid_input_dim, self.hidden_dim, self.hidden_dim, self.mlp_layers)
        self.mesh_node_embed = MLP(3, self.hidden_dim, self.hidden_dim, self.mlp_layers)  # xyz coords
        self.g2m_edge_embed = MLP(4, self.hidden_dim, self.hidden_dim, self.mlp_layers)
        self.mesh_edge_embed = MLP(4, self.hidden_dim, self.hidden_dim, self.mlp_layers)
        self.m2g_edge_embed = MLP(4, self.hidden_dim, self.hidden_dim, self.mlp_layers)

        # Encoder, processor, decoder
        self.encoder = Encoder(self.hidden_dim, self.mlp_layers, self.aggregation)
        self.processor = Processor(
            self.hidden_dim, self.processor_layers, self.mlp_layers, self.aggregation
        )
        self.decoder = Decoder(self.hidden_dim, self.mlp_layers, self.aggregation)

        # Output head for multi-frame prediction
        output_channels = self.output_len * self.in_channels
        self.output_head = nn.Sequential(
            MLP(self.hidden_dim, self.hidden_dim, self.hidden_dim, self.mlp_layers),
            nn.Linear(self.hidden_dim, output_channels),
        )

        # Cache graph features
        self.register_buffer("mesh_pos", self.graph_builder.mesh_vertices)
        self.register_buffer("g2m_efeat", self.graph_builder.g2m_graph.edata["x"])
        self.register_buffer("mesh_efeat", self.graph_builder.mesh_graph.edata["x"])
        self.register_buffer("m2g_efeat", self.graph_builder.m2g_graph.edata["x"])

    def prepare_input(self, x: torch.Tensor) -> torch.Tensor:
        """
        Prepare input for processing.

        Args:
            x: [B, T, C, H, W] input tensor
        Returns:
            [B, C_concat, H, W] or [B, H*W, C_encoded] depending on temporal encoding
        """
        B, T, C, H, W = x.shape

        if self.temporal_encoding == 'concat':
            # Concatenate temporal frames
            x = rearrange(x, 'b t c h w -> b (t c) h w')

            if self.add_3d_dim:
                # Create pseudo-3D by duplicating data
                # This simulates having both surface and depth information
                x_surface = x
                x_depth = x * 0.9  # Slightly attenuated for depth simulation
                x = torch.cat([x_surface, x_depth], dim=1)

            return x
        else:
            # RNN-based temporal encoding
            x = rearrange(x, 'b t c h w -> (b h w) t c')
            _, hidden = self.temporal_encoder(x)
            # Use final hidden state
            x_encoded = hidden[-1]  # [(B*H*W), hidden_dim]
            return rearrange(x_encoded, '(b h w) d -> b (h w) d', b=B, h=H, w=W)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through GraphCast.

        Args:
            x: [B, T_in, C, H, W] input features
        Returns:
            [B, T_out, C, H, W] output predictions
        """
        B, T_in, C, H, W = x.shape
        device = x.device

        # Keep graphs on CPU to avoid DGL CUDA issues
        # DGL will automatically handle feature transfer between CPU graph and GPU tensors
        g2m_graph = self.graph_builder.g2m_graph
        mesh_graph = self.graph_builder.mesh_graph
        m2g_graph = self.graph_builder.m2g_graph

        # Handle batch processing
        outputs = []
        for b in range(B):
            x_single = x[b:b+1]  # Keep batch dimension

            # Prepare input
            x_processed = self.prepare_input(x_single)

            if self.temporal_encoding == 'concat':
                # Reshape: [1, C_concat, H, W] -> [N, C_concat]
                grid_feat = rearrange(x_processed, '1 c h w -> (h w) c')
            else:
                # Already in [1, N, C] format
                grid_feat = x_processed[0]  # Remove batch dim

            # Ensure features are on correct device
            mesh_pos = self.mesh_pos.to(device)
            g2m_efeat = self.g2m_efeat.to(device)
            mesh_efeat = self.mesh_efeat.to(device)
            m2g_efeat = self.m2g_efeat.to(device)

            # Embed features
            grid_feat = self.grid_embed(grid_feat)
            mesh_node_feat = self.mesh_node_embed(mesh_pos)
            g2m_efeat_embed = self.g2m_edge_embed(g2m_efeat)
            mesh_efeat_embed = self.mesh_edge_embed(mesh_efeat)
            m2g_efeat_embed = self.m2g_edge_embed(m2g_efeat)

            # Encode: grid -> mesh (use device-local graph)
            grid_feat, mesh_node_feat = self.encoder(
                g2m_efeat_embed, grid_feat, mesh_node_feat, g2m_graph
            )

            # Process on mesh (use device-local graph)
            mesh_efeat_embed, mesh_node_feat = self.processor(
                mesh_efeat_embed, mesh_node_feat, mesh_graph
            )

            # Decode: mesh -> grid (use device-local graph)
            grid_feat = self.decoder(
                m2g_efeat_embed, grid_feat, mesh_node_feat, m2g_graph
            )

            # Output
            output = self.output_head(grid_feat)

            # Reshape: [N, C_out] -> [1, T_out, C, H, W]
            output = rearrange(
                output,
                '(h w) (t c) -> 1 t c h w',
                h=H, w=W, t=self.output_len, c=self.in_channels
            )

            outputs.append(output)

        # Concatenate batch
        return torch.cat(outputs, dim=0)

    def to(self, *args, **kwargs):
        """Override to() to move parameters to target device.
        
        Note: We keep graph structures on CPU to avoid DGL CUDA compatibility issues.
        Graph node/edge features are registered as buffers and will be moved automatically.
        DGL handles feature transfer between CPU graphs and GPU tensors efficiently.
        """
        # Call parent to() - moves all parameters and registered buffers
        # This includes mesh_pos, g2m_efeat, mesh_efeat, m2g_efeat
        self = super().to(*args, **kwargs)
        
        # Note: Graphs (mesh_graph, g2m_graph, m2g_graph) remain on CPU
        # This avoids DGL CUDA transfer crashes and is more efficient for static graphs
        
        return self


# =============================================================================
# Autoregressive GraphCast for Long-term Prediction
# =============================================================================

class GraphCastAutoregressive(GraphCast):
    """
    Autoregressive version of GraphCast for long-term prediction.
    Uses single-frame prediction and rolls out for multiple steps.
    """

    def __init__(self, args):
        # Force single frame output for autoregressive mode
        args_auto = dict(args)
        args_auto['output_len'] = 1
        super().__init__(args_auto)

        self.rollout_steps = args.get('rollout_steps', 1)

    def forward(self, x: torch.Tensor, rollout_steps: Optional[int] = None) -> torch.Tensor:
        """
        Autoregressive forward pass.

        Args:
            x: [B, T_in, C, H, W] input features
            rollout_steps: Number of autoregressive steps (default: self.rollout_steps)
        Returns:
            [B, rollout_steps, C, H, W] output predictions
        """
        if rollout_steps is None:
            rollout_steps = self.rollout_steps

        B, T_in, C, H, W = x.shape
        predictions = []

        current_input = x

        for step in range(rollout_steps):
            # Predict next frame
            next_frame = super().forward(current_input)  # [B, 1, C, H, W]
            predictions.append(next_frame)

            # Update input: slide window and add prediction
            if T_in > 1:
                current_input = torch.cat([
                    current_input[:, 1:],  # Remove oldest frame
                    next_frame  # Add new prediction
                ], dim=1)
            else:
                current_input = next_frame

        # Concatenate all predictions
        return torch.cat(predictions, dim=1)


# =============================================================================
# Test
# =============================================================================

# if __name__ == "__main__":
#     import yaml

#     device = "cuda" if torch.cuda.is_available() else "cpu"

#     # Test configuration matching your project
#     test_args = {
#         'input_len': 7,
#         'output_len': 1,
#         'in_channels': 2,
#         'input_res': [240, 240],
#         'hidden_dim': 64,  # Reduced for testing
#         'mesh_level': 3,   # Reduced for testing
#         'processor_layers': 4,
#         'mlp_layers': 1,
#         'multimesh': True,
#         'aggregation': 'sum',
#         'add_3d_dim': True,
#         'temporal_encoding': 'concat'
#     }

#     print("Testing GraphCast model...")
#     print(f"Device: {device}")

#     # Test standard model
#     model = GraphCast(test_args).to(device)
#     x = torch.randn(2, 7, 2, 240, 240).to(device)  # Batch of 2

#     print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
#     print(f"Input shape: {x.shape}")

#     # Forward pass
#     y = model(x)
#     print(f"Output shape: {y.shape}")
#     print(f"Expected shape: [2, 1, 2, 240, 240]")
#     assert y.shape == (2, 1, 2, 240, 240), f"Output shape mismatch!"

#     # Test autoregressive model
#     print("\nTesting Autoregressive GraphCast...")
#     test_args['rollout_steps'] = 3
#     model_auto = GraphCastAutoregressive(test_args).to(device)

#     y_auto = model_auto(x, rollout_steps=3)
#     print(f"Autoregressive output shape: {y_auto.shape}")
#     print(f"Expected shape: [2, 3, 2, 240, 240]")
#     assert y_auto.shape == (2, 3, 2, 240, 240), f"Autoregressive output shape mismatch!"

#     # Memory usage
#     if torch.cuda.is_available():
#         print(f"\nGPU memory: {torch.cuda.max_memory_allocated() / 1024**3:.2f} GB")

#     print("\nAll tests passed!")