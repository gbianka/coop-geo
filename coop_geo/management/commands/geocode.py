#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, urllib2, time, json, random
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from geodjangofla.models import Commune, Departement, Canton
from coop_geo import models

GMAP_URL = "http://maps.googleapis.com/maps/api/geocode/json?address=%s"\
           "&sensor=false"

LOG_FILE_NAME = '/tmp/geocode.log'

class Command(BaseCommand):
    help = 'Geocodage google automatique de données depuis l\'adresse'

    def handle(self, *args, **options):
        connection_failed, no_response = [], []
        many_responses, success = [], []
        locations = models.Location.objects.filter(point__isnull=True,
                                                   city__isnull=False)
        nb_locations = locations.count()
        for idx, location in enumerate(locations.all()):
            self.stdout.write('\r * traitement %d/%d' % (idx+1, nb_locations))
            self.stdout.flush()
            time.sleep(0.5 + float('0.%d'%random.randint(1, 10)))
            addr = location.city.replace(' ', '+')
            if location.adr1:
                addr += ",+" + location.adr1.replace(' ', '+')
            if location.zipcode:
                addr += ",+" + location.zipcode.replace(' ', '+')
            try:
                r = urllib2.urlopen(GMAP_URL % addr)
            except urllib2.URLError:
                r = None
            if not r or r.msg != 'OK':
                connection_failed.append(unicode(location) + \
                                         u" - %d" % location.id)
                continue
            res = json.loads(r.read())

            results = res.get('results')
            if not results:
                no_response.append(unicode(location) + \
                                   u" - %d" % location.id)
                continue
            if len(results) > 1:
                many_responses.append(unicode(location) + \
                                      u" - %d" % location.id)
                continue
            try:
                latlon = results[0].get('geometry').get('location')
            except AttributeError:
                no_response += 1
                no_response.append(unicode(location) + \
                                   u" - %d" % location.id)
                continue
            wkt = 'SRID=4326;POINT (%s %s)' % (latlon['lng'], latlon['lat'])
            location.point = wkt
            location.save()
            success.append(unicode(location) + u" (%d)" % location.id)
        self.stdout.write('\n\n')
        for items, lbl in (
                (success, "lieu(x) geolocalise(s)\n"),
                (many_responses, "requete(s) avec trop de reponses\n"),
                (no_response, "requete(s) sans reponse\n"),
                (connection_failed, "connexion(s) echouee(s)\n"),):
            self.stdout.write(" * %d %s" % (len(items), lbl))
            with open(LOG_FILE_NAME, 'a+') as log_file:
                log_file.write(lbl)
                log_file.write("#"*len(lbl))
                log_file.write('\n\n')
                for item in items:
                    log_file.write(item + '\n')
                log_file.write('\n\n')

