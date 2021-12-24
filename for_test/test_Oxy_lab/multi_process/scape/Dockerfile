FROM python:3.8
WORKDIR /machine
COPY . .
RUN pip install -r requirements.txt
ADD scraper.py .
CMD ["python", "./scraping_with_oxylabs_machine1.py"]

