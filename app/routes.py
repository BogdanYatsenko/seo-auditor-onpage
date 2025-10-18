from flask import Blueprint, render_template_string, request, redirect, url_for
from .database import SessionLocal
from .models import Lead
from .notify import notify_manager

bp = Blueprint('routes', __name__)

INDEX_HTML = '''
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Telegram CRM — Leads</title>
    <style>
      body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 24px; }
      input, textarea { width: 100%; padding: 8px; margin: 6px 0; }
      table { width: 100%; border-collapse: collapse; margin-top: 20px; }
      th, td { border: 1px solid #ddd; padding: 8px; }
      th { background: #f4f4f4; text-align: left; }
      .row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
      .btn { padding: 10px 14px; border: 0; background: #111; color: #fff; cursor: pointer; border-radius: 8px; }
    </style>
  </head>
  <body>
    <h1>Leads</h1>
    <form method="post" action="{{ url_for('routes.add_lead') }}">
      <div class="row">
        <div><label>Name</label><input name="name" required></div>
        <div><label>Phone</label><input name="phone" required></div>
      </div>
      <label>Note</label>
      <textarea name="note" rows="3"></textarea>
      <button class="btn" type="submit">Add lead</button>
    </form>

    <table>
      <thead><tr><th>ID</th><th>Name</th><th>Phone</th><th>Note</th><th>Source</th><th>Created</th></tr></thead>
      <tbody>
      {% for l in leads %}
        <tr>
          <td>{{ l.id }}</td>
          <td>{{ l.name }}</td>
          <td>{{ l.phone }}</td>
          <td>{{ l.note }}</td>
          <td>{{ l.source }}</td>
          <td>{{ l.created_at }}</td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
  </body>
</html>
'''

@bp.get("/")
def index():
    db = SessionLocal()
    leads = db.query(Lead).order_by(Lead.id.desc()).limit(200).all()
    db.close()
    return render_template_string(INDEX_HTML, leads=leads)

@bp.post("/lead")
def add_lead():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    note = request.form.get("note", "").strip()
    if not name or not phone:
        return redirect(url_for('routes.index'))
    db = SessionLocal()
    lead = Lead(name=name, phone=phone, note=note, source="web")
    db.add(lead)
    db.commit()
    notify_manager(f"<b>New lead (web)</b>\nName: {name}\nPhone: {phone}\nNote: {note}")
    db.close()
    return redirect(url_for('routes.index'))
