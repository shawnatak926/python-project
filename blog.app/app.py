from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

posts = []
post_id = 1

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/post/<int:id>')
def post(id):
    for p in posts:
        if p['id'] == id:
            return render_template('post.html', post=p)
    return "게시글이 없습니다.", 404

@app.route('/create', methods=['GET', 'POST'])
def create():
    global post_id
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        posts.append({'id': post_id, 'title': title, 'content': content})
        post_id += 1
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    for p in posts:
        if p['id'] == id:
            if request.method == 'POST':
                p['title'] = request.form['title']
                p['content'] = request.form['content']
                return redirect(url_for('post', id=id))
            return render_template('edit.html', post=p)
    return "게시글이 없습니다.", 404

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    global posts
    posts = [p for p in posts if p['id'] != id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)