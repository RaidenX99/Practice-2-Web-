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
        
        # Задача 1: Закон распределения ДСВ и нахождение неизвестной вероятности
        p1 = round(random.uniform(0.1, 0.2), 2)
        p2 = round(random.uniform(0.2, 0.3), 2)
        p3 = round(random.uniform(0.1, 0.2), 2)
        # Сумма должна быть равна 1.0, остаток идет на p4
        p4 = round(1.0 - (p1 + p2 + p3), 2)
        if p4 <= 0:
            p4 = 0.15
            p1 = 0.25
            p2 = 0.35
            p3 = 0.25
            
        variant['task_1'] = {
            'text': f"Дискретная случайная величина $X$ задана законом распределения:\n\n" \
                    f"| $X$ | 1 | 2 | 3 | 4 |\n" \
                    f"|---|---|---|---|---|\n" \
                    f"| $P$ | {p1} | {p2} | {p3} | $p_4$ |\n\n" \
                    f"Найдите значение вероятности $p_4$. (Ответ запишите с точностью до 2 знаков).",
            'answer': str(round(p4, 2))
        }

        # Задача 2: Математическое ожидание ДСВ
        x_vals = [2, 4, 6, 8]
        probs = [0.2, 0.3, 0.4, 0.1]
        # Перемешаем для индивидуальности
        math_exp = sum(x * p for x, p in zip(x_vals, probs))
        
        variant['task_2'] = {
            'text': f"Дан закон распределения ДСВ $X$:\n\n" \
                    f"| $X$ | {x_vals[0]} | {x_vals[1]} | {x_vals[2]} | {x_vals[3]} |\n" \
                    f"|---|---|---|---|---|\n" \
                    f"| $P$ | {probs[0]} | {probs[1]} | {probs[2]} | {probs[3]} |\n\n" \
                    f"Найдите математическое ожидание $M(X)$. (Ответ округлите до 2 знаков).",
            'answer': str(round(math_exp, 2))
        }

        # Задача 3: Дисперсия ДСВ
        # Вычислим M(X) и M(X^2)
        mx = sum(x * p for x, p in zip(x_vals, probs))
        mx2 = sum((x**2) * p for x, p in zip(x_vals, probs))
        dx = mx2 - (mx**2)
        
        variant['task_3'] = {
            'text': f"Используя данные предыдущей задачи ($M(X) = {mx}$), найдите дисперсию $D(X)$ случайной величины $X$. (Ответ округлите до 2 знаков).",
            'answer': str(round(dx, 2))
        }

        # Задача 4: Биномиальное распределение (число успехов)
        n_trials = random.randint(5, 8)
        p_success = round(random.uniform(0.3, 0.6), 2)
        k_success = random.randint(2, 4)
        
        # Формула Бернулли: C_n^k * p^k * q^(n-k)
        q = 1.0 - p_success
        comb_val = math.comb(n_trials, k_success)
        binom_prob = comb_val * (p_success ** k_success) * (q ** (n_trials - k_success))
        
        variant['task_4'] = {
            'text': f"Проводится серия из $n = {n_trials}$ независимых испытаний, в каждом из которых вероятность появления события равна $p = {p_success}$. Найти вероятность того, что событие появится ровно $k = {k_success}$ раза. (Ответ округлите до 4 знаков).",
            'answer': str(round(binom_prob, 4))
        }

        # Теоретический вопрос
        cq_pool = [
            "Что такое дискретная случайная величина и какими свойствами обладает ее закон распределения?",
            "Дайте определение математического ожидания дискретной случайной величины и опишите его механический смысл.",
            "Что характеризует дисперсия случайной величины? Какова связь между дисперсией и среднеквадратичным отклонением?",
            "Напишите формулу Бернулли и объясните условия ее применения в теории вероятностей."
        ]
        selected_q = random.choice(cq_pool)
        variant['task_99'] = {
            'title': 'Контрольный теоретический вопрос',
            'text': f"ОБЯЗАТЕЛЬНО прикрепите фото с развернутым рукописным ответом на вопрос:\n\n1. {selected_q}",
            'answer': 'Ручная проверка (Требуется фото)'
        }
        
        return variant

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

        def is_close(val1, val2, tol=0.01):
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
                    details[task_key] = {'is_correct': True, 'correct_answer': "Фото прикреплено", 'student_answer': f"Фото ({len(photo_list)} шт.)"}
                else:
                    details[task_key] = {'is_correct': False, 'correct_answer': "Требуется фото", 'student_answer': "Нет фото!"}
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
