import sys
import xml.etree.ElementTree as ET
import shutil
from datetime import date, datetime
from xml.dom import minidom

TASK = "resources/task.xml"
TEMPLATE = "resources/template.xml"

def parse_wbs_file(wbs_path):
    lines = []
    with open(wbs_path, 'r', encoding='utf8') as file:
        for line in file:
            line = line.strip()
            if line != "":
                lines.append(line)
    return lines

def collect_wbs_tags(lines, day, time):
    tasks = []
    id = 1
    for line in lines:
        num = line.split(None, 1)[0]
        indent_lvl = num.strip(".").count(".") + 1
        task_element = ET.Element("Task")
        data = {
            'UID': id,
            'ID': id,
            'Name': line,
            'OutlineNumber': num,
            'OutlineLevel': indent_lvl
        }
        for tag, value in data.items():
            child = ET.SubElement(task_element, tag)
            child.text = str(value)

        tasks.append(task_element)
        id += 1

    return tasks

def transform_to_xml(task_path, tasks):
    tree = ET.parse(task_path)
    root = tree.getroot()
    container = []
    for task in tasks:
        for tag, value in task.items():
            element = root.find(tag)
            if element is None:
                element = ET.SubElement(root, tag)
            element.text = '' if value is None else str(value)
        xml_bytes = ET.tostring(root, encoding='utf-8')
        container.append(xml_bytes.decode('utf-8'))

    return container


def create_output_file(output_path, template_path):
    shutil.copyfile(template_path, output_path)

def insert_metadata(output_path, day, time):
    meta_tags = {
        'StartDate': day + "T08:00:00",
        'FinishDate': day + "T17:00:00",
        'CurrentDate': time
    }
    tree = ET.parse(output_path)
    root = tree.getroot()
    for tag, value in meta_tags.items():
        element = root.find(tag)
        if element is None:
            element = ET.SubElement(root, tag)
        element.text = '' if value is None else str(value)

    xml_bytes = ET.tostring(root, encoding='utf-8')
    pretty = minidom.parseString(xml_bytes).toprettyxml(indent='  ', encoding='utf-8')

    with open(output_path, 'wb') as file:
        file.write(pretty)


def insert_tasks_to_output(template_path, tasks):



if __name__ == '__main__':
    wbs, project_file = sys.argv[1:3]
    wbs_lines = parse_wbs_file(wbs)
    day = date.today().isoformat()
    time = datetime.now().isoformat()
    wbs_tasks = collect_wbs_tags(wbs_lines, day, time)
    xml_tasks = transform_to_xml(TASK, wbs_tasks)
    create_output_file(project_file, TEMPLATE)
    insert_metadata(project_file, day, time)
    insert_tasks_to_output(project_file, xml_tasks)
    print(xml_tasks)

