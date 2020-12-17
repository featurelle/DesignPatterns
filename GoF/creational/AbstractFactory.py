import random


class CourseFactory:
    def __init__(self, courses_factory=None):
        self.course_factory = courses_factory

    def show_course(self):
        course = self.course_factory()

        print(f'We have a course named {course}')
        print(f'its price is {course.fee()}')


class DSA:
    def fee(self):
        return 11000

    def __str__(self):
        return "DSA"


class STL:
    def fee(self):
        return 8000

    def __str__(self):
        return "STL"


class SDE:
    def fee(self):
        return 15000

    def __str__(self):
        return 'SDE'


def random_course():
    return random.choice([SDE, STL, DSA])()


if __name__ == "__main__":

    course = CourseFactory(random_course)

    for _ in range(5):
        course.show_course()
