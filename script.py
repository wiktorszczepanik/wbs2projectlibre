import sys
import re
from datetime import date, datetime
import shutil
import xml.etree.ElementTree as ET


TASK = "resources/task.xml"
ASSIGNMENT = "resources/assignment.xml"
TEMPLATE = "resources/template.xml"
NS = "http://schemas.microsoft.com/project"


def insert_xml_metadata(output_path, day, time):
    meta_tags = {
        'Name': 'Template',
        'Title': 'Template',
        'StartDate': f"{day}T08:00:00",
        'FinishDate': f"{day}T17:00:00",
        'CurrentDate': time
    }
    tree = ET.parse(output_path)
    root = tree.getroot()
    for tag, value in meta_tags.items():
        element = root.find(f".//{{*}}{tag}")
        element.text = str(value)

    ET.register_namespace("", NS)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)


def parse_wbs_file(wbs_path):
    lines = []
    with open(wbs_path, 'r', encoding='utf8') as file:
        for raw in file:
            # Unicode cleanup
            text = re.sub(r'[\u000B\u000C\u0085\u2028\u2029]', '\n', raw)
            for line in text.split("\n"):
                line = line.strip()
                if line != "":
                    lines.append(line)
    return lines


def wbs_to_xml_tasks(lines, day, time):
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
            'Type': 0,
            'IsNull': 0,
            'CreateDate': time,
            'WBS': "",
            'OutlineNumber': num,
            'OutlineLevel': indent_lvl,
            'Priority': 500,
            'Start': f"{day}T08:00:00",
            'Finish': f"{day}T17:00:00",
            'Duration': "PT8H0M0S",
            'DurationFormat': 39,
            'Resume': f"{day}T08:00:00",
            'ResumeValid': 0,
            'EffortDriven': 1,
            'Recurring': 0,
            'OverAllocated': 0,
            'Estimated': 1,
            'Milestone': 0,
            'Summary': 0,
            'Critical': 0,
            'IsSubproject': 0,
            'IsSubprojectReadOnly': 0,
            'ExternalTask': 0,
            'FixedCostAccrual': 2,
            'PercentComplete': 0,
            'PercentWorkComplete': 0,
            'RemainingDuration': "PT8H0M0S",
            'ConstraintType': 0,
            'CalendarUID': -1,
            'ConstraintDate': "1970-01-01T00:00:00",
            'LevelAssignments': 0,
            'LevelingCanSplit': 0,
            'LevelingDelay': 0,
            'LevelingDelayFormat': 7,
            'IgnoreResourceCalendar': 0,
            'HideBar': 0,
            'Rollup': 0,
            'EarnedValueMethod': 0,
            'Active': 1,
            'Manual': 0
        }
        for tag, value in data.items():
            child = ET.SubElement(task_element, tag)
            child.text = str(value)

        tasks.append(task_element)
        id += 1

    return tasks


def wbs_to_xml_assignments(lines, day, time):
    assignment = []
    uid = 1
    for _ in lines:
        task_element = ET.Element("Assignment")
        data = {
            'UID': uid,
            'TaskUID': uid,
            'ResourceUID': -65535,
            'Finish': f"{day}T17:00:00",
            'HasFixedRateUnits': 1,
            'FixedMaterial': 0,
            'RemainingWork': "PT8H0M0S",
            'Start': f"{day}T08:00:00",
            'Stop': "1970-01-01T01:00:00",
            'Resume': f"{day}T08:00:00",
            'Units': 1,
            'Work': "PT8H0M0S",
            'WorkContour': 0
        }
        for tag, value in data.items():
            child = ET.SubElement(task_element, tag)
            child.text = str(value)

        timephased_data = {
            'Type': 1,
            'UID': uid,
            'Start': f"{day}T08:00:00",
            'Finish': f"{day}T17:00:00",
            'Unit': 3,
            'Value': "PT8H0M0S"
        }
        tp = ET.SubElement(task_element, "TimephasedData")
        for tag, value in timephased_data.items():
            child = ET.SubElement(tp, tag)
            child.text = str(value)

        assignment.append(task_element)
        uid += 1

    return assignment


def insert_xml_tasks(tasks, output_path):
    tree = ET.parse(output_path)
    root = tree.getroot()
    tasks_node = root.find(".//{*}Tasks")

    if tasks_node is None:
        tasks_node = ET.SubElement(root, "Tasks")

    for task in tasks:
        if isinstance(task, str):
            task = ET.fromstring(task)
        tasks_node.append(task)

    ET.indent(tree, space="    ")
    tree.write(output_path, encoding="utf-8", xml_declaration=True)


def insert_xml_assignments(tasks, output_path):
    tree = ET.parse(output_path)
    root = tree.getroot()
    assignments_node = root.find(".//{*}Assignments")

    if assignments_node is None:
        assignments_node = ET.SubElement(root, "Assignments")

    for task in tasks:
        assignments_node.append(task)

    ET.indent(tree, space="    ")
    tree.write(output_path, encoding="utf-8", xml_declaration=True)


if __name__ == '__main__':
    wbs, project_file = sys.argv[1:3]
    day = date.today().isoformat()
    time = datetime.now().isoformat(timespec="seconds")

    shutil.copyfile(TEMPLATE, project_file)
    insert_xml_metadata(project_file, day, time)

    wbs_lines = parse_wbs_file(wbs)
    xml_tasks = wbs_to_xml_tasks(wbs_lines, day, time)
    xml_assignments = wbs_to_xml_assignments(wbs_lines, day, time)

    insert_xml_tasks(xml_tasks, project_file)
    insert_xml_assignments(xml_assignments, project_file)

    print("Done!")
