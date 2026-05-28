from typing import Optional

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import dgl
import dgl.function as fn
from torch import Tensor
from typing import Tuple, List, Optional
from einops import rearrange, repeat, reduce
from sklearn.neighbors import NearestNeighbors
from .base import BaseModel

# Try to import CuGraphOps acceleration
try:
    from pylibcugraphops.pytorch import BipartiteCSC
    USE_CUGRAPHOPS = True
except ImportError:
    USE_CUGRAPHOPS = False
    print("[in NNG.py]⚠️  CuGraphOps not available for NNG, using DGL backend (slower)")


# ============================================================================
# CuGraphOps Graph Structure (if available)
# ============================================================================
class CuGraphCSC:
    """Lightweight CuGraphOps wrapper"""
    def __init__(self, offsets, indices, num_src, num_dst):
        self.offsets = offsets
        self.indices = indices
        self.num_src_nodes = num_src
        self.num_dst_nodes = num_dst
        self.bipartite_csc = None
        self.dgl_graph = None

    @staticmethod
    def from_dgl(graph):
        """Create from DGL graph"""
        if hasattr(graph, "adj_tensors"):
            offsets, indices, edge_perm = graph.adj_tensors("csc")
        else:
            offsets, indices, edge_perm = graph.adj_sparse("csc")

        csc = CuGraphCSC(
            offsets.to(dtype=torch.int64),
            indices.to(dtype=torch.int64),
            graph.num_src_nodes(),
            graph.num_dst_nodes(),
        )
        return csc, edge_perm

    def to_bipartite_csc(self):
        """Convert to BipartiteCSC"""
        if not USE_CUGRAPHOPS or not self.offsets.is_cuda:
            raise RuntimeError("CuGraphOps not available or data not on GPU")

        if self.bipartite_csc is None:
            self.bipartite_csc = BipartiteCSC(
                self.offsets, self.indices, self.num_src_nodes
            )
        return self.bipartite_csc

    def to_dgl_graph(self):
        """Convert to DGL graph"""
        if self.dgl_graph is None:
            offsets = self.offsets
            dst_degree = offsets[1:] - offsets[:-1]
            src_indices = self.indices
            dst_indices = torch.repeat_interleave(
                torch.arange(
                    0, offsets.size(0) - 1, dtype=offsets.dtype, device=offsets.device
                ),
                dst_degree,
                dim=0,
            )
            self.dgl_graph = dgl.heterograph(
                {("src", "e", "dst"): ("coo", (src_indices, dst_indices))},
                idtype=torch.int32,
            )
        return self.dgl_graph

    def to(self, device):
        self.offsets = self.offsets.to(device)
        self.indices = self.indices.to(device)
        return self


# ============================================================================
# Graph Operation Functions
# ============================================================================
def concat_efeat(efeat, nfeat, graph):
    """Concatenate edge features and node features"""
    if isinstance(nfeat, Tensor):
        src_feat = dst_feat = nfeat
    else:
        src_feat, dst_feat = nfeat

    if isinstance(graph, CuGraphCSC):
        graph = graph.to_dgl_graph()

    with graph.local_scope():
        graph.srcdata["x"] = src_feat
        graph.dstdata["x"] = dst_feat
        graph.edata["x"] = efeat
        graph.apply_edges(
            lambda edges: {
                "cat": torch.cat(
                    [edges.data["x"], edges.src["x"], edges.dst["x"]], dim=1
                )
            }
        )
        return graph.edata["cat"]


def aggregate_and_concat(efeat, nfeat, graph, aggregation="sum"):
    """Aggregate edge features to nodes"""
    if USE_CUGRAPHOPS and isinstance(graph, CuGraphCSC) and efeat.is_cuda:
        from pylibcugraphops.pytorch.operators import agg_concat_e2n
        bipartite = graph.to_bipartite_csc()
        return agg_concat_e2n(nfeat, efeat, bipartite, aggregation)

    if isinstance(graph, CuGraphCSC):
        graph = graph.to_dgl_graph()

    with graph.local_scope():
        graph.edata["x"] = efeat
        if aggregation == "sum":
            graph.update_all(fn.copy_e("x", "m"), fn.sum("m", "h"))
        elif aggregation == "mean":
            graph.update_all(fn.copy_e("x", "m"), fn.mean("m", "h"))
        return torch.cat([graph.dstdata["h"], nfeat], dim=-1)


