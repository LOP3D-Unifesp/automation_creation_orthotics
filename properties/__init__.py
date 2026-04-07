from .align_limb import AlignAxisProperties
from .diagnostics import DiagnosticsProperties
from .mesh_reduction import MeshReductionProperties
from .quad_remesh import QuadRemeshProperties
from .repair import RepairProperties
from .join_bones import FINGER_DEFS, NEXT_POINT_LABELS, AcoJointPoint, AcoRigHand

CLASSES = (
    AlignAxisProperties,
    DiagnosticsProperties,
    MeshReductionProperties,
    QuadRemeshProperties,
    RepairProperties,
    AcoJointPoint, 
    AcoRigHand
)

__all__ = [
    "CLASSES",
    "AlignAxisProperties",
    "DiagnosticsProperties",
    "MeshReductionProperties",
    "QuadRemeshProperties",
    "RepairProperties",
    "AcoJointPoint", 
    "AcoRigHand",
    "FINGER_DEFS", 
    "NEXT_POINT_LABELS",
]
