import json
import os


def generate_data():
    citizens = [
        {
            "citizen_id": i,
            "town": "Москва",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "name": f"Иванов Иван Иванович {i}",
            "birth_date": "16.12.1986",
            "gender": "male",
            "relatives": []
        } for i in range(1, 10001)
    ]
    from random import randint
    for k in range(1, 12001):
        while True:
            i = randint(1, 5 * k) % 10000 + 1
            j = randint(i, 15 * k) % 10000 + 1
            if i != j:
                break
        citizens[i - 1]['relatives'].append(j)
        citizens[i - 1]['relatives'].sort()
        citizens[j - 1]['relatives'].append(i)
        citizens[j - 1]['relatives'].sort()

    with open(os.path.abspath('tests') + '/test-data.txt', 'w') as f:
        f.write(json.dumps(citizens))

if __name__ == '__main__':
    generate_data()
