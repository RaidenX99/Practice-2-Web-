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

        # 1. Формула Бернулли: Монета (гербы)
        n1 = rng.choice([8, 10, 12])
        k1 = rng.randint(3, n1 - 2)
        ans1 = math.comb(n1, k1) * (0.5 ** n1)
        pool.append({
            'text': f"Какова вероятность выпадения ровно {k1} гербов при {n1} подбросах симметричной монеты? (Округление до 4 знаков).",
            'answer': str(round(ans1, 4))
        })

        # 2. Формула Бернулли: Кубик (шестерка)
        n2 = rng.choice([8, 10, 12])
        k2 = rng.randint(2, 4)
        p2 = 1 / 6
        q2 = 5 / 6
        ans2 = math.comb(n2, k2) * (p2 ** k2) * (q2 ** (n2 - k2))
        pool.append({
            'text': f"Какова вероятность того, что при {n2} подбросах игрального кубика ровно {k2} раза выпадет 6 очков? (Округление до 4 знаков).",
            'answer': str(round(ans2, 4))
        })

        # 3. Схема Бернулли: Лечение больных
        p3 = rng.choice([0.7, 0.75, 0.8, 0.85])
        n3 = 5
        k3 = 4
        ans3 = math.comb(n3, k3) * (p3 ** k3) * ((1 - p3) ** (n3 - k3))
        pool.append({
            'text': f"Применяемый метод лечения приводит к выздоровлению в {int(p3*100)}% случаев. Какова вероятность того, что из выбранных {n3} больных выздоровеет ровно {k3}? (Округление до 4 знаков).",
            'answer': str(round(ans3, 4))
        })

        # 4. Схема Бернулли: Всхожесть семян (не менее половины)
        p4 = 0.8
        n4 = 6
        # не менее половины (>= 3)
        ans4 = sum(math.comb(n4, k) * (p4**k) * ((1-p4)**(n4-k)) for k in range(3, n4+1))
        pool.append({
            'text': f"Всхожесть семян данного растения равна 80%. Найти вероятность того, что из шести посаженных семян взойдет не менее половины. (Округление до 4 знаков).",
            'answer': str(round(ans4, 4))
        })

        # 5. Кубик: четное число очков
        n5 = 12
        k5 = 3
        p5 = 0.5
        ans5 = math.comb(n5, k5) * (p5 ** n5)
        pool.append({
            'text': f"Какова вероятность, что при {n5} подбросах кубика ровно {k5} раза выпадет четное число очков? (Округление до 4 знаков).",
            'answer': str(round(ans5, 4))
        })

        # 6. Спортсмен (больше 8 побед из 10)
        p6 = 0.6
        n6 = 10
        # больше 8 -> 9 или 10
        ans6 = sum(math.comb(n6, k) * (p6**k) * ((1-p6)**(n6-k)) for k in range(9, 11))
        pool.append({
            'text': f"Вероятность того, что спортсмен победит в матче, равна 0.6. Какова вероятность того, что в {n6} поединках он одержит больше 8 побед? (Округление до 4 знаков).",
            'answer': str(round(ans6, 4))
        })

        # 7. Адвокат (не проиграет ни одного из 3 дел, p=0.7)
        p7 = 0.7
        n7 = 3
        # не проиграет ни одного = выиграет все 3
        ans7 = math.comb(n7, 3) * (p7**3) * ((1-p7)**0)
        pool.append({
            'text': f"Адвокат выигрывает в суде в среднем 70% дел. Найти вероятность того, что из трех дел он не проиграет ни одного. (Округление до 4 знаков).",
            'answer': str(round(ans7, 4))
        })

        # 8. Передача сообщения: ровно 3 искажения из 10 (p=0.1)
        p8 = 0.1
        n8 = 10
        k8 = 3
        ans8 = math.comb(n8, k8) * (p8**k8) * ((1-p8)**(n8-k8))
        pool.append({
            'text': f"При передаче сообщения вероятность искажения сигнала равна 0.1. Какова вероятность того, что пакет из 10 сигналов содержит ровно 3 искаженных сигнала? (Округление до 4 знаков).",
            'answer': str(round(ans8, 4))
        })

        # 9. Передача сообщения: 0 искажений из 10
        ans9 = math.comb(10, 0) * (0.9**10)
        pool.append({
            'text': f"При передаче сообщения вероятность искажения сигнала равна 0.1. Какова вероятность того, что пакет из 10 сигналов не содержит искаженных сигналов вообще? (Округление до 4 знаков).",
            'answer': str(round(ans9, 4))
        })

        # 10. Лотерейные билеты: хотя бы пару раз (выиграть >= 2 из 20, p=0.05)
        p10 = 0.05
        n10 = 20
        # хотя бы пару раз (>= 2) через противоположное (0 или 1)
        p_less_2 = math.comb(n10, 0)*(1-p10)**20 + math.comb(n10, 1)*p10*(1-p10)**19
        ans10 = 1 - p_less_2
        pool.append({
            'text': f"Вероятность выигрыша по лотерейному билету равна 0.05. Какова вероятность выиграть хотя бы пару раз (2 и более раза), купив 20 билетов? (Округление до 4 знаков).",
            'answer': str(round(ans10, 4))
        })

        # 11. Тест с выбором ответа (как в примере 3): 11 вопросов, 4 варианта, сдан при k >= 2
        # P(сдан) = 1 - P(0 или 1)
        p11 = 0.25
        n11 = 11
        p_fail = math.comb(n11, 0)*(0.75**11) + math.comb(n11, 1)*(0.25)*(0.75**10)
        ans11 = 1 - p_fail
        pool.append({
            'text': f"Тест состоит из 11 вопросов, к каждому 4 варианта (1 правильный). Для прохождения нужно ответить не менее чем на 2 вопроса. Найти вероятность прохождения теста наугад. (Округление до 4 знаков).",
            'answer': str(round(ans11, 4))
        })

        # 12. Мат. ожидание в схеме Бернулли (n=15, p=0.3)
        n12, p12 = 15, 0.3
        pool.append({
            'text': f"В схеме Бернулли число испытаний $n = {n12}$, вероятность успеха $p = {p12}$. Найдите математическое ожидание числа успехов $M(X)$. (Округление до 2 знаков).",
            'answer': str(round(n12 * p12, 2))
        })

        # 13. Дисперсия в схеме Бернулли (n=20, p=0.4)
        n13, p13 = 20, 0.4
        d13 = n13 * p13 * (1 - p13)
        pool.append({
            'text': f"Для биномиального распределения с параметрами $n = {n13}$ и огранченным $p = {p13}$ найдите дисперсию $D(X)$. (Округление до 2 знаков).",
            'answer': str(round(d13, 2))
        })

        # 14. Теннисист (пример 5): матч из 3 партий, p=1/3
        p14 = 1/3
        # победа в матче из 3 партий если выиграно >= 2 партий
        ans14 = math.comb(3, 2)*(p14**2)*(1-p14) + math.comb(3, 3)*(p14**3)
        pool.append({
            'text': f"Игрок играет в 2 раза хуже соперника (вероятность выиграть одну партию равна 1/3). Какова вероятность выиграть матч из 3 партий (выиграть не менее 2 партий)? (Округление до 4 знаков).",
            'answer': str(round(ans14, 4))
        })

        # 15. Теннисист: матч из 5 партий, p=1/3 (нужно выиграть >= 3 партий)
        p15 = 1/3
        ans15 = sum(math.comb(5, k) * (p15**k) * ((1-p15)**(5-k)) for k in range(3, 6))
        pool.append({
            'text': f"Игрок играет в 2 раза хуже соперника (вероятность выиграть партию 1/3). Какова вероятность выиграть матч из 5 партий (выиграть не менее 3 партий)? (Округление до 4 знаков).",
            'answer': str(round(ans15, 4))
        })

        # 16. Экстрасенс (пример 4): угадал 9 раз из 10 при p=1/2
        ans16 = math.comb(10, 9) * (0.5**10)
        pool.append({
            'text': f"Человек угадывает предмет в руке с вероятностью 0.5. Какова вероятность угадать ровно 9 раз из 10 попыток? (Округление до 4 знаков).",
            'answer': str(round(ans16, 4))
        })

        # 17. Экстрасенс: угадал 3 из 4
        ans17 = math.comb(4, 3) * (0.5**4)
        pool.append({
            'text': f"Человек угадывает предмет в руке с вероятностью 0.5. Какова вероятность угадать ровно 3 раза из 4 попыток? (Округление до 4 знаков).",
            'answer': str(round(ans17, 4))
        })

        # 18. Стрелок: победит больше 8 из 10 (p=0.6) - повтор для рандома с другими числами
        p18 = 0.7
        n18 = 10
        ans18 = sum(math.comb(n18, k) * (p18**k) * ((1-p18)**(n18-k)) for k in range(9, 11))
        pool.append({
            'text': f"Спортсмен побеждает в матче с вероятностью 0.7. Какова вероятность того, что в 10 поединках он одержит больше 8 побед (9 или 10)? (Округление до 4 знаков).",
            'answer': str(round(ans18, 4))
        })

        # 19. Монета: 5 гербов из 10
        ans19 = math.comb(10, 5) * (0.5**10)
        pool.append({
            'text': f"Какова вероятность выпадения ровно 5 гербов при 10 подбросах монеты? (Округление до 4 знаков).",
            'answer': str(round(ans19, 4))
        })

        # 20. Адвокат: из 8 дел выиграет больше половины (> 4 дел, то есть от 5 до 8, p=0.7)
        p20 = 0.7
        n20 = 8
        ans20 = sum(math.comb(n20, k) * (p20**k) * ((1-p20)**(n20-k)) for k in range(5, 9))
        pool.append({
            'text': f"Адвокат выигрывает в суде в среднем 70% дел. Найти вероятность того, что из восьми дел он выиграет больше половины (от 5 до 8 дел). (Округление до 4 знаков).",
            'answer': str(round(ans20, 4))
        })

        rng.shuffle(pool)

        variant = {}
        for idx, task_item in enumerate(pool):
            task_num = idx + 1
            variant[f"task_{task_num}"] = task_item

        cq_pool = [
            "Сформулируйте определение схемы Бернулли и запишите формулу для вычисления вероятности $P_n(k)$.",
            "В чем заключается принцип обратного события и когда его целесообразно использовать при расчетах по схеме Бернулли?",
            "Как вычисляется вероятность того, что число появлений события в схеме Бернулли лежит в заданном интервале от $k_1$ до $k_2$?",
            "Чему равны математическое ожидание и дисперсия для биномиального распределения (в схеме Бернулли)?"
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
