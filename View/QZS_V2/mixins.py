#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class MainMixin(object):

    components = {}


    def __init__(self):

        super(MainMixin, self).__init__()

    def registerComponent(self,name,component):

        self.components[name] = component

