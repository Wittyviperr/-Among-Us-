from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random
import time
import uuid

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Predefined users (username/password)
users = {
    "user1": {"password": "pass1", "role": "crewmate"},
    "user2": {"password": "pass2", "role": "crewmate"},
    "user3": {"password": "pass3", "role": "crewmate"},
    "user4": {"password": "pass4", "role": "crewmate"},
    "user5": {"password": "pass5", "role": "crewmate"},
    "user6": {"password": "pass6", "role": "crewmate"},
    "user7": {"password": "pass7", "role": "crewmate"},
    "user8": {"password": "pass8", "role": "crewmate"},
    "user9": {"password": "pass9", "role": "crewmate"},
    "imposter": {"password": "imposterpass", "role": "imposter"},
}

# Admin credentials
admin_credentials = {
    "username": "admin",
    "password": "adminpass"
}

# Sample tasks
tasks = [
    "Fix Wiring", "Calibrate Distributor", "Clear Leaves", "Swipe Card",
    "Upload Data", "Clean Vent", "Start Reactor", "Align Engine"
]

# Store player data
players = {}

# Game state
game_state = {
    "timer_start": None,
    "paused": False,
    "remaining_time": 1200,
    "game_started": False,
    "voting_in_progress": False,
    "votes": {},
    "voted_users": set(),  # Users who have already voted
}


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            if username not in players:
                players[username] = {
                    "tasks": [],
                    "alive": True,
                    "role": users[username]["role"]
                }
            session_id = str(uuid.uuid4())
            session["session_id"] = session_id
            session["username"] = username
            return redirect(url_for("dashboard", session_id=session_id, username=username))
        else:
            return "Invalid username or password!", 400

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    session_id = request.args.get("session_id")
    username = request.args.get("username")
    if not session_id or not username or username not in players:
        return redirect(url_for("login"))

    player = players[username]
    if game_state["paused"] or not game_state["game_started"]:
        time_left = game_state["remaining_time"]
    else:
        elapsed = time.time() - game_state["timer_start"]
        time_left = max(0, game_state["remaining_time"] - elapsed)

    alive = sum(1 for p in players.values() if p["alive"])
    dead = len(players) - alive

    return render_template(
        "dashboard.html",
        username=username,
        player=player,
        game_state=game_state,
        time_left=round(time_left),
        alive=alive,
        dead=dead,
        players=players
    )


@app.route("/mark_dead", methods=["POST"])
def mark_dead():
    if not session.get("admin"):
        return redirect(url_for("admin_dashboard"))

    username_to_mark_dead = request.form.get("username")
    if username_to_mark_dead in players and players[username_to_mark_dead]["alive"]:
        players[username_to_mark_dead]["alive"] = False
        players[username_to_mark_dead]["message"] = "You were ejected"
    return redirect(url_for("admin_dashboard"))

@app.route("/pause_timer", methods=["POST"])
def pause_timer():
    """Pause the timer when a player calls an emergency meeting."""
    username = session.get("username")
    if not username:
        return jsonify({"error": "Unauthorized"}), 401

    if not game_state["paused"]:
        elapsed = time.time() - game_state["timer_start"]
        game_state["remaining_time"] -= elapsed
        game_state["paused"] = True
        game_state["timer_start"] = None  # Reset the start time
    return jsonify({"success": True, "message": "Emergency meeting called. Game paused."})


@app.route("/resume_timer", methods=["POST"])
def resume_timer():
    """Resume the timer. Admin-only route."""
    if not session.get("admin"):
        return jsonify({"error": "Unauthorized"}), 401

    if game_state["paused"]:
        game_state["timer_start"] = time.time()
        game_state["paused"] = False
    return jsonify({"success": True, "message": "Game resumed"})



@app.route("/start_game", methods=["POST"])
def start_game():
    if not session.get("admin"):
        return redirect(url_for("admin_dashboard"))

    if not game_state["game_started"]:
        game_state["game_started"] = True
        game_state["timer_start"] = time.time()
    return redirect(url_for("admin_dashboard"))


@app.route("/restart_game", methods=["POST"])
def restart_game():
    if not session.get("admin"):
        return redirect(url_for("admin_dashboard"))

    # Reset game state
    for username in players:
        players[username]["tasks"] = []
        players[username]["alive"] = True

    game_state["timer_start"] = None
    game_state["paused"] = False
    game_state["remaining_time"] = 1200
    game_state["game_started"] = False
    game_state["voting_in_progress"] = False
    game_state["votes"] = {}

    return redirect(url_for("admin_dashboard"))


@app.route("/logout")
def logout():
    username = request.args.get("username")
    if username in players:
        del players[username]
    session.clear()
    return redirect(url_for("login"))


@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == admin_credentials["username"] and password == admin_credentials["password"]:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return "Invalid admin credentials!", 400

    return render_template("admin_login.html")


@app.route("/admin/dashboard", methods=["GET", "POST"])
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        username = request.form["username"]
        assigned_tasks = request.form.getlist("tasks")
        if username in players:
            players[username]["tasks"] = assigned_tasks
            return redirect(url_for("admin_dashboard"))

    return render_template("admin_dashboard.html", game_state=game_state, players=players, tasks=tasks)




@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))

@app.route("/broadcast_message", methods=["POST"])
def broadcast_message():
    if not session.get("admin"):
        return redirect(url_for("admin_dashboard"))

    message_type = request.form.get("message_type")

    if message_type == "imposter_ejected":
        game_state["broadcast_message"] = "Imposter was ejected! Crewmates win!"
        game_state["game_started"] = False  # End the game
    elif message_type == "time_ends":
        game_state["broadcast_message"] = "Game time ends! Imposter wins!"
        game_state["game_started"] = False  # End the game

    return redirect(url_for("admin_dashboard"))



if __name__ == "__main__":
    app.run(debug=True)
