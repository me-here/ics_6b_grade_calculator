# Author: Mihir Thanekar
# Run this file as a script by typing python grade_calculator.py in the terminal.
# Make sure to copy your grades from gradescope into the grades_from_gradescope.txt file.
_PATH_TO_GRADESCOPE = 'grades_from_gradescope.txt'


class CategoryCalculator:
    '''Calculates the grade for a specific category.'''

    def __init__(self, description):
        self._numerator = 0
        self._denominator = 0
        self._description = description

    def add_assignment(self, numerator: float, denominator: float) -> None:
        self._numerator += numerator
        self._denominator += denominator

    def calculate_percentage(self) -> float:
        if self._denominator == 0:
            raise ValueError('How come you have no assignments?')
        return self._numerator / self._denominator

    def description(self) -> str:
        return self._description


class GradeCalculator:
    def __init__(self):
        self._total_grade = 0
        self._homework_calculator = CategoryCalculator('HW')
        self._quiz_calculator = CategoryCalculator('Quiz')
        self._current_category_calculator = None
        self._current_assignment_number = 0

    def _calculate_gradescope(self) -> None:
        with open(_PATH_TO_GRADESCOPE) as file:
            for line in file:
                self._update_current_calculator_with(line)
                self._add_assignment_if_parseable(line)

    def calculate_grades(self) -> None:
        lectures = float(input('Lecture grade: ')) * 0.09
        participation = float(input('Participation grade: ')) * 0.07
        challenge_activities = float(
            input('Challenge activities grade: ')) * 0.06

        readings = float(input('Reading grade: ')) * 0.09
        tests = float(input('Test Grade: ')) * 0.4
        evaluations = 1  # assuming you completed your evaluations.

        self._calculate_gradescope()
        quizzes = self._quiz_calculator.calculate_percentage() * 100 * 0.09
        homeworks = self._homework_calculator.calculate_percentage() * 100 * 0.09
        self._total_grade = lectures + participation + \
            challenge_activities + readings + tests + evaluations + quizzes + homeworks
        print(f'Your total grade (before the final) is {self._total_grade}')
        print('Do not panic, this is your grade if you did not take the final.')
        min_final_grade_to_get_a_90 = 10 * (90 - self._total_grade)
        print(
            f'You can get a 90 in the class by getting a {round(min_final_grade_to_get_a_90, 2)}% on the final')
        print('Happy studying!')

    def _add_assignment_if_parseable(self, line: str) -> None:
        try:
            numerator, denominator = line.split('/')
            numerator, denominator = float(
                numerator), float(denominator)
        except:
            pass
        else:
            if self._current_category_calculator == self._quiz_calculator:
                if self._current_assignment_number >= 4:
                    numerator = min(numerator, 5)
                    denominator = 5
            self._current_category_calculator.add_assignment(
                numerator, denominator)

    def _update_current_calculator_with(self, line: str) -> None:
        if line.startswith(self._homework_calculator.description()):
            self._current_category_calculator = self._homework_calculator
        elif line.startswith(self._quiz_calculator.description()):
            self._current_category_calculator = self._quiz_calculator
        try:
            self._current_assignment_number = int(line.split()[-1])
        except:
            pass


if __name__ == '__main__':
    GradeCalculator().calculate_grades()
