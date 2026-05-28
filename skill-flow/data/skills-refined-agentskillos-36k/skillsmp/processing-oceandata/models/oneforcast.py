"""OneForecast Model - DataParallel Compatible Version"""

import torch
import torch.nn as nn
import dgl
import dgl.function as fn
import numpy as np
from typing import Tuple, List, Optional
from einops import rearrange
from sklearn.neighbors import NearestNeighbors
from scipy.spatial import transform
from .base import BaseModel
import copy


# ============================================================================
# Core Graph Utilities (same as before)
# ============================================================================

def create_graph(src, dst, to_bidirected=True, dtype=torch.int32):
    """Create DGL graph from source and destination nodes."""
    graph = dgl.graph((src, dst), idtype=dtype)
    if to_bidirected:
        graph = dgl.to_bidirected(graph)
    return graph


def create_heterograph(src, dst, labels, dtype=torch.int32, num_nodes_dict=None):
    """Create heterogeneous DGL graph."""
    return dgl.heterograph(
        {labels: ("coo", (src, dst))}, num_nodes_dict=num_nodes_dict, idtype=dtype
    )


def latlon2xyz(latlon: torch.Tensor, radius=1.0, unit="deg") -> torch.Tensor:
    """Convert lat/lon to 3D Cartesian coordinates."""
    if unit == "deg":
        latlon = latlon * np.pi / 180
    lat, lon = latlon[:, 0], latlon[:, 1]
    x = radius * torch.cos(lat) * torch.cos(lon)
    y = radius * torch.cos(lat) * torch.sin(lon)
    z = radius * torch.sin(lat)
    return torch.stack([x, y, z], dim=1)


def xyz2latlon(xyz: torch.Tensor, radius=1.0, unit="deg") -> torch.Tensor:
    """Convert 3D Cartesian coordinates to lat/lon."""
    lat = torch.arcsin(xyz[:, 2] / radius)
    lon = torch.arctan2(xyz[:, 1], xyz[:, 0])
    if unit == "deg":
        return torch.stack([lat * 180 / np.pi, lon * 180 / np.pi], dim=1)
    return torch.stack([lat, lon], dim=1)


def geospatial_rotation(
    invar: torch.Tensor, theta: torch.Tensor, axis: str, unit="rad"
) -> torch.Tensor:
    """Apply rotation to geospatial coordinates."""
    if unit == "deg":
        theta = theta * np.pi / 180

    invar = invar.unsqueeze(-1)
    rotation = torch.zeros((theta.size(0), 3, 3), device=invar.device)
    cos, sin = torch.cos(theta), torch.sin(theta)

    if axis == "x":
        rotation[:, 0, 0] = 1.0
        rotation[:, 1, 1] = cos
        rotation[:, 1, 2] = -sin
        rotation[:, 2, 1] = sin
        rotation[:, 2, 2] = cos
    elif axis == "y":
        rotation[:, 0, 0] = cos
        rotation[:, 0, 2] = sin
        rotation[:, 1, 1] = 1.0
        rotation[:, 2, 0] = -sin
        rotation[:, 2, 2] = cos
    elif axis == "z":
        rotation[:, 0, 0] = cos
        rotation[:, 0, 1] = -sin
        rotation[:, 1, 0] = sin
        rotation[:, 1, 1] = cos
        rotation[:, 2, 2] = 1.0

    return torch.matmul(rotation, invar).squeeze(-1)


def add_edge_features(graph, pos, normalize=True):
    """Add edge features to graph based on node positions."""
    if isinstance(pos, tuple):
        src_pos, dst_pos = pos
    else:
        src_pos = dst_pos = pos

    src, dst = graph.edges()
    src_pos, dst_pos = src_pos[src.long()], dst_pos[dst.long()]

    # Convert to local coordinate system
    dst_latlon = xyz2latlon(dst_pos, unit="rad")
    dst_lat, dst_lon = dst_latlon[:, 0], dst_latlon[:, 1]

    theta_azimuthal = torch.where(dst_lon >= 0, 2 * np.pi - dst_lon, -dst_lon)
    theta_polar = torch.where(dst_lat >= 0, dst_lat, 2 * np.pi + dst_lat)

    src_pos = geospatial_rotation(src_pos, theta_azimuthal, "z", "rad")
    dst_pos = geospatial_rotation(dst_pos, theta_azimuthal, "z", "rad")
    src_pos = geospatial_rotation(src_pos, theta_polar, "y", "rad")
    dst_pos = geospatial_rotation(dst_pos, theta_polar, "y", "rad")

    disp = src_pos - dst_pos
    disp_norm = torch.linalg.norm(disp, dim=-1, keepdim=True)

    if normalize:
        max_norm = disp_norm.max()
        graph.edata["x"] = torch.cat([disp / max_norm, disp_norm / max_norm], dim=-1)
    else:
        graph.edata["x"] = torch.cat([disp, disp_norm], dim=-1)

    return graph


