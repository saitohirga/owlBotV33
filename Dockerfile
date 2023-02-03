FROM gorialis/discord.py:buster-master-extras
WORKDIR /app
COPY . .
CMD ["python3", "main.py"]