import requests
from jinja2 import Template

template_id ='3fa85f64-5717-4562-b3fc-2c963f66afa6'
template_url = f'http://localhost:8000/Napi/v1/template/{template_id}'
templ_body = requests.get(template_url)
templ = f"{templ_body.content.decode().strip('"')}"
templ_data = {
        'title': 'Новое письмо!',
        'text': 'Произошло что-то интересное! :)',
        'image': 'https://pictures.s3.yandex.net:443/resources/news_1682073799.jpeg'
    }


template = Template(templ)
body = template.render(**templ_data)
with open('mail.html', 'w') as f:
    f.writelines(body)
print(body)