# ============================================================================
# Basic MLP Modules
# ============================================================================
class MLP(nn.Module):
    def __init__(
        self,
        input_dim: int,
        output_dim: int,
        hidden_dim: int = 512,
        hidden_layers: int = 1,
        norm_type: Optional[str] = "LayerNorm",
    ):
        super().__init__()
        layers = [nn.Linear(input_dim, hidden_dim), nn.SiLU()]
        for _ in range(hidden_layers - 1):
            layers += [nn.Linear(hidden_dim, hidden_dim), nn.SiLU()]
        layers.append(nn.Linear(hidden_dim, output_dim))

        if norm_type == "LayerNorm":
            layers.append(nn.LayerNorm(output_dim))

        self.model = nn.Sequential(*layers)

    def forward(self, x: Tensor) -> Tensor:
        return self.model(x)


class EdgeMLP(nn.Module):
    """Edge update MLP"""
    def __init__(
        self,
        efeat_dim: int,
        src_dim: int,
        dst_dim: int,
        output_dim: int,
        hidden_dim: int = 512,
        hidden_layers: int = 2,
    ):
        super().__init__()
        self.mlp = MLP(
            efeat_dim + src_dim + dst_dim, output_dim, hidden_dim, hidden_layers
        )

    def forward(self, efeat: Tensor, nfeat, graph) -> Tensor:
        if isinstance(nfeat, Tensor):
            src_feat = dst_feat = nfeat
        else:
            src_feat, dst_feat = nfeat

        cat_feat = concat_efeat(efeat, (src_feat, dst_feat), graph)
        return self.mlp(cat_feat)


# ============================================================================
# Temporal Encoding Module
# ============================================================================
class TemporalEncoder(nn.Module):
    """Temporal encoding for multi-frame processing"""
    def __init__(self, hidden_dim, input_len):
        super().__init__()
        self.input_len = input_len
        self.temporal_embedding = nn.Parameter(torch.randn(input_len, hidden_dim))
        self.temporal_mlp = MLP(hidden_dim * 2, hidden_dim, hidden_dim)

    def forward(self, x, time_step):
        """
        x: (B*H*W, hidden_dim) - flattened spatial features
        time_step: int - current time step
        """
        temporal_emb = self.temporal_embedding[time_step].unsqueeze(0)
        temporal_emb = temporal_emb.expand(x.shape[0], -1)
        x_concat = torch.cat([x, temporal_emb], dim=-1)
        return self.temporal_mlp(x_concat)


# ============================================================================
# Encoder/Decoder/Processor Modules
# ============================================================================
class Embedder(nn.Module):
    def __init__(
        self, input_dim_grid=2, input_dim_mesh=3, input_dim_edges=4, hidden_dim=512,
        input_len=7, add_3d_dim=True
    ):
        super().__init__()
        # Adapt input dimensions for 2D ocean data
        # If add_3d_dim is True, we expand 2D data to 3D by adding a depth dimension
        grid_input_dim = input_dim_grid * 2 if add_3d_dim else input_dim_grid  # 2D + pseudo-3D

        self.grid_mlp = MLP(grid_input_dim, hidden_dim, hidden_dim)
        self.mesh_mlp = MLP(input_dim_mesh, hidden_dim, hidden_dim)
        self.g2m_edge_mlp = MLP(input_dim_edges, hidden_dim, hidden_dim)
        self.mesh_edge_mlp = MLP(input_dim_edges, hidden_dim, hidden_dim)

        # Temporal encoder for multi-frame processing
        self.temporal_encoder = TemporalEncoder(hidden_dim, input_len)
        self.add_3d_dim = add_3d_dim

    def forward(self, grid_feat, mesh_feat, g2m_efeat, mesh_efeat, time_step=None):
        # Process 2D data for both 2D and 3D pathways
        if self.add_3d_dim:
            # Duplicate 2D features to simulate 3D processing
            # Add a small constant as pseudo-depth information
            pseudo_3d_feat = grid_feat.clone()
            pseudo_3d_feat = pseudo_3d_feat + 0.01  # Small offset for 3D pathway
            grid_feat = torch.cat([grid_feat, pseudo_3d_feat], dim=-1)

        grid_emb = self.grid_mlp(grid_feat)

        # Add temporal encoding if processing multiple frames
        if time_step is not None:
            grid_emb = self.temporal_encoder(grid_emb, time_step)

        return (
            grid_emb,
            self.mesh_mlp(mesh_feat),
            self.g2m_edge_mlp(g2m_efeat),
            self.mesh_edge_mlp(mesh_efeat),
        )


