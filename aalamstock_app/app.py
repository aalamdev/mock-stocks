import json
import os
import webob.exc
import random

from aalam_common.config import cfg
from aalam_common.redisdb import redis_conn
from aalam_common import wsgi
from aalam_common import auth
from aalam_common import role_mgmt
from aalam_common import CALLBACK_ROUTES, STATE_VALIDATION


class StockAppHandler(wsgi.BaseHandler):
    def __init__(self, mapper):
        super(StockAppHandler, self).__init__(mapper)

    def item_description(self, request, item_id):
        item_id = int(item_id)
        request.static_file = {"resource": "item-description_%d.html" % (item_id % 4),
                               "path": os.path.join(cfg.CONF.package_dir,
                                                    "resources",
                                                    "item-description_%d.html" % (item_id % 4))}

    def get_items(self, request):
        max_items = int(request.params.get("max", 0))
        with open(os.path.join(cfg.CONF.statics_dir, 'getitems.json'), 'r') as f:
            getitems_dict = json.load(f)
            return random.sample(getitems_dict, random.choice(
              range(1, len(getitems_dict))) if max_items > 10 else max_items)

    def get_types(self, request):
        with open(os.path.join(cfg.CONF.statics_dir, 'gettypes.json'), 'r') as f:
            gettypes_dict = json.load(f)
            return gettypes_dict

    def getitem_details(self, request, item_id):
        with open(os.path.join(cfg.CONF.statics_dir, 'getitemdetails.json'), 'r') as f:
            getitemdetails_dict = json.load(f)
            return getitemdetails_dict

    def items_properties(self, request):
        with open(os.path.join(cfg.CONF.statics_dir, 'itemsproperties.json'), 'r')as f:
            itemsproperties_dict = json.load(f)
            return itemsproperties_dict

    def item_images(self, request, item_id):
        with open(os.path.join(cfg.CONF.statics_dir, 'itemimages.json'), 'r')as f:
            itemimages_dict = json.load(f)
            return itemimages_dict

    def get_image(self, request, item_id):
        item_id = int(item_id)
        request.static_file = {
          "resource": "/aalam/stock/item/img",
          "path": os.path.join(cfg.CONF.statics_dir, "images", "flower-%d.jpg" % (item_id % 8))
        }


def routes_cb(mapper):
    with mapper.submapper(handler=StockAppHandler(mapper)) as m:
        m.connect("/aalam/stock/item/{item_id}/description",
                  action="item_description",
                  conditions={"method": ['GET']})

        m.connect("/aalam/stock/items",
                  action="get_items",
                  conditions={"method": ['GET']})

        m.connect("/aalam/stock/types",
                  action="get_types",
                  conditions={"method": ['GET']})

        m.connect("/aalam/stock/item/{item_id}",
                  action="getitem_details",
                  conditions={"method": ['GET']})

        m.connect("/aalam/stock/items_properties",
                  action="items_properties",
                  conditions={"method": ['GET']})

        m.connect("/aalam/stock/{item_id}/images",
                  action="item_images",
                  conditions={"method": ['GET']})

        m.connect("/aalam/stock/item/{item_id}/image/_/face_img",
                  action="get_image",
                  conditions={"method": ['GET']})


def entry(state):
    if state != STATE_VALIDATION:
        pass

    return {CALLBACK_ROUTES: routes_cb}
