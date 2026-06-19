from ..operators import *
from ..panels import *
from ..properties import (
    AlignAxisProperties,
    DiagnosticsProperties,
    MeshReductionProperties,
    QuadRemeshProperties,
    RepairProperties,
    AcoJointPoint, 
    AcoRigHand,
    PointToScore,
    PointMarkers,
    ProcessingTime,
    ProcessingTime_State, 
    
)


PROPERTY_CLASSES = (
    AlignAxisProperties,
    DiagnosticsProperties,
    MeshReductionProperties,
    QuadRemeshProperties,
    RepairProperties,
    AcoJointPoint, 
    AcoRigHand,
    PointToScore,
    PointMarkers,
    ProcessingTime,
    ProcessingTime_State, 
    
)


PANEL_CLASSES = (
    ACO_PT_OrthosisInitialization,
    ACO_PT_OrthosisPrepareModel,
    ACO_PT_OrthosisAdvancedModeling,
    ACO_PT_OrthosisRoadmap,
)


OPERATOR_CLASSES= (
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
    ACO_OT_create_bone_score_markers,
    ACO_OT_delete_bone_score_markers,
    ACO_OT_clear_points_bones,
    ACO_OT_mark_point_modal, 
    ACO_OT_select_finger ,
    ACO_OT_undo_point, 
    ACO_OT_generate_bones,
    ACO_OT_redo_finger_bone, 
    ACO_OT_cancel_selected_finger,
    ACO_current_mesh_information,
    ACO_OT_delete_one_score_markers,
    ACO_OT_processing_time_start,
    ACO_OT_processing_time_stop,
    ACO_OT_toggle_pause,
)

CLASSES = PROPERTY_CLASSES + OPERATOR_CLASSES + PANEL_CLASSES 

