bl_info = {
    "name": "AnimeLighting",
    "author": "noenii",
    "version": (1, 1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Shader Panel",
    "description": "Controls the lighting for my Anime Shader.",
    "warning": "This is meant only for debugging.",
    "category": "Material",
    "doc_url": "https://github.com/noenii/AnimeShader",
}
import bpy
def RTUpdater(self, context):
    
    print("RTUpdater Starting")

    if not context.scene.live_update_enabled:
        
        print("updater disabled.")
        return
    
    for obj in context.selected_objects:
            
            print("obj: looping through selected")

            if obj.type != 'MESH':

                print("obj: active is not a mesh")
                continue

            for slot in obj.material_slots:

                mat = slot.material
                print(f"material: {mat.name}")

                if not mat or not mat.use_nodes:

                    print(f"material: {mat.name} does not use nodes")
                    continue

                nodes = mat.node_tree.nodes

                for node in nodes:
                    
                    print(f"node: {node.name}")

                    if isinstance(node, bpy.types.ShaderNodeGroup):

                        print("node: node group found")

                        if node.type == "GROUP" and node.node_tree and node.node_tree.name == "anime_shader":

                            print("node: anime shader found")

                            try:

                                mat.node_tree.nodes["Mix"].inputs[7].default_value = (*context.scene.lighting_color, 1.0)
                                print(f"node: Successfully updated: {mat.name}")
                                break
                            
                            except Exception as b:

                                print(f"node: Error in: {mat.name}, {b}")

class ShaderUpdater(bpy.types.Operator):

    bl_idname = "object.shader_updater_internal"
    bl_label = "Shader Updater"
    bl_description = "Update lighting of all materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        print("executing shader updater")
        
        for obj in context.selected_objects:

            print("obj: looping through selected")

            if obj.type != 'MESH':

                print("obj: active is not a mesh")
                continue

            for slot in obj.material_slots:

                mat = slot.material
                print(f"material: {mat.name}")

                if not mat or not mat.use_nodes:

                    print(f"material: {mat.name} does not use nodes")
                    continue

                nodes = mat.node_tree.nodes

                for node in nodes:
                    
                    print(f"node: {node.name}")

                    if isinstance(node, bpy.types.ShaderNodeGroup):

                        print("node: node group found")

                        if node.type == "GROUP" and node.node_tree and node.node_tree.name == "anime_shader":

                            print("node: anime shader found")

                            try:

                                mat.node_tree.nodes["Mix"].inputs[7].default_value = (*context.scene.lighting_color, 1.0)
                                print(f"node: Successfully updated: {mat.name}")
                                break
                            
                            except Exception as b:

                                print(f"node: Error in: {mat.name}, {b}")

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

    try:

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

    except Exception as c:

        print(f"registering: something went terribly wrong, error: {c}")

def unregister():

    try:

        bpy.utils.unregister_class(ShaderUpdater)
        bpy.utils.unregister_class(ShaderPanel)
        del bpy.types.Scene.lighting_color
        del bpy.types.Scene.live_update_enabled

    except Exception as d:

        print(f"unregistering: something went terribly wrong, error: {d}")

if __name__ == "__main__":

    register()