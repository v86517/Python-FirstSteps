import multiprocessing
import time
import random
import os
from prettytable import PrettyTable

class Question:
    def __init__(self, question_text):
        self.text = question_text

class Person:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

class Student(Person):
    def __init__(self, name, gender):
        Person.__init__(self, name, gender)
        self.name = name
        self.gender = gender
        self.status = 'Очередь'  # Варианты: Очередь, Сдал, Провалил
        self.exam_start = None
        self.exam_finish = None
        self.result = None

class Examiner(Person):
    def __init__(self, name, gender):
        Person.__init__(self, name, gender)
        self.name = name
        self.gender = gender
        self.current_student = "-"
        self.number_students = 0
        self.failed_students_cnt = 0
        self.work_time = 0.0
        self.take_break = False

def create_student(line: str):
    name_gender = line.strip().split()
    return Student(name_gender[0], name_gender[1])

def create_examiner(line: str):
    name_gender = line.strip().split()
    return Examiner(name_gender[0], name_gender[1])

def calc_prob(n, gender):
    prob_list = []
    balance = 1.0
    for i in range(n - 1):
        p = balance / 1.168
        prob_list.append(p)
        balance -= p
    prob_list.append(balance)
    if gender == 'Ж':
        prob_list.reverse()
    return prob_list

# выбор слова из списка words со своими вероятностями
def select_word(words, gen):
    probs = calc_prob(len(words), gen)
    return random.choices(words, weights=probs, k=1)[0]

# выбор ответа/ответов экзаменатором
def examiner_select_words(words):
    available = words.copy()
    selected = []
    if available:
        word = random.choice(available)
        selected.append(word)
        available.remove(word)
        while available and random.random() < 1/3:
            word = random.choice(available)
            selected.append(word)
            available.remove(word)
    return selected

def simulate_exam(student, questions_list, best_questions):
    correct_answer = 0
    wrong_answer = 0
    if len(questions_list) >= 3:
        questions = random.sample(questions_list, k=3)
    else:
        questions = [random.choice(questions_list) for _ in range(3)]
    for i in questions:
        words_list = i.text.split()
        if i.text not in best_questions:
            best_questions[i.text] = 0
        student_answer = select_word(words_list, student.gender)
        correct_answers = examiner_select_words(words_list)
        if student_answer in correct_answers:
            correct_answer += 1
            best_questions[i.text] = best_questions[i.text] + 1 if i.text in best_questions else 1
        else:
            wrong_answer += 1
    examiner_mood = random.random()
    if examiner_mood < 1/8:
        exam_result = "Провалил"
    elif examiner_mood < 1/4:
        exam_result = "Сдал"
    else:
        exam_result = "Сдал" if correct_answer > wrong_answer else "Провалил"
    return exam_result

def examiner_process(ns, examiner, student_queue, shared_students, shared_questions, best_questions):
    while True:
        student_name = student_queue.get() #student_queue - очередь из списка студентов и тремя None
        if student_name is None:
            break
        student = None
        for i in shared_students:
            if i['name'] == student_name:
                student = i
                break
        examiner['current_student'] = student['name']
        student['exam_start'] = time.time() - ns.exam_start_time
        exam_duration = (len(examiner['name'])) + random.uniform(-1, 1)
        time.sleep(exam_duration)
        temp_student = create_student(str(student['name'])+' '+str(student['gender']))
        exam_result = simulate_exam(temp_student, list(shared_questions), best_questions)
        student['exam_finish'] = time.time() - ns.exam_start_time
        student['result'] = exam_result
        student['status'] = exam_result
        examiner['number_students'] += 1
        if exam_result == 'Провалил':
            examiner['failed_students_cnt'] += 1
        examiner['work_time'] += exam_duration
        examiner['current_student'] = '-'
        if (not examiner['take_break']) and ((time.time() - ns.exam_start_time) >= 30):
            examiner['take_break'] = True
            examiner['current_student'] = 'Обед'
            time.sleep(random.uniform(12, 18))
            examiner['current_student'] = '-'
    examiner['current_student'] = '-'

def print_process(shared_students, shared_examiners, student_queue, ns):
    while ns.simulation or not student_queue.empty():
        os.system('cls' if os.name == 'nt' else 'clear')
        stud_status_tab = PrettyTable()
        stud_status_tab.field_names = ["Студент", "Статус"]
        #order = {"Очередь": 0, "В процессе": 0, "Сдал": 1, "Провалил": 2}
        order = {"Очередь": 0, "Сдал": 1, "Провалил": 2}
        sorted_students = sorted(shared_students, key=lambda s: order.get(s['status']))
        for i in sorted_students:
            stud_status_tab.add_row([i['name'], i['status']])
        print(stud_status_tab)
        print()

        examiners_tab = PrettyTable()
        examiners_tab.field_names = ["Экзаменатор", "Текущий студент", "Всего студентов", "Завалил", "Время работы"]
        for i in shared_examiners:
            current = i['current_student'] if i['current_student'] else "-"
            examiners_tab.add_row([i['name'], current, i['number_students'], i['failed_students_cnt'], f"{i['work_time']:.2f}"])
        print(examiners_tab)
        print()

        remaining = len([i for i in shared_students if i['status'] == "Очередь"])
        total = len(shared_students)
        print(f"Осталось в очереди: {remaining} из {total}")
        elapsed = time.time() - ns.exam_start_time
        print(f"Время с момента начала экзамена: {elapsed:.2f} секунд")
        time.sleep(1)

