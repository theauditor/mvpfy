from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List

app = FastAPI()

# Middleware to enable CORS (Cross-Origin Resource Sharing)
origins = ["*"]  # You can replace "*" with the specific domains you want to allow
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def replace_and_write_html(token_code, domainame):
    # Input and output file paths
    input_file_path = "template/example.html"
    output_file_path = f"template/{domainame}.html"

    try:
        # Read content from the input file
        with open(input_file_path, "r") as input_file:
            file_content = input_file.read()

        # Replace ==TOKEN== with the provided token_code
        replaced_content = file_content.replace("==TOKEN==", token_code)

        # Write the modified content to the output file
        with open(output_file_path, "w") as output_file:
            output_file.write(replaced_content)

        print(f"File successfully written to: {output_file_path}")
    except Exception as e:
        print(f"Error: {str(e)}")


import subprocess
import os
def git_commit_and_push(domain_name):
    try:
        # Change directory to "template/"
        template_directory = "template/"
        os.chdir(template_directory)

        # Git add the specified file
        subprocess.run(["git", "add", f"{domain_name}.html"], check=True)

        # Git commit with the specified message
        commit_message = f"Update {domain_name} content"
        #subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Git push to origin
        #subprocess.run(["git", "push", "origin"], check=True)

        print("Git commands executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing Git commands: {str(e)}")

# Function to write HTML and perform Git commit and push
def process_and_commit(token_code, domain_name):
    try:
        # Call the HTML write function
        replace_and_write_html(token_code, domain_name)

        # Call the Git commit and push function
        git_commit_and_push(domain_name)

        return {"message": f"https://glassdemo.getglass.co/{domain_name}.html"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error processing and committing: {str(e)}"},
        )

# FastAPI endpoint
@app.post("/process-and-commit")
async def process_and_commit_endpoint(
    token_code: str ,
    domain_name: str
):
    return process_and_commit(token_code, domain_name)








# Dependency to get the client's IP address
def get_client_ip(request: Request):
    return request.client.host

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
