# TRS

TRS is a service that processes the stream (rtmp, hls), creates subtitles on the fly, tracks the plot, and makes summaries (including news, key points) using AI.

## 🛠️ Getting Started

Follow the steps below to set up and run the TRS Service.

### ⚙️ Configure Environment Variables

Copy the example environment file and fill in the necessary values:

```bash
  cp .env.example .env
```

Edit the `.env` file to set your environment variables. You can use the default values or customize them as needed.


### 🐳 Build and Run the Docker Container

Start the Docker container with the following command:

```bash
  docker-compose up --build -d
```
This command will build the Docker image and start the container.


Then, API will be available at `http://localhost:8000`.
Documentation will be available at `http://localhost:8000/docs`.
