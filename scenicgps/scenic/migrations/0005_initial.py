# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'GeoPt'
        db.create_table('scenic_geopt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lng', self.gf('django.db.models.fields.FloatField')()),
            ('geohash', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('scenic', ['GeoPt'])

        # Adding model 'Route'
        db.create_table('scenic_route', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('plString', self.gf('django.db.models.fields.CharField')(max_length=3000)),
        ))
        db.send_create_signal('scenic', ['Route'])

        # Adding model 'User'
        db.create_table('scenic_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device_id', self.gf('django.db.models.fields.CharField')(max_length=40, unique=True)),
        ))
        db.send_create_signal('scenic', ['User'])

        # Adding model 'RouteRating'
        db.create_table('scenic_routerating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scenic.User'])),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scenic_routerating_related', to=orm['scenic.Route'])),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('scenic', ['RouteRating'])

        # Adding unique constraint on 'RouteRating', fields ['user', 'route']
        db.create_unique('scenic_routerating', ['user_id', 'route_id'])

        # Adding model 'ScenicContent'
        db.create_table('scenic_sceniccontent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('geopt', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scenic_sceniccontent_related', to=orm['scenic.GeoPt'])),
        ))
        db.send_create_signal('scenic', ['ScenicContent'])

        # Adding model 'PanoramioContent'
        db.create_table('scenic_panoramiocontent', (
            ('sceniccontent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['scenic.ScenicContent'], unique=True, primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('scenic', ['PanoramioContent'])

        # Adding model 'UserContent'
        db.create_table('scenic_usercontent', (
            ('sceniccontent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['scenic.ScenicContent'], unique=True, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scenic.User'])),
        ))
        db.send_create_signal('scenic', ['UserContent'])

        # Adding model 'UserPicture'
        db.create_table('scenic_userpicture', (
            ('usercontent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['scenic.UserContent'], unique=True, primary_key=True)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('magHeading', self.gf('django.db.models.fields.FloatField')()),
            ('trueHeading', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('scenic', ['UserPicture'])

        # Adding model 'UserComment'
        db.create_table('scenic_usercomment', (
            ('usercontent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['scenic.UserContent'], unique=True, primary_key=True)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('scenic', ['UserComment'])

        # Adding model 'ContentRating'
        db.create_table('scenic_contentrating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scenic.User'])),
            ('content', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scenic.ScenicContent'])),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('scenic', ['ContentRating'])

        # Adding unique constraint on 'ContentRating', fields ['user', 'content']
        db.create_unique('scenic_contentrating', ['user_id', 'content_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'ContentRating', fields ['user', 'content']
        db.delete_unique('scenic_contentrating', ['user_id', 'content_id'])

        # Removing unique constraint on 'RouteRating', fields ['user', 'route']
        db.delete_unique('scenic_routerating', ['user_id', 'route_id'])

        # Deleting model 'GeoPt'
        db.delete_table('scenic_geopt')

        # Deleting model 'Route'
        db.delete_table('scenic_route')

        # Deleting model 'User'
        db.delete_table('scenic_user')

        # Deleting model 'RouteRating'
        db.delete_table('scenic_routerating')

        # Deleting model 'ScenicContent'
        db.delete_table('scenic_sceniccontent')

        # Deleting model 'PanoramioContent'
        db.delete_table('scenic_panoramiocontent')

        # Deleting model 'UserContent'
        db.delete_table('scenic_usercontent')

        # Deleting model 'UserPicture'
        db.delete_table('scenic_userpicture')

        # Deleting model 'UserComment'
        db.delete_table('scenic_usercomment')

        # Deleting model 'ContentRating'
        db.delete_table('scenic_contentrating')


    models = {
        'scenic.contentrating': {
            'Meta': {'unique_together': "(('user', 'content'),)", 'object_name': 'ContentRating'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scenic.ScenicContent']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scenic.User']"})
        },
        'scenic.geopt': {
            'Meta': {'object_name': 'GeoPt'},
            'geohash': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {})
        },
        'scenic.panoramiocontent': {
            'Meta': {'object_name': 'PanoramioContent', '_ormbases': ['scenic.ScenicContent']},
            'sceniccontent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['scenic.ScenicContent']", 'unique': 'True', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'scenic.route': {
            'Meta': {'object_name': 'Route'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plString': ('django.db.models.fields.CharField', [], {'max_length': '3000'})
        },
        'scenic.routerating': {
            'Meta': {'unique_together': "(('user', 'route'),)", 'object_name': 'RouteRating'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scenic_routerating_related'", 'to': "orm['scenic.Route']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scenic.User']"})
        },
        'scenic.sceniccontent': {
            'Meta': {'object_name': 'ScenicContent'},
            'geopt': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scenic_sceniccontent_related'", 'to': "orm['scenic.GeoPt']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'scenic.user': {
            'Meta': {'object_name': 'User'},
            'device_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'scenic.usercomment': {
            'Meta': {'object_name': 'UserComment', '_ormbases': ['scenic.UserContent']},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'usercontent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['scenic.UserContent']", 'unique': 'True', 'primary_key': 'True'})
        },
        'scenic.usercontent': {
            'Meta': {'object_name': 'UserContent', '_ormbases': ['scenic.ScenicContent']},
            'sceniccontent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['scenic.ScenicContent']", 'unique': 'True', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scenic.User']"})
        },
        'scenic.userpicture': {
            'Meta': {'object_name': 'UserPicture', '_ormbases': ['scenic.UserContent']},
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'magHeading': ('django.db.models.fields.FloatField', [], {}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'trueHeading': ('django.db.models.fields.FloatField', [], {}),
            'usercontent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['scenic.UserContent']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['scenic']
