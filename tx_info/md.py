import json
import os


def json_to_markdown_table(json_data):
    # Define the table header
    table_header = ["Title", "URL", "Translated %",
                    "Total Chars", "Total Words",
                    "Untranslated Chars", "Untranslated Words",
                    "Translated Chars", "Translated Words"]

    # Create the table header row in Markdown format
    md_table = f"| {' | '.join(table_header)} |\n"
    md_table += f"| {' | '.join(['---'] * len(table_header))} |\n"

    total_percent = 0

    # Iterate through each item in the JSON and add rows to the Markdown table
    for repo_id, data in json_data.items():
        percent = int(data.get("translated-chars-data", 1)) / int(data.get("total-chars-data", 1))
        total_percent += percent
        row = [
            data.get("title", ""),
            data.get("url", ""),
            str(round(percent, 2)),
            data.get("total-chars-data", ""),
            data.get("total-words-data", ""),
            data.get("untranslated-chars-data", ""),
            data.get("untranslated-words-data", ""),
            data.get("translated-chars-data", ""),
            data.get("translated-words-data", ""),
        ]
        md_table += f"| {' | '.join(row)} |\n"

    total_percent = total_percent / len(json_data)
    return total_percent, md_table


def read_json_files_from_directory(directory_path):
    # Iterate through the files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)

            # Read the JSON file and load the data
            with open(file_path, 'r', encoding='utf-8') as f:
                yield filename.split(".json")[0], json.load(f)


def save_markdown_table(md_table, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_table)


def langs_to_markdown_table(json_data):
    # Define the table header
    table_header = ["Lang", "Translated %"]

    # Create the table header row in Markdown format
    md_table = f"| {' | '.join(table_header)} |\n"
    md_table += f"| {' | '.join(['---'] * len(table_header))} |\n"


    # Iterate through each item in the JSON and add rows to the Markdown table
    for lang, percent in json_data.items():
        row = [
            lang,
            str(round(percent, 2))
        ]
        md_table += f"| {' | '.join(row)} |\n"

    return md_table


# Define the directory containing the JSON files and the output markdown file
json_directory = os.path.dirname(__file__)

lang_data = {}
# Read JSON files, convert them to a markdown table, and save the table to a file
for lang, json_data in read_json_files_from_directory(json_directory):
    percent, markdown_table = json_to_markdown_table(json_data)
    output_md_file = f"translate_status_{lang}.md"
    save_markdown_table(markdown_table, output_md_file)
    lang_data[lang] = percent

markdown_table = langs_to_markdown_table(lang_data)
output_md_file = f"translate_status.md"
save_markdown_table(markdown_table, output_md_file)