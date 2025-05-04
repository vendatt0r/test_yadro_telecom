import xml.etree.ElementTree as ET

def parse_uml_model(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    classes = []
    aggregations = []

    for cls in root.findall("Class"):
        class_info = {
            "name": cls.get("name"),
            "isRoot": cls.get("isRoot") == "true",
            "documentation": cls.get("documentation"),
            "attributes": []
        }
        for attr in cls.findall("Attribute"):
            class_info["attributes"].append({
                "name": attr.get("name"),
                "type": attr.get("type")
            })
        classes.append(class_info)

    for agg in root.findall("Aggregation"):
        aggregations.append({
            "source": agg.get("source"),
            "target": agg.get("target"),
            "sourceMultiplicity": agg.get("sourceMultiplicity"),
            "targetMultiplicity": agg.get("targetMultiplicity")
        })

    return classes, aggregations
