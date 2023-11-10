from flask import Flask, request, jsonify, send_from_directory, redirect, session
from waitress import serve
from tracks import EDUCATIONAL_TRACKS

app = Flask(__name__)

@app.route('/start_track', methods=['POST'])
def start_track():
  track_name = request.json.get('track')
  EDUCATIONAL_TRACKS.keys()
  track = EDUCATIONAL_TRACKS.get(track_name)
  if track is None:
    return jsonify({"error": "Track not found"}), 400
  # Start the student at the first step of the track.
  step_index = 0
  step = track['steps'][step_index]
  return jsonify({"prompt": step['prompt'], "step_index": step_index})

@app.route('/next_step', methods=['POST'])
def next_step():
  track_name = request.json.get('track')
  step_index = request.json.get('step_index')
  user_response = request.json.get('user_response')

  track = EDUCATIONAL_TRACKS.get(track_name)
  if track is None:
    return jsonify({"error": "Track not found"}), 400

  if step_index >= len(track['steps']):
    return jsonify({"error": "No more steps in this track"}), 400

  # Provide feedback for the current step.
  current_step = track['steps'][step_index]
  feedback = current_step['response']

  # Move to the next step if available.
  step_index += 1
  if step_index < len(track['steps']):
    next_step = track['steps'][step_index]
    return jsonify({
      "feedback": feedback,  # Include feedback in the response
      "next_prompt": next_step['prompt'],
      "step_index": step_index
    })
  else:
    return jsonify({
      "feedback": feedback,  # Include feedback in the response
      "next_prompt": None,
      "step_index": step_index
    })
  
@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
  return send_from_directory('.well-known',
                             'ai-plugin.json',
                             mimetype='application/json')


@app.route('/openapi.yaml')
def serve_openapi_yaml():
  return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')


@app.route('/logo.png')
def serve_logo():
  return send_from_directory('.', 'logo.png', mimetype='image/png')

@app.route('/legal')
def serve_legal():
  return send_from_directory('.', 'legal', mimetype='text/yaml')


if __name__ == '__main__':
  serve(app, host="0.0.0.0", port=8080)