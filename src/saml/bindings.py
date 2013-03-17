# # -*- coding: utf-8 -*-
# from __future__ import print_function, unicode_literals, division
# import abc
# import base64
# import zlib


# class Redirect(object):

#     @staticmethod
#     def receive(message):
#         return zlib.decompress(base64.b64decode(message), -15)

#     @staticmethod
#     def send(message):
#         return base64.b64encode(zlib.compress(message)[2:-4])}
