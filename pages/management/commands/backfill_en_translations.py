from django.core.management.base import BaseCommand

from pages.models import FAQ, Partner

# Ready-made English translations keyed by the exact Ukrainian source text.
# Texts with no entry here (placeholder/junk content) are copied as-is so the
# English site never shows an empty string.
TRANSLATIONS = {
    'почему с 21 ?': 'Why is entry 21+ only?',
    'потомучто': 'Just because.',
    'бджет': 'Budget',
}

# (model, [(ua_field, en_field), ...])
FIELD_PAIRS = [
    (FAQ, [('question_ua', 'question_en'), ('answer_ua', 'answer_en')]),
    (Partner, [('description_ua', 'description_en')]),
]


class Command(BaseCommand):
    help = 'One-off backfill of empty *_en fields with English translations of the *_ua content.'

    def handle(self, *args, **options):
        for model, pairs in FIELD_PAIRS:
            for obj in model.objects.all():
                changed = []
                for ua_field, en_field in pairs:
                    ua_text = getattr(obj, ua_field, '') or ''
                    if not ua_text.strip() or getattr(obj, en_field, ''):
                        continue  # nothing to translate, or already filled manually
                    en_text = TRANSLATIONS.get(ua_text.strip(), ua_text)
                    if en_text == ua_text:
                        self.stdout.write(self.style.WARNING(
                            f'{model.__name__}#{obj.pk} {ua_field}: no translation, copied source text'
                        ))
                    setattr(obj, en_field, en_text)
                    changed.append(en_field)
                if changed:
                    obj.save(update_fields=changed)
                    self.stdout.write(f'{model.__name__}#{obj.pk}: filled {", ".join(changed)}')
        self.stdout.write(self.style.SUCCESS('Backfill complete.'))
