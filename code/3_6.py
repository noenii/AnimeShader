bl_info = {
    "name": "AnimeLighting",
    "author": "noenii",
    "version": (1, 1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Shader Panel",
    "description": "Controls the lighting for my Anime Shader.",
    "warning": "",
    "category": "Material",
    "doc_url": "https://github.com/noenii/AnimeShader",
}
import bpy
def RTUpdater(self, context):
    if not context.scene.live_update_enabled:
        return
    for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue
            for slot in obj.material_slots:
                mat = slot.material
                if not mat or not mat.use_nodes:
                    continue
                nodes = mat.node_tree.nodes
                for node in nodes:
                    if isinstance(node, bpy.types.ShaderNodeGroup):
                        if node.type == "GROUP" and node.node_tree and node.node_tree.name == "anime_shader":
                            try:
                                mat.node_tree.nodes["Mix"].inputs[7].default_value = (*context.scene.lighting_color, 1.0)
                                print(f"Successfully updated: {mat.name}")
                                break
                            except:
                                pass     
class ShaderUpdater(bpy.types.Operator):
    bl_idname = "object.shader_updater_internal"
    bl_label = "Shader Updater"
    bl_description = "Update lighting of all materials"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue
            for slot in obj.material_slots:
                mat = slot.material
                if not mat or not mat.use_nodes:
                    continue
                nodes = mat.node_tree.nodes
                for node in nodes:
                    if isinstance(node, bpy.types.ShaderNodeGroup):
                        if node.type == "GROUP" and node.node_tree and node.node_tree.name == "anime_shader":
                            try:
                                mat.node_tree.nodes["Mix"].inputs[7].default_value = (*context.scene.lighting_color, 1.0)
                                print(f"Successfully updated: {mat.name}")
                                break
                            except:
                                pass
        self.report({'INFO'}, "Done! :D")
        return {'FINISHED'}
class ShaderPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_shader_panel"
    bl_label = "Shader Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Shader"
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "lighting_color", text="Color")
        layout.prop(scene, "live_update_enabled", text="Live Update", toggle=True)
        layout.operator("object.shader_updater_internal", text="Apply", icon="COLOR")
def register():
    bpy.utils.register_class(ShaderUpdater)
    bpy.utils.register_class(ShaderPanel)
    bpy.types.Scene.lighting_color = bpy.props.FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=(0.5, 0.5, 0.5),
        description="Pick a color for all active object's materials",
        update=RTUpdater
    )
    bpy.types.Scene.live_update_enabled = bpy.props.BoolProperty(
        name="Live Update",
        default=False,
        description="Automatically update materials when the color changes",
    )
def unregister():
    bpy.utils.unregister_class(ShaderUpdater)
    bpy.utils.unregister_class(ShaderPanel)
    del bpy.types.Scene.lighting_color
    del bpy.types.Scene.live_update_enabled
if __name__ == "__main__":
    register()