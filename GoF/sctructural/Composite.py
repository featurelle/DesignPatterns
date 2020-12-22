from abc import ABC, abstractmethod


class TodoList(ABC):

    @abstractmethod
    def make_html(self):
        pass


class Todo(TodoList):

    def __init__(self, task: str):
        self.task = task

    def make_html(self):
        return f'<input type="checkbox">{self.task}'


class Project(TodoList):

    def __init__(self, name: str, stages: list[TodoList]):
        self.name = name
        self.stages = stages

    def make_html(self):
        html = f'<h1>{self.name}</h1>\n<ul>\n'
        for stage in self.stages:
            html += f'\t<li>{stage.make_html()}</li>\n'
        return html + '</ul>\n'


def demo():
    work = [Todo('Wake up'),
            Todo('Go to work'),
            Todo('Survive'),
            Todo('Go Home'),
            Todo('Sleep'),
            Todo('Repeat')]

    project1 = Project('Work', work)
    task1 = Todo('Buy food')
    task2 = Todo('Weekend party')

    bigger_project = [project1, task1, task2]

    project2 = Project('4 days plan', bigger_project)

    print(project1.make_html())
    print('\n\n')
    print(project2.make_html())


if __name__ == "__main__":
    demo()