class Encoder(nn.Module):
    def __init__(self, hidden_dim=512, aggregation="sum"):
        super().__init__()
        self.aggregation = aggregation
        self.edge_mlp = EdgeMLP(
            hidden_dim, hidden_dim, hidden_dim, hidden_dim, hidden_dim
        )
        self.src_mlp = MLP(hidden_dim, hidden_dim, hidden_dim)
        self.dst_mlp = MLP(hidden_dim * 2, hidden_dim, hidden_dim)

    def forward(self, efeat, grid_feat, mesh_feat, graph):
        efeat_new = self.edge_mlp(efeat, (grid_feat, mesh_feat), graph)
        cat_feat = aggregate_and_concat(efeat_new, mesh_feat, graph, self.aggregation)
        mesh_feat_new = self.dst_mlp(cat_feat) + mesh_feat
        grid_feat_new = self.src_mlp(grid_feat) + grid_feat
        return grid_feat_new, mesh_feat_new


class Decoder(nn.Module):
    def __init__(self, hidden_dim=512, aggregation="sum", output_len=1):
        super().__init__()
        self.aggregation = aggregation
        self.edge_mlp = EdgeMLP(
            hidden_dim, hidden_dim, hidden_dim, hidden_dim, hidden_dim
        )
        self.node_mlp = MLP(hidden_dim * 2, hidden_dim, hidden_dim)
        self.m2g_edge_mlp = MLP(4, hidden_dim, hidden_dim)

        # Output projection for multi-frame
        self.output_len = output_len
        self.frame_projections = nn.ModuleList([
            MLP(hidden_dim, hidden_dim, hidden_dim) for _ in range(output_len)
        ])

    def forward(self, m2g_efeat, grid_feat, mesh_feat, graph, frame_idx=0):
        m2g_efeat_emb = self.m2g_edge_mlp(m2g_efeat)
        efeat_new = self.edge_mlp(m2g_efeat_emb, (mesh_feat, grid_feat), graph)
        cat_feat = aggregate_and_concat(efeat_new, grid_feat, graph, self.aggregation)
        decoded = self.node_mlp(cat_feat) + grid_feat

        # Apply frame-specific projection
        if frame_idx < len(self.frame_projections):
            decoded = self.frame_projections[frame_idx](decoded)

        return decoded


class ProcessorLayer(nn.Module):
    def __init__(self, hidden_dim=512, aggregation="sum"):
        super().__init__()
        self.aggregation = aggregation
        self.edge_mlp = EdgeMLP(
            hidden_dim, hidden_dim, hidden_dim, hidden_dim, hidden_dim
        )
        self.node_mlp = MLP(hidden_dim * 2, hidden_dim, hidden_dim)

    def forward(self, efeat, nfeat, graph):
        efeat_new = self.edge_mlp(efeat, nfeat, graph) + efeat
        cat_feat = aggregate_and_concat(efeat_new, nfeat, graph, self.aggregation)
        nfeat_new = self.node_mlp(cat_feat) + nfeat
        return efeat_new, nfeat_new


class Processor(nn.Module):
    def __init__(self, num_layers=16, hidden_dim=512, aggregation="sum"):
        super().__init__()
        self.layers = nn.ModuleList(
            [ProcessorLayer(hidden_dim, aggregation) for _ in range(num_layers)]
        )

    def forward(self, efeat, nfeat, graph):
        for layer in self.layers:
            efeat, nfeat = layer(efeat, nfeat, graph)
        return efeat, nfeat


# ============================================================================
# Geometry Utility Functions
# ============================================================================
def deg2rad(deg):
    return deg * np.pi / 180


def rad2deg(rad):
    return rad * 180 / np.pi


def latlon2xyz(latlon: Tensor, radius: float = 1) -> Tensor:
    latlon_rad = deg2rad(latlon)
    lat, lon = latlon_rad[:, 0], latlon_rad[:, 1]
    x = radius * torch.cos(lat) * torch.cos(lon)
    y = radius * torch.cos(lat) * torch.sin(lon)
    z = radius * torch.sin(lat)
    return torch.stack([x, y, z], dim=1)


def xyz2latlon(xyz: Tensor, radius: float = 1) -> Tensor:
    lat = torch.arcsin(xyz[:, 2] / radius)
    lon = torch.arctan2(xyz[:, 1], xyz[:, 0])
    return torch.stack([rad2deg(lat), rad2deg(lon)], dim=1)


