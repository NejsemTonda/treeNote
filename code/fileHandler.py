import config
import os
from convertor import convert


class FileHandler:
    def __init__(self):
        self.opened_file = None
        self.edit_file = "edit" + config.ext

        if not os.path.exists(self.edit_file):
            raise FileNotFoundError(config.no_init_msg)

    def changed_to_file(self, file_name):

        if self.opened_file is not None:
            self.save_current_file()
        self.load_file(f"notes/{file_name}{config.ext}")

    def save_current_file(self):
        file = NoteFile(self.edit_file)
        # if topic changed, delete old file
        if file.path != self.opened_file:
            delete_file(self.opened_file)

        convert(file.path)
        file.dump()

    def load_file(self, file_path):
        file = NoteFile(file_path)
        file.dump(dest=self.edit_file)
        self.opened_file = file.path

    def get_current_topic(self):
        with open(self.edit_file, "r") as file:
            name = file.readline()[1:].strip()
            return name


def delete_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    else:
        print(f"Tried to delete {file_name}, but the file doesn't exist.")


def check_for_delete(node):
    for n in node.childs:
        if n.name.lower() in ["delete", "del"]:
            node.childs.remove(n)
            return


def get_correct_name(topic):
    new_path = config.notes_dir + topic + "{}" + config.ext

    x = ""
    while os.path.exists(new_path.format(x)):
        x = 1 if x == "" else x + 1

    return topic + str(x)


def create_file(topic):
    with open(config.notes_dir + topic + config.ext, "w") as file:
        file.write("# " + topic)


def init_files():
    dir_name = os.path.basename(os.getcwd())
    if not os.path.exists(config.notes_dir):
        os.makedirs(config.notes_dir)

    if not os.path.exists(config.notes_dir + dir_name):
        create_file(dir_name)

    if not os.path.exists(config.cache_dir):
        os.makedirs(config.cache_dir)

    if not os.path.exists(f"edit{config.ext}"):
        open(f"edit{config.ext}", "w").close()

    if not os.path.exists(".session"):
        open(f".session", "w").close()


class NoteFile:
    def __init__(self, name):
        self.topic = None
        self.content = ""
        with open(name, "r") as file:
            while line := file.readline():
                if not self.topic:
                    self.topic = line[1:].strip()
                self.content += line
        self.topic = "unnamed" if not self.topic else self.topic
        self.path = f"notes/{self.topic}{config.ext}"

    def dump(self, dest=None):
        if not dest:
            dest = self.path
        with open(dest, "w") as save_to:
            save_to.write(self.content)
