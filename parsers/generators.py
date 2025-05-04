def generate_meta_json(classes):
    meta = []
    for cls in classes:
        meta.append({
            "className": cls["name"],
            "documentation": cls["documentation"],
            "attributes": cls["attributes"]
        })
    return meta

def generate_config_xml(classes, aggregations):
    def indent(level):
        return "  " * level

    def generate_node(cls, class_map, agg_map, level):
        lines = [f"{indent(level)}<{cls['name']}>"]
        for attr in cls["attributes"]:
            lines.append(f"{indent(level+1)}<{attr['name']}>{attr['type']}</{attr['name']}>")
        for child_name in agg_map.get(cls["name"], []):
            child_cls = class_map[child_name]
            lines.extend(generate_node(child_cls, class_map, agg_map, level + 1))
        lines.append(f"{indent(level)}</{cls['name']}>")
        return lines

    class_map = {cls["name"]: cls for cls in classes}
    agg_map = {}
    for agg in aggregations:
        parent = agg["target"]
        child = agg["source"]
        agg_map.setdefault(parent, []).append(child)

    root_cls = next(cls for cls in classes if cls["isRoot"])
    xml_lines = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>"]
    xml_lines.extend(generate_node(root_cls, class_map, agg_map, 0))
    return "\n".join(xml_lines)
