from django.db import migrations

# Placeholder copy keyed by slug — Roman can edit wording later in the admin.
DESCRIPTIONS = {
    'concerts': {
        'ua': 'Живі виступи топових локальних та гастрольних артистів.',
        'en': 'Live music nights with top local and touring acts.',
    },
    'club-shows': {
        'ua': 'Танцювальні ночі з диджеями до самого ранку.',
        'en': 'Late-night DJ sets and dancefloors that run till morning.',
    },
    'corporate-events': {
        'ua': 'Тімбілдинги, презентації та корпоративи під ключ.',
        'en': 'Team-buildings, launches and company parties, fully handled.',
    },
    'weddings': {
        'ua': 'Весілля вашої мрії — від камерних до масштабних.',
        'en': 'The wedding of your dreams, intimate or grand.',
    },
    'birthday-parties': {
        'ua': 'Дні народження, які запам’ятаються надовго.',
        'en': 'Birthday celebrations your guests will keep talking about.',
    },
    'stand-up': {
        'ua': 'Комедійні вечори з найкращими стендап-коміками.',
        'en': 'Comedy nights headlined by the sharpest stand-up talent.',
    },
    'activities': {
        'ua': 'Активний відпочинок, ігри та пригоди для компаній.',
        'en': 'Active outings, games and adventures for any group.',
    },
    'festivals': {
        'ua': 'Масштабні фестивалі просто неба з насиченою програмою.',
        'en': 'Large-scale open-air festivals with a packed line-up.',
    },
    'private-parties': {
        'ua': 'Приватні вечірки на будь-який привід та бюджет.',
        'en': 'Private parties tailored to any occasion and budget.',
    },
    'custom-event': {
        'ua': 'Немає вашого формату? Придумаємо та реалізуємо будь-яку ідею під ключ.',
        'en': 'Don’t see your format? We’ll design and deliver any idea, end to end.',
    },
}


def seed_descriptions(apps, schema_editor):
    Category = apps.get_model('events', 'Category')
    for slug, copy in DESCRIPTIONS.items():
        Category.objects.filter(slug=slug).update(
            description_ua=copy['ua'],
            description_en=copy['en'],
        )


def unseed_descriptions(apps, schema_editor):
    Category = apps.get_model('events', 'Category')
    Category.objects.filter(slug__in=DESCRIPTIONS.keys()).update(
        description_ua='', description_en=''
    )


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_category_description_en_category_description_ua'),
    ]

    operations = [
        migrations.RunPython(seed_descriptions, unseed_descriptions),
    ]
