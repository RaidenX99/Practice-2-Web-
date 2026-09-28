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
        rng = random.Random(self.seed)
        pool = []

        # --- БЛОК 1: Законы распределения ДСВ и неизвестные вероятности (Задачи 1 - 5) ---
        
        # Задача 1
        p1_1 = round(rng.uniform(0.1, 0.2), 2)
        p1_2 = round(rng.uniform(0.2, 0.3), 2)
        p1_3 = round(rng.uniform(0.1, 0.2), 2)
        p1_4 = round(1.0 - (p1_1 + p1_2 + p1_3), 2)
        if p1_4 <= 0:
            p1_1, p1_2, p1_3, p1_4 = 0.2, 0.3, 0.2, 0.3
        pool.append({
            'text': f"Дискретная случайная величина $X$ задана законом распределения:\n\n| $X$ | 1 | 2 | 3 | 4 |\n|---|---|---|---|---|\n| $P$ | {p1_1} | {p1_2} | {p1_3} | $p_4$ |\n\nНайдите значение неизвестной вероятности $p_4$. (Округление до 2 знаков).",
            'answer': str(round(p1_4, 2))
        })

        # Задача 2
        p2_1 = round(rng.uniform(0.05, 0.15), 2)
        p2_2 = round(rng.uniform(0.15, 0.25), 2)
        p2_3 = round(rng.uniform(0.2, 0.4), 2)
        p2_4 = round(1.0 - (p2_1 + p2_2 + p2_3), 2)
        if p2_4 <= 0:
            p2_1, p2_2, p2_3, p2_4 = 0.1, 0.2, 0.3, 0.4
        pool.append({
            'text': f"Дискретная случайная величина $X$ задана законом распределения:\n\n| $X$ | -1 | 0 | 1 | 2 |\n|---|---|---|---|---|\n| $P$ | $p_1$ | {p2_2} | {p2_3} | {p2_4} |\n\nНайдите значение вероятности $p_1$, если сумма всех вероятностей равна единице. (Округление до 2 знаков).",
            'answer': str(round(p2_1, 2))
        })

        # Задача 3
        k3 = rng.choice([2, 3, 4, 5])
        p3_rest = round(1.0 - (0.1 + 0.2 + 0.3 + 0.1 * k3), 2)
        if p3_rest <= 0: p3_rest = 0.15
        pool.append({
            'text': f"Закон распределения ДСВ $X$ задан вероятностями: $P(X=1) = 0.1$, $P(X=2) = 0.2$, $P(X=3) = 0.3$, $P(X=4) = {round(0.1*k3, 2)}$, а для $X=5$ вероятность равна $p_5$. Найдите $p_5$. (Округление до 2 знаков).",
            'answer': str(round(p3_rest, 2))
        })

        # Задача 4
        a4 = round(rng.uniform(0.1, 0.3), 2)
        b4 = round(rng.uniform(0.3, 0.5), 2)
        c4 = round(1.0 - (a4 + b4), 2)
        pool.append({
            'text': f"ДСВ $X$ принимает три значения с вероятностями {a4}, {b4} и $p_3$. Найдите $p_3$. (Округление до 2 знаков).",
            'answer': str(round(c4, 2))
        })

        # Задача 5
        pool.append({
            'text': f"Сумма всех возможных вероятностей в законе распределения дискретной случайной величины всегда строго равна какому числу?",
            'answer': "1"
        })

        # --- БЛОК 2: Математическое ожидание ДСВ (Задачи 6 - 10) ---
        
        # Задача 6
        x6 = [1, 2, 3, 4]
        p6 = [0.1, 0.3, 0.4, 0.2]
        mx6 = sum(x*p for x,p in zip(x6, p6))
        pool.append({
            'text': f"Дан закон распределения ДСВ $X$:\n\n| $X$ | {x6[0]} | {x6[1]} | {x6[2]} | {x6[3]} |\n|---|---|---|---|---|\n| $P$ | {p6[0]} | {p6[1]} | {p6[2]} | {p6[3]} |\n\nНайдите математическое ожидание $M(X)$. (Округление до 2 знаков).",
            'answer': str(round(mx6, 2))
        })

        # Задача 7
        x7 = [2, 4, 6]
        p7 = [0.2, 0.5, 0.3]
        mx7 = sum(x*p for x,p in zip(x7, p7))
        pool.append({
            'text': f"ДСВ $X$ задана таблично:\n\n| $X$ | {x7[0]} | {x7[1]} | {x7[2]} |\n|---|---|---|---|\n| $P$ | {p7[0]} | {p7[1]} | {p7[2]} |\n\nНайдите математическое ожидание $M(X)$. (Округление до 2 знаков).",
            'answer': str(round(mx7, 2))
        })

        # Задача 8
        x8 = [0, 1, 2, 3]
        p8 = [0.4, 0.3, 0.2, 0.1]
        mx8 = sum(x*p for x,p in zip(x8, p8))
        pool.append({
            'text': f"Число сбоев сервера $X$ имеет распределение:\n\n| $X$ | {x8[0]} | {x8[1]} | {x8[2]} | {x8[3]} |\n|---|---|---|---|---|\n| $P$ | {p8[0]} | {p8[1]} | {p8[2]} | {p8[3]} |\n\nНайти среднее число сбоев (матожидание). (Округление до 2 знаков).",
            'answer': str(round(mx8, 2))
        })

        # Задача 9
        x9 = [-2, 0, 3, 5]
        p9 = [0.1, 0.4, 0.3, 0.2]
        mx9 = sum(x*p for x,p in zip(x9, p9))
        pool.append({
            'text': f"Для ДСВ $X$ заданы значения {-2}, {0}, {3}, {5} с вероятностями {p9[0]}, {p9[1]}, {p9[2]}, {p9[3]}. Найти $M(X)$. (Округление до 2 знаков).",
            'answer': str(round(mx9, 2))
        })

        # Задача 10
        x10 = [5, 10, 15]
        p10 = [0.5, 0.3, 0.2]
        mx10 = sum(x*p for x,p in zip(x10, p10))
        pool.append({
            'text': f"Выигрыш в лотерее $X$ (в тыс. руб.) имеет распределение:\n\n| $X$ | {x10[0]} | {x10[1]} | {x10[2]} |\n|---|---|---|---|\n| $P$ | {p10[0]} | {p10[1]} | {p10[2]} |\n\nНайти математическое ожидание выигрыша. (Округление до 2 знаков).",
            'answer': str(round(mx10, 2))
        })

        # --- БЛОК 3: Дисперсия и среднеквадратичное отклонение (Задачи 11 - 15) ---
        
        # Задача 11
        x11 = [1, 3, 5]
        p11 = [0.2, 0.5, 0.3]
        m11 = sum(x*p for x,p in zip(x11, p11))
        m2_11 = sum((x**2)*p for x,p in zip(x11, p11))
        d11 = m2_11 - (m11**2)
        pool.append({
            'text': f"Дана ДСВ $X$:\n\n| $X$ | {x11[0]} | {x11[1]} | {x11[2]} |\n|---|---|---|---|\n| $P$ | {p11[0]} | {p11[1]} | {p11[2]} |\n\nНайдите дисперсию $D(X)$ по формуле $D(X) = M(X^2) - (M(X))^2$. (Округление до 2 знаков).",
            'answer': str(round(d11, 2))
        })

        # Задача 12
        x12 = [2, 4]
        p12 = [0.4, 0.6]
        m12 = sum(x*p for x,p in zip(x12, p12))
        m2_12 = sum((x**2)*p for x,p in zip(x12, p12))
        d12 = m2_12 - (m12**2)
        pool.append({
            'text': f"ДСВ $X$ принимает значения {x12[0]} и {x12[1]} с вероятностями {p12[0]} и {p12[1]}. Найдите дисперсию $D(X)$. (Округление до 2 знаков).",
            'answer': str(round(d12, 2))
        })

        # Задача 13
        d13 = 1.44
        pool.append({
            'text': f"Дисперсия дискретной случайной величины $X$ равна $D(X) = {d13}$. Найдите среднеквадратичное отклонение $\sigma(X)$. (Округление до 2 знаков).",
            'answer': str(round(math.sqrt(d13), 2))
        })

        # Задача 14
        x14 = [1, 2, 3]
        p14 = [0.3, 0.5, 0.2]
        m14 = sum(x*p for x,p in zip(x14, p14))
        m2_14 = sum((x**2)*p for x,p in zip(x14, p14))
        d14 = m2_14 - (m14**2)
        pool.append({
            'text': f"Для ДСВ с законом:\n\n| $X$ | 1 | 2 | 3 |\n|---|---|---|---|\n| $P$ | 0.3 | 0.5 | 0.2 |\n\nНайдите дисперсию $D(X)$. (Округление до 2 знаков).",
            'answer': str(round(d14, 2))
        })

        # Задача 15
        d15 = 2.25
        pool.append({
            'text': f"Среднеквадратичное отклонение $\sigma(X) = 1.5$. Чему равна дисперсия этой случайной величины $D(X)$? (Округление до 2 знаков).",
            'answer': str(round(d15, 2))
        })

        # --- БЛОК 4: Схема Бернулли и биномиальное распределение (Задачи 16 - 20) ---
        
        # Задача 16
        n16, p16, k16 = 5, 0.4, 2
        ans16 = math.comb(n16, k16) * (p16**k16) * ((1-p16)**(n16-k16))
        pool.append({
            'text': f"Проводится $n = {n16}$ независимых испытаний (схема Бернулли) с вероятностью успеха $p = {p16}$. Найти вероятность того,чество успехов будет ровно $k = {k16}$. (Округление до 4 знаков).",
            'answer': str(round(ans16, 4))
        })

        # Задача 17
        n17, p17, k17 = 4, 0.5, 3
        ans17 = math.comb(n17, k17) * (p17**k17) * ((1-p17)**(n17-k17))
        pool.append({
            'text': f"Монета подбрасывается 4 раза. Какова вероятность того, что герб выпадет ровно 3 раза?",
            'answer': str(round(ans17, 4))
        })

        # Задача 18
        n18, p18 = 4, 0.2
        # Число сбоев в биномиальном распределении M(X) = n * p
        mx18 = n18 * p18
        pool.append({
            'text': f"Вероятность сбоя процессора в одном цикле равна $p = {p18}$. Проведено $n = {n18}$ независимых циклов. Найти математическое ожидание числа сбоев $M(X)$. (Округление до 2 знаков).",
            'answer': str(round(mx18, 2))
        })

        # Задача 19
        n19, p19 = 10, 0.3
        # Дисперсия биномиального распределения D(X) = n * p * q
        dx19 = n19 * p19 * (1 - p19)
        pool.append({
            'text': f"Для биномиального распределения с параметрами $n = {n19}$ и $p = {p19}$ найдите дисперсию $D(X)$. (Округление до 2 знаков).",
            'answer': str(round(dx19, 2))
        })

        # Задача 20
        n20, p20, k20 = 6, 0.5, 4
        ans20 = math.comb(n20, k20) * (p20**k20) * ((1-p20)**(n20-k20))
        pool.append({
            'text': f"В серии из $n = {n20}$ испытаний Бернулли с вероятностью успеха $p = {p20}$ найти вероятность ровно $k = {k20}$ успехов. (Округление до 4 знаков).",
            'answer': str(round(ans20, 4))
        })

        # Перемешиваем пул задач индивидуально для студента
        rng.shuffle(pool)

        variant = {}
        for idx, task_item in enumerate(pool):
            task_num = idx + 1
            variant[f"task_{task_num}"] = task_item

        # Контрольный теоретический вопрос
        cq_pool = [
            "Что такое дискретная случайная величина и какими свойствами обладает ее закон распределения?",
            "Дайте определение математического ожидания дискретной случайной величины и опишите его механический смысл.",
            "Что характеризует дисперсия случайной величины? Какова связь между дисперсией и среднеквадратичным отклонением?",
            "Напишите формулу Бернулли и объясните условия ее применения в теории вероятностей.",
            "Каковы формулы для расчета математического ожидания и дисперсии биномиального распределения?"
        ]
        variant['task_99'] = {
            'title': 'Контрольный теоретический вопрос',
            'text': f"ОБЯЗАТЕЛЬНО прикрепите фото с развернутым рукописным ответом на вопрос:\n\n{rng.choice(cq_pool)}",
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
