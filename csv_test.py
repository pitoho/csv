import csv
import pytest
import os

@pytest.fixture
def original_data():
    data = {}
    with open('files/grades.csv', mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            last_name = row['Last name'].strip()
            first_name = row['First name'].strip()
            ssn = row['SSN'].strip()
            tests = [float(row[f'Test{i}']) for i in range(1, 5)]
            valid_tests = [test for test in tests if test >= 0]

            if valid_tests:
                average_grade = sum(valid_tests) / len(valid_tests)
            else:
                average_grade = 0.0

            data[(last_name, first_name, ssn)] = average_grade

    return data

@pytest.fixture
def generated_data():
    data = {}
    with open('files/new.csv', mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            last_name = row['Last name'].strip()
            first_name = row['First name'].strip()
            ssn = row['SSN'].strip()
            average_grade = float(row['Average Grade'])
            data[(last_name, first_name, ssn)] = average_grade

    return data

def test_generated_csv_matches_original(original_data, generated_data):
    assert original_data == generated_data, "Данные в CSV не совпадают с оригиналом"

def test_generated_csv_exists():
    assert os.path.exists('files/new.csv'), "Созданый CSV файл не существует"

def test_generated_csv_structure():
    with open('files/new.csv', mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        assert csv_reader.fieldnames == ['Last name', 'First name', 'SSN', 'Average Grade'], "CSV структуры не совпадают"

def test_empty_average_grades(original_data):
    empty_grades = [avg for avg in original_data.values() if avg == 0.0]
    assert not empty_grades, f" {len(empty_grades)} пустая средняя длина"

def test_valid_average_grades(original_data):
    invalid_grades = [avg for avg in original_data.values() if not (0.0 <= avg <= 100.0)]
    assert not invalid_grades, f" {len(invalid_grades)} неправильная средняя длина"

def test_original_csv_exists():
    assert os.path.exists('files/grades.csv'), "Изначальный CSV файл не существует"
