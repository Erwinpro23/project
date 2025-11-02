from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .model import Note
from . import db
from datetime import datetime
import json

view = Blueprint("view", __name__)

# -----------------------------
# Trang chính
# -----------------------------
@view.route("/home", methods=["GET", "POST"])
@view.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        # Lấy dữ liệu từ form
        work = request.form.get("work_name")
        start_date = request.form.get("start_date")
        finish_date = request.form.get("finish_date")
        status = request.form.get('status')  # ✅ Thêm dòng này
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None
        finish_date_obj = datetime.strptime(finish_date, "%Y-%m-%d").date() if finish_date else None
        if not work:
            flash("Work name cannot be empty!", category="error")
        else:
            new_note = Note(
                work_name=work,
                start_date=start_date_obj,
                finish_date=finish_date_obj,
                is_done=(status == "Finish"),
                user_id=current_user.id
            )
            db.session.add(new_note)
            db.session.commit()
            flash("Task added successfully!", category="success")
            return redirect(url_for("view.home"))

    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, notes=notes)

# -----------------------------
# API xóa task
# -----------------------------
@view.route("/delete-note", methods=["POST"])
@login_required
def delete_note():
    note_data = json.loads(request.data)
    note_id = note_data.get("noteId")

    result = Note.query.get(note_id)
    if result and result.user_id == current_user.id:
        db.session.delete(result)
        db.session.commit()
        return jsonify({"code": 200, "message": "Task deleted"})
    return jsonify({"code": 403, "message": "Unauthorized"}), 403

# -----------------------------
# API toggle trạng thái hoàn thành
# -----------------------------
@view.route("/toggle-done", methods=["POST"])
@login_required
def toggle_done():
    note_data = json.loads(request.data)
    note_id = note_data.get("noteId")

    result = Note.query.get(note_id)
    if result and result.user_id == current_user.id:
        result.is_done = not result.is_done
        db.session.commit()
        return jsonify({"code": 200, "status": result.is_done})
    return jsonify({"code": 403, "message": "Unauthorized"}), 403

@view.route("/update-status", methods=["POST"])
@login_required
def update_status():
    note_data = json.loads(request.data)
    note_id = note_data.get("noteId")
    new_status = note_data.get("status")

    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        note.is_done = (new_status == "Finish")
        db.session.commit()
        return jsonify({"code": 200, "message": "Status updated"})
    return jsonify({"code": 403, "message": "Unauthorized"}), 403
