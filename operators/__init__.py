from .align import ACO_OT_align_limb_axis
from .alert import ACO_OT_alert_error_popup, ACO_OT_alert_info_popup
from .decimation import (
    ACO_OT_decimate_collapse,
    ACO_OT_decimate_planar,
    ACO_OT_decimate_un_subdivide,
    ACO_OT_number_of_vertices_and_faces,
)
from .environment import (
    ACO_OT_import_stl,
    ACO_OT_load_example_scan,
    ACO_OT_prepare_environment,
)
from .prepare_model import ACO_OT_prepare_model_auto
from .repair import ACO_OT_repair_mesh
from .reduction_tools import (
    ACO_OT_apply_mesh_reduction_pipeline,
    ACO_OT_apply_quad_remesh,
    ACO_OT_apply_reduction_preset,
)

from .clear_points_bones import ACO_OT_clear_points_bones
from .mark_point import ACO_OT_mark_point_modal, ACO_OT_select_finger  
from .undo_point import ACO_OT_undo_point
from .rigging import  ACO_OT_generate_bones


CLASSES = (
    ACO_OT_alert_error_popup,
    ACO_OT_alert_info_popup,
    ACO_OT_prepare_environment,
    ACO_OT_import_stl,
    ACO_OT_load_example_scan,
    ACO_OT_align_limb_axis,
    ACO_OT_prepare_model_auto,
    ACO_OT_apply_reduction_preset,
    ACO_OT_apply_mesh_reduction_pipeline,
    ACO_OT_apply_quad_remesh,
    ACO_OT_decimate_un_subdivide,
    ACO_OT_decimate_planar,
    ACO_OT_decimate_collapse,
    ACO_OT_number_of_vertices_and_faces,
    ACO_OT_repair_mesh,
    ACO_OT_clear_points_bones,
    ACO_OT_mark_point_modal, 
    ACO_OT_select_finger ,
    ACO_OT_undo_point, 
    ACO_OT_generate_bones,

)

__all__ = [
    "CLASSES",
    "ACO_OT_prepare_environment",
    "ACO_OT_import_stl",
    "ACO_OT_load_example_scan",
    "ACO_OT_align_limb_axis",
    "ACO_OT_alert_error_popup",
    "ACO_OT_alert_info_popup",
    "ACO_OT_prepare_model_auto",
    "ACO_OT_apply_reduction_preset",
    "ACO_OT_apply_mesh_reduction_pipeline",
    "ACO_OT_apply_quad_remesh",
    "ACO_OT_decimate_collapse",
    "ACO_OT_decimate_planar",
    "ACO_OT_decimate_un_subdivide",
    "ACO_OT_number_of_vertices_and_faces",
    "ACO_OT_repair_mesh",
    "ACO_OT_clear_points_bones",
    "ACO_OT_mark_point_modal", 
    "ACO_OT_select_finger",
    "ACO_OT_undo_point",
    "ACO_OT_generate_bones",
]