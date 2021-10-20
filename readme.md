# Test project for google trending news data mart for 112ua.tv

## Setup & run
> __Required__: _Docker_ & _Docker Compose_
```bash
docker-compose up --build
```

### Used stack:
* Python - of course
* Django - mainly for UI and django-celery-results as django was used celery for scheduling
* Celery - For running crawler, fetching google trends and managing both with scheduling
* Postgres - As it scales nicely if project continues
* Scrapy - For cralwling 112ua.tv