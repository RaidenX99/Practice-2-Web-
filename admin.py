# -*- coding: utf-8 -*-
import streamlit as st
import json
import base64
from core import PracticeEngine

st.set_page_config(page_title="Панель проверки - Практика 2", layout="wide", page_icon="🛡️")

st.title("🛡️ Панель преподавателя - Практика №2")

if 'admin_auth' not in st.session_state:
    st.session_state.admin_auth = False
    
if not st.session_state.admin_auth:
    pwd = st.text_input("Введите секретный пароль доступа:", type="password")
    if st.button("Войти"):
        if pwd == "urtisi": 
            st.session_state.admin_auth = True
            st.rerun()
        else:
            st.error("Неверный пароль!")
else:
    if st.button("🚪 Выйти"):
        st.session_state.admin_auth = False
        st.rerun()
        
    uploaded_files = st.file_uploader("Загрузите файлы отчетов (.json)", type=["json"], accept_multiple_files=True)
    
    if uploaded_files:
        for file in uploaded_files:
            try:
                data = json.load(file)
                student_id = data.get("student_id", "Неизвестно")
                encrypted_answers = data.get("answers", {})
                file_hash = data.get("verification_key", "")
                
                decrypted_answers = {}
                for k, v in encrypted_answers.items():
                    if isinstance(v, list):
                        decrypted_list = []
                        for photo_v in v:
                            try:
                                decrypted_list.append(base64.b64decode(photo_v.encode('utf-8')).decode('utf-8')[::-1])
                            except Exception:
                                pass
                        decrypted_answers[k] = decrypted_list
                    else:
                        try:
                            decrypted_answers[k] = base64.b64decode(v.encode('utf-8')).decode('utf-8')[::-1]
                        except Exception:
                            decrypted_answers[k] = ""
                        
                engine = PracticeEngine(student_id)
                expected_hash = engine.generate_security_hash(student_id, decrypted_answers)
                
                with st.expander(f"Студент: {student_id} | Время решения: {data.get('time_spent', 'Н/Д')}", expanded=True):
                    if expected_hash != file_hash:
                        st.error("🚨 ОШИБКА АНТИЧИТА: Файл был изменен вручную!")
                    else:
                        result = engine.check_answers(decrypted_answers)
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Оценка", result['mark'])
                        col2.metric("Выполнено", f"{result['percent']}%")
                        col3.metric("Верно", f"{result['correct_count']} из {result['total_count']}")
                        
                        st.write("---")
                        for task_key, details in sorted(result['details'].items(), key=lambda x: int(x[0].split('_')[1]) if x[0] != 'task_99' else 99):
                            status = "✅" if details['is_correct'] else "❌"
                            if task_key == 'task_99':
                                st.write(f"{status} **Теория:** {details['student_answer']}")
                            else:
                                st.write(f"{status} **Задача {task_key.split('_')[1]}:** Ввел: `{details['student_answer']}` | Правильно: `{details['correct_answer']}`")
                            
                            for idx, photo_b64 in enumerate(result.get('photos', {}).get(task_key, [])):
                                st.image(base64.b64decode(photo_b64), caption=f"Решение {idx+1}", width=400)
                            st.write("---")
            except Exception as e:
                st.error(f"Ошибка чтения файла: {e}")
