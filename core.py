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
        variant['task_5'] = self._task_5_bernoulli_range()
        variant['task_6'] = self._task_6_bernoulli_majority()
        variant['task_7'] = self._task_7_binomial_props()
        variant['task_8'] = self._task_8_find_n()
        
        cq_pool = [
            "Сформулируйте условия применения схемы независимых испытаний Бернулли.",
            "Запишите формулу Бернулли и объясните физический смысл каждого ее параметра.",
            "Что такое «наивероятнейшее число наступлений события» и как оно вычисляется по формуле?",
            "Что называют биномиальным законом распределения?",
            "Чему равны математическое ожидание и дисперсия случайной величины, распределенной по биномиальному закону?",
            "Как вычислить вероятность того, что в n испытаниях событие наступит хотя бы один раз?",
            "Как по формуле Бернулли вычислить вероятность того, что событие наступит не менее k1 и не более k2 раз?",
            "Чем отличаются зависимые испытания от независимых? Приведите пример из инфокоммуникаций."
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
        ans = 1 - (p_fail ** N)
        return {'text': text, 'answer': str(round(ans, 4))}

    def _task_3_bernoulli_less_than(self):
        N = random.randint(5, 7)
        p = round(random.uniform(0.1, 0.3), 2)
        text = f"Отдел кибербезопасности проверяет {N} узлов сети. Вероятность обнаружить уязвимость на каждом узле равна {p}. Найти вероятность того, что уязвимость будет найдена НЕ БОЛЕЕ ЧЕМ на 2 узлах (то есть 0, 1 или 2). (Ответ округлите до 4 знаков)"
        ans = sum([math.comb(N, k) * (p**k) * ((1 - p)**(N - k)) for k in range(3)])
        return {'text': text, 'answer': str(round(ans, 4))}

    def _task_4_most_probable(self):
        N = random.randint(15, 30)
        p = round(random.uniform(0.15, 0.45), 2)
        while ((N + 1) * p).is_integer():
            N = random.randint(15, 30)
            p = round(random.uniform(0.15, 0.45), 2)
        
        k0 = math.floor((N + 1) * p)
        text = f"Заведующий лабораториями тестирует партию из {N} Wi-Fi адаптеров. Вероятность того, что адаптер не пройдет стресс-тест, составляет {p}. Найти наивероятнейшее число адаптеров, не прошедших тест, используя соответствующую формулу."
        return {'text': text, 'answer': str(k0)}

    def _task_5_bernoulli_range(self):
        N = random.randint(6, 9)
        K1 = random.randint(2, 3)
        K2 = random.randint(4, 5)
        p = round(random.uniform(0.4, 0.7), 2)
        text = f"Система мониторинга опрашивает {N} датчиков температуры в серверной стойке. Вероятность успешного ответа от любого датчика равна {p}. Найти вероятность того, что на запрос ответят от {K1} до {K2} датчиков включительно. (Ответ округлите до 4 знаков)"
        ans = sum([math.comb(N, k) * (p**k) * ((1 - p)**(N - k)) for k in range(K1, K2 + 1)])
        return {'text': text, 'answer': str(round(ans, 4))}

    def _task_6_bernoulli_majority(self):
        N = random.choice([5, 7, 9])
        majority = (N + 1) // 2
        p = round(random.uniform(0.75, 0.95), 2)
        text = f"Кластер баз данных состоит из {N} узлов. Для принятия решения (консенсуса) необходимо, чтобы активно работало строгое большинство узлов (то есть {majority} и более). Вероятность доступности одного узла равна {p}. Какова вероятность успешного достижения консенсуса? (Ответ округлите до 4 знаков)"
        ans = sum([math.comb(N, k) * (p**k) * ((1 - p)**(N - k)) for k in range(majority, N + 1)])
        return {'text': text, 'answer': str(round(ans, 4))}

    def _task_7_binomial_props(self):
        N = random.randint(20, 80)
        p = round(random.uniform(0.4, 0.8), 2)
        text = f"Случайная величина X — число успешно доставленных IP-пакетов из {N} отправленных. Вероятность доставки одного пакета p = {p}. В ответе запишите через пробел два числа: математическое ожидание M(X) и дисперсию D(X). (Пример: 45.5 12.2)"
        mx = N * p
        dx = N * p * (1 - p)
        return {'text': text, 'answer': f"{round(mx, 2)} {round(dx, 2)}"}

    def _task_8_find_n(self):
        p = round(random.uniform(0.15, 0.35), 2)
        P_min = round(random.uniform(0.95, 0.99), 2)
        text = f"Вероятность успешной авторизации на RADIUS-сервере при одной попытке равна {p}. Какое минимальное число попыток N нужно совершить инженеру, чтобы с вероятностью не менее {P_min} авторизоваться ХОТЯ БЫ ОДИН раз? (Укажите целое число)"
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
            if ' ' in str(val1) and ' ' in str(val2):
                parts1 = str(val1).split()
                parts2 = str(val2).split()
                if len(parts1) == len(parts2):
                    return all(abs(float(p1) - float(p2)) <= tol for p1, p2 in zip(parts1, parts2))
                return False
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