def add_edge_features(graph, pos, normalize=True):
    if isinstance(pos, tuple):
        src_pos, dst_pos = pos
    else:
        src_pos = dst_pos = pos

    src, dst = graph.edges()
    src_pos = src_pos[src.long()]
    dst_pos = dst_pos[dst.long()]

    disp = src_pos - dst_pos
    disp_norm = torch.linalg.norm(disp, dim=-1, keepdim=True)

    if normalize:
        max_norm = torch.max(disp_norm)
        graph.edata["x"] = torch.cat([disp / max_norm, disp_norm / max_norm], dim=-1)
    else:
        graph.edata["x"] = torch.cat([disp, disp_norm], dim=-1)

    return graph


# ============================================================================
# Mesh Generation
# ============================================================================
class TriangularMesh:
    def __init__(self, vertices: np.ndarray, faces: np.ndarray):
        self.vertices = vertices
        self.faces = faces


def get_icosahedron() -> TriangularMesh:
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
    return TriangularMesh(vertices.astype(np.float32), np.array(faces, dtype=np.int32))


def split_triangles(mesh: TriangularMesh) -> TriangularMesh:
    vertices_list = list(mesh.vertices)
    child_vertex_map = {}

    def get_midpoint(idx1, idx2):
        key = tuple(sorted([idx1, idx2]))
        if key not in child_vertex_map:
            midpoint = (mesh.vertices[idx1] + mesh.vertices[idx2]) / 2
            midpoint /= np.linalg.norm(midpoint)
            child_vertex_map[key] = len(vertices_list)
            vertices_list.append(midpoint)
        return child_vertex_map[key]

    new_faces = []
    for i1, i2, i3 in mesh.faces:
        i12, i23, i31 = get_midpoint(i1, i2), get_midpoint(i2, i3), get_midpoint(i3, i1)
        new_faces.extend(
            [[i1, i12, i31], [i12, i2, i23], [i31, i23, i3], [i12, i23, i31]]
        )

    return TriangularMesh(
        np.array(vertices_list, dtype=np.float32), np.array(new_faces, dtype=np.int32)
    )


def get_mesh_hierarchy(splits: int) -> List[TriangularMesh]:
    meshes = [get_icosahedron()]
    for _ in range(splits):
        meshes.append(split_triangles(meshes[-1]))
    return meshes


