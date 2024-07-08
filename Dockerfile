FROM python:3.11-alpine

COPY ./requirements.txt /app/requirements.txt
COPY ./account_info.py /app/account_info.py

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# Set time zone
ENV TZ="US/Eastern"

COPY . /app

ENTRYPOINT [ "python" ]

# -u means unbuffered output so I can see the print statements
CMD ["-u", "live_data.py" ]