# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'GeoPt.geohash'
        db.add_column('scenic_geopt', 'geohash', self.gf('django.db.models.fields.CharField')(default='asdfasdf', max_length=50), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'GeoPt.geohash'
        db.delete_column('scenic_geopt', 'geohash')


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
