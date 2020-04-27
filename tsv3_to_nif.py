from pynif import NIFCollection
import os
import re


def compare_next_line(lines: list, link: str, number: int) -> int:
    no_next_line = False
    try:
        lines[number+1]
    except IndexError:
        no_next_line = True

    if no_next_line:
        if lines[number].split("\t")[3].rstrip() == link:
            return number
        else:
            return number - 1
    else:
        if lines[number+1].split("\t")[3].rstrip() != link:
            return number
        else:
            return compare_next_line(lines, link, number+1)


def find_text(lines: list) -> int:
    for i, line in enumerate(lines):
        if line.startswith("#Text"):
            return(i)


dataset = "Name of the data set"
knowledge_base = "Name of knowledge base"
directory = "Directory to input files (TSV3)"

collection = NIFCollection(uri=f"http://kit.edu/{dataset}/{knowledge_base}")

for files in sorted([f for f in os.listdir(directory)]):
    if not str(files).endswith(".DS_Store"):
        with open(directory + "/" + files + "/admin.tsv") as f:
            lines = f.readlines()
            text_line_number = find_text(lines)

            context = collection.add_context(
                uri=f"http://kit.edu/{dataset}/{knowledge_base}/{files}", mention=lines[text_line_number].replace("#Text=", "").rstrip())

            previous_link = ""

            for i, line in enumerate(lines):
                if i > text_line_number:
                    link = line.split("\t")[3].rstrip()
                    link_cleaned = re.sub(
                        r"\[[0-9]+\]", "", link.strip()).lstrip("<").rstrip(">").replace("\\", "")

                    if link != "_" and link.strip() != "" and link != previous_link:
                        entity = line.split("\t")[2]
                        entity_lines = compare_next_line(lines, link, i) - i
                        entity_begin = int(line.split("\t")[1].split("-")[0])
                        entity_end = int(lines[compare_next_line(
                            lines, link, i)].split("\t")[1].split("-")[1])
                        context.add_phrase(beginIndex=entity_begin, endIndex=entity_end,
                                           annotator="http://kit.edu/agnos", taIdentRef=link_cleaned)
                        previous_link = link

nif_file = collection.dumps(format="turtle")

with open(f"{dataset}_{knowledge_base}_output.ttl", "w") as outp:
    outp.write(nif_file)

