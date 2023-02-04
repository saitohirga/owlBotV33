FROM gorialis/discord.py:buster-master-extras
COPY . /app
WORKDIR /app
CMD ["python3", "main.py"]