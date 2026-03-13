from .align import ACO_OT_align_limb_axis
from .alert import ACO_OT_alert_error_popup, ACO_OT_alert_info_popup
from .decimation import (
    ACO_OT_decimate_collapse,
    ACO_OT_decimate_planar,
    ACO_OT_decimate_un_subdivide,
    ACO_OT_number_of_vertices_and_faces,
)

CLASSES = (
    ACO_OT_alert_error_popup,
    ACO_OT_alert_info_popup,
    ACO_OT_align_limb_axis,
    ACO_OT_decimate_un_subdivide,
    ACO_OT_decimate_planar,
    ACO_OT_decimate_collapse,
    ACO_OT_number_of_vertices_and_faces,
)

__all__ = [
    "CLASSES",
    "ACO_OT_align_limb_axis",
    "ACO_OT_alert_error_popup",
    "ACO_OT_alert_info_popup",
    "ACO_OT_decimate_collapse",
    "ACO_OT_decimate_planar",
    "ACO_OT_decimate_un_subdivide",
    "ACO_OT_number_of_vertices_and_faces",
]