def exam_summary(ns, shared_examiners, shared_students, best_questions):
    os.system('cls' if os.name == 'nt' else 'clear')
    stud_status_tab = PrettyTable()
    stud_status_tab.field_names = ["Студент", "Статус"]
    passed = [i for i in shared_students if i['result'] == "Сдал"]
    failed = [i for i in shared_students if i['result'] == "Провалил"]
    sorted_students = passed + failed
    for i in sorted_students:
        stud_status_tab.add_row([i['name'], i['result']])
    print(stud_status_tab)
    print()

    examiners_tab = PrettyTable()
    examiners_tab.field_names = ["Экзаменатор", "Всего студентов", "Завалил", "Время работы"]
    for i in shared_examiners:
        examiners_tab.add_row([i['name'], i['number_students'], i['failed_students_cnt'], f"{i['work_time']:.2f}"])
    print(examiners_tab)
    print()

    total_time = time.time() - ns.exam_start_time
    print(f"Время с момента начала экзамена и до его завершения: {total_time:.2f} секунд")


    if passed:
        best_time = min(i['exam_finish'] for i in passed if i['exam_finish'] is not None)
        best_students = [i['name'] for i in passed if abs(i['exam_finish'] - best_time) < 0.01]
        print("Имена лучших студентов: " + ", ".join(best_students))
    else:
        print("Имена лучших студентов: -")

    best_examiners = []
    best_fail_rate = 1.0
    for i in shared_examiners:
        if i['number_students'] > 0:
            fail_rate = i['failed_students_cnt'] / i['number_students']
            if fail_rate < best_fail_rate:
                best_fail_rate = fail_rate
                best_examiners = [i['name']]
            elif abs(fail_rate - best_fail_rate) < 1e-6:
                best_examiners.append(i['name'])
    if best_examiners:
        print("Имена лучших экзаменаторов: " + ", ".join(best_examiners))
    else:
        print("Имена лучших экзаменаторов: -")

    if failed:
        earliest_fail = min(i['exam_finish'] for i in failed if i['exam_finish'] is not None)
        expelled = [i['name'] for i in failed if abs(i['exam_finish'] - earliest_fail) < 0.01]
        print("Имена студентов, которых после экзамена отчислят: " + ", ".join(expelled))
    else:
        print("Имена студентов, которых после экзамена отчислят: -")

    if best_questions:
        max_correct = max(best_questions.values())
        best_qs = [i for i, cnt in best_questions.items() if cnt == max_correct]
        print("Лучшие вопросы: " + ", ".join(best_qs))
    else:
        print("Лучшие вопросы: -")
    number_students = len(shared_students)
    passed_cnt = len(passed)
    success_rate = passed_cnt / number_students if number_students > 0 else 0
    total_result = "экзамен удался" if success_rate > 0.85 else "экзамен не удался"
    print("Вывод: " + total_result)

def main():
    mgr = multiprocessing.Manager()
    shared_examiners = mgr.list()
    shared_students = mgr.list()
    shared_questions = mgr.list()

    def append_shared_lists(file_name, shared_list_name):
        with open(file_name, encoding="utf-8") as f_in:
            lines = list(filter(lambda l: l.strip(), f_in.readlines()))
            for line in lines:
                if file_name == 'examiners.txt':
                    examiner = create_examiner(line)
                    shared_list_name.append(mgr.dict(vars(examiner)))
                if file_name == 'students.txt':
                    stud = create_student(line)
                    shared_list_name.append(mgr.dict(vars(stud)))
                if file_name == 'questions.txt':
                    Question(line.strip())
                    shared_questions.append(Question(line.strip()))

    append_shared_lists('examiners.txt', shared_examiners)
    append_shared_lists('students.txt', shared_students)
    append_shared_lists('questions.txt', shared_questions)
    best_questions = mgr.dict()

    ns = mgr.Namespace()
    ns.exam_start_time = time.time()
    ns.simulation = True

    # добавляем студентов в очередь и добавляем столько None сколько экзаменаторов
    student_queue = multiprocessing.Queue()
    for i in shared_students:
        student_queue.put(i['name'])
    for _ in range(len(shared_examiners)):
        student_queue.put(None)

    # запускаем дочерний процесс вывода
    print_proc = multiprocessing.Process(target=print_process,
                                         args=(shared_students, shared_examiners, student_queue, ns))
    print_proc.start()

    # запускаем дочерние процессы экзамена
    examiner_processes = []
    for i in shared_examiners:
        p = multiprocessing.Process(target= examiner_process,
                                    args=(ns, i, student_queue, shared_students, shared_questions, best_questions))
        p.start()
        examiner_processes.append(p)

    # устанавливаем ожидание окончания работы дочерних процессов
    for i in examiner_processes:
        i.join()

    ns.simulation = False
    print_proc.join()

    exam_summary(ns, shared_examiners, shared_students, best_questions)

if __name__ == '__main__':
    main()
