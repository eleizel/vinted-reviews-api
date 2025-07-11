from flask import Flask, jsonify, request
from vinted import Vinted

app = Flask(__name__)
vinted = Vinted(domain="es")

@app.route("/reviews", methods=["GET"])
def get_reviews():
    user_id = request.args.get("user_id", type=int)

    if not user_id:
        return jsonify({"error": "Missing or invalid user_id parameter"}), 400

    try:
        response = vinted.user_feedbacks(user_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    reviews = []

    for feedback in response.user_feedbacks:
        if "valoración automática" in feedback.feedback.lower():
            continue

        review = {
            "username": feedback.user.login,
            "rating": feedback.rating,
            "review_text": feedback.feedback,
            "profile_photo_url": next(
                (thumb.url for thumb in feedback.user.photo.thumbnails if thumb.type == "thumb100"),
                feedback.user.photo.url
            )
        }
        reviews.append(review)

    return jsonify(reviews)
