from .align_limb import AlignAxisProperties
from .diagnostics import DiagnosticsProperties
from .mesh_reduction import MeshReductionProperties
from .quad_remesh import QuadRemeshProperties
from .repair import RepairProperties

CLASSES = (
    AlignAxisProperties,
    DiagnosticsProperties,
    MeshReductionProperties,
    QuadRemeshProperties,
    RepairProperties,
)

__all__ = [
    "CLASSES",
    "AlignAxisProperties",
    "DiagnosticsProperties",
    "MeshReductionProperties",
    "QuadRemeshProperties",
    "RepairProperties",
]
