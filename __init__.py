import os
import random

if "bpy" in locals():
    import importlib
    importlib.reload(spacestation)
else:
    from . import spacestation

import bpy
import bpy.utils.previews

bl_info = {
    "name": "Spacestation Generator",
    "author": "Rahix",
    "version": (0, 2, 2),
    "blender": (4, 2, 0),
    "location": "View3D > Add > Mesh",
    "description": "Procedural Spacestation generator",
    "category": "Add Mesh"
}

class GenerateSpacestation(bpy.types.Operator):
    bl_idname = "mesh.generate_spacestation"
    bl_label  = "Spacestation"
    bl_options = {'REGISTER', 'UNDO'}

    use_seed: bpy.props.BoolProperty(default=False, name="Use Seed")  # type: ignore
    seed: bpy.props.IntProperty(default=5, name="Seed (Requires 'Use Seed')")  # type: ignore
    internal_seed: bpy.props.IntProperty(default=0, options={'HIDDEN'})  # type: ignore
    use_background: bpy.props.BoolProperty(default=False, name="Use Background")  # type: ignore
    parts_min: bpy.props.IntProperty(default=3, min=0, name="Min. Parts")  # type: ignore
    parts_max: bpy.props.IntProperty(default=8, min=3, name="Max. Parts")  # type: ignore
    torus_major_min: bpy.props.FloatProperty(default=2.0, min=0.1, name="Min. Torus radius")  # type: ignore
    torus_major_max: bpy.props.FloatProperty(default=5.0, min=0.1, name="Max. Torus radius")  # type: ignore
    torus_minor_min: bpy.props.FloatProperty(default=0.1, min=0.1, name="Min. Torus thickness")  # type: ignore
    torus_minor_max: bpy.props.FloatProperty(default=0.5, min=0.1, name="Max. Torus thickness")  # type: ignore
    bevelbox_min: bpy.props.FloatProperty(default=0.2, min=0.1, name="Min. Bevelbox scale")  # type: ignore
    bevelbox_max: bpy.props.FloatProperty(default=0.5, min=0.1, name="Max. Bevelbox scale")  # type: ignore
    cylinder_min: bpy.props.FloatProperty(default=0.5, min=0.1, name="Min. Cylinder radius")  # type: ignore
    cylinder_max: bpy.props.FloatProperty(default=3.0, min=0.1, name="Max. Cylinder radius")  # type: ignore
    cylinder_h_min: bpy.props.FloatProperty(default=0.3, min=0.1, name="Min. Cylinder height")  # type: ignore
    cylinder_h_max: bpy.props.FloatProperty(default=1.0, min=0.1, name="Max. Cylinder height")  # type: ignore
    storage_min: bpy.props.FloatProperty(default=0.5, min=0.1, name="Min. Storage height")  # type: ignore
    storage_max: bpy.props.FloatProperty(default=1.0, min=0.1, name="Max. Storage height")  # type: ignore

    def invoke(self, context, event):
        self.internal_seed = random.randint(0, 100000)
        return self.execute(context)

    def execute(self, context):
        config = {
            "min_parts":      self.parts_min,
            "max_parts":      self.parts_max,
            "torus_major_min":self.torus_major_min,
            "torus_major_max":self.torus_major_max,
            "torus_minor_min":self.torus_minor_min,
            "torus_minor_max":self.torus_minor_max,
            "bevelbox_min":   self.bevelbox_min,
            "bevelbox_max":   self.bevelbox_max,
            "cylinder_min":   self.cylinder_min,
            "cylinder_max":   self.cylinder_max,
            "cylinder_h_min": self.cylinder_h_min,
            "cylinder_h_max": self.cylinder_h_max,
            "storage_min":    self.storage_min,
            "storage_max":    self.storage_max
        }
        base_seed = self.seed if self.use_seed else self.internal_seed
        seed = base_seed + hash(tuple(sorted(config.items()))) % 100000
        spacestation.generate_station(seed, config)
        if self.use_background:
            spacestation.apply_background()
        return {'FINISHED'}

icons = None

def add_menu_entry(self, context):
    self.layout.operator(
        GenerateSpacestation.bl_idname,
        text="Spacestation",
        icon_value=icons["spacestation"].icon_id
    )

def register():
    global icons
    if icons is None:
        icons = bpy.utils.previews.new()
        icons.load(
            "spacestation",
            os.path.join(os.path.dirname(__file__), "icons", "spacestation.png"),
            "IMAGE"
        )
    bpy.utils.register_class(GenerateSpacestation)
    bpy.types.VIEW3D_MT_mesh_add.append(add_menu_entry)

def unregister():
    global icons
    bpy.types.VIEW3D_MT_mesh_add.remove(add_menu_entry)
    bpy.utils.unregister_class(GenerateSpacestation)
    if icons is not None:
        bpy.utils.previews.remove(icons)
        icons = None

if __name__ == "__main__":
    register()
