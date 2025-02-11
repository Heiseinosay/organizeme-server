from flask import Flask, request, jsonify
from dbutils import connect_to_db, create_account, login_auth, select_all_subjects, insert_subject, edit_subject_name, fetch_subject_name, delete_subject_name, add_task, select_subject_task, update_selected_task, delete_task_name, task_accomplished, select_all_accomplished, calendar_task, insert_notification, get_user_summary, get_user_notification, search_item

app = Flask(__name__)

@app.route("/members")
def members():
    # connect_to_db() 
    # create_account()
    return {"members": ["member1", "member2", "member3"]}

@app.route("/auth_login", methods=["POST"])
def auth_login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    res = login_auth(email, password)
    print(res)
    return jsonify(res)


@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("mail")
    password = data.get("password")

    print(f"Received signup data: {first_name}, {last_name}, {email}, {password}")
    res = create_account(first_name, last_name, email, password)
    print("res: ", res)
    return jsonify(res), 201


@app.route("/get_all_subjects", methods=['GET'])
def get_all_subjects():
    uid = request.args.get("uid")
    res = select_all_subjects(uid)
    print(res)
    
    return res


@app.route("/add_subject", methods=['POST'])
def add_subject():
    data = request.json
    uid = data.get("uid")
    subjectName = data.get("subjectName")
    res = insert_subject(uid, subjectName)
    print(res)
    
    return res


@app.route("/get_subject_name", methods=['GET'])
def get_subject_name():
    sid = request.args.get("sid")
    print(sid)
    res = fetch_subject_name(sid)

    return res


@app.route("/update_subject_name", methods=['POST'])
def update_subject_name():
    data = request.json
    sid = data.get("subjectID")
    subjectName = data.get("subjectName")
    res = edit_subject_name(sid, subjectName)
    # print(sid, subjectName)

    return res


@app.route("/delete_subject", methods=['DELETE'])
def delete_subject():
    sid = request.args.get("sid")
    res = delete_subject_name(sid)
    # print("sid: ", sid)
    # print(res)

    return res


@app.route("/create_task", methods=['POST'])
def create_task():
    # print("Im here")
    data = request.json
    uid = data.get("userID")
    sid = data.get("subjectID")
    title = data.get("title")
    description = data.get("description")
    dueDate = data.get("dueDate")
    reminder = data.get("reminder")
    priority = data.get("priority")
    status = data.get("status")
    # print(uid, sid, title, description, dueDate, reminder, priority, status)
    res = add_task(uid, sid, title, description, dueDate, reminder, priority, status)
    # print(res)

    return res


@app.route("/get_subject_task", methods=['GET'])
def get_subject_task():
    uid = request.args.get("uid")
    sid = request.args.get("sid")

    # print(uid, sid)
    res = select_subject_task(uid, sid)
    
    return res


@app.route("/update_task", methods=['POST'])
def update_task():
    data = request.json
    tid = data.get("taskID")
    uid = data.get("userID")
    sid = data.get("subjectID")
    title = data.get("title")
    description = data.get("description")
    due = data.get("due")
    reminder = data.get("reminder")
    priority = data.get("priority")
    status = data.get("status")

    # print(tid, uid, sid, title, description, due, reminder, priority, status)
    res = update_selected_task(tid, uid, sid, title, description, due, reminder, priority, status)
    
    
    return res


@app.route("/delete_subject_task", methods=['DELETE'])
def delete_subject_task():
    tid = request.args.get("tid")
    uid = request.args.get("uid")
    sid = request.args.get("sid")
    
    # print(tid, uid, sid)
    res = delete_task_name(tid, uid, sid)

    return res


@app.route("/moveToAccomplish", methods=['POST'])
def move_to_accomplish():
    data = request.json
    tid = data.get("TaskID")
    uid = data.get("UserID")
    sid = data.get("SubjectID")
    
    # print(tid, uid, sid)
    res = task_accomplished(tid, uid, sid)

    return res


@app.route("/get_all_accomplished", methods=['GET'])
def get_all_accomplished():
    uid = request.args.get("uid")
    res = select_all_accomplished(uid)
    # print(res)
    
    return res


@app.route("/get_all_task", methods=['GET'])
def get_all_task():
    uid = request.args.get("uid")

    # print(uid)
    res = calendar_task(uid)
    
    return res


@app.route("/create_notification", methods=['POST'])
def create_notification():
    data = request.json
    uid = data.get("uid")
    
    # print("connected: ", uid)
    insert_notification(uid)

    return { 'status ': True }


@app.route("/get_summary", methods=['GET'])
def get_summary():
    uid = request.args.get("uid")

    # print("Summary: ", uid)
    res = get_user_summary(uid)
    
    return res


@app.route("/get_notification", methods=['GET'])
def get_notification():
    uid = request.args.get("uid")

    # print("Summary: ", uid)
    res = get_user_notification(uid)
    
    return res


@app.route("/search_by_name_description", methods=['GET'])
def search_by_name_description():
    uid = request.args.get("uid")
    searchTerm = request.args.get("keyword")

    print("SEARCH: ", uid, searchTerm)
    res = search_item(uid, searchTerm)
    
    return res
    # return { 'status': True }


if __name__ == "__main__":
    app.run()
    # app.run(debug=True, port=5000)