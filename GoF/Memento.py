"""This code demonstrates a possible implementation of the Memento pattern in Python
Let's say we want to have a story of some actions and we also want to be able to undo and redo our actions"""


class Memento:
    def __init__(self, content):
        self.content = content


class TextEditor:
    def __init__(self):
        self.content = str()

    def write(self, string):
        self.content = string

    def save(self):
        return Memento(self.content)

    def undo(self, memento):
        self.content = memento.content


class History:
    def save(self, editor_):
        self.obj = editor_.save()

    def undo(self, editor_):
        editor_.undo(self.obj)


if __name__ == '__main__':
    history = History()

    editor = TextEditor()

    editor.write("Hello world")
    print(editor.content + '\n')

    history.save(editor)

    editor.write("How are you?")

    print(editor.content + '\n')

    history.undo(editor)

    print(editor.content + '\n')
