from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0007_article_current_revision_alter_article_decision_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='current_revision',
        ),
    ]

