from flask import Flask, render_template, request, session, redirect, url_for
import random
import game_data

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for session

@app.route("/", methods=["GET", "POST"])
def high_low():
    #Initialize session values if not set
    if "score" not in session:
        session["score"] = 0
    if "feedback" not in session:
        session["feedback"] = ""
    if "game_over" not in session:
        session["game_over"] = False
    if "choice_a" not in session or "choice_b" not in session:
        session["choice_a"] = random.choice(game_data.data)
        session["choice_b"] = random.choice(game_data.data)
        while session["choice_a"] == session["choice_b"]:
            session["choice_b"] = random.choice(game_data.data)
        session["choice_a_followers"] = session["choice_a"]["follower_count"]
        session["choice_b_followers"] = session["choice_b"]["follower_count"]

    #Handle user choice submission if game is not over
    if request.method == "POST" and "choice" in request.form and not session.get("game_over", False):
        user_choice = request.form["choice"]
        a_followers = session["choice_a_followers"]
        b_followers = session["choice_b_followers"]

        correct_choice = "A" if a_followers > b_followers else "B"

        if user_choice == correct_choice:
            session["score"] += 1
            session["feedback"] = f"✅ Correct! Score: {session['score']}"

            #Generate new random choices for next round
            choice_a = random.choice(game_data.data)
            choice_b = random.choice(game_data.data)
            while choice_a == choice_b:
                choice_b = random.choice(game_data.data)
            session["choice_a"] = choice_a
            session["choice_b"] = choice_b
            session["choice_a_followers"] = choice_a["follower_count"]
            session["choice_b_followers"] = choice_b["follower_count"]
        else:
            session["feedback"] = f"❌ Wrong! Final score: {session['score']}"
            session["score"] = 0
            session["game_over"] = True

    #Pass current choices to template
    choice_a = session.get("choice_a")
    choice_b = session.get("choice_b")

    return render_template(
        "index.html",
        a=choice_a,
        b=choice_b,
        score=session.get("score", 0),
        feedback=session.get("feedback", ""),
        game_over=session.get("game_over", False)
    )


@app.route("/restart")
def restart():
    #Clears session and restarts the game.
    session.clear()
    return redirect(url_for("high_low"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
