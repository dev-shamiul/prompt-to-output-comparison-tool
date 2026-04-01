from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

API_KEY = "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"

def generate_output(prompt):

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": "openai/gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
    )

    result = response.json()

    return result["choices"][0]["message"]["content"]


def score_prompt(prompt, output):

    score = 0

    if len(prompt) > 15:
        score += 3

    if "example" in prompt.lower():
        score += 3

    if len(output) > 100:
        score += 4

    return score


@app.route("/", methods=["GET","POST"])
def index():

    results = []
    best_prompt = None
    best_score = -1

    if request.method == "POST":

        prompts = [
            request.form.get("prompt1"),
            request.form.get("prompt2"),
            request.form.get("prompt3")
        ]

        for p in prompts:

            if p:

                output = generate_output(p)

                score = score_prompt(p, output)

                results.append({
                    "prompt": p,
                    "output": output,
                    "score": score
                })

                if score > best_score:
                    best_score = score
                    best_prompt = p

    return render_template(
        "index.html",
        results=results,
        best_prompt=best_prompt
    )


if __name__ == "__main__":
    app.run(debug=True)
