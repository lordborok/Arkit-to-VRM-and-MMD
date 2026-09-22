bl_info = {
    "name": "ARKit → VRM/MMD Expression Generator",
    "author": "Hans + Copilot",
    "version": (1, 3, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > ARKit -> VRM/MMD",
    "description": "Automatically bake VRM/MMD expression shapekeys from ARKit presets without mix bleed",
    "category": "Animation",
}

import bpy

# -------------------------------------------------------------------
# PRESET DEFINITIONS (tune these to your liking)
# -------------------------------------------------------------------

VRM_PRESETS = {
    "BlinkLeft": {"eyeBlinkLeft": 1.0},
    "BlinkRight": {"eyeBlinkRight": 1.0},
    "Blink": {"eyeBlinkLeft": 1.0, "eyeBlinkRight": 1.0},
    "LookUp": {"eyeLookUpLeft": 1.0, "eyeLookUpRight": 1.0},
    "LookDown": {"eyeLookDownLeft": 1.0, "eyeLookDownRight": 1.0},
    "LookLeft": {"eyeLookInLeft": 1.0, "eyeLookOutRight": 1.0},
    "LookRight": {"eyeLookOutLeft": 1.0, "eyeLookInRight": 1.0},
    "Joy": {
        "mouthSmileLeft": 1.0,
        "mouthSmileRight": 1.0,
        "eyeSquintLeft": 0.4,
        "eyeSquintRight": 0.4,
    },
    "Angry": {
        "browDownLeft": 1.0,
        "browDownRight": 1.0,
        "mouthFrownLeft": 0.8,
        "mouthFrownRight": 0.8,
    },
    "Sorrow": {
        "browInnerUp": 0.8,
        "mouthFrownLeft": 0.6,
        "mouthFrownRight": 0.6,
    },
    "Surprised": {
        "eyeWideLeft": 1.0,
        "eyeWideRight": 1.0,
        "jawOpen": 1.0,
    },
    "A": {"jawOpen": 1.0},
    "I": {"mouthSmileLeft": 0.8, "mouthSmileRight": 0.8},
    "U": {"mouthPucker": 1.0},
    "E": {
        "mouthSmileLeft": 0.6,
        "mouthSmileRight": 0.6,
        "jawOpen": 0.3,
    },
    "O": {
        "mouthPucker": 0.8,
        "jawOpen": 0.6,
    },
    # VRM 1.0 vowel preset names.
    "aa": {"jawOpen": 1.0},
    "ih": {"mouthSmileLeft": 0.8, "mouthSmileRight": 0.8},
    "ou": {"mouthPucker": 1.0},
    "ee": {
        "mouthSmileLeft": 0.6,
        "mouthSmileRight": 0.6,
        "jawOpen": 0.3,
    },
    "oh": {"mouthPucker": 0.8, "jawOpen": 0.6},
}

MMD_PRESETS = {
    "ウィンク": {"eyeBlinkLeft": 1.0},
    "ウィンク右": {"eyeBlinkRight": 1.0},
    "ウィンク２": {"eyeBlinkLeft": 1.0, "eyeSquintLeft": 0.4},
    "ウィンク２右": {"eyeBlinkRight": 1.0, "eyeSquintRight": 0.4},
    "まばたき": {"eyeBlinkLeft": 1.0, "eyeBlinkRight": 1.0},
    "なごみ": {
        "eyeSquintLeft": 0.7,
        "eyeSquintRight": 0.7,
        "mouthSmileLeft": 0.4,
        "mouthSmileRight": 0.4,
    },
    "はぅ": {"eyeWideLeft": 0.7, "eyeWideRight": 0.7},
    "びっくり": {
        "eyeWideLeft": 1.0,
        "eyeWideRight": 1.0,
        "jawOpen": 1.0,
    },
    "じと目": {
        "eyeSquintLeft": 0.7,
        "eyeSquintRight": 0.7,
        "browDownLeft": 0.3,
        "browDownRight": 0.3,
    },
    "キリッ": {"browDownLeft": 0.7, "browDownRight": 0.7},
    "はちゅ目": {"eyeWideLeft": 0.8, "eyeWideRight": 0.8},
    "笑い": {
        "mouthSmileLeft": 1.0,
        "mouthSmileRight": 1.0,
        "eyeSquintLeft": 0.4,
        "eyeSquintRight": 0.4,
    },
    "怒り": {
        "browDownLeft": 1.0,
        "browDownRight": 1.0,
        "mouthFrownLeft": 0.8,
        "mouthFrownRight": 0.8,
    },
    "悲しみ": {
        "browInnerUp": 0.8,
        "mouthFrownLeft": 0.6,
        "mouthFrownRight": 0.6,
    },
    "驚き": {
        "eyeWideLeft": 1.0,
        "eyeWideRight": 1.0,
        "jawOpen": 1.0,
    },
    "あ": {"jawOpen": 1.0},
    "い": {"mouthSmileLeft": 0.8, "mouthSmileRight": 0.8},
    "う": {"mouthPucker": 1.0},
    "え": {
        "mouthSmileLeft": 0.6,
        "mouthSmileRight": 0.6,
        "jawOpen": 0.3,
    },
    "お": {
        "mouthPucker": 0.8,
        "jawOpen": 0.6,
    },
    "ん": {"mouthClose": 1.0},
    "にやり": {"mouthSmileLeft": 0.8, "mouthSmileRight": 0.8},
    "にやり２": {
        "mouthSmileLeft": 0.8,
        "mouthSmileRight": 0.8,
        "eyeSquintLeft": 0.4,
        "eyeSquintRight": 0.4,
    },
    "口角上げ": {"mouthSmileLeft": 0.7, "mouthSmileRight": 0.7},
    "口角下げ": {"mouthFrownLeft": 0.7, "mouthFrownRight": 0.7},
    "への字口": {"mouthFrownLeft": 1.0, "mouthFrownRight": 1.0},
    "ω口": {"mouthPucker": 0.8},
    "猫口": {"mouthPucker": 0.5, "mouthSmileLeft": 0.3, "mouthSmileRight": 0.3},
    "困る": {"browInnerUp": 0.8},
    "真面目": {"browDownLeft": 0.2, "browDownRight": 0.2},
    "上": {"browOuterUpLeft": 0.7, "browOuterUpRight": 0.7},
    "下": {"browDownLeft": 0.7, "browDownRight": 0.7},
}


def get_presets(fmt: str):
    return VRM_PRESETS if fmt == "VRM" else MMD_PRESETS


def reset_all_shape_keys(key_blocks):
    """Set ALL shapekey values to 0 (including previously baked expressions)."""
    for kb in key_blocks:
        kb.value = 0.0
    bpy.context.view_layer.update()


def apply_weights(key_blocks, weights):
    """Apply ARKit weights on a clean slate."""
    for name, value in weights.items():
        if name in key_blocks:
            key_blocks[name].value = value
    bpy.context.view_layer.update()


class ARKIT_OT_generate_all(bpy.types.Operator):
    """Generate all VRM/MMD expression shapekeys from ARKit presets"""
    bl_idname = "arkit.generate_all_expressions"
    bl_label = "Generate All Expressions"
    bl_options = {'REGISTER', 'UNDO'}

    target_format: bpy.props.EnumProperty(
        name="Target Format",
        items=[('VRM', "VRM", "VRM-style expressions"),
               ('MMD', "MMD", "MMD-style expressions")],
        default='VRM',
    )

    overwrite_existing: bpy.props.BoolProperty(
        name="Overwrite Existing",
        description="Remove existing shapekeys with the same name before recreating",
        default=False,
    )

    def execute(self, context):
        obj = context.object
        if not obj or obj.type != "MESH":
            self.report({'ERROR'}, "Select a mesh with shapekeys")
            return {'CANCELLED'}

        if not obj.data.shape_keys or not obj.data.shape_keys.key_blocks:
            self.report({'ERROR'}, "Object has no shapekeys")
            return {'CANCELLED'}

        presets = get_presets(self.target_format)

        created = 0
        updated = 0

        for expr_name, weights in presets.items():
            # Always start from a completely clean mix
            reset_all_shape_keys(obj.data.shape_keys.key_blocks)
            obj.data.update()

            # Handle existing shapekey
            key_blocks = obj.data.shape_keys.key_blocks
            if expr_name in key_blocks:
                if self.overwrite_existing:
                    idx = key_blocks.find(expr_name)
                    obj.active_shape_key_index = idx
                    bpy.ops.object.shape_key_remove()
                    bpy.context.view_layer.update()
                    updated += 1
                else:
                    # Skip if not overwriting
                    continue

            # Apply ARKit weights for this expression
            key_blocks = obj.data.shape_keys.key_blocks
            apply_weights(key_blocks, weights)
            obj.data.update()

            # Bake new shapekey from current mix
            new_key = obj.shape_key_add(name=expr_name, from_mix=True)

            # IMPORTANT: set new shapekey value to 0 so it doesn't affect the next bake
            new_key.value = 0.0
            # Clear the source mix before starting the next expression.
            reset_all_shape_keys(obj.data.shape_keys.key_blocks)
            obj.data.update()
            bpy.context.view_layer.update()

            created += 1

        self.report(
            {'INFO'},
            f"{self.target_format}: Created {created}, Updated {updated}"
        )
        return {'FINISHED'}


class ARKIT_PT_expression_panel(bpy.types.Panel):
    bl_label = "ARKit → VRM/MMD Expressions"
    bl_idname = "ARKIT_PT_expression_generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ARKit Expr"

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        col.label(text="Auto-generate expressions from ARKit presets")

        scene = context.scene
        col.prop(scene, "arkit_target_format", text="Target")
        col.prop(scene, "arkit_overwrite_existing", text="Overwrite Existing")

        op = col.operator("arkit.generate_all_expressions", text="Generate All Expressions")
        op.target_format = scene.arkit_target_format
        op.overwrite_existing = scene.arkit_overwrite_existing


classes = (
    ARKIT_OT_generate_all,
    ARKIT_PT_expression_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.arkit_target_format = bpy.props.EnumProperty(
        name="Target Format",
        items=[('VRM', "VRM", "VRM-style expressions"),
               ('MMD', "MMD", "MMD-style expressions")],
        default='VRM',
    )
    bpy.types.Scene.arkit_overwrite_existing = bpy.props.BoolProperty(
        name="Overwrite Existing",
        description="Remove existing shapekeys with the same name before recreating",
        default=False,
    )


def unregister():
    del bpy.types.Scene.arkit_target_format
    del bpy.types.Scene.arkit_overwrite_existing

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
