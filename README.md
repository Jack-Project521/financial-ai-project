# financial-ai-project
## Product Vision
Build an AI-powered enterprise-level financial and operational data analytics platform supporting both cloud and on-premise deployment. 
Through natural language interaction (LLM + RAG), it enables employees and management to quickly access value chain data including procurement, production, inventory, 
sales, and P&L, while recording user interactions for continuous system optimization.

## Installation
This service runs in Docker container.

### Docker
- Download Docker Desktop from https://www.docker.com/products/docker-desktop/
- Choose the version adapted for your env, then run Docker Desktop app that will manage all your docker images and containers. Always run it first before starting your project.
- Login with your own docker account (register it at first if you don't have one)

### OPENAI_API_KEY
The key should be configured in .env file in docker, which you can't find on GitHub due to the classification.

- Create .env file under the project directory after pulling all codes, then give the content OPENAI_API_KEY="your_key".
- Don't worry about this file that is already put in the .gitignore, so it will not be committed to GitHub.

## Run project
- Confirm first the Docker Desktop has been started.
- Go to the Terminal in Pycharm, run 'docker-compose up' to start the installation of docker images and container, it takes a while at first time.
  - Note: if your local Pycharm can't find docker command, follow the step below to fix the shell configuration problem:
    ```
    In PyCharm:
    Settings → Tools → Terminal → check "Shell path".
    If it says /bin/bash or similar, change it to (type manually):
    
    /bin/zsh -l
   
    or
    
    /bin/bash -l
    
    (the -l makes it a login shell, so it loads your PATH from .zprofile or .bash_profile).
    ```
    
## Stop Docker 
Could use both below to stop

- docker-compose down
- Ctrl + c

## Delete folders in Docker
The openai_chroma and uploads folder could be deleted in Docker Desktop

- Click your container 'python-server'
- Go to Files tab, then find /code/financial-ai-project, all project contents there.