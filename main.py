from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Calculation(BaseModel):
    num1: float
    num2: float
    operation: str

@app.post("/cal/")
async def calculate(calc: Calculation):
    if calc.operation == "+":
        result = calc.num1 + calc.num2
    elif calc.operation == "-":
        result = calc.num1 - calc.num2
    elif calc.operation == "*":
        result = calc.num1 * calc.num2
    elif calc.operation == "/":
        if calc.num2 == 0:
            return {"error": "Cannot divide by zero"}
        result = calc.num1 / calc.num2
    else:
        return {"error": "Invalid operation"}
    return {"result": result}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Calculator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            input {
                margin: 5px;
            }
        </style>
    </head>
    <body>
        <h1>Simple Calculator</h1>
        <form id="calcForm">
            <input type="number" name="num1" placeholder="Number 1" required>
            <select name="operation" required>
                <option value="+">+</option>
                <option value="-">-</option>
                <option value="*">*</option>
                <option value="/">/</option>
            </select>
            <input type="number" name="num2" placeholder="Number 2" required>
            <button type="submit">Calculate</button>
        </form>
        <h2 id="result"></h2>
        <script>
            document.getElementById("calcForm").onsubmit = async function(event) {
                event.preventDefault();

                const formData = new FormData(event.target);
                const data = Object.fromEntries(formData.entries());

                const response = await fetch("/cal/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                const resultElement = document.getElementById("result");
                if (result.error) {
                    resultElement.textContent = "Error: " + result.error;
                } else {
                    resultElement.textContent = "Result: " + result.result;
                }
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
