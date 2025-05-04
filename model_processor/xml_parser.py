import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class ClassAttribute:
    name: str
    type: str


@dataclass
class ClassChild:
    name: str
    type: str = "class"
    min: Optional[str] = None
    max: Optional[str] = None


@dataclass
class ClassModel:
    name: str
    is_root: bool
    documentation: str
    attributes: List[ClassAttribute] = field(default_factory=list)
    children: List[ClassChild] = field(default_factory=list)


class XmlModelParser:
    def __init__(self, xml_file_path: str):
        self.xml_file_path = xml_file_path

    def parse(self) -> Dict[str, ClassModel]:
        tree = ET.parse(self.xml_file_path)
        root = tree.getroot()

        classes = {}
        aggregations = []

        for elem in root:
            if elem.tag == "Class":
                class_name = elem.attrib["name"]
                classes[class_name] = ClassModel(
                    name=class_name,
                    is_root=elem.attrib["isRoot"] == "true",
                    documentation=elem.attrib.get("documentation", ""),
                    attributes=[
                        ClassAttribute(attr.attrib["name"], attr.attrib["type"])
                        for attr in elem.findall("Attribute")
                    ],
                )

            elif elem.tag == "Aggregation":
                aggregations.append(
                    {
                        "source": elem.attrib["source"],
                        "target": elem.attrib["target"],
                        "sourceMultiplicity": elem.attrib["sourceMultiplicity"],
                        "targetMultiplicity": elem.attrib["targetMultiplicity"],
                    }
                )

        for agg in aggregations:
            source = agg["source"]
            target = agg["target"]

            if target in classes:
                multiplicity = agg["sourceMultiplicity"].split("..")
                classes[target].children.append(
                    ClassChild(name=source, min=multiplicity[0], max=multiplicity[-1])
                )

        return classes
