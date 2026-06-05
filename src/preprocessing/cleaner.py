import re
import os


class TextCleaner:

    def __init__(self):
        pass

    def remove_extra_spaces(self, text):
        return re.sub(r"[ \t]+", " ", text)

    def remove_multiple_newlines(self, text):
        return re.sub(r"\n{2,}", "\n", text)

    def remove_special_characters(self, text):
        text = re.sub(r"[^\x00-\x7F]+", " ", text)
        return text

    def remove_duplicate_lines(self, text):

        seen = set()
        cleaned_lines = []

        for line in text.split("\n"):

            line = line.strip()

            if not line:
                continue

            if line not in seen:
                cleaned_lines.append(line)
                seen.add(line)

        return "\n".join(cleaned_lines)

    def clean_text(self, text):

        text = self.remove_special_characters(text)

        text = self.remove_duplicate_lines(text)

        text = self.remove_multiple_newlines(text)

        text = self.remove_extra_spaces(text)

        return text.strip()
    


def process_text_folder(
    input_folder,
    output_folder
):

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    cleaner = TextCleaner()

    for file_name in os.listdir(input_folder):

        if not file_name.endswith(".txt"):
            continue

        input_path = os.path.join(
            input_folder,
            file_name
        )

        with open(
            input_path,
            "r",
            encoding="utf-8"
        ) as file:

            raw_text = file.read()

        cleaned_text = cleaner.clean_text(
            raw_text
        )

        output_path = os.path.join(
            output_folder,
            file_name
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(cleaned_text)

        print(f" Cleaned: {file_name}")