def add_node_features(graph, pos):
    """Add node features based on positions."""
    latlon = xyz2latlon(pos)
    lat, lon = latlon[:, 0], latlon[:, 1]
    graph.ndata["x"] = torch.stack(
        [torch.cos(lat), torch.sin(lon), torch.cos(lon)], dim=-1
    )
    return graph


def faces_to_edges(faces: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Convert faces to edges."""
    senders = np.concatenate([faces[:, 0], faces[:, 1], faces[:, 2]])
    receivers = np.concatenate([faces[:, 1], faces[:, 2], faces[:, 0]])
    return senders, receivers


# ============================================================================
# Simplified Mesh Generation
# ============================================================================

class TriangularMesh:
    def __init__(self, vertices: np.ndarray, faces: np.ndarray):
        self.vertices = vertices
        self.faces = faces


def get_icosahedron() -> TriangularMesh:
    """Create icosahedron mesh."""
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

    angle = 2 * np.arcsin(phi / np.sqrt(3))
    rotation = transform.Rotation.from_euler("y", (np.pi - angle) / 2)
    vertices = rotation.apply(vertices)

    return TriangularMesh(vertices.astype(np.float32), np.array(faces, dtype=np.int32))


def split_triangle_mesh(mesh: TriangularMesh) -> TriangularMesh:
    """Subdivide triangular mesh."""
    vertices_list = list(mesh.vertices)
    child_map = {}

    def get_child_vertex(i1, i2):
        key = tuple(sorted([i1, i2]))
        if key not in child_map:
            pos = (mesh.vertices[i1] + mesh.vertices[i2]) / 2
            pos /= np.linalg.norm(pos)
            child_map[key] = len(vertices_list)
            vertices_list.append(pos)
        return child_map[key]

    new_faces = []
    for i1, i2, i3 in mesh.faces:
        i12 = get_child_vertex(i1, i2)
        i23 = get_child_vertex(i2, i3)
        i31 = get_child_vertex(i3, i1)
        new_faces.extend(
            [[i1, i12, i31], [i12, i2, i23], [i31, i23, i3], [i12, i23, i31]]
        )

    return TriangularMesh(
        np.array(vertices_list, dtype=np.float32), np.array(new_faces, dtype=np.int32)
    )


def get_mesh_hierarchy(splits: int) -> List[TriangularMesh]:
    """Generate mesh hierarchy by subdivision."""
    meshes = [get_icosahedron()]
    for _ in range(splits):
        meshes.append(split_triangle_mesh(meshes[-1]))
    return meshes


def merge_meshes(meshes: List[TriangularMesh]) -> TriangularMesh:
    """Merge multiple meshes into one."""
    return TriangularMesh(
        vertices=meshes[-1].vertices,
        faces=np.concatenate([m.faces for m in meshes], axis=0),
    )


# ============================================================================
# Neural Network Components
# ============================================================================

class MLP(nn.Module):
    """Simple MLP with optional normalization."""

    def __init__(self, in_dim, out_dim, hidden_dim, num_layers=1, norm=True):
        super().__init__()
        layers = []

        for i in range(num_layers):
            layers.extend(
                [nn.Linear(in_dim if i == 0 else hidden_dim, hidden_dim), nn.SiLU()]
            )

        layers.append(nn.Linear(hidden_dim, out_dim))
        if norm:
            layers.append(nn.LayerNorm(out_dim))

        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)


class EdgeMLP(nn.Module):
    """MLP for edge feature updates using concatenation - DataParallel compatible."""

    def __init__(self, efeat_dim, nfeat_dim, out_dim, hidden_dim, num_layers=1):
        super().__init__()
        self.mlp = MLP(efeat_dim + 2 * nfeat_dim, out_dim, hidden_dim, num_layers)

    def forward(self, efeat, nfeat, src_idx, dst_idx):
        """
        Modified forward to accept indices directly instead of graph.
        This ensures indices are on the same device as features.
        """
        # Handle both single tensor and tuple of tensors
        if isinstance(nfeat, tuple):
            src_feat, dst_feat = nfeat
            cat_feat = torch.cat([efeat, src_feat[src_idx], dst_feat[dst_idx]], dim=-1)
        else:
            cat_feat = torch.cat([efeat, nfeat[src_idx], nfeat[dst_idx]], dim=-1)

        return self.mlp(cat_feat)


class GraphEncoder(nn.Module):
    """Encode grid to mesh - DataParallel compatible."""

    def __init__(self, hidden_dim, num_layers=1):
        super().__init__()
        self.edge_mlp = EdgeMLP(
            hidden_dim, hidden_dim, hidden_dim, hidden_dim, num_layers
        )
        self.dst_mlp = MLP(hidden_dim * 2, hidden_dim, hidden_dim, num_layers)
        self.src_mlp = MLP(hidden_dim, hidden_dim, hidden_dim, num_layers)

    def forward(self, efeat, src_feat, dst_feat, src_idx, dst_idx, num_dst_nodes):
        """Modified to work without graph object."""
        # Update edges
        efeat_new = self.edge_mlp(efeat, (src_feat, dst_feat), src_idx, dst_idx)

        # Manual aggregation without DGL
        agg_feat = torch.zeros(num_dst_nodes, efeat_new.shape[1],
                              dtype=efeat_new.dtype, device=efeat_new.device)
        agg_feat.index_add_(0, dst_idx, efeat_new)

        # Update nodes
        dst_feat_new = dst_feat + self.dst_mlp(torch.cat([agg_feat, dst_feat], dim=-1))
        src_feat_new = src_feat + self.src_mlp(src_feat)

        return src_feat_new, dst_feat_new


class GraphDecoder(nn.Module):
    """Decode mesh to grid - DataParallel compatible."""

    def __init__(self, hidden_dim, num_layers=1):
        super().__init__()
        self.edge_mlp = EdgeMLP(
            hidden_dim, hidden_dim, hidden_dim, hidden_dim, num_layers
        )
        self.node_mlp = MLP(hidden_dim * 2, hidden_dim, hidden_dim, num_layers)

    def forward(self, efeat, src_feat, dst_feat, src_idx, dst_idx, num_dst_nodes):
        """Modified to work without graph object."""
        # Update edges
        efeat_new = self.edge_mlp(efeat, (src_feat, dst_feat), src_idx, dst_idx)

        # Manual aggregation
        agg_feat = torch.zeros(num_dst_nodes, efeat_new.shape[1],
                              dtype=efeat_new.dtype, device=efeat_new.device)
        agg_feat.index_add_(0, dst_idx, efeat_new)

        # Update dst nodes
        return dst_feat + self.node_mlp(torch.cat([agg_feat, dst_feat], dim=-1))


class MeshProcessor(nn.Module):
    """Process mesh features - DataParallel compatible."""

    def __init__(self, hidden_dim, num_layers=16):
        super().__init__()
        self.layers = nn.ModuleList(
            [
                nn.ModuleDict(
                    {
                        "edge": EdgeMLP(
                            hidden_dim, hidden_dim, hidden_dim, hidden_dim, 1
                        ),
                        "node": MLP(hidden_dim * 2, hidden_dim, hidden_dim, 1),
                    }
                )
                for _ in range(num_layers)
            ]
        )

    def forward(self, efeat, nfeat, src_idx, dst_idx, num_nodes):
        """Modified to work without graph object."""
        for layer in self.layers:
            # Update edges
            efeat = efeat + layer["edge"](efeat, nfeat, src_idx, dst_idx)

            # Manual aggregation
            agg = torch.zeros(num_nodes, efeat.shape[1],
                            dtype=efeat.dtype, device=efeat.device)
            agg.index_add_(0, dst_idx, efeat)

            # Update nodes
            nfeat = nfeat + layer["node"](torch.cat([agg, nfeat], dim=-1))

        return efeat, nfeat


# ============================================================================
# Main Model - DataParallel Compatible
# ============================================================================

class OneForecast(BaseModel):
    """
    OneForecast adapted for DataParallel training.
    Key changes:
    - Graph operations are replaced with index-based operations
    - Each forward pass creates its own graph copy on the correct device
    - No shared state between GPU replicas
    """

    def __init__(self, args):
        super(BaseModel, self).__init__()

        # Temporal configuration
        self.input_len = args.get('input_len', 7)
        self.output_len = args.get('output_len', 1)
        self.in_channels = args.get('in_channels', 2)

        # Spatial configuration
        self.input_res = tuple(args.get('input_res', [240, 240]))

        # Model architecture
        self.hidden_dim = args.get('hidden_dim', 256)
        self.num_layers = args.get('num_layers', 1)
        self.processor_layers = args.get('processor_layers', 8)
        self.mesh_level = args.get('mesh_level', 4)
        self.multimesh = args.get('multimesh', False)

        # Build graph structure (CPU only, will be copied to device as needed)
        self._build_graph_structure()

        # Input projection
        input_dim = self.input_len * self.in_channels
        self.input_projection = nn.Sequential(
            nn.Linear(input_dim, self.hidden_dim),
            nn.LayerNorm(self.hidden_dim),
            nn.ReLU(inplace=True)
        )

        # Embedders
        self.grid_embedder = MLP(self.hidden_dim, self.hidden_dim, self.hidden_dim, self.num_layers)
        self.mesh_node_embedder = MLP(3, self.hidden_dim, self.hidden_dim, self.num_layers)
        self.mesh_edge_embedder = MLP(4, self.hidden_dim, self.hidden_dim, self.num_layers)
        self.g2m_edge_embedder = MLP(4, self.hidden_dim, self.hidden_dim, self.num_layers)
        self.m2g_edge_embedder = MLP(4, self.hidden_dim, self.hidden_dim, self.num_layers)

        # Core components (DataParallel compatible)
        self.encoder = GraphEncoder(self.hidden_dim, self.num_layers)
        self.processor = MeshProcessor(self.hidden_dim, self.processor_layers)
        self.decoder = GraphDecoder(self.hidden_dim, self.num_layers)

        # Output head
        output_dim = self.output_len * self.in_channels
        self.output_head = nn.Sequential(
            nn.Linear(self.hidden_dim, self.hidden_dim),
            nn.LayerNorm(self.hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(self.hidden_dim, output_dim)
        )

    def _build_graph_structure(self):
        """Build graph structure on CPU."""
        H, W = self.input_res
        lat = torch.linspace(-90, 90, H + 1)[:-1]
        lon = torch.linspace(-180, 180, W + 1)[1:]
        lat_lon_grid = torch.stack(torch.meshgrid(lat, lon, indexing="ij"), dim=-1)
        lat_lon_grid = rearrange(lat_lon_grid, "h w c -> (h w) c")

        # Build mesh
        meshes = get_mesh_hierarchy(self.mesh_level)
        mesh = merge_meshes(meshes) if self.multimesh else meshes[-1]

        self.mesh_vertices = mesh.vertices
        self.mesh_faces = mesh.faces

        # Get mesh edges
        mesh_src, mesh_dst = faces_to_edges(mesh.faces)
        self.register_buffer("mesh_src_idx", torch.from_numpy(mesh_src).long())
        self.register_buffer("mesh_dst_idx", torch.from_numpy(mesh_dst).long())
        self.num_mesh_nodes = len(self.mesh_vertices)

        # Store mesh positions
        mesh_pos = torch.from_numpy(self.mesh_vertices).float()
        self.register_buffer("mesh_pos", mesh_pos)

        # Create mesh edge features
        mesh_graph = create_graph(mesh_src, mesh_dst)
        mesh_graph = add_edge_features(mesh_graph, mesh_pos)
        mesh_graph = add_node_features(mesh_graph, mesh_pos)
        self.register_buffer("mesh_nfeat_static", mesh_graph.ndata["x"])
        self.register_buffer("mesh_efeat_static", mesh_graph.edata["x"])

        # Build g2m connections
        grid_xyz = latlon2xyz(lat_lon_grid)
        nbrs = NearestNeighbors(n_neighbors=4).fit(self.mesh_vertices)
        distances, indices = nbrs.kneighbors(grid_xyz.numpy())

        finest_mesh = meshes[-1]
        max_dist = self._max_edge_length(finest_mesh)

        g2m_src, g2m_dst = [], []
        for i in range(len(grid_xyz)):
            for j in range(4):
                if distances[i][j] <= 0.6 * max_dist:
                    g2m_src.append(i)
                    g2m_dst.append(indices[i][j])

        self.register_buffer("g2m_src_idx", torch.tensor(g2m_src, dtype=torch.long))
        self.register_buffer("g2m_dst_idx", torch.tensor(g2m_dst, dtype=torch.long))

        # Create g2m edge features
        g2m_graph = create_heterograph(g2m_src, g2m_dst, ("grid", "g2m", "mesh"))
        g2m_graph.srcdata["pos"] = grid_xyz.float()
        g2m_graph.dstdata["pos"] = mesh_pos
        g2m_graph = add_edge_features(
            g2m_graph,
            (g2m_graph.srcdata["pos"], g2m_graph.dstdata["pos"]),
        )
        self.register_buffer("g2m_efeat_static", g2m_graph.edata["x"])

        # Build m2g connections
        centroids = self._get_centroids(self.mesh_vertices, self.mesh_faces)
        nbrs = NearestNeighbors(n_neighbors=1).fit(centroids)
        _, indices = nbrs.kneighbors(grid_xyz.numpy())
        indices = indices.flatten()

        m2g_src = [p for i in indices for p in self.mesh_faces[i]]
        m2g_dst = [i for i in range(len(grid_xyz)) for _ in range(3)]

        self.register_buffer("m2g_src_idx", torch.tensor(m2g_src, dtype=torch.long))
        self.register_buffer("m2g_dst_idx", torch.tensor(m2g_dst, dtype=torch.long))
        self.num_grid_nodes = len(grid_xyz)

        # Create m2g edge features
        m2g_graph = create_heterograph(m2g_src, m2g_dst, ("mesh", "m2g", "grid"))
        m2g_graph.srcdata["pos"] = mesh_pos
        m2g_graph.dstdata["pos"] = grid_xyz.float()
        m2g_graph = add_edge_features(
            m2g_graph,
            (m2g_graph.srcdata["pos"], m2g_graph.dstdata["pos"]),
        )
        self.register_buffer("m2g_efeat_static", m2g_graph.edata["x"])

    @staticmethod
    def _max_edge_length(mesh):
        src, dst = faces_to_edges(mesh.faces)
        diffs = mesh.vertices[src] - mesh.vertices[dst]
        return np.sqrt(np.max(np.sum(diffs**2, axis=1)))

    @staticmethod
    def _get_centroids(vertices, faces):
        return np.array(
            [(vertices[f[0]] + vertices[f[1]] + vertices[f[2]]) / 3 for f in faces]
        )

    def forward(self, x):
        """
        DataParallel compatible forward pass.
        Args:
            x: [B, T_in, C, H, W] input tensor
        Returns:
            [B, T_out, C, H, W] output tensor
        """
        B, T_in, C, H, W = x.shape
        device = x.device

        # Process batch all at once instead of loop
        # Reshape: [B, T_in, C, H, W] -> [B, H*W, T_in*C]
        x = rearrange(x, 'b t c h w -> b (h w) (t c)')

        # Project to hidden dimension
        grid_feat = self.input_projection(x)  # [B, H*W, hidden_dim]

        # Process each sample (still need loop due to graph operations)
        outputs = []
        for i in range(B):
            sample_feat = grid_feat[i]  # [H*W, hidden_dim]

            # Embed features
            sample_feat = self.grid_embedder(sample_feat)
            mesh_nfeat = self.mesh_node_embedder(self.mesh_nfeat_static)
            mesh_efeat = self.mesh_edge_embedder(self.mesh_efeat_static)
            g2m_efeat = self.g2m_edge_embedder(self.g2m_efeat_static)
            m2g_efeat = self.m2g_edge_embedder(self.m2g_efeat_static)

            # Encode: grid -> mesh
            sample_feat, mesh_nfeat = self.encoder(
                g2m_efeat, sample_feat, mesh_nfeat,
                self.g2m_src_idx, self.g2m_dst_idx, self.num_mesh_nodes
            )

            # Process mesh
            mesh_efeat, mesh_nfeat = self.processor(
                mesh_efeat, mesh_nfeat,
                self.mesh_src_idx, self.mesh_dst_idx, self.num_mesh_nodes
            )

            # Decode: mesh -> grid
            sample_feat = self.decoder(
                m2g_efeat, mesh_nfeat, sample_feat,
                self.m2g_src_idx, self.m2g_dst_idx, self.num_grid_nodes
            )

            # Output projection
            out = self.output_head(sample_feat)  # [H*W, T_out*C]

            # Reshape: [H*W, T_out*C] -> [T_out, C, H, W]
            out = out.reshape(H, W, self.output_len, C)
            out = rearrange(out, 'h w t c -> t c h w')

            outputs.append(out)

        # Stack outputs: [B, T_out, C, H, W]
        return torch.stack(outputs, dim=0)


class OneForecastAutoregressive(OneForecast):
    """Autoregressive version of OneForecast for long-term prediction.
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
