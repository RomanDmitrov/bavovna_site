from django.db import migrations

# Two-sentence descriptions per category (max_length=160). Roman can still
# edit wording later in the admin.
DESCRIPTIONS = {
    'concerts': {
        'ua': 'Живі виступи топових локальних та гастрольних артистів. Атмосфера великої сцени в самому серці Дубліна.',
        'en': 'Live sets from top local and touring artists. Big-stage energy right in the heart of Dublin.',
    },
    'club-shows': {
        'ua': 'Танцювальні ночі з найкращими діджеями до самого ранку. Потужний звук, світло та драйв справжнього клубу.',
        'en': 'Dancefloor nights with the best DJs until sunrise. Powerful sound, lights and true club energy.',
    },
    'corporate-events': {
        'ua': 'Тімбілдинги, презентації та корпоративи під ключ. Продумаємо програму, локацію й кейтеринг для вашої команди.',
        'en': 'Team-buildings, launches and company parties, fully handled. We plan the programme, venue and catering for your team.',
    },
    'weddings': {
        'ua': 'Весілля вашої мрії — від камерних церемоній до масштабних святкувань. Створимо ідеальний день до найменших деталей.',
        'en': 'The wedding of your dreams, from intimate ceremonies to grand celebrations. We craft your perfect day down to every detail.',
    },
    'birthday-parties': {
        'ua': 'Дні народження, які запам’ятаються надовго. Тематичне оформлення, розваги та святкова атмосфера для будь-якого віку.',
        'en': 'Birthdays your guests will keep talking about. Themed décor, entertainment and a festive vibe for any age.',
    },
    'stand-up': {
        'ua': 'Комедійні вечори з найкращими стендап-коміками. Гострий гумор, живі емоції та невимушена атмосфера.',
        'en': 'Comedy nights with the sharpest stand-up talent. Sharp humour, live emotion and an easy-going vibe.',
    },
    'activities': {
        'ua': 'Активний відпочинок, ігри та пригоди для компаній. Заряд емоцій та нові враження далеко за межами звичайної вечірки.',
        'en': 'Active outings, games and adventures for any group. A rush of emotion and fresh experiences beyond the usual party.',
    },
    'festivals': {
        'ua': 'Масштабні фестивалі просто неба з насиченою програмою. Музика, фудкорти та розваги для тисяч гостей.',
        'en': 'Large-scale open-air festivals with a packed line-up. Music, food courts and entertainment for thousands of guests.',
    },
    'private-parties': {
        'ua': 'Приватні вечірки на будь-який привід та бюджет. Камерна атмосфера, ваша музика й повна свобода формату.',
        'en': 'Private parties for any occasion and budget. An intimate vibe, your music and full freedom of format.',
    },
    'custom-event': {
        'ua': 'Немає вашого формату? Придумаємо та реалізуємо будь-яку ідею під ключ. Від концепції до останньої деталі — усе беремо на себе.',
        'en': 'Don’t see your format? We’ll design and deliver any idea end to end. From concept to the last detail, we handle it all.',
    },
}

# Previous single-sentence copy, restored on reverse.
OLD_DESCRIPTIONS = {
    'concerts': {'ua': 'Живі виступи топових локальних та гастрольних артистів.', 'en': 'Live music nights with top local and touring acts.'},
    'club-shows': {'ua': 'Танцювальні ночі з диджеями до самого ранку.', 'en': 'Late-night DJ sets and dancefloors that run till morning.'},
    'corporate-events': {'ua': 'Тімбілдинги, презентації та корпоративи під ключ.', 'en': 'Team-buildings, launches and company parties, fully handled.'},
    'weddings': {'ua': 'Весілля вашої мрії — від камерних до масштабних.', 'en': 'The wedding of your dreams, intimate or grand.'},
    'birthday-parties': {'ua': 'Дні народження, які запам’ятаються надовго.', 'en': 'Birthday celebrations your guests will keep talking about.'},
    'stand-up': {'ua': 'Комедійні вечори з найкращими стендап-коміками.', 'en': 'Comedy nights headlined by the sharpest stand-up talent.'},
    'activities': {'ua': 'Активний відпочинок, ігри та пригоди для компаній.', 'en': 'Active outings, games and adventures for any group.'},
    'festivals': {'ua': 'Масштабні фестивалі просто неба з насиченою програмою.', 'en': 'Large-scale open-air festivals with a packed line-up.'},
    'private-parties': {'ua': 'Приватні вечірки на будь-який привід та бюджет.', 'en': 'Private parties tailored to any occasion and budget.'},
    'custom-event': {'ua': 'Немає вашого формату? Придумаємо та реалізуємо будь-яку ідею під ключ.', 'en': 'Don’t see your format? We’ll design and deliver any idea, end to end.'},
}


def apply(descriptions):
    def _run(apps, schema_editor):
        Category = apps.get_model('events', 'Category')
        for slug, copy in descriptions.items():
            Category.objects.filter(slug=slug).update(
                description_ua=copy['ua'],
                description_en=copy['en'],
            )
    return _run


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_seed_category_descriptions'),
    ]

    operations = [
        migrations.RunPython(apply(DESCRIPTIONS), apply(OLD_DESCRIPTIONS)),
    ]
