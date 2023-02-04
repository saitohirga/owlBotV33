FROM gorialis/discord.py:buster-master-extras

COPY . /app
WORKDIR /app

CMD ["pwd"]