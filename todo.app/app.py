from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# DB 연결 함수
def get_db_connection():
    conn = sqlite3.connect('todo.db')  # 같은 폴더에 있는 DB 파일
    conn.row_factory = sqlite3.Row     # 딕셔너리처럼 접근 가능하게 함
    return conn

# 처음 실행 시 DB 테이블 생성
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            done INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 메인 페이지 - 할 일 목록 출력
@app.route('/')
def index():
    conn = get_db_connection()
    todos = conn.execute('SELECT * FROM todos ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

# 할 일 추가
@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    if content.strip():  # 빈 문자열이 아니면 추가
        conn = get_db_connection()
        conn.execute('INSERT INTO todos (content) VALUES (?)', (content,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

# 완료 처리 (토글 방식)
@app.route('/done/<int:todo_id>', methods=['POST'])
def done(todo_id):
    conn = get_db_connection()
    conn.execute('UPDATE todos SET done = NOT done WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# 삭제
@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# 서버 시작 전 DB 초기화
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
