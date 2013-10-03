# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OrganizerType'
        db.create_table(u'livinglots_organize_organizertype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('is_group', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'livinglots_organize', ['OrganizerType'])


    def backwards(self, orm):
        # Deleting model 'OrganizerType'
        db.delete_table(u'livinglots_organize_organizertype')


    models = {
        u'livinglots_organize.organizertype': {
            'Meta': {'object_name': 'OrganizerType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['livinglots_organize']