from flask import Flask, request, jsonify
from intent_parser import parse_intent
from device_controller import DeviceController

app = Flask(__name__)
controller = DeviceController()


@app.route("/process_command", methods=["POST"])
def process_command():
    data = request.get_json() or {}
    command = data.get("command", "").strip()
    if not command:
        return jsonify({"error": "No command provided"}), 400

    intent = parse_intent(command)
    if not intent.get("appliance") or not intent.get("action"):
        return jsonify({
            "message": "Sorry, I didn't understand that.",
            "recognized": command,
            "states": controller.get_states(),
        })

    appliance = intent["appliance"]
    action = intent["action"]

    result = controller.perform(appliance, action)

    spoken = result.get("message")

    return jsonify({
        "message": result.get("message"),
        "appliance": appliance,
        "action": action,
        "states": controller.get_states(),
        "spoken": spoken,
    })


@app.route("/states", methods=["GET"])
def states():
    return jsonify(controller.get_states())


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", "5000"))
    app.run(port=port, debug=True)
