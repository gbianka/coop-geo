# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

AREA_TYPES = (('TW', u'town'),
              ('DP', u"departement"),
              ('CT', u"district"),
              ('CC', u"town group"),
              ('RG', u"region"),
              ('PY', u"country"),
             )

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AreaType'
        db.create_table('coop_geo_areatype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('txt_idx', self.gf('django.db.models.fields.CharField')(max_length='50')),
        ))
        db.send_create_signal('coop_geo', ['AreaType'])

        # Deleting field 'AreaRelations.relation_type'
        db.delete_column('coop_geo_arearelations', 'relation_type')

        # Adding field 'Area.area_type_tmp'
        db.add_column('coop_geo_area', 'area_type_tmp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coop_geo.AreaType'], null=True, blank=True), keep_default=False)
        db.start_transaction()
        for area in orm.Area.objects.all():
            area_type, created = orm.AreaType.objects.get_or_create(
                    label=dict(AREA_TYPES)[area.area_type],
                    txt_idx=area.area_type)
            area.area_type_tmp = area_type
            area.save()
        db.commit_transaction()

    def backwards(self, orm):
        
        # Deleting model 'AreaType'
        db.delete_table('coop_geo_areatype')

        # User chose to not deal with backwards NULL issues for 'AreaRelations.relation_type'
        raise RuntimeError("Cannot reverse this migration. 'AreaRelations.relation_type' and its values cannot be restored.")

        # Deleting field 'Area.area_type_tmp'
        db.delete_column('coop_geo_area', 'area_type_tmp_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'coop_geo.area': {
            'Meta': {'object_name': 'Area'},
            'area_type': ('django.db.models.fields.CharField', [], {'default': "u'TW'", 'max_length': '2'}),
            'area_type_tmp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_geo.AreaType']", 'null': 'True', 'blank': 'True'}),
            'default_location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'associated_area'", 'null': 'True', 'to': "orm['coop_geo.Location']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'polygon': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'related_areas': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['coop_geo.Area']", 'through': "orm['coop_geo.AreaRelations']", 'symmetrical': 'False'}),
            'update_auto': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'coop_geo.arealink': {
            'Meta': {'object_name': 'AreaLink'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_geo.Area']", 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'coop_geo.arearelations': {
            'Meta': {'object_name': 'AreaRelations'},
            'child': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_rels'", 'to': "orm['coop_geo.Area']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_rels'", 'to': "orm['coop_geo.Area']"})
        },
        'coop_geo.areatype': {
            'Meta': {'object_name': 'AreaType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'txt_idx': ('django.db.models.fields.CharField', [], {'max_length': "'50'"})
        },
        'coop_geo.located': {
            'Meta': {'object_name': 'Located'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_geo.Location']", 'null': 'True', 'blank': 'True'}),
            'location_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'main_location': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'coop_geo.location': {
            'Meta': {'object_name': 'Location'},
            'adr1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'adr2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coop_geo.Area']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['coop_geo']
