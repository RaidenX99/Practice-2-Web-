# -*- coding: utf-8 -*-
import random
import math
import hashlib
import json

SECRET_SALT = "Ural_Telecom_2026_Secret"

class PracticeEngine:
    def __init__(self, student_id: str):
        self.student_id = student_id.strip().upper()
        self.seed = self._generate_seed()
        random.seed(self.seed)

    def _generate_seed(self):
        hash_obj = hashlib.md5(self.student_id.encode())
        return int(hash_obj.hexdigest(), 16)

    def generate_variant(self) -> dict:
        variant = {}
        
        variant['task_1'] = self._task_1_bernoulli_exact()
        variant['task_2'] = self._task_2_bernoulli_at_least_one()
        variant['task_3'] = self._task_3_bernoulli_less_than()
        variant['task_4'] = self._task_4_most_probable()
        variant['task_5'] = self._task_5_poisson_exact()
        variant['task_6'] = self._task_6_poisson_at_least()
        variant['task_7'] = self._task_7_binomial_props()
        variant['task_8'] = self._task_8_find_n()
        
        cq_pool = [
            "Сформулируйте условия применения схемы независимых испытаний Бернулли.",
            "Запишите формулу Бернулли и объясните физический смысл каждого ее параметра.",
            "При каких условиях формула Бернулли заменяется приближенной формулой Пуассона?",
            "Что такое «наивероятнейшее число наступлений события» и как оно вычисляется?",
            "В каких случаях применяется локальная теорема Муавра-Лапласа? Запишите её формулу.",
            "Объясните суть интегральной теоремы Муавра-Лапласа. Для чего используется функция Лапласа Ф(x)?",
            "Чему равны математическое ожидание и дисперсия случайной величины, распределенной по биномиальному закону?",
            "Как вычислить вероятность того, что в n испытаниях событие наступит хотя бы один раз?"
        ]
        
        selected_questions = random.sample(cq_pool, 3)
        questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(selected_questions)])
        
        variant['task_99'] = {
            'title': 'Контрольные теоретические вопросы (Схема Бернулли)',
            'text': f"ОБЯЗАТЕЛЬНО прикрепите фото с развернутым рукописным ответом на следующие вопросы:\n\n{questions_text}",
            'answer': 'Ручная проверка (Требуется фото)'
        }
        
        return variant

    def _task_1_bernoulli_exact(self):
        N = random.randint(5, 12)
        K = random.randint(2, N - 2)
        p = round(random.uniform(0.6, 0.9), 2)
        text = f"В серверной УрТИСИ работают {N} независимых коммутаторов. Вероятность того, что коммутатор проработает месяц без сбоев, равна {p}. Найти вероятность того, что за месяц без сбоев отработают ровно {K} коммутаторов. (Ответ округлите до 4 знаков)"
        ans = math.comb(N, K) * (p**K) * ((1 - p)**(N - K))
        return {'text': text, 'answer': str(round(ans, 4))}

    def _task_2_bernoulli_at_least_one(self):
        N = random.randint(4, 8)
        p_fail = round(random.uniform(0.05, 0.2), 2)
        text = f"Пакет данных передается по {N} независимым резервным каналам. Вероятность потери пакета в каждом канале равна {p_fail}. Найти вероятность того, что пакет будет успешно доставлен ХОТЯ БЫ ПО ОДНОМУ каналу. (Ответ округлите до 4 знаков)"
        # Вероятность хотя бы одной успешной доставки = 1 - вероятность потери во всех каналах
        ans = 1 - (p_fail ** N)
        return {'text': text, 'answer': str(round(ans, 4))}

    def _task_3_bernoulli_less_than(self):
        N = random.randint(5, 7)
        p = round(random.uniform(0.1, 0.3), 2)
        text = f"Отдел кибербезопасности проверяет {N} узлов сети. Вероятность обнаружить уязвимость на каждом узле равна {p}. Найти вероятность того, что уязвимость будет найдена НЕ БОЛЕЕ ЧЕМ на 2 узлах. (Ответ округлите до 4 знаков)"
        ans = sum([math.comb(N, k) * (p**k) * ((1 - p)**(N - k)) for k in range(3)])
        return {'text': text, 'answer': str(round(ans, 4))}

    def _task_4_most_probable(self):
        N = random.randint(150, 300)
        p = round(random.uniform(0.02, 0.15), 2)
        while ((N + 1) * p).is_integer(): # Исключаем ситуацию с двумя ответами
            N = random.randint(150, 300)
            p = round(random.uniform(0.02, 0.15), 2)
        
        k0 = math.floor((N + 1) * p)
        text = f"Заведующий лабораториями закупил партию из {N} Raspberry Pi. Вероятность заводского брака для каждой платы составляет {p}. Найти наивероятнейшее число бракованных плат в партии."
        return {'text': text, 'answer': str(k0)}

    def _task_5_poisson_exact(self):
        N = random.choice([1000, 2000, 5000])
        p = round(random.uniform(0.001, 0.005), 4)
        K = random.randint(2, 6)
        lam = N * p
        text = f"Магистральный маршрутизатор обрабатывает {N} пакетов в секунду. Вероятность отбрасывания одного пакета крайне мала и равна p = {p}. Используя формулу Пуассона, найти вероятность того, что будет отброшено ровно {K} пакета. (Ответ округлите до 4 знаков)"
        ans = ((lam**K) / math.factorial(K)) * math.exp(-lam)
        return {'text': text, 'answer': str(round(ans, 4))}

    def _task_6_poisson_at_least(self):
        N = random.choice([500, 800, 1500])
        p = round(random.uniform(0.002, 0.008), 4)
        lam = N * p
        text = f"Среди {N} строк программного кода вероятность критической ошибки в одной строке равна {p}. Используя формулу Пуассона, найти вероятность того, что в коде содержится ХОТЯ БЫ ОДНА критическая ошибка. (Ответ округлите до 4 знаков)"
        ans = 1 - math.exp(-lam) # 1 - P(0)
        return {'text': text, 'answer': str(round(ans, 4))}

    def _task_7_binomial_props(self):
        N = random.randint(50, 200)
        p = round(random.uniform(0.4, 0.8), 2)
        text = f"Случайная величина X — число успешно доставленных сообщений из {N} отправленных. Вероятность доставки одного сообщения p = {p}. В ответе запишите через пробел два числа: математическое ожидание M(X) и дисперсию D(X). (Пример: 45.5 12.2)"
        mx = N * p
        dx = N * p * (1 - p)
        return {'text': text, 'answer': f"{round(mx, 2)} {round(dx, 2)}"}

    def _task_8_find_n(self):
        p = round(random.uniform(0.15, 0.35), 2)
        P_min = round(random.uniform(0.95, 0.99), 2)
        text = f"Вероятность успешной авторизации на RADIUS-сервере при одной попытке равна {p}. Какое минимальное число попыток N нужно совершить инженеру, чтобы с вероятностью не менее {P_min} авторизоваться ХОТЯ БЫ ОДИН раз? (Укажите целое число)"
        # 1 - (1-p)^N >= P_min -> (1-p)^N <= 1 - P_min
        ans = math.ceil(math.log(1 - P_min) / math.log(1 - p))
        return {'text': text, 'answer': str(ans)}

    @staticmethod
    def generate_security_hash(student_id: str, student_answers: dict) -> str:
        answers_str = json.dumps(student_answers, sort_keys=True)
        raw_data = f"{student_id}_{answers_str}_{SECRET_SALT}"
        return hashlib.sha256(raw_data.encode('utf-8')).hexdigest()

    def check_answers(self, student_answers: dict) -> dict:
        variant = self.generate_variant()
        correct_count = 0
        total_count = len(variant)
        details = {}

        def is_close(val1, val2, tol=0.002):
            # Если это строка с пробелом (как в Задаче 7: "M(X) D(X)")
            if ' ' in str(val1) and ' ' in str(val2):
                parts1 = str(val1).split()
                parts2 = str(val2).split()
                if len(parts1) == len(parts2):
                    return all(abs(float(p1) - float(p2)) <= tol for p1, p2 in zip(parts1, parts2))
                return False
            # Если это одно число
            try:
                return abs(float(val1) - float(val2)) <= tol
            except ValueError:
                return str(val1).strip().lower() == str(val2).strip().lower()

        for task_key, task_data in variant.items():
            photo_list = student_answers.get(f"{task_key}_photo", [])
            has_photo = bool(photo_list)
            
            student_ans_str = student_answers.get(task_key, "").strip().replace(',', '.')
            correct_ans_str = str(task_data.get('answer', ''))
            
            if task_key == 'task_99':
                if has_photo:
                    is_correct = True
                    correct_count += 1
                    details[task_key] = {
                        'is_correct': True, 'correct_answer': "Фото прикреплено",
                        'student_answer': f"Фото ({len(photo_list)} шт.)"
                    }
                else:
                    details[task_key] = {
                        'is_correct': False, 'correct_answer': "Требуется фото",
                        'student_answer': "Нет фото!"
                    }
                continue

            is_correct = is_close(student_ans_str, correct_ans_str)

            if not has_photo:
                is_correct = False
                student_ans_str = f"{student_ans_str} (Нет фото!)" if student_ans_str else "Нет ответа (Нет фото!)"

            if is_correct: correct_count += 1
            details[task_key] = {'is_correct': is_correct, 'correct_answer': correct_ans_str, 'student_answer': student_ans_str}

        score_percent = (correct_count / total_count) * 100
        if score_percent >= 85: mark = 5
        elif score_percent >= 70: mark = 4
        elif score_percent >= 50: mark = 3
        else: mark = 2

        photos_dict = {k: student_answers.get(f"{k}_photo") for k in variant.keys() if student_answers.get(f"{k}_photo")}

        return {
            'correct_count': correct_count,
            'total_count': total_count,
            'percent': round(score_percent, 1),
            'mark': mark,
            'details': details,
            'photos': photos_dict
        }