def faces_to_edges(faces: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    src = np.concatenate([faces[:, 0], faces[:, 1], faces[:, 2]])
    dst = np.concatenate([faces[:, 1], faces[:, 2], faces[:, 0]])
    return src, dst


# ============================================================================
# Graph Construction
# ============================================================================
class Graph:
    def __init__(
        self, lat_lon_grid, mesh_level=6, multimesh=True, use_cugraphops=False
    ):
        self.use_cugraphops = use_cugraphops and USE_CUGRAPHOPS
        self.lat_lon_grid_flat = rearrange(lat_lon_grid, "h w c -> (h w) c")

        meshes = get_mesh_hierarchy(mesh_level)
        if multimesh:
            all_vertices = meshes[-1].vertices
            all_faces = np.concatenate([m.faces for m in meshes], axis=0)
        else:
            all_vertices = meshes[-1].vertices
            all_faces = meshes[-1].faces

        self.mesh_vertices = all_vertices
        self.mesh_faces = all_faces
        self.mesh_src, self.mesh_dst = faces_to_edges(all_faces)
        self.finest_mesh_vertices = meshes[-1].vertices
        finest_src, finest_dst = faces_to_edges(meshes[-1].faces)

        src_coords = self.finest_mesh_vertices[finest_src]
        dst_coords = self.finest_mesh_vertices[finest_dst]
        self.max_edge_len = np.sqrt(
            np.max(np.sum((src_coords - dst_coords) ** 2, axis=1))
        )

    def create_mesh_graph(self):
        graph = dgl.graph((self.mesh_src, self.mesh_dst), idtype=torch.int32)
        graph = dgl.to_bidirected(graph)
        mesh_pos = torch.tensor(self.mesh_vertices, dtype=torch.float32)
        graph = add_edge_features(graph, mesh_pos)

        latlon = xyz2latlon(mesh_pos)
        lat, lon = deg2rad(latlon[:, 0]), deg2rad(latlon[:, 1])
        graph.ndata["x"] = torch.stack(
            [torch.cos(lat), torch.sin(lon), torch.cos(lon)], dim=-1
        )

        if self.use_cugraphops:
            csc, edge_perm = CuGraphCSC.from_dgl(graph)
            edata = graph.edata["x"][edge_perm]
            return csc, graph.ndata["x"], edata

        return graph, graph.ndata["x"], graph.edata["x"]

    def create_g2m_graph(self):
        cartesian_grid = latlon2xyz(self.lat_lon_grid_flat)
        nbrs = NearestNeighbors(n_neighbors=4).fit(self.mesh_vertices)
        distances, indices = nbrs.kneighbors(cartesian_grid.numpy())

        src, dst = [], []
        for i in range(len(cartesian_grid)):
            for j in range(4):
                if distances[i][j] <= 0.6 * self.max_edge_len:
                    src.append(i)
                    dst.append(indices[i][j])

        graph = dgl.heterograph(
            {("grid", "g2m", "mesh"): (src, dst)}, idtype=torch.int32
        )
        graph.srcdata["pos"] = cartesian_grid.to(torch.float32)
        graph.dstdata["pos"] = torch.tensor(self.mesh_vertices, dtype=torch.float32)
        graph = add_edge_features(graph, (graph.srcdata["pos"], graph.dstdata["pos"]))

        if self.use_cugraphops:
            csc, edge_perm = CuGraphCSC.from_dgl(graph)
            edata = graph.edata["x"][edge_perm]
            return csc, edata

        return graph, graph.edata["x"]

    def create_m2g_graph(self):
        cartesian_grid = latlon2xyz(self.lat_lon_grid_flat)
        centroids = np.array(
            [self.mesh_vertices[face].mean(axis=0) for face in self.mesh_faces],
            dtype=np.float32,
        )

        nbrs = NearestNeighbors(n_neighbors=1).fit(centroids)
        _, indices = nbrs.kneighbors(cartesian_grid.numpy())
        indices = indices.flatten()

        src = [p for i in indices for p in self.mesh_faces[i]]
        dst = [i for i in range(len(cartesian_grid)) for _ in range(3)]

        graph = dgl.heterograph(
            {("mesh", "m2g", "grid"): (src, dst)}, idtype=torch.int32
        )
        graph.srcdata["pos"] = torch.tensor(self.mesh_vertices, dtype=torch.float32)
        graph.dstdata["pos"] = cartesian_grid.to(torch.float32)
        graph = add_edge_features(graph, (graph.srcdata["pos"], graph.dstdata["pos"]))

        if self.use_cugraphops:
            csc, edge_perm = CuGraphCSC.from_dgl(graph)
            edata = graph.edata["x"][edge_perm]
            return csc, edata

        return graph, graph.edata["x"]


# ============================================================================
# Main Model
# ============================================================================
class NNG(BaseModel):
    """Neural Network on Graphs for Ocean Velocity Prediction"""

    def __init__(self, args):
        super(BaseModel, self).__init__()

        # Extract parameters from args
        self.input_len = args.get('input_len', 7)
        self.output_len = args.get('output_len', 1)
        self.in_channels = args.get('in_channels', 2)  # uo, vo
        self.input_res = args.get('input_res', (240, 240))

        # Model architecture parameters
        self.mesh_level = args.get('mesh_level', 5)
        self.multimesh = args.get('multimesh', True)
        self.hidden_dim = args.get('hidden_dim', 128)
        self.processor_layers = args.get('processor_layers', 16)
        self.aggregation = args.get('aggregation', 'sum')
        self.use_cugraphops = args.get('use_cugraphops', True)
        self.add_3d_dim = args.get('add_3d_dim', True)  # Whether to process 2D data as pseudo-3D

        # Create lat-lon grid for 240x240 resolution
        lats = torch.linspace(-90, 90, steps=self.input_res[0] + 1)[:-1]
        lons = torch.linspace(-180, 180, steps=self.input_res[1] + 1)[1:]
        lat_grid, lon_grid = torch.meshgrid(lats, lons, indexing="ij")
        self.lat_lon_grid = torch.stack([lat_grid, lon_grid], dim=-1)

        # Build graphs
        self.use_cugraphops = self.use_cugraphops and USE_CUGRAPHOPS
        self.graph = Graph(
            self.lat_lon_grid, self.mesh_level, self.multimesh, self.use_cugraphops
        )

        mesh_graph_out = self.graph.create_mesh_graph()
        g2m_graph_out = self.graph.create_g2m_graph()
        m2g_graph_out = self.graph.create_m2g_graph()

        if self.use_cugraphops:
            self.mesh_graph, self.mesh_ndata, self.mesh_edata = mesh_graph_out
            self.g2m_graph, self.g2m_edata = g2m_graph_out
            self.m2g_graph, self.m2g_edata = m2g_graph_out
        else:
            self.mesh_graph, self.mesh_ndata, self.mesh_edata = mesh_graph_out
            self.g2m_graph, self.g2m_edata = g2m_graph_out
            self.m2g_graph, self.m2g_edata = m2g_graph_out

        # Model components
        self.embedder = Embedder(
            self.in_channels, 3, 4, self.hidden_dim,
            self.input_len, self.add_3d_dim
        )
        self.encoder = Encoder(self.hidden_dim, self.aggregation)
        self.processor = Processor(self.processor_layers, self.hidden_dim, self.aggregation)
        self.decoder = Decoder(self.hidden_dim, self.aggregation, self.output_len)

        # Output projection for each output frame
        self.output_mlps = nn.ModuleList([
            MLP(self.hidden_dim, self.in_channels, self.hidden_dim, norm_type=None)
            for _ in range(self.output_len)
        ])

        # Move graphs to appropriate device
        self._graphs_device = None

    def _move_graphs_to_device(self, device):
        """Move graphs to device (called once)"""
        if self._graphs_device != device:
            self.mesh_ndata = self.mesh_ndata.to(device)
            self.mesh_edata = self.mesh_edata.to(device)
            self.g2m_edata = self.g2m_edata.to(device)
            self.m2g_edata = self.m2g_edata.to(device)

            if self.use_cugraphops:
                self.mesh_graph = self.mesh_graph.to(device)
                self.g2m_graph = self.g2m_graph.to(device)
                self.m2g_graph = self.m2g_graph.to(device)
            else:
                self.mesh_graph = self.mesh_graph.to(device)
                self.g2m_graph = self.g2m_graph.to(device)
                self.m2g_graph = self.m2g_graph.to(device)

            self._graphs_device = device

    def forward(self, x: Tensor) -> Tensor:
        """
        x: (B, T_in, C, H, W)
        return: (B, T_out, C, H, W)
        """
        B, T_in, C, H, W = x.shape
        device = x.device

        # Move graphs to device if needed
        self._move_graphs_to_device(device)

        # Process each batch item separately (NNG currently supports batch_size=1)
        outputs = []
        for b in range(B):
            batch_outputs = []

            # Process input frames sequentially and accumulate features
            accumulated_grid_feat = None

            for t in range(T_in):
                # Extract single frame
                frame = x[b, t]  # (C, H, W)
                frame = rearrange(frame, "c h w -> (h w) c")  # (H*W, C)

                # Embedding with temporal encoding
                grid_emb, mesh_emb, g2m_emb, mesh_edge_emb = self.embedder(
                    frame, self.mesh_ndata, self.g2m_edata, self.mesh_edata, time_step=t
                )

                # Encode
                grid_feat, mesh_feat = self.encoder(g2m_emb, grid_emb, mesh_emb, self.g2m_graph)

                # Accumulate features across time
                if accumulated_grid_feat is None:
                    accumulated_grid_feat = grid_feat
                else:
                    accumulated_grid_feat = accumulated_grid_feat + grid_feat * 0.5  # Weighted accumulation

                # Process
                mesh_edge_feat, mesh_feat = self.processor(
                    mesh_edge_emb, mesh_feat, self.mesh_graph
                )

            # Decode for each output frame
            for out_t in range(self.output_len):
                # Decode with frame-specific processing
                grid_out = self.decoder(
                    self.m2g_edata, accumulated_grid_feat, mesh_feat,
                    self.m2g_graph, frame_idx=out_t
                )

                # Output projection
                output = self.output_mlps[out_t](grid_out)
                output = rearrange(
                    output, "(h w) c -> c h w", h=self.input_res[0], w=self.input_res[1]
                )
                batch_outputs.append(output)

            # Stack output frames
            batch_output = torch.stack(batch_outputs, dim=0)  # (T_out, C, H, W)
            outputs.append(batch_output)

        # Stack batch outputs
        output = torch.stack(outputs, dim=0)  # (B, T_out, C, H, W)

        return output


class NNGAutoregressive(NNG):
    """Autoregressive version of NNG for long-term prediction.
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