import random


class CourseFactory:
    def __init__(self, courses_factory=None):
        self.course_factory = courses_factory

    def show_course(self):
        course = self.course_factory()

        print(f'We have a course named {course}')
        print(f'its price is {course.fee()}')


class Course1:
    def fee(self):
        return 11000

    def __str__(self):
        return "DSA"


class Course2:
    def fee(self):
        return 8000

    def __str__(self):
        return "STL"


class Course3:
    def fee(self):
        return 15000

    def __str__(self):
        return 'SDE'


def random_course():
    return random.choice([Course3, Course2, Course1])()


if __name__ == "__main__":

    course = CourseFactory(random_course)

    for _ in range(5):
        course.show_course()
