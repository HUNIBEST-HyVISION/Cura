# Copyright (c) 2018 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

from .BaseMaterialsModel import BaseMaterialsModel, getAvailableMaterials


class GenericMaterialsModel(BaseMaterialsModel):

    def __init__(self, parent = None):
        super().__init__(parent)

        from cura.CuraApplication import CuraApplication
        self._machine_manager = CuraApplication.getInstance().getMachineManager()
        self._extruder_manager = CuraApplication.getInstance().getExtruderManager()
        self._material_manager = CuraApplication.getInstance().getMaterialManager()

        self._machine_manager.globalContainerChanged.connect(self._update)
        self._extruder_manager.activeExtruderChanged.connect(self._update)
        self._material_manager.materialsUpdated.connect(self._update)

        self._update()

    def _update(self):
        global_stack = self._machine_manager.activeMachine
        if global_stack is None:
            self.setItems([])
            return

        result_dict = getAvailableMaterials(self._extruder_position)
        if result_dict is None:
            self.setItems([])
            return

        item_list = []
        for root_material_id, container_node in result_dict.items():
            metadata = container_node.metadata
            # Only add results for generic materials
            if metadata["brand"].lower() != "generic":
                continue

            item = {"root_material_id": root_material_id,
                    "id": metadata["id"],
                    "name": metadata["name"],
                    "brand": metadata["brand"],
                    "material": metadata["material"],
                    "color_name": metadata["color_name"],
                    "container_node": container_node
                    }
            item_list.append(item)

        # Sort the item list by material name alphabetically
        item_list = sorted(item_list, key = lambda d: d["name"])

        self.setItems(item_list)
