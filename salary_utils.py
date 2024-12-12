def predict_salary(salary_from, salary_to):
    if salary_from is None and salary_to is not None:
        return salary_to * 0.8
    elif salary_from is not None and salary_to is None:
        return salary_from * 1.2
    elif salary_from is not None and salary_to is not None:
        return (salary_from + salary_to) / 2
    return None
