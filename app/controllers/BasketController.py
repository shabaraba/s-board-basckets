import datetime

from marshmallow import ValidationError

from app.common.managers import SessionManager, HttpManager
from app.common.abstracts.AbstractController import AbstractController
from app.domains.AccountDomainService import AccountDomainService
from app.domains.BasketAssociationDomainService import BasketAssociationDomainService
from app.domains.BasketDomainService import BasketDomainService
from app.validators import BasketValidators


class Basket(AbstractController):
    def __init__(self) ->None:
        super().__init__()
        self._basketDomainService = None

    async def on_get(self, req, resp):
        self._logger.info('access DailyBasket')
        self._basketDomainService = BasketDomainService(self._loginAccount)
        nowYear = datetime.datetime.now().year
        nowMonth = datetime.datetime.now().month
        dailyBasketList = await self._basketDomainService.getDailyBasketListByMonth(nowYear, nowMonth)

        jsonDailyBasketList = [await model.serialize for model in dailyBasketList]

        await self.render(
            'baskets/index.pug',
            dailyBasketList = jsonDailyBasketList
        )
        
class Associate(AbstractController):
    def __init__(self) -> None:
        super().__init__()
        self._basketAssociationDomainService = None

    async def on_get(self, req, resp):
        self._logger.info('access associate')
        self._logger.info(await self._loginAccount.accountSetting)
        if HttpManager.isBookingRedirect(resp):
            return

        await HttpManager.render(
            resp,
            self._loginAccount, 
            'baskets/association/index.pug'
        )

class AssociateResult(AbstractController):
    def __init__(self) -> None:
        super().__init__()
        self._basketAssociationDomainService = None

    async def on_get(self, req, resp):
        if HttpManager.isBookingRedirect(resp):
            self._logger.info('redirect')
            return
        try:
            schema = BasketValidators.AccosiationCondition()
            query = schema.load(req.params)
        except ValidationError as e:
            SessionManager.set(resp.session, SessionManager.KEY_ERROR_MESSAGES, e.messages)
            resp.redirect('/baskets/associate', status_code=302)
            return

        self._basketAssociationDomainService = await BasketAssociationDomainService.createInstance(self._loginAccount)
        targetStore = await self._basketAssociationDomainService.targetStore
        fpgrowth = await self._basketAssociationDomainService.associate(
            query['date_from'],
            query['date_to']
        )

        vis = await self._basketAssociationDomainService.convertAssociationResultToVisJs(fpgrowth)
        pickUpMessage = await self._basketAssociationDomainService.convertAssociationResultToPickUpMessage(
            fpgrowth,
            targetStore["storeId"],
            query['date_from'],
            query['date_to']
        )

        visDict = vis.toDict()

        await HttpManager.render(
            resp = resp,
            account = self._loginAccount,
            path = "baskets/association/result.pug",
            search_from = query['date_from'],
            search_to = query['date_to'],
            vis = visDict,
            pickUpMessage = pickUpMessage,
        )
        return
