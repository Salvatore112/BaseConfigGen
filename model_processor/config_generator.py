import json
from typing import Dict
from dataclasses import asdict
from .xml_parser import ClassModel, ClassChild


class ConfigGenerator:
    def __init__(self, class_model: Dict[str, ClassModel]):
        self.class_model = class_model

    def generate_config_xml(self) -> str:
        root_class = next(
            (name for name, model in self.class_model.items() if model.is_root), None
        )

        if not root_class:
            return ""

        return self._build_xml_element(root_class)

    def _build_xml_element(self, class_name: str, indent: int = 0) -> str:
        class_info = self.class_model[class_name]
        indent_str = "    " * indent
        xml_lines = []

        xml_lines.append(f"{indent_str}<{class_name}>")

        for attr in class_info.attributes:
            xml_lines.append(f"{indent_str}    <{attr.name}>{attr.type}</{attr.name}>")

        for child in class_info.children:
            if child.name in self.class_model:
                xml_lines.append(self._build_xml_element(child.name, indent + 1))

        xml_lines.append(f"{indent_str}</{class_name}>")

        return "\n".join(xml_lines)

    def generate_meta_json(self) -> json:
        meta = []

        for class_name, class_info in self.class_model.items():
            entry = {
                "class": class_name,
                "documentation": class_info.documentation,
                "isRoot": class_info.is_root,
                "parameters": [],
            }

            for attr in class_info.attributes:
                entry["parameters"].append({"name": attr.name, "type": attr.type})

            for child in class_info.children:
                child_entry = {"name": child.name, "type": child.type}

                if child.min is not None and child.max is not None:
                    entry["min"] = child.min
                    entry["max"] = child.max

                entry["parameters"].append(child_entry)

            meta.append(entry)

        return json.dumps(meta, indent=4)
