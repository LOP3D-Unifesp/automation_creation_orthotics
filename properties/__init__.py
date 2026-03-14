from .align_limb import AlignAxisProperties
from .diagnostics import DiagnosticsProperties
from .mesh_reduction import MeshReductionProperties
from .quad_remesh import QuadRemeshProperties

CLASSES = (
    AlignAxisProperties,
    DiagnosticsProperties,
    MeshReductionProperties,
    QuadRemeshProperties,
)

__all__ = [
    "CLASSES",
    "AlignAxisProperties",
    "DiagnosticsProperties",
    "MeshReductionProperties",
    "QuadRemeshProperties",
]

