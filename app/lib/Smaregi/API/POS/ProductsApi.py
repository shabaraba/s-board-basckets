from urllib.parse import urlencode
from flask import redirect


from ..BaseServiceApi import BaseServiceApi


class ProductsApi(BaseServiceApi):
    def __init__(self, config):
        super().__init__(config)


    def __repr__(self):
        # return '<{}, {}, {}>".format(self.id, self.)"'
        pass


    def getProductList(self, field=None, sort=None, whereDict=None):
        contractId = self.config.contractId
        self.uriPos = self.config.uriApi + '/' + contractId + '/pos'
        self.uri = self.uriPos + '/products'
        
        header = self._getHeader()
        body = self._getBody('productId,productName', sort, whereDict)
        
        result = self._api(self.uri, header, body)

        self.logger.info(result)
        return result


    def getProductById(self, id, field=None, sort=None, whereDict=None):
        contractId = self.config.contractId
        self.uriPos = self.config.uriApi + '/' + contractId + '/pos'
        self.uri = self.uriPos + '/products/' + id
        
        header = self._getHeader()
        body = self._getBodyForDetail('productId,productName', sort, whereDict)
        
        result = self._api(self.uri, header, body)
        return result