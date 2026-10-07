import os
from flask import Flask, render_template, request, jsonify
from application.query_service import QueryService
from application.search_service import SearchService

def create_app(query_service: QueryService, search_service: SearchService) -> Flask:
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates"))
    app = Flask(__name__, template_folder=template_dir)

    @app.route("/")
    def index():
        catalog = search_service.product_repo.get_all()
        orders = search_service.order_repo.get_all()
        return render_template("index.html", catalog=catalog, orders=orders)

    @app.route("/api/search", methods=["POST"])
    def api_search():
        data = request.get_json() or {}
        mode = data.get("mode", "text").lower()
        query = data.get("query", "")

        if mode == "text":
            q_obj = query_service.text_query(query)
            res = search_service.search_text(q_obj["query"], q_obj["tokens"])
            return jsonify(res)

        elif mode == "voice":
            q_obj = query_service.voice_query(query)
            res = search_service.search_voice(q_obj)
            return jsonify(res)

        elif mode == "image":
            q_obj = query_service.image_query(query)
            res = search_service.search_image(q_obj)
            return jsonify(res)

        elif mode == "order":
            q_obj = query_service.order_query(query)
            res = search_service.search_order(q_obj["query"])
            return jsonify(res)

        elif mode == "multimodal":
            text_q = data.get("text", "")
            img_q = data.get("image", "")
            q_obj = query_service.multimodal_query(text_q, img_q)
            res = search_service.search_multimodal(q_obj)
            return jsonify(res)

        return jsonify({"error": f"Unknown mode: {mode}"}), 400

    @app.route("/api/catalog")
    def api_catalog():
        return jsonify(search_service.product_repo.get_all())

    